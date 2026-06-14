"""Main dashboard for the AI Business Automation Agent."""

from __future__ import annotations

import streamlit as st

from utils.analytics import (
    generation_timeline_chart,
    history_frame,
    init_session_state,
    metric_snapshot,
    module_bar_chart,
    module_donut_chart,
)
from utils.config import configure_logging, get_settings
from utils.prompts import PROMPT_TEMPLATES
from utils.ui import (
    apply_enterprise_theme,
    configure_page,
    render_metric_grid,
    render_page_header,
    render_sidebar,
    render_template_cards,
)


configure_page("Executive Dashboard")
configure_logging()
init_session_state()
apply_enterprise_theme()
render_sidebar()

settings = get_settings()

render_page_header(
    "Enterprise AI Operating System",
    settings.app_name,
    "A consulting-grade business automation platform for executive support, meeting intelligence, reporting, research, communications, SWOT analysis, and workflow automation planning.",
)

if settings.effective_demo_mode:
    st.warning(
        "Demo mode is active because `OPENAI_API_KEY` is not configured or `DEMO_MODE=true`. "
        "The app will generate deterministic sample outputs until an API key is supplied."
    )
else:
    st.success(f"Connected to OpenAI model `{settings.openai_model}`.")

render_metric_grid(metric_snapshot())

st.markdown("### Analytics Dashboard")
chart_col, donut_col = st.columns([1.35, 1])
with chart_col:
    st.plotly_chart(module_bar_chart(), use_container_width=True)
with donut_col:
    st.plotly_chart(module_donut_chart(), use_container_width=True)

st.markdown("### Activity Timeline")
st.plotly_chart(generation_timeline_chart(), use_container_width=True)

history = history_frame()
st.markdown("### Session History")
if history.empty:
    st.info("Generated outputs will appear here during this Streamlit session.")
else:
    st.dataframe(history, use_container_width=True, hide_index=True)

st.markdown("### Prompt Templates")
template_cols = st.columns(2)
for index, template in enumerate(PROMPT_TEMPLATES):
    with template_cols[index % 2]:
        render_template_cards([template])
