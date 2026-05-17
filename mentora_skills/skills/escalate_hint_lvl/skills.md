---
skill_id: "escalate-hint-lvl"          
name: "Escalate Hint Level Gradually"              
skill_type: "instructional"
stance: "hint"                   
tags: ["phonetics", "hints", "scaffolding", "socratic", "stuck"]
course_types: ["humanities"]         
learning_goal_tags:                  
  - "manage-effort"
  - "request-targeted-help"
trigger_signals:
  - "student-says-im-still-stuck"
  - "attempted-then-asked-for-help"
  - "silence-after-attempt"
  - "student-gives-wrong-answer-after-hint"
  - "student-requests-another-hint"
  - "productive-struggle-zone"
chip_icon: "📈"                      # OPTIONAL — single emoji for the UI
version: "0.1.0"                     # OPTIONAL — semver, defaults to "0.1.0"
python_entry: "logic.py"
---

# Escalate Hint Level Gradually

## Description
When a student is stuck on a question, produces the next-most-specific
hint without revealing the answer. Supports pre-built hint ladders for
common HW1 question types (feature classification, midsagittal diagram
identification, IPA transcription, multi-select feature matching,
feature-description-to-IPA-symbol matching for Q11, symbol-to-formal-
description for definition questions, and IPA-chart navigation) and
accepts custom ladders from the orchestrator for other question shapes.
Stateless — the orchestrator tracks which level has already been given.

## When to Trigger

### Fires when:
- Student has attempted the question and is stuck ("I don't know,"
  "I'm lost," silence after an attempt, or a wrong answer followed by
  a request for help)
- Student has already received a hint and needs a more specific one
- Orchestrator determines the student is in a productive-struggle zone,
  not a misconception zone

### Does NOT fire when:
- Student hasn't attempted the question yet — ask them to try first
- Student's wrong answer reveals a misconception rather than being
  stuck (use `repair-miscon` instead)
- Student lacks prerequisite knowledge entirely (use
  `dx-prereq-gaps` instead)
- Student is at max hint level and still stuck — that's a signal to
  step back, not to hint harder

### Boundary cases:
- **First hint in a session**: call with `current_level: 0`, get level
  1 hint
- **Student has been hinting across multiple turns**: orchestrator
  maintains `current_level` in session state and increments each call
- **Unfamiliar question shape**: pass a `custom_ladder` (a list of
  hint strings) and the skill will walk through it the same way

## Tutor Stance
- Start abstract, end concrete. Early hints invite the student to
  access what they already know; later hints anchor them to a specific
  observation.
- Never jump a level. If the current level didn't click, go to the
  next one, not three levels down. The gradient matters.
- When max level is reached and the student is still stuck, do NOT
  reveal the answer. That's a signal to switch skills — probably
  `dx-prereq-gaps` or a concept refresher.
- Between hints, give the student time to try again. Hints are
  scaffolding, not narration.

## Flow

### Step 1 — Get the next hint
Call `run()` with `hint_type` (or `custom_ladder`) and `current_level`.
The skill returns the hint text and the new level.

### Step 2 — Deliver the hint and wait
Give the hint as a single message. Then pause. Let the student try
again before hinting further.

### Step 3 — If the student responds correctly, stop hinting
Acknowledge the work and move on. Don't keep hinting a question they've
now answered.

### Step 4 — If they're still stuck, escalate
Re-call the skill with the incremented level. Repeat until resolution
or until `is_max_level` is true.

### Step 5 — At max level, switch skills
If the student is still stuck after the final hint, the orchestrator
should step back: either diagnose a prerequisite gap, repair a
misconception, or acknowledge struggle and move on. Do not give the
answer.

## Safe Output Types
- Hint text from the returned ladder (verbatim or lightly adapted for
  the student's tone)
- Short acknowledgments between hints ("take your time")
- A transition line when max level is reached ("we've worked through
  this from several angles — let me ask a different question")

## Must Avoid
- Giving the answer, even when the student asks directly
- Jumping multiple levels at once
- Hinting on a question the student hasn't yet attempted
- Adding sub-hints inside a single hint (diluting the gradient)
- Continuing to hint after max level — the ladder ends deliberately

## Example Exchange
> **Student:** "For question 4, I have no idea what the manner of [θ]
> is."
>
> **Tutor:** *(level 1 hint)* "This is a good one to work through
> carefully. What do you notice when you say [θ] a few times in a row?"
>
> **Student:** "I don't know, it's just... a th sound."
>
> **Tutor:** *(level 2 hint)* "Every consonant has three features:
> place, manner, and voicing. The question is asking about manner —
> which is about what the airflow is doing. Is it stopped completely,
> is there friction, is it free?"
>
> **Student:** "Oh... I think it's friction? My tongue is between my
> teeth and air is still coming through."
>
> **Tutor:** "Exactly — that's a fricative. Air flowing with turbulence
> through a narrow gap."

## Disambiguation from Other Skills
- `contrastive-hint` produces *a* hint — specifically, a contrast
  between two sounds. **This skill** produces a *series* of hints that
  escalate in specificity for one question.
- `repair-miscon` fires when the student's stuckness is caused
  by a wrong mental model. **This skill** fires when the mental model
  is fine but access to the answer is blocked.
- `dx-prereq-gaps` fires when hints aren't landing because
  the student lacks a foundational concept. **This skill** assumes
  prerequisites are in place.

## Inputs Expected by logic.py
- `current_level` (int): 0 means no hint given yet; the skill returns
  level 1. N means N hints given; skill returns level N+1.
- `hint_type` (str, optional): one of the known catalog keys (see
  `list_hint_types()`)
- `custom_ladder` (list of str, optional): a custom list of hints,
  lowest to highest specificity. Overrides `hint_type`.

## Outputs Returned by logic.py
A dict:
- `next_level` (int): the level of the hint being returned
- `hint_text` (str or None): the hint, or None if at max
- `is_max_level` (bool): True if `next_level` is the last hint in the
  ladder; subsequent calls will return None
- `total_levels` (int): how many hints are in this ladder total
- `error` (str or None)

## Notes for Reusers
The `HINT_LADDERS` catalog is HW1-specific. To extend to other
assignments, add new keys to the catalog or pass `custom_ladder` per
call. The ladder design philosophy (abstract → concrete, never reach
the answer) is the reusable pattern — the specific hint wording is not.
