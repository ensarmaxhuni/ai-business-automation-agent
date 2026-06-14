"""Shared Pydantic models for the AI Business Automation Agent."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class GeneratedResult(BaseModel):
    """Normalized structured output returned by an AI workflow."""

    title: str = Field(..., min_length=1)
    module_key: str = Field(..., min_length=1)
    module_name: str = Field(..., min_length=1)
    sections: Dict[str, str] = Field(default_factory=dict)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model: str = "demo"
    is_demo: bool = False


class HistoryItem(BaseModel):
    """Session history item used by the dashboard and page sidebars."""

    id: str
    result: GeneratedResult


class ModulePrompt(BaseModel):
    """Prompt configuration for a business automation module."""

    key: str
    name: str
    description: str
    system_role: str
    user_prompt: str
    sections: List[str]


class PromptTemplateItem(BaseModel):
    """Reusable executive prompt template shown in the dashboard."""

    name: str
    best_for: str
    prompt: str
