"""
rubric-scorer / logic.py
========================
Scores a piece of student text against a list of plain-language rubric criteria.

Entry point:
    run(input: dict) -> dict

See skills.md for full schema documentation.
"""

from __future__ import annotations

import re
from typing import Any


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(input: dict[str, Any]) -> dict[str, Any]:
    """
    Score student text against rubric criteria.

    Args:
        input: {
            "text":            str   — student text to evaluate (required)
            "rubric":          list  — list of criterion strings (required)
            "strict":          bool  — require ≥3 keyword matches (default False)
            "min_keyword_len": int   — min word length to be a keyword (default 4)
        }

    Returns:
        {
            "met":     list[str]  — criteria matched
            "missed":  list[str]  — criteria not matched
            "score":   float      — fraction matched, rounded to 2dp
            "total":   int        — total criteria count
            "summary": str        — one-sentence natural-language summary
        }

    Raises:
        ValueError: if required keys are missing or types are wrong
    """
    text: str = _require_str(input, "text")
    rubric: list[str] = _require_list(input, "rubric")
    strict: bool = bool(input.get("strict", False))
    min_kw_len: int = int(input.get("min_keyword_len", 4))

    text_lower = text.lower()
    met: list[str] = []
    missed: list[str] = []

    for criterion in rubric:
        if not isinstance(criterion, str) or not criterion.strip():
            missed.append(criterion)
            continue
        if _criterion_met(criterion, text_lower, strict=strict, min_keyword_len=min_kw_len):
            met.append(criterion)
        else:
            missed.append(criterion)

    total = len(rubric)
    score = round(len(met) / total, 2) if total > 0 else 0.0
    summary = _make_summary(met, missed, total)

    return {
        "met": met,
        "missed": missed,
        "score": score,
        "total": total,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _keywords_from(phrase: str, min_len: int) -> list[str]:
    """Extract content keywords from a criterion phrase."""
    words = re.findall(r"[a-z']+", phrase.lower())
    return [w for w in words if len(w) >= min_len]


def _criterion_met(criterion: str, text_lower: str, *, strict: bool, min_keyword_len: int) -> bool:
    """Return True if the criterion is satisfied by the text."""
    keywords = _keywords_from(criterion, min_keyword_len)
    if not keywords:
        # No content keywords — treat as unverifiable → not met
        return False

    matches = sum(1 for kw in keywords if kw in text_lower)

    if strict:
        return matches >= min(3, len(keywords))
    else:
        # Non-strict: any keyword match counts
        return matches >= 1


def _make_summary(met: list[str], missed: list[str], total: int) -> str:
    n_met = len(met)
    if total == 0:
        return "No rubric criteria were provided."
    if n_met == total:
        return f"Met all {total} criteria."
    if n_met == 0:
        criteria_list = ", ".join(missed)
        return f"Met 0 of {total} criteria; missing: {criteria_list}."
    criteria_list = ", ".join(missed)
    return f"Met {n_met} of {total} criteria; missing: {criteria_list}."


def _require_str(d: dict, key: str) -> str:
    if key not in d:
        raise ValueError(f"Missing required field: '{key}'")
    if not isinstance(d[key], str):
        raise ValueError(f"Field '{key}' must be a string, got {type(d[key]).__name__}")
    return d[key]


def _require_list(d: dict, key: str) -> list:
    if key not in d:
        raise ValueError(f"Missing required field: '{key}'")
    if not isinstance(d[key], list):
        raise ValueError(f"Field '{key}' must be a list, got {type(d[key]).__name__}")
    return d[key]
