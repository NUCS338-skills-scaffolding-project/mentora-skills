"""
edge-case-gen / logic.py
========================
Generates a structured list of edge cases for a Python function
using heuristic rules over its type annotations.

Entry point:
    run(input: dict) -> dict

See skills.md for full schema documentation.
"""

from __future__ import annotations

import ast
import re
from typing import Any


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(input: dict[str, Any]) -> dict[str, Any]:
    """
    Generate edge cases for a Python function.

    Args:
        input: {
            "signature": str  — Python function signature (required)
            "docstring":  str  — function docstring (optional, default "")
            "n":          int  — max edge cases to return (optional, default 8)
        }

    Returns:
        {
            "edge_cases":      list[dict]  — generated edge case records
            "param_summary":   list[dict]  — parsed param names + type hints
            "docstring_hints": list[str]   — constraint phrases from docstring
        }
    """
    signature: str = _require_str(input, "signature")
    docstring: str = str(input.get("docstring", ""))
    n: int = max(1, int(input.get("n", 8)))

    params = _parse_params(signature)
    docstring_hints = _extract_docstring_hints(docstring)
    candidates = _generate_candidates(params, docstring_hints)

    # Deduplicate by id, then cap at n
    seen: set[str] = set()
    edge_cases: list[dict] = []
    for c in candidates:
        if c["id"] not in seen:
            seen.add(c["id"])
            edge_cases.append(c)
        if len(edge_cases) >= n:
            break

    return {
        "edge_cases": edge_cases,
        "param_summary": [{"name": p["name"], "type_hint": p["type_hint"]} for p in params],
        "docstring_hints": docstring_hints,
    }


# ---------------------------------------------------------------------------
# Signature parser
# ---------------------------------------------------------------------------

def _parse_params(signature: str) -> list[dict]:
    """
    Parse a function signature and return a list of param dicts.
    Each dict has: name, type_hint (str, may be "unknown").
    """
    # Strip leading "def " and trailing ": ..." return annotation
    sig = signature.strip()
    # Extract just the argument list
    m = re.search(r"\(([^)]*)\)", sig)
    if not m:
        return []
    arg_str = m.group(1).strip()
    if not arg_str:
        return []

    params = []
    for raw in arg_str.split(","):
        raw = raw.strip()
        if not raw or raw in ("self", "cls", "*", "**"):
            continue
        # Strip default value
        raw = raw.split("=")[0].strip()
        # Strip **kwargs / *args prefix
        raw = raw.lstrip("*")
        if not raw:
            continue
        if ":" in raw:
            name, _, hint = raw.partition(":")
            params.append({"name": name.strip(), "type_hint": hint.strip()})
        else:
            params.append({"name": raw.strip(), "type_hint": "unknown"})
    return params


# ---------------------------------------------------------------------------
# Docstring hint extractor
# ---------------------------------------------------------------------------

_CONSTRAINT_PATTERNS = [
    r"must be (positive|negative|non-?negative|non-?zero|non-?empty)",
    r"raises?\s+\w+error\s+if\s+[^\.\n]+",
    r"cannot be (empty|none|null|negative|zero)",
    r"(should|must) not be (empty|none|null|negative|zero)",
    r"length (must|should) be",
    r"at least \d+",
    r"at most \d+",
    r"between \d+ and \d+",
]

_CONSTRAINT_RE = re.compile("|".join(_CONSTRAINT_PATTERNS), re.IGNORECASE)


def _extract_docstring_hints(docstring: str) -> list[str]:
    hints = []
    for sentence in re.split(r"[.!\n]", docstring):
        s = sentence.strip()
        if s and _CONSTRAINT_RE.search(s):
            hints.append(s)
    return hints[:6]  # cap at 6


# ---------------------------------------------------------------------------
# Heuristic rule engine
# ---------------------------------------------------------------------------

