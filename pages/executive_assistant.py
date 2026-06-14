"""Executive AI Assistant page."""

from __future__ import annotations

import streamlit as st

from utils.analytics import init_session_state, record_generation
from utils.config import configure_logging
from utils.llm import generate_business_output
from utils.prompts import get_template_names, get_template_prompt
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


configure_page("Executive AI Assistant")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("executive_assistant")

render_page_header(
    "Module 1",
    "Executive AI Assistant",
    "Turn strategic requests into executive summaries, insights, recommendations, and action plans.",
)

with st.form("executive_assistant_form"):
    template_name = st.selectbox("Prompt template", ["Custom"] + get_template_names())
    business_request = st.text_area(
        "Business request",
        placeholder="Example: Create a growth strategy for a B2B SaaS company entering mid-market healthcare.",
        height=190,
    )
    output_style = st.selectbox(
        "Output style",
        ["Executive concise", "Consulting detailed", "Board-ready", "Operational action plan"],
    )
    submitted = st.form_submit_button("Generate Executive Output", use_container_width=True)

if submitted:
    if not business_request.strip():
        st.error("Enter a business request before generating.")
    else:
        inputs = {
            "business_request": business_request,
            "output_style": output_style,
            "template_context": get_template_prompt(template_name) if template_name != "Custom" else "Custom request",
        }
        with st.spinner("Synthesizing executive-grade response..."):
            try:
                result = generate_business_output("executive_assistant", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Executive output generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
