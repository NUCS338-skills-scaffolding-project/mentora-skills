"""
logic.py — Session Opener Context Builder
Reads the assignment doc and learning goals doc, then uses the LLM
to dynamically form a diagnostic opening question from goal 1.
Works for any assignment, any subject.
"""

import re
import json
import urllib.request


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_learning_goals(learning_goals_text: str) -> list[dict]:
    """
    Parses a markdown learning goals doc and returns an ordered list of goals.
    Each goal is a dict with:
      - index: int (1-based order)
      - title: str
      - description: str
    """
    goals = []
    pattern = r"(\d+)\.\s+\*\*(.+?)\*\*\s+[—-]\s+(.+)"
    for match in re.finditer(pattern, learning_goals_text):
        goals.append({
            "index": int(match.group(1)),
            "title": match.group(2).strip(),
            "description": match.group(3).strip(),
        })
    return goals


def get_first_goal(learning_goals_text: str) -> dict | None:
    """
    Returns the first learning goal from the doc.
    Learning goals follow the order of the assignment,
    so goal 1 is always the right entry point.
    """
    goals = parse_learning_goals(learning_goals_text)
    return goals[0] if goals else None


def get_assignment_name(assignment_text: str) -> str:
    """
    Extracts the assignment name from the assignment doc.
    Looks for the first heading or bolded title.
    Falls back to 'your assignment' if nothing is found.
    """
    heading_match = re.search(r"^#{1,3}\s+(.+)", assignment_text, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    bold_match = re.search(r"\*\*(.+?)\*\*", assignment_text)
    if bold_match:
        return bold_match.group(1).strip()

    return "your assignment"


# ── LLM call ──────────────────────────────────────────────────────────────────

def generate_diagnostic_question(assignment_name: str, goal_title: str, goal_description: str) -> str:
    """
    Calls the LLM to generate one diagnostic question from the first learning goal.
    The question must be:
    - Grounded in the specific concept named in goal_title
    - Answerable from zero — the student has not started yet
    - A yes/no or simple open question that naturally opens into conversation
    - Not a summary or explanation of the goal
    """
    prompt = f"""You are forming the opening question for a tutoring session.

Assignment: {assignment_name}
First learning goal title: {goal_title}
First learning goal description: {goal_description}

Write ONE short diagnostic question that:
- Is grounded in the concept named in the learning goal title
- Can be answered by a student who has not started the assignment yet
- Surfaces prior knowledge — not progress
- Is a yes/no or simple open question (yes/no preferred as it opens conversation naturally)
- Is direct and concrete — no filler

Return only the question, nothing else. No preamble, no punctuation beyond the question mark."""

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["content"][0]["text"].strip()


# ── Main entry point ───────────────────────────────────────────────────────────

def build_opener_context(assignment_text: str, learning_goals_text: str) -> dict:
    """
    Main entry point. Returns a context dict for the session opener skill:
      - assignment_name: str
      - first_goal_title: str
      - first_goal_description: str
      - opener_prompt: str — fully formed one-line opener ready for the tutor
    """
    assignment_name = get_assignment_name(assignment_text)
    first_goal = get_first_goal(learning_goals_text)

    if not first_goal:
        return {
            "assignment_name": assignment_name,
            "first_goal_title": None,
            "first_goal_description": None,
            "opener_prompt": f"Hi! I see you have the {assignment_name} — what are you working on today?",
        }

    diagnostic_question = generate_diagnostic_question(
        assignment_name=assignment_name,
        goal_title=first_goal["title"],
        goal_description=first_goal["description"],
    )

    # Lowercase the first letter so it flows naturally after the dash
    opener_prompt = f"Hi! I see you have the {assignment_name} — {diagnostic_question[0].lower()}{diagnostic_question[1:]}"

    return {
        "assignment_name": assignment_name,
        "first_goal_title": first_goal["title"],
        "first_goal_description": first_goal["description"],
        "opener_prompt": opener_prompt,
    }
