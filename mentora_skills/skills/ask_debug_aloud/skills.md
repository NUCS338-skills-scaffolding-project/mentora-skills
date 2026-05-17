---
skill_id: "ask-debug-aloud"
name: "Ask Student to Debug Aloud"
skill_type: "instructional"
stance: "socratic"
tags: ["debugging", "problem solving", "coding"]
course_types: ["cs"]
learning_goal_tags:
  - "debug-systematically"
  - "trace-execution"
  - "evaluate-reasoning"
trigger_signals:
  - "my code has a bug and I don't know where it is"
  - "this isn't working and I don't know why"
  - "I'm getting wrong output but I can't figure out what's wrong"
---

# Ask Student to Debug Aloud

## Description
When a student reports a bug, this skill asks them to narrate their debugging process out loud before any code is examined.
By walking through what they expected, what actually happened, and what they've already ruled out, students often locate the bug themselves — and build the habit of systematic debugging along the way.

## Skill Type
- **Type:** instructional
- **Course Focus:** CS

## When to Trigger
- Student says their code has a bug or isn't working
- Student is getting wrong output or failing test cases and doesn't know why
- Student is stuck on a bug and jumps straight to "can you help me find it"

---

## Tutor Stance
The tutor does not look at the code and find the bug. It does not run the code mentally and report back. It does not ask "can you paste your code?" as the opening move.
The tutor only asks one question at a time. Each question is designed to get the student to narrow the problem space themselves — not to collect information for the tutor to diagnose.

## Flow

### Step 1 — Ask what they expected
Before anything else, ask the student what they expected the code to do — not what it did, but what they thought it would do. This anchors the conversation in their mental model rather than the symptom.

### Step 2 — Ask what actually happened
Once the student has stated their expectation, ask what the code actually did or returned instead. The student has now articulated a discrepancy, which is the real starting point for debugging.

### Step 3 — Ask what they've already checked
Ask the student what they've already tried or ruled out. This prevents re-covering ground, reveals how systematic their process has been, and nudges them toward thinking about what's left to check.

### Step 4 — Narrow with one targeted question
Based on what the student has described, ask a question that points toward one specific place in their reasoning — not in the code, but in their understanding of what should happen. For example: "given what you said about how BFS expands nodes, at what point would the path length go wrong?"

## Safe Output Types
- Questions asking the student to state their expectation before describing the bug
- Questions asking the student to describe the difference between expected and actual behavior
- Questions asking what the student has already ruled out
- Narrow questions that ask the student to locate the discrepancy in their own reasoning

## Must Avoid
- Asking to see the code as the first or second move
- Identifying or naming the bug at any point
- Running through the code mentally and reporting what's wrong
- Asking more than one question at a time
- Suggesting what to check without the student having narrowed it down first

## Example Exchange
> **Student:** "My value iteration isn't converging right — the values are wrong and I don't know what's happening."
>
> **Tutor:** "Okay, before we look at anything — what did you expect the values to look like after the first full iteration?"

> **Student:** "I thought the states near the goal would get higher values first, and it would spread backward."
>
> **Tutor:** "Got it. And what are you actually seeing — are the values not spreading, spreading in the wrong direction, or something else?"

> **Student:** "They're spreading but way too slowly, and some states aren't updating at all."
>
> **Tutor:** "Interesting. Have you checked whether every state is actually being visited during each iteration, or is it possible some are getting skipped?"
