---
skill_id: "edge-case-gen"
name: "Edge Case Generator"
skill_type: "code"
tags: ["testing", "edge-cases", "cs", "unit-tests", "verification"]
course_types: ["cs"]
learning_goal_tags:
  - "handle-edge-cases"
  - "design-test-plans"
trigger_signals:
  - "student-writing-tests"
  - "student-missing-edge-cases"
  - "student-only-happy-path"
  - "student-needs-test-ideas"
python_entry: "logic.py"
chip_icon: "🧪"
version: "0.1.0"
---

# Edge Case Generator

## Description

Given a Python function signature (as a string) and an optional docstring, generates a structured list of edge cases worth testing. Uses heuristic rules over type annotations and common patterns to surface boundary values, empty inputs, type extremes, and error-producing inputs — without relying on an LLM. Intended as a fast, deterministic first pass before a student writes their test suite.

## When to Trigger

- Student has written a function signature and needs test ideas beyond the happy path
- Student's test suite only covers normal inputs and the orchestrator detects missing coverage
- Student asks "what else should I test?"
- Assignment requires explicit edge-case coverage

## Inputs

A dict with keys:

- `signature` (str, required): the Python function signature, e.g. `"def clamp(value: int, low: int, high: int) -> int"`
- `docstring` (str, optional, default `""`): the function's docstring — used to extract additional boundary hints from natural-language constraints like "must be positive" or "raises ValueError if empty"
- `n` (int, optional, default `8`): maximum number of edge cases to return

## Outputs

A dict with keys:

- `edge_cases` (list[dict]): each entry has:
  - `id` (str): short slug, e.g. `"empty-list-input"`
  - `description` (str): what scenario this tests
  - `category` (str): one of `boundary`, `empty`, `type-extreme`, `error-condition`, `none-null`, `ordering`
  - `example_input_hint` (str): a natural-language hint for what to pass, e.g. `"value=0, low=0, high=0"`
  - `expected_behavior` (str): what the function should do (return, raise, etc.)
- `param_summary` (list[dict]): parsed parameters with `name` and `type_hint`
- `docstring_hints` (list[str]): constraint phrases extracted from the docstring

## Usage

```python
from logic import run

result = run({
    "signature": "def clamp(value: int, low: int, high: int) -> int",
    "docstring": "Returns value clamped to [low, high]. Raises ValueError if low > high.",
    "n": 5
})
# result["edge_cases"] might include:
# [
#   {"id": "low-equals-high",    "description": "Range is a single point",    ...},
#   {"id": "value-below-low",    "description": "Value below lower bound",     ...},
#   {"id": "value-above-high",   "description": "Value above upper bound",     ...},
#   {"id": "low-gt-high-raises", "description": "low > high should raise",     ...},
#   {"id": "value-equals-low",   "description": "Value exactly at lower bound",...},
# ]
```

## Notes

Parsing is done with Python's `inspect` and `ast` modules — no external dependencies. The generator applies a fixed set of heuristic rules per type (int → zero/negative/max, list → empty/single-element, str → empty/whitespace/unicode, etc.) and ranks candidates by estimated test value. Results are deterministic for a given input. For richer semantic generation, replace the rule engine with an LLM call that respects the same output schema.
