"""Business Report Generator page."""

from __future__ import annotations

import streamlit as st

from utils.analytics import init_session_state, record_generation
from utils.config import configure_logging
from utils.llm import generate_business_output
from utils.ui import (
    apply_enterprise_theme,
    configure_page,
    handle_generation_error,
    render_export_buttons,
    render_history_browser,
    render_page_header,
    render_result,
    render_selected_history,
    render_sidebar,
)


configure_page("Business Report Generator")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("report_generator")

render_page_header(
    "Module 4",
    "Business Report Generator",
    "Generate professional business reports with situation analysis, findings, recommendations, implementation planning, and risk assessment.",
)

with st.form("report_generator_form"):
    col_a, col_b = st.columns([1.1, 0.9])
    with col_a:
        topic = st.text_input("Report topic", placeholder="Example: AI automation strategy for finance operations")
    with col_b:
        industry = st.text_input("Industry", placeholder="Example: Financial services")
    context = st.text_area("Business context", placeholder="Describe the company, goals, constraints, audience, and known issues.", height=210)
    submitted = st.form_submit_button("Generate Business Report", use_container_width=True)

if submitted:
    if not topic.strip() or not industry.strip():
        st.error("Enter both a report topic and industry.")
    else:
        inputs = {"topic": topic, "industry": industry, "context": context}
        with st.spinner("Building consulting-grade report..."):
            try:
                result = generate_business_output("report_generator", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Business report generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
