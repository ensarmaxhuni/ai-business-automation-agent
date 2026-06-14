"""Meeting Intelligence page."""

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


configure_page("Meeting Intelligence")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()
render_history_browser("meeting_intelligence")

render_page_header(
    "Module 2",
    "Meeting Intelligence",
    "Transform raw meeting notes into decisions, action items, risks, follow-ups, and an executive brief.",
)

with st.form("meeting_intelligence_form"):
    meeting_type = st.selectbox("Meeting type", ["Executive sync", "Client meeting", "Sales review", "Operations review", "Project standup", "Board meeting"])
    audience = st.selectbox("Audience", ["Executive team", "Client stakeholders", "Project team", "Board members", "Department leads"])
    meeting_notes = st.text_area(
        "Meeting notes",
        placeholder="Paste meeting transcript, notes, or bullet points here.",
        height=260,
    )
    submitted = st.form_submit_button("Analyze Meeting", use_container_width=True)

if submitted:
    if not meeting_notes.strip():
        st.error("Paste meeting notes before analyzing.")
    else:
        inputs = {"meeting_type": meeting_type, "audience": audience, "meeting_notes": meeting_notes}
        with st.spinner("Extracting meeting intelligence..."):
            try:
                result = generate_business_output("meeting_intelligence", inputs)
            except Exception as exc:
                handle_generation_error(exc)
            else:
                record_generation(result)
                st.success("Meeting intelligence generated.")
                render_result(result)
                render_export_buttons(result)

render_selected_history()
