"""Professional Email Generator page."""

from __future__ import annotations

import streamlit as st

from utils.analytics import init_session_state, record_generation
from utils.config import configure_logging
from utils.llm import generate_business_output
from utils.ui import (
    apply_enterprise_theme,
    configure_page,
    handle_generation_error,
    render_copyable_text,
    render_export_buttons,
    render_history_browser,
    render_page_header,
    render_result,
    render_selected_history,
    render_sidebar,
)


configure_page("Professional Email Generator")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("email_generator")

render_page_header(
    "Module 3",
    "Professional Email Generator",
    "Draft polished stakeholder communication with executive, professional, and concise variants.",
)

with st.form("email_generator_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        email_type = st.selectbox("Email type", ["Client update", "Sales follow-up", "Executive request", "Internal announcement", "Partnership outreach", "Project escalation"])
        tone = st.selectbox("Tone", ["Professional", "Executive", "Warm and polished", "Direct", "Consultative", "Diplomatic"])
    with col_b:
        recipient_type = st.selectbox("Recipient type", ["Client executive", "Prospect", "Internal leader", "Team member", "Vendor", "Investor"])
        purpose = st.text_input("Purpose", placeholder="Example: Request approval for a pilot automation project")
    additional_context = st.text_area("Additional context", placeholder="Add details, constraints, dates, or stakeholder context.", height=160)
    submitted = st.form_submit_button("Generate Email", use_container_width=True)

if submitted:
    if not purpose.strip():
        st.error("Enter the email purpose before generating.")
    else:
        inputs = {
            "email_type": email_type,
            "recipient_type": recipient_type,
            "tone": tone,
            "purpose": purpose,
            "additional_context": additional_context,
        }
        with st.spinner("Composing professional communication..."):
            try:
                result = generate_business_output("email_generator", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Email generated.")
                render_result(result)
                st.markdown("### Copy-ready versions")
                for index, (section, value) in enumerate(result.sections.items()):
                    if section != "Subject Line":
                        render_copyable_text(section, value, f"email_copy_{index}")
                render_export_buttons(result)

render_selected_history()
