---
skill_id: "rubric-scorer"
name: "Rubric Scorer"
skill_type: "code"
tags: ["rubric", "scoring", "feedback", "assessment", "writing", "cs"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "verify-claims"
  - "evaluate-reasoning"
trigger_signals:
  - "student-submitted-draft"
  - "student-requesting-feedback"
  - "rubric-check-needed"
python_entry: "logic.py"
chip_icon: "📋"
version: "0.1.0"
---

# Rubric Scorer

## Description

Given a piece of student text and a list of rubric criteria (plain-language strings), scores which criteria are demonstrably met and which are missing. Returns a structured result with met/missed lists, a 0–1 score, and a short summary. Designed to give the orchestrator fast, deterministic feedback signals before the tutor constructs a response.

## When to Trigger

- A student has submitted a draft essay, explanation, or response and the orchestrator needs to know how many rubric criteria are satisfied before selecting a skill
- The current assignment has a rubric and the session needs a feedback signal
- The orchestrator is about to invoke a follow-up skill and needs to know what's still missing

## Inputs

A dict with keys:

- `text` (str, required): the student's text to evaluate
- `rubric` (list[str], required): list of plain-language rubric criteria, e.g. `["Contains a clear thesis", "Cites at least two sources"]`
- `strict` (bool, optional, default `false`): if `true`, a criterion is only met if at least 3 words from the criterion phrase appear verbatim in the text (rather than any keyword match)
- `min_keyword_len` (int, optional, default `4`): minimum character length a word must have to be considered a content keyword (filters out stop words like "the", "a", "is")

## Outputs

A dict with keys:

- `met` (list[str]): criteria that were matched in the text
- `missed` (list[str]): criteria that were not matched
- `score` (float): fraction of criteria met, rounded to 2 decimal places (e.g. `0.75`)
- `total` (int): total number of criteria evaluated
- `summary` (str): a one-sentence natural-language summary, e.g. "Met 3 of 4 criteria; missing: Cites at least two sources."

## Usage

```python
from logic import run

result = run({
    "text": "The French Revolution was driven by economic inequality. Historians like Schama argue that fiscal crisis was central.",
    "rubric": [
        "Contains a clear thesis",
        "Mentions economic causes",
        "Cites at least two sources",
        "Discusses political consequences"
    ]
})
# result == {
#     "met":    ["Contains a clear thesis", "Mentions economic causes"],
#     "missed": ["Cites at least two sources", "Discusses political consequences"],
#     "score":  0.5,
#     "total":  4,
#     "summary": "Met 2 of 4 criteria; missing: Cites at least two sources, Discusses political consequences."
# }
```

## Notes

Matching is keyword-based: content words (length ≥ `min_keyword_len`) are extracted from each criterion and checked against the lowercased text. This is intentionally simple and fast — not semantic. For richer matching, replace the `_keywords_match` helper with an embedding-based check. Pure function; no side effects; safe to call repeatedly.