# Maps type hint patterns → list of (id_suffix, description, category, input_hint, expected_behavior)
_INT_RULES = [
    ("zero",     "Zero value",           "boundary",      "param=0",             "should handle zero without error"),
    ("negative", "Negative value",       "boundary",      "param=-1",            "depends on function contract"),
    ("large",    "Large positive value", "type-extreme",  "param=10**9",         "should not overflow or error unexpectedly"),
]
_STR_RULES = [
    ("empty-str",     "Empty string",         "empty",         'param=""',             "depends — may raise or return default"),
    ("whitespace",    "Whitespace-only string","boundary",      'param="   "',          "should handle or strip whitespace"),
    ("very-long-str", "Very long string",     "type-extreme",  'param="a"*10000',      "should not crash on large input"),
    ("unicode",       "Unicode / non-ASCII",  "boundary",      'param="héllo wörld"',  "should handle multi-byte chars"),
]
_LIST_RULES = [
    ("empty-list",    "Empty list",           "empty",         "param=[]",             "depends — may raise or return default"),
    ("single-item",   "Single-element list",  "boundary",      "param=[x]",            "should work correctly with one element"),
    ("large-list",    "Large list",           "type-extreme",  "param=[...] * 10000",  "should not have quadratic blowup"),
    ("dupes",         "List with duplicates", "boundary",      "param=[x, x, x]",      "behavior with repeated elements"),
]
_DICT_RULES = [
    ("empty-dict",   "Empty dict",    "empty",    "param={}",                "may raise KeyError or return default"),
    ("missing-key",  "Missing key",   "boundary", 'param={"other": val}',   "should raise KeyError or handle gracefully"),
]
_BOOL_RULES = [
    ("bool-true",  "True branch",  "boundary", "param=True",  "true path exercised"),
    ("bool-false", "False branch", "boundary", "param=False", "false path exercised"),
]
_NONE_RULES = [
    ("none-input", "None passed instead of value", "none-null", "param=None", "should raise TypeError or handle None"),
]

_TYPE_MAP: dict[str, list[tuple]] = {
    "int":    _INT_RULES,
    "float":  _INT_RULES,  # reuse int rules for floats
    "str":    _STR_RULES,
    "list":   _LIST_RULES,
    "dict":   _DICT_RULES,
    "bool":   _BOOL_RULES,
}

_DOCSTRING_EDGE_RULES = [
    (r"raises?\s+\w+error\s+if\s+(.+)", "docstring-raises-condition",
     "error-condition", "condition from docstring", "should raise as documented"),
    (r"must be positive",               "must-be-positive",
     "boundary", "param=0 or param=-1", "should raise or reject non-positive"),
    (r"must be non-?empty",             "must-be-non-empty",
     "empty", "param=[] or param=''", "should raise or reject empty input"),
    (r"must be non-?negative",          "must-be-non-negative",
     "boundary", "param=-1", "should raise or reject negative"),
]


def _generate_candidates(params: list[dict], docstring_hints: list[str]) -> list[dict]:
    candidates: list[dict] = []

    for param in params:
        name = param["name"]
        hint = param["type_hint"].lower().strip()

        # None is always worth testing for any typed param
        if hint not in ("unknown", "bool"):
            candidates.append({
                "id": f"{name}-is-none",
                "description": f"'{name}' passed as None instead of {hint}",
                "category": "none-null",
                "example_input_hint": f"{name}=None",
                "expected_behavior": "should raise TypeError or handle None explicitly",
            })

        # Match base type
        base = hint.split("[")[0]  # handle list[int] → list
        rules = _TYPE_MAP.get(base, [])
        for (suffix, desc, category, hint_tmpl, expected) in rules:
            candidates.append({
                "id": f"{name}-{suffix}",
                "description": f"'{name}': {desc}",
                "category": category,
                "example_input_hint": hint_tmpl.replace("param", name),
                "expected_behavior": expected,
            })

    # Add ordering edge case when ≥2 params of the same base type
    int_params = [p["name"] for p in params if p["type_hint"].lower().startswith(("int", "float"))]
    if len(int_params) >= 2:
        a, b = int_params[0], int_params[1]
        candidates.append({
            "id": f"{a}-equals-{b}",
            "description": f"'{a}' equals '{b}' — boundary where both bounds meet",
            "category": "boundary",
            "example_input_hint": f"{a}=5, {b}=5",
            "expected_behavior": "edge behavior when bounds/values are equal",
        })
        candidates.append({
            "id": f"{a}-greater-than-{b}",
            "description": f"'{a}' > '{b}' — inverted ordering",
            "category": "ordering",
            "example_input_hint": f"{a}=10, {b}=0",
            "expected_behavior": "depends on contract — may raise or swap",
        })

    # Docstring-derived candidates
    for hint_text in docstring_hints:
        for pattern, eid, category, ex_hint, expected in _DOCSTRING_EDGE_RULES:
            if re.search(pattern, hint_text, re.IGNORECASE):
                m = re.search(pattern, hint_text, re.IGNORECASE)
                desc_suffix = m.group(1).strip() if m and m.lastindex else hint_text
                candidates.append({
                    "id": eid,
                    "description": f"Docstring constraint: '{desc_suffix[:80]}'",
                    "category": category,
                    "example_input_hint": ex_hint,
                    "expected_behavior": expected,
                })
                break  # one rule per hint sentence

    return candidates


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _require_str(d: dict, key: str) -> str:
    if key not in d:
        raise ValueError(f"Missing required field: '{key}'")
    if not isinstance(d[key], str):
        raise ValueError(f"Field '{key}' must be a string, got {type(d[key]).__name__}")
    return d[key]
