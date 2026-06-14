"""Reusable Streamlit UI components and enterprise styling."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Dict, Iterable

import streamlit as st
import streamlit.components.v1 as components

from .analytics import get_history, metric_snapshot
from .config import get_settings
from .export import build_export_filename, export_docx, export_pdf, export_txt
from .schemas import GeneratedResult


ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "assets" / "logo.png"


def configure_page(title: str) -> None:
    st.set_page_config(
        page_title=f"{title} | AI Business Automation Agent",
        page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_enterprise_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #05070d;
            --panel: rgba(17, 24, 39, 0.72);
            --panel-strong: rgba(15, 23, 42, 0.88);
            --line: rgba(255, 255, 255, 0.10);
            --text: #f8fafc;
            --muted: #94a3b8;
            --teal: #5eead4;
            --blue: #93c5fd;
            --amber: #fbbf24;
            --rose: #fda4af;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: var(--text);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 8%, rgba(94, 234, 212, 0.13), transparent 30%),
                radial-gradient(circle at 88% 10%, rgba(147, 197, 253, 0.12), transparent 24%),
                linear-gradient(145deg, #05070d 0%, #09111f 44%, #0b1118 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(5, 7, 13, 0.42);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        [data-testid="stSidebar"] {
            background: rgba(8, 13, 23, 0.88);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1240px;
        }

        #MainMenu, footer {visibility: hidden;}
        .stDeployButton {display: none;}

        h1, h2, h3 {
            letter-spacing: 0;
            color: #ffffff;
        }

        p, li, label, span, div {
            letter-spacing: 0;
        }

        .hero-shell {
            border: 1px solid var(--line);
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(17, 24, 39, 0.58));
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
            border-radius: 8px;
            padding: 28px;
            margin-bottom: 18px;
            backdrop-filter: blur(24px);
        }

        .eyebrow {
            color: var(--teal);
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 8px;
        }

        .hero-title {
            font-size: 38px;
            font-weight: 800;
            line-height: 1.08;
            margin: 0 0 10px 0;
            color: #ffffff;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.55;
            max-width: 820px;
        }

        .glass-card {
            border: 1px solid var(--line);
            background: var(--panel);
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(20px);
            margin-bottom: 14px;
        }

        .section-title {
            color: #ffffff;
            font-size: 16px;
            font-weight: 750;
            margin-bottom: 8px;
        }

        .muted {
            color: var(--muted);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            border: 1px solid rgba(94, 234, 212, 0.35);
            background: rgba(94, 234, 212, 0.10);
            color: #ccfbf1;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: 700;
        }

        .demo-pill {
            display: inline-flex;
            border: 1px solid rgba(251, 191, 36, 0.45);
            background: rgba(251, 191, 36, 0.12);
            color: #fde68a;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: 700;
        }

        .metric-card {
            border: 1px solid var(--line);
            background: rgba(15, 23, 42, 0.72);
            border-radius: 8px;
            padding: 16px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .metric-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 800;
            margin-top: 4px;
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input {
            background: rgba(15, 23, 42, 0.78) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
        }

        .stTextArea textarea {
            min-height: 150px;
        }

        .stButton > button, .stDownloadButton > button, button[kind="primary"] {
            border-radius: 8px !important;
            border: 1px solid rgba(94, 234, 212, 0.38) !important;
            background: linear-gradient(135deg, #5eead4 0%, #93c5fd 100%) !important;
            color: #06111f !important;
            font-weight: 800 !important;
            min-height: 42px;
            box-shadow: 0 14px 35px rgba(94, 234, 212, 0.18);
        }

        .stDownloadButton > button {
            background: rgba(15, 23, 42, 0.88) !important;
            color: #e5e7eb !important;
            box-shadow: none;
        }

        div[data-testid="stAlert"] {
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
        }

        .copy-box {
            width: 100%;
            min-height: 170px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,.12);
            background: rgba(2,6,23,.72);
            color: #e5e7eb;
            padding: 12px;
            font: 14px Inter, sans-serif;
            line-height: 1.55;
        }

        .copy-button {
            border: 1px solid rgba(94,234,212,.38);
            background: linear-gradient(135deg, #5eead4, #93c5fd);
            color: #06111f;
            font-weight: 800;
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            margin: 0 0 10px 0;
        }

        @media (max-width: 760px) {
            .hero-title { font-size: 29px; }
            .hero-shell { padding: 20px; }
            .block-container { padding-left: 1rem; padding-right: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    settings = get_settings()
    if LOGO_PATH.exists():
        st.sidebar.image(str(LOGO_PATH), width=64)
    st.sidebar.markdown(f"### {settings.app_name}")
    st.sidebar.caption(settings.app_tagline)
    status = "Demo mode" if settings.effective_demo_mode else f"OpenAI: {settings.openai_model}"
    st.sidebar.markdown(f"<span class='status-pill'>{html.escape(status)}</span>", unsafe_allow_html=True)
    st.sidebar.divider()
    snapshot = metric_snapshot()
    st.sidebar.metric("Tasks", snapshot["Total Tasks Generated"])
    st.sidebar.metric("Reports", snapshot["Reports Generated"])
    st.sidebar.metric("Emails", snapshot["Emails Generated"])
    st.sidebar.metric("Automation Plans", snapshot["Automation Plans Created"])


def render_page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="eyebrow">{html.escape(eyebrow)}</div>
            <div class="hero-title">{html.escape(title)}</div>
            <div class="hero-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_grid(metrics: Dict[str, int]) -> None:
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(label)}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _content_to_html(content: str) -> str:
    lines = content.strip().splitlines()
    html_parts = []
    in_list = False

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue
        if line.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p>{html.escape(line)}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "".join(html_parts) or "<p>No content returned.</p>"


def render_result(result: GeneratedResult) -> None:
    badge = "<span class='demo-pill'>Demo output</span>" if result.is_demo else "<span class='status-pill'>OpenAI generated</span>"
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="eyebrow">Generated deliverable</div>
            <h2 style="margin:0 0 10px 0;">{html.escape(result.title)}</h2>
            {badge}
            <p class="muted" style="margin-top:10px;">Model: {html.escape(result.model)} | {result.generated_at.strftime('%Y-%m-%d %H:%M UTC')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for section_name, content in result.sections.items():
        section_html = _content_to_html(content)
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">{html.escape(section_name)}</div>
                <div>{section_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_export_buttons(result: GeneratedResult) -> None:
    st.markdown("#### Export")
    col_pdf, col_docx, col_txt = st.columns(3)
    with col_pdf:
        st.download_button(
            "Download PDF",
            data=export_pdf(result),
            file_name=build_export_filename(result, "pdf"),
            mime="application/pdf",
            use_container_width=True,
        )
    with col_docx:
        st.download_button(
            "Download DOCX",
            data=export_docx(result),
            file_name=build_export_filename(result, "docx"),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with col_txt:
        st.download_button(
            "Download TXT",
            data=export_txt(result),
            file_name=build_export_filename(result, "txt"),
            mime="text/plain",
            use_container_width=True,
        )


def render_copyable_text(label: str, value: str, key: str) -> None:
    text_json = json.dumps(value)
    label_json = json.dumps(label)
    components.html(
        f"""
        <button class="copy-button" onclick='navigator.clipboard.writeText({text_json}); this.innerText="Copied"; setTimeout(() => this.innerText="Copy " + {label_json}, 1200);'>
            Copy {html.escape(label)}
        </button>
        <textarea class="copy-box" readonly>{html.escape(value)}</textarea>
        <style>
        .copy-box {{
            width: 100%;
            min-height: 170px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,.12);
            background: rgba(2,6,23,.72);
            color: #e5e7eb;
            padding: 12px;
            font: 14px Inter, sans-serif;
            line-height: 1.55;
        }}
        .copy-button {{
            border: 1px solid rgba(94,234,212,.38);
            background: linear-gradient(135deg, #5eead4, #93c5fd);
            color: #06111f;
            font-weight: 800;
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            margin: 0 0 10px 0;
        }}
        </style>
        """,
        height=260,
    )


def render_history_browser(module_key: str | None = None) -> None:
    history = get_history(module_key)
    if not history:
        st.sidebar.caption("No history yet for this workspace session.")
        return

    labels = [f"{item.result.generated_at.strftime('%H:%M')} - {item.result.module_name}: {item.result.title[:42]}" for item in history]
    selected_label = st.sidebar.selectbox("Session history", labels, key=f"history_{module_key or 'all'}")
    selected = history[labels.index(selected_label)]
    if st.sidebar.button("Show selected output", use_container_width=True, key=f"show_history_{module_key or 'all'}"):
        st.session_state["selected_history_id"] = selected.id


def render_selected_history() -> None:
    selected_id = st.session_state.get("selected_history_id")
    if not selected_id:
        return
    for item in get_history():
        if item.id == selected_id:
            st.info("Showing a previous output from this session.")
            render_result(item.result)
            render_export_buttons(item.result)
            break


def render_template_cards(templates: Iterable[object]) -> None:
    for template in templates:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">{html.escape(template.name)}</div>
                <p class="muted" style="margin:0 0 8px 0;">{html.escape(template.best_for)}</p>
                <p style="margin:0;">{html.escape(template.prompt)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def handle_generation_error(exc: Exception) -> None:
    st.error(f"Generation failed: {exc}")
    st.caption("Check your OpenAI API key, model name, network access, and dependency installation.")
