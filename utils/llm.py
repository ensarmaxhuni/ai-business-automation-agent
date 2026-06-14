"""LLM orchestration for business automation workflows."""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List

from .config import get_settings
from .prompts import get_module_prompt
from .schemas import GeneratedResult

logger = logging.getLogger(__name__)


class LLMGenerationError(RuntimeError):
    """Raised when the AI provider fails to return a usable response."""


def _format_prompt(template: str, inputs: Dict[str, Any]) -> str:
    safe_inputs = {key: str(value or "").strip() for key, value in inputs.items()}
    return template.format(**safe_inputs)


def _build_messages(module_key: str, inputs: Dict[str, Any]) -> List[Dict[str, str]]:
    prompt = get_module_prompt(module_key)
    expected_sections = ", ".join(prompt.sections)
    user_prompt = _format_prompt(prompt.user_prompt, inputs)
    user_prompt += f"""

Required section names, in this exact order:
{expected_sections}

Quality bar:
- Make the content specific to the request.
- Use executive-ready language.
- Include practical next steps where relevant.
- Keep each section focused and scannable.
"""
    return [
        {"role": "system", "content": prompt.system_role},
        {"role": "user", "content": user_prompt},
    ]


def _extract_json(raw_content: str) -> Dict[str, Any]:
    content = raw_content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if not match:
            raise
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("AI response did not contain a JSON object.")
    return parsed


def _normalize_sections(module_key: str, sections: Dict[str, Any]) -> Dict[str, str]:
    prompt = get_module_prompt(module_key)
    normalized: Dict[str, str] = {}
    for section in prompt.sections:
        value = sections.get(section) or sections.get(section.lower()) or ""
        normalized[section] = str(value).strip() or "No content returned for this section."
    return normalized


def _demo_response(module_key: str, inputs: Dict[str, Any]) -> GeneratedResult:
    prompt = get_module_prompt(module_key)
    subject = (
        inputs.get("business_request")
        or inputs.get("topic")
        or inputs.get("subject")
        or inputs.get("workflow")
        or inputs.get("purpose")
        or "the requested business initiative"
    )
    context = "; ".join(f"{key.replace('_', ' ').title()}: {value}" for key, value in inputs.items() if value)
    sections: Dict[str, str] = {}

    for section in prompt.sections:
        if section in {"Estimated Time Savings", "Estimated Cost Savings"}:
            sections[section] = (
                f"Initial estimate for {subject}: 20-35% productivity improvement after process standardization, "
                "intake automation, and AI-assisted review. Validate with a two-week baseline measurement before committing ROI."
            )
        elif "Action" in section or "Roadmap" in section or "Implementation" in section:
            sections[section] = (
                f"- Define success metrics and executive owner for {subject}.\n"
                "- Map the current workflow, decision points, handoffs, and data sources.\n"
                "- Pilot the highest-value use case with governance, auditability, and human approval.\n"
                "- Scale after measuring cycle time, quality, cost impact, and stakeholder satisfaction."
            )
        elif section == "Subject Line":
            sections[section] = f"Next steps regarding {subject}"
        elif "Email" in section or "Version" in section:
            sections[section] = (
                f"Hello,\n\nI wanted to share a concise update regarding {subject}. Based on the current context, "
                "the recommended next step is to align on objectives, confirm owners, and move forward with a practical execution plan.\n\n"
                "Please let me know if you would like me to prepare a more detailed brief.\n\nBest regards,"
            )
        else:
            sections[section] = (
                f"{section} for {subject}: The priority is to convert the request into a measurable business outcome. "
                f"Relevant context: {context or 'No additional context provided.'} "
                "Recommended focus areas include stakeholder alignment, operating impact, risk controls, execution milestones, and KPI tracking."
            )

    return GeneratedResult(
        title=f"{prompt.name}: {str(subject)[:70]}",
        module_key=module_key,
        module_name=prompt.name,
        sections=sections,
        inputs=inputs,
        generated_at=datetime.utcnow(),
        model="demo-mode",
        is_demo=True,
    )


def generate_business_output(module_key: str, inputs: Dict[str, Any]) -> GeneratedResult:
    """Generate structured business output using OpenAI or deterministic demo mode."""

    settings = get_settings()
    prompt = get_module_prompt(module_key)

    if settings.effective_demo_mode:
        logger.info("Using demo mode for module=%s", module_key)
        return _demo_response(module_key, inputs)

    try:
        from openai import OpenAI, OpenAIError
    except ImportError as exc:
        logger.exception("OpenAI SDK is not installed.")
        raise LLMGenerationError("OpenAI SDK is not installed. Run `pip install -r requirements.txt`.") from exc

    client = OpenAI(api_key=settings.openai_api_key)
    messages = _build_messages(module_key, inputs)

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            response_format={"type": "json_object"},
        )
    except OpenAIError as exc:
        logger.exception("OpenAI request failed for module=%s", module_key)
        raise LLMGenerationError(f"OpenAI request failed: {exc}") from exc

    content = response.choices[0].message.content or ""
    try:
        parsed = _extract_json(content)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.exception("Could not parse AI response for module=%s", module_key)
        raise LLMGenerationError("The AI response could not be parsed into structured JSON.") from exc

    raw_sections = parsed.get("sections", {})
    if not isinstance(raw_sections, dict):
        raise LLMGenerationError("The AI response did not include a valid `sections` object.")

    return GeneratedResult(
        title=str(parsed.get("title") or prompt.name),
        module_key=module_key,
        module_name=prompt.name,
        sections=_normalize_sections(module_key, raw_sections),
        inputs=inputs,
        generated_at=datetime.utcnow(),
        model=settings.openai_model,
        is_demo=False,
    )
