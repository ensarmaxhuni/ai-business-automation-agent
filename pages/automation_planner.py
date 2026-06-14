"""Business Automation Planner page."""

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


configure_page("Business Automation Planner")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("automation_planner")

render_page_header(
    "Module 7",
    "Business Automation Planner",
    "Analyze manual workflows, identify bottlenecks, estimate savings, and create an AI automation implementation roadmap.",
)

with st.form("automation_planner_form"):
    workflow = st.text_area(
        "Workflow description",
        placeholder="Example: Our HR team manually reviews resumes, screens candidates, schedules interviews, and updates applicant records.",
        height=220,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        team = st.text_input("Business team", placeholder="Example: HR recruiting")
    with col_b:
        volume = st.text_input("Monthly volume or scale", placeholder="Example: 600 resumes, 80 interviews")
    submitted = st.form_submit_button("Create Automation Plan", use_container_width=True)

if submitted:
    if not workflow.strip():
        st.error("Describe the workflow before generating an automation plan.")
    else:
        inputs = {"workflow": workflow, "team": team or "Business operations", "volume": volume or "Not specified"}
        with st.spinner("Mapping automation opportunities..."):
            try:
                result = generate_business_output("automation_planner", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Automation plan generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
