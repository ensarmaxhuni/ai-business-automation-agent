"""Prompt registry for enterprise business automation workflows."""

from __future__ import annotations

from typing import Dict, List

from .schemas import ModulePrompt, PromptTemplateItem


BASE_SYSTEM_ROLE = """
You are an enterprise AI business automation consultant working with senior leaders.
Write with the rigor of a top-tier consulting partner and the clarity of an executive chief of staff.
Use concrete business language, measurable actions, and pragmatic recommendations.
Avoid generic motivational writing. Be concise, structured, and board-ready.
Return only valid JSON matching this schema:
{
  "title": "Short professional title",
  "sections": {
    "Section Name": "Clear markdown content"
  }
}
Do not wrap the JSON in markdown fences.
"""


MODULE_PROMPTS: Dict[str, ModulePrompt] = {
    "executive_assistant": ModulePrompt(
        key="executive_assistant",
        name="Executive AI Assistant",
        description="Convert business requests into executive summaries, insights, recommendations, and action plans.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Business request:
{business_request}

Requested output style:
{output_style}

Template context:
{template_context}

Create an executive-grade response for a business leader.
        """,
        sections=["Executive Summary", "Key Insights", "Recommendations", "Action Plan"],
    ),
    "meeting_intelligence": ModulePrompt(
        key="meeting_intelligence",
        name="Meeting Intelligence",
        description="Extract decisions, risks, follow-ups, and an executive brief from meeting notes.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Meeting type:
{meeting_type}

Audience:
{audience}

Meeting notes:
{meeting_notes}

Convert the notes into a concise meeting intelligence brief.
        """,
        sections=[
            "Meeting Summary",
            "Key Decisions",
            "Action Items",
            "Risks Identified",
            "Follow-Up Tasks",
            "Executive Brief",
        ],
    ),
    "email_generator": ModulePrompt(
        key="email_generator",
        name="Professional Email Generator",
        description="Generate polished stakeholder communication in multiple executive-ready formats.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Email type:
{email_type}

Recipient type:
{recipient_type}

Tone:
{tone}

Purpose:
{purpose}

Additional context:
{additional_context}

Generate the communication with a polished commercial tone.
        """,
        sections=["Subject Line", "Professional Email", "Executive Version", "Concise Version"],
    ),
    "report_generator": ModulePrompt(
        key="report_generator",
        name="Business Report Generator",
        description="Create consulting-grade reports with findings, recommendations, implementation plans, and risks.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Topic:
{topic}

Industry:
{industry}

Context:
{context}

Create a structured professional business report.
        """,
        sections=[
            "Executive Summary",
            "Situation Analysis",
            "Key Findings",
            "Strategic Recommendations",
            "Implementation Plan",
            "Risk Assessment",
            "Conclusion",
        ],
    ),
    "research_analyst": ModulePrompt(
        key="research_analyst",
        name="AI Research Analyst",
        description="Produce strategic research briefs on industries, markets, and business topics.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Research topic:
{topic}

Market or region:
{market}

Decision context:
{decision_context}

Create an executive research analyst brief. Use current strategic reasoning, but do not invent citations or real-time facts.
        """,
        sections=[
            "Industry Overview",
            "Market Trends",
            "Opportunities",
            "Risks",
            "Strategic Insights",
            "Future Outlook",
            "Executive Summary",
        ],
    ),
    "swot_generator": ModulePrompt(
        key="swot_generator",
        name="SWOT Analysis Generator",
        description="Create a consulting-style SWOT analysis for a company, initiative, market, or product.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Subject:
{subject}

Industry:
{industry}

Strategic context:
{context}

Create a professional SWOT analysis for executive review.
        """,
        sections=["Strengths", "Weaknesses", "Opportunities", "Threats"],
    ),
    "automation_planner": ModulePrompt(
        key="automation_planner",
        name="Business Automation Planner",
        description="Identify workflow bottlenecks and produce a practical automation roadmap.",
        system_role=BASE_SYSTEM_ROLE,
        user_prompt="""
Workflow description:
{workflow}

Business team:
{team}

Monthly volume or scale:
{volume}

Create an automation plan that balances process improvement, AI opportunities, governance, and measurable value.
        """,
        sections=[
            "Current Process",
            "Bottlenecks",
            "Automation Opportunities",
            "AI Opportunities",
            "Estimated Time Savings",
            "Estimated Cost Savings",
            "Recommended Tools",
            "Implementation Roadmap",
        ],
    ),
}


PROMPT_TEMPLATES: List[PromptTemplateItem] = [
    PromptTemplateItem(
        name="CEO Briefing",
        best_for="Rapid executive updates",
        prompt="Prepare a concise CEO briefing on the current business situation, key risks, strategic options, and recommended next actions.",
    ),
    PromptTemplateItem(
        name="Consulting Report",
        best_for="Client-ready analysis",
        prompt="Create a consulting-style report with context, diagnosis, strategic recommendations, implementation roadmap, and risks.",
    ),
    PromptTemplateItem(
        name="Board Presentation",
        best_for="Board and investor meetings",
        prompt="Draft a board-level narrative covering performance, strategic priorities, operating risks, financial implications, and leadership asks.",
    ),
    PromptTemplateItem(
        name="Market Analysis",
        best_for="Industry research",
        prompt="Analyze the market landscape, demand drivers, competitive dynamics, opportunities, threats, and near-term outlook.",
    ),
    PromptTemplateItem(
        name="Investor Memo",
        best_for="Capital allocation decisions",
        prompt="Write an investor memo covering thesis, market opportunity, business model, risks, mitigants, financial logic, and decision recommendation.",
    ),
    PromptTemplateItem(
        name="Business Strategy",
        best_for="Strategic planning",
        prompt="Develop a business strategy with objectives, target segments, value proposition, operating model, roadmap, and KPIs.",
    ),
    PromptTemplateItem(
        name="Operations Review",
        best_for="Process and productivity reviews",
        prompt="Assess operational performance, bottlenecks, automation candidates, quality issues, metrics, and improvement roadmap.",
    ),
]


def get_module_prompt(module_key: str) -> ModulePrompt:
    try:
        return MODULE_PROMPTS[module_key]
    except KeyError as exc:
        raise ValueError(f"Unknown module key: {module_key}") from exc


def get_template_names() -> List[str]:
    return [template.name for template in PROMPT_TEMPLATES]


def get_template_prompt(name: str) -> str:
    for template in PROMPT_TEMPLATES:
        if template.name == name:
            return template.prompt
    return ""
