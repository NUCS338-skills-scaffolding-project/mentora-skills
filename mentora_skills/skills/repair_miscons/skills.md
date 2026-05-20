---
skill_id: "repair-miscons"
name: "Repair Misconceptions"
stance: "reframe"
skill_type: "instructional"
tags: ["phonetics", "misconceptions", "socratic", "repair"]
course_types: ["humanities"]
learning_goal_tags:
  - "verify-claims"
  - "surface-assumptions"
  - "interpret-evidence"
trigger_signals:
  - "student-says-th-is-one-sound"
  - "student-says-y-always-vowel"
  - "student-says-just-sound-it-out"
  - "student-confuses-spelling-with-pronunciation"
  - "student-says-letters-equal-sounds"
  - "student-says-ph-is-puh-huh"
  - "claim-matches-known-misconception"
  - "student-confidently-wrong"
chip_icon: "⛏️"
version: "0.1.0"
python_entry: "logic.py"
---

# Repair Misconceptions

## Description
Recognizes common phonetics misconceptions a student is exhibiting and
returns the structured information needed to repair them through Socratic
questioning rather than direct correction. Pulls from the course-wide
misconceptions catalog maintained in `context/misconceptions.md`.

## When to Trigger

### Fires when:
- Student makes a claim that matches a known misconception (e.g.
  "th is one sound," "y is always a vowel," "you can just sound out
  the spelling")
- Student's wrong answer on a classification or transcription question
  reveals an underlying wrong mental model (not just a factual slip)
- Student asks a question premised on a misconception (e.g. "why does
  nasal mean it's only in the nose?")

### Does NOT fire when:
- Student has the right mental model but a factual gap — use
  `dx-prereq-gaps` instead
- Student is confusing two specific sounds but has a coherent model
  otherwise — use `contrastive-hint` instead
- Student has a novel wrong belief that isn't in the catalog. Note it
  for future catalog additions rather than forcing it into an existing
  category.

## Tutor Stance
- Never tell the student "you're wrong." The misconception isn't
  repaired by contradiction — it's repaired by the student noticing
  the evidence themselves.
- Use the `correction_target` question verbatim or lightly adapted.
  These are designed to surface the contradiction physically (hand on
  throat, say the word slowly, etc.).
- Give the student space to articulate what they notice. The repair
  comes from *their* observation, not from the tutor's explanation.
- Once the student notices the evidence, briefly name the correct
  concept. Don't lecture — a sentence or two is enough.

## Flow

### Step 1 — Confirm the misconception is at play
Re-voice what you're hearing: "It sounds like you're thinking *th* is
one sound — is that right?" This gives the student a chance to clarify
if you've misidentified.

### Step 2 — Ask the correction_target question
Use the Socratic prompt from the catalog. These are designed to make
the contradiction visible through the student's own body or observation.

### Step 3 — Listen for the noticing moment
Wait for the student to describe what they observed ("oh, I feel
vibration for *this* but not *thing*"). That's the repair.

### Step 4 — Briefly name the correct model
One or two sentences. "Right — *th* is actually two different sounds,
[θ] voiceless and [ð] voiced. Same place, same manner, different
voicing." Then return to whatever they were working on.

## Safe Output Types
- Socratic questions drawn from or adapted from the `correction_target`
  field
- Brief acknowledgment phrases when the student notices the evidence
- One- or two-sentence correct-model summaries after the noticing moment
- Requests for clarification if it's ambiguous which misconception is
  at play

## Must Avoid
- Flat contradictions ("no, that's wrong"). Even when true, they shut
  down the learning moment.
- Lectures. If the correct-model summary is longer than two sentences,
  it's a lecture.
- Stacking multiple misconceptions in one correction. Repair them one
  at a time.
- Calling out the student's confusion as a "common mistake" in a way
  that embarrasses them. The framing is "here's something interesting
  to notice," not "here's what you got wrong."

## Example Exchange
> **Student:** "I can sound out *phone* from the letters — ph makes a
> 'puh-huh' sound, right?"
>
> **Tutor:** "Good question — let's test it. Put your hand flat in
> front of your mouth and say *phone*. Then say *pot*. What do you feel
> on your hand each time?"
>
> **Student:** "A little puff of air on *pot*. Not on *phone*."
>
> **Tutor:** "Right. *Pot* starts with [p] — a stop, with a puff of
> air on release. *Phone* starts with [f] — a fricative, no puff
> because air is flowing continuously. The spelling *ph* is actually
> just [f], even though the letters are p and h. English spelling and
> pronunciation don't line up as neatly as it looks."

## Disambiguation from Other Skills
- `contrastive-hint` fires when the student distinguishes two
  specific sounds but is confused about what differs between them.
  **This skill** fires when the student holds a general wrong model
  that affects many sounds.
- `dx-prereq-gaps` fires when the student is missing a
  concept they never learned. **This skill** fires when the student
  *has* learned the concept but internalized a wrong version.
- `escalate-hint-lvl` fires during a stuck moment within
  a correct model. **This skill** repairs the model itself.

## Inputs Expected by logic.py
- `misconception_id` (str): one of the known misconception IDs (see
  `list_misconceptions()`)
- OR `topic` (str): a keyword like "spelling" or "voicing" to find
  matching misconceptions

## Outputs Returned by logic.py
A dict (if called with `misconception_id`) with:
- `misconception_id` (str)
- `title` (str): short human-readable name
- `claim` (str): the wrong belief, stated in a student's voice
- `why_wrong` (str): the factual correction
- `correction_target` (str): the Socratic prompt to ask the student
- `related_concepts` (list of str): concept tags this connects to
- `error` (str or None)

Or a list of matching dicts if called with `topic`. Empty list if no
match.

## Notes for Reusers
The `MISCONCEPTIONS` dict in `logic.py` is keyed by stable string IDs
derived from `context/misconceptions.md`. When adding a new
misconception, update both files (markdown for humans, Python for
programmatic access). Future work could auto-parse the markdown; for
this POC the duplication is cheap and keeps `logic.py` dependency-free.