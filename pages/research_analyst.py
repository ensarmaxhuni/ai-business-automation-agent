"""AI Research Analyst page."""

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


configure_page("AI Research Analyst")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("research_analyst")

render_page_header(
    "Module 5",
    "AI Research Analyst",
    "Produce strategic research briefs covering market trends, opportunities, risks, strategic insights, and future outlook.",
)

with st.form("research_analyst_form"):
    topic = st.text_input("Research topic", placeholder="Example: Artificial Intelligence in Banking")
    market = st.text_input("Market or region", placeholder="Example: United States, enterprise banking")
    decision_context = st.text_area(
        "Decision context",
        placeholder="Example: We are evaluating whether to launch AI-enabled workflow automation products for regional banks.",
        height=190,
    )
    submitted = st.form_submit_button("Generate Research Brief", use_container_width=True)

if submitted:
    if not topic.strip():
        st.error("Enter a research topic before generating.")
    else:
        inputs = {"topic": topic, "market": market or "Global", "decision_context": decision_context}
        with st.spinner("Synthesizing research analyst brief..."):
            try:
                result = generate_business_output("research_analyst", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Research brief generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
