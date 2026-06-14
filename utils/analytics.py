"""Session analytics and history management."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

import pandas as pd
import plotly.express as px
import streamlit as st

from .schemas import GeneratedResult, HistoryItem


MODULE_LABELS: Dict[str, str] = {
    "executive_assistant": "Executive Assistant",
    "meeting_intelligence": "Meetings",
    "email_generator": "Emails",
    "report_generator": "Reports",
    "research_analyst": "Research",
    "swot_generator": "SWOT",
    "automation_planner": "Automation Plans",
}


def init_session_state() -> None:
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("analytics_counts", {key: 0 for key in MODULE_LABELS})


def record_generation(result: GeneratedResult) -> None:
    init_session_state()
    history_item = HistoryItem(id=str(uuid4()), result=result)
    st.session_state.history.insert(0, history_item.model_dump())
    st.session_state.analytics_counts[result.module_key] = st.session_state.analytics_counts.get(result.module_key, 0) + 1


def get_history(module_key: str | None = None) -> List[HistoryItem]:
    init_session_state()
    items = [HistoryItem(**item) for item in st.session_state.history]
    if module_key:
        items = [item for item in items if item.result.module_key == module_key]
    return items


def get_counts() -> Dict[str, int]:
    init_session_state()
    return {key: int(st.session_state.analytics_counts.get(key, 0)) for key in MODULE_LABELS}


def total_tasks_generated() -> int:
    return sum(get_counts().values())


def metric_snapshot() -> Dict[str, int]:
    counts = get_counts()
    return {
        "Total Tasks Generated": total_tasks_generated(),
        "Reports Generated": counts.get("report_generator", 0),
        "Emails Generated": counts.get("email_generator", 0),
        "Research Requests": counts.get("research_analyst", 0),
        "Automation Plans Created": counts.get("automation_planner", 0),
    }


def module_count_frame() -> pd.DataFrame:
    counts = get_counts()
    rows = [{"Module": MODULE_LABELS[key], "Count": count} for key, count in counts.items()]
    return pd.DataFrame(rows)


def history_frame() -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for item in get_history():
        rows.append(
            {
                "Generated At": item.result.generated_at,
                "Module": item.result.module_name,
                "Title": item.result.title,
                "Model": item.result.model,
            }
        )
    if not rows:
        return pd.DataFrame(columns=["Generated At", "Module", "Title", "Model"])
    return pd.DataFrame(rows)


def module_bar_chart():
    df = module_count_frame()
    fig = px.bar(
        df,
        x="Module",
        y="Count",
        color="Module",
        color_discrete_sequence=["#5eead4", "#93c5fd", "#fbbf24", "#fda4af", "#c4b5fd", "#86efac", "#f9a8d4"],
        text="Count",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb"},
        showlegend=False,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def module_donut_chart():
    df = module_count_frame()
    if int(df["Count"].sum()) == 0:
        df["Count"] = 1
    fig = px.pie(
        df,
        names="Module",
        values="Count",
        hole=0.58,
        color_discrete_sequence=["#5eead4", "#93c5fd", "#fbbf24", "#fda4af", "#c4b5fd", "#86efac", "#f9a8d4"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb"},
        legend={"orientation": "h", "y": -0.05},
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
    )
    return fig


def generation_timeline_chart():
    df = history_frame()
    if df.empty:
        df = pd.DataFrame(
            {
                "Generated At": [datetime.utcnow()],
                "Module": ["No activity yet"],
                "Count": [0],
            }
        )
    else:
        df["Generated At"] = pd.to_datetime(df["Generated At"]).dt.floor("min")
        df = df.groupby(["Generated At", "Module"], as_index=False).size().rename(columns={"size": "Count"})

    fig = px.line(
        df,
        x="Generated At",
        y="Count",
        color="Module",
        markers=True,
        color_discrete_sequence=["#5eead4", "#93c5fd", "#fbbf24", "#fda4af", "#c4b5fd", "#86efac", "#f9a8d4"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e5e7eb"},
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig
