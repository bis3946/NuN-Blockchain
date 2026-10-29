"""Conservative rule-based prototype for NuN-SUE.

This baseline detects a few obvious request/question patterns. It is not a
full semantic model and never executes commands or authorizes downstream work.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any


@dataclass(frozen=True)
class Interpretation:
    original_text: str
    normalized_text: str
    language: str
    intent: str
    meaning: str
    confidence: float
    needs_clarification: bool
    route: str
    action_allowed: bool = False
    policy_reason: str = "Interpretation alone never authorizes downstream actions."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def understand_sentence(text: str, language: str = "auto") -> Interpretation:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        raise ValueError("text must not be empty")
    if len(normalized) > 10_000:
        raise ValueError("text exceeds 10000-character limit")

    lang = language.lower()
    lower = normalized.lower()
    if lang == "auto":
        markers = ("č", "ć", "ž", "š", "đ", "molim", "što", "kako", "zašto")
        lang = "hr" if any(marker in lower for marker in markers) else "en"
    if lang not in {"hr", "en"}:
        raise ValueError("language must be 'auto', 'hr', or 'en'")

    if "?" in normalized:
        intent, meaning, confidence, clarify, route = (
            "question", "The input appears to ask a question.", 0.85, False, "question_handler"
        )
    elif lang == "hr" and re.match(
        r"^(molim te\s+)?(provjeri|objasni|prikaži|pokreni|napravi|analiziraj|nastavi)\b", lower
    ):
        intent, meaning, confidence, clarify, route = (
            "request", "The input appears to request an action.", 0.78, False, "request_review"
        )
    elif lang == "en" and re.match(
        r"^(please\s+)?(check|explain|show|run|create|analyze|continue)\b", lower
    ):
        intent, meaning, confidence, clarify, route = (
            "request", "The input appears to request an action.", 0.78, False, "request_review"
        )
    elif len(normalized.split()) < 2:
        intent, meaning, confidence, clarify, route = (
            "unclear", "There is too little text to infer a reliable intent.", 0.25, True, "clarification"
        )
    else:
        intent, meaning, confidence, clarify, route = (
            "assertion_or_unclear", "Context is required for a reliable interpretation.",
            0.40, True, "clarification"
        )

    return Interpretation(
        original_text=text,
        normalized_text=normalized,
        language=lang,
        intent=intent,
        meaning=meaning,
        confidence=confidence,
        needs_clarification=clarify or confidence < 0.5,
        route=route,
    )
