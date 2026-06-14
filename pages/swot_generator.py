"""SWOT Analysis Generator page."""

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


configure_page("SWOT Analysis Generator")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("swot_generator")

render_page_header(
    "Module 6",
    "SWOT Analysis Generator",
    "Create consulting-style SWOT analysis for companies, initiatives, products, markets, or transformation programs.",
)

with st.form("swot_generator_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        subject = st.text_input("Subject", placeholder="Example: Launching an AI customer support assistant")
    with col_b:
        industry = st.text_input("Industry", placeholder="Example: B2B SaaS")
    context = st.text_area("Strategic context", placeholder="Add market, company, customer, competitor, or operational context.", height=200)
    submitted = st.form_submit_button("Generate SWOT Analysis", use_container_width=True)

if submitted:
    if not subject.strip():
        st.error("Enter a subject before generating.")
    else:
        inputs = {"subject": subject, "industry": industry or "General business", "context": context}
        with st.spinner("Building strategic SWOT analysis..."):
            try:
                result = generate_business_output("swot_generator", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("SWOT analysis generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
