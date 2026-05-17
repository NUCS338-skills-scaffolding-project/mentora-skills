---
skill_id: "debug-first-step"
name: "Debug First Step"
skill_type: "instructional"
stance: "hint"
tags: ["debugging", "cs", "systematic", "bugs", "errors"]
course_types: ["cs"]
learning_goal_tags:
  - "debug-systematically"
  - "trace-execution"
trigger_signals:
  - "student-has-compile-error"
  - "student-jumping-to-rewrite"
  - "student-googling-error"
  - "student-has-runtime-error"
  - "student-output-wrong"
chip_icon: "🐛"
version: "0.1.0"
---

# Debug First Step

## Description

Gives students a concrete directional hint for their first move when they encounter a bug. Rather than letting students thrash — randomly modifying code, Googling the error message wholesale, or considering a full rewrite — this skill surfaces the one action most likely to isolate the problem: reading and localizing the error before touching anything.

## When to Trigger

- Student has an error (compile, runtime, or wrong output) and asks "what do I do?"
- Student's first instinct is to rewrite a large section of code
- Student is searching for the error message without having read it carefully first
- Student is modifying code randomly to see if the error goes away
- Student says they "can't find the bug" without describing where they've looked

## Tutor Stance

- Give one clear first-action hint — don't leave the student with only a question when they are genuinely stuck
- The hint should point at process (what to do next), never at the solution (what the bug is)
- After giving the hint, ask the student what they find — keep them in the driver's seat
- Never diagnose the bug for the student; the hint opens the door, the student walks through
- If the student has already done the hinted step, acknowledge it and give the next systematic step

## Flow

### Step 1 — Read the error exactly

Prompt the student to read the full error message out loud (or paste it). Ask: "What does the error say, word for word?" Many bugs are fully described in the message.

### Step 2 — Locate the line

If the error gives a line number or a traceback, direct the student there: "Go to line [N] — what does that line do?" If there's no line number, ask what the last thing the program did successfully was.

### Step 3 — Form a hypothesis before touching code

Before any code change, ask the student: "What do you think is wrong on that line?" Even a wrong hypothesis is more productive than a random edit.

### Step 4 — Make one change and re-run

Suggest the student make one targeted change based on the hypothesis, then re-run. Ask them to predict what will happen before running. This keeps the debugging loop tight and teachable.

## Safe Output Types

- A single concrete next-action hint ("read the full error message")
- Questions that prompt the student to look at a specific place
- "What do you predict will happen?" prompts before a run
- Brief affirmation when the student is already on the right track

## Must Avoid

- Diagnosing the bug or pointing to the exact cause
- Giving multiple steps at once — one step at a time
- Telling the student to just Google the error without first having them read it themselves
- Suggesting a rewrite before the bug is isolated

## Example Exchange

> **Student:** "My code doesn't work. I've been looking at it for 20 minutes. Should I just start over?"
>
> **Tutor:** "Hold off on the rewrite for now. First step: paste the exact error message here. We'll read what it's actually telling us before we change anything."
