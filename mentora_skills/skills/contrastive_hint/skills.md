---
skill_id: "contrastive-hint"
name: "Give Contrastive Hint"
skill_type: "instructional"
stance: "hint"
tags: ["phonetics", "consonants", "place-manner-voicing", "socratic"]
course_types: ["humanities"]
learning_goal_tags:
  - "interpret-evidence"
  - "verify-claims"
trigger_signals:
  - "student-confusing-specific-sound-pair"
  - "student-cant-tell-pair-apart"
  - "student-asks-difference-between-sounds"
  - "wrong-answer-confuses-neighboring-sound"
  - "student-names-two-ipa-symbols"
python_entry: "logic.py"
---

# Give Contrastive Hint

## Description
Helps a student distinguish two consonants they are confusing by asking a
Socratic question focused on the single feature that differs. Uses the
IPA reference module to identify which of {place, manner, voicing} is the
point of contrast, then prompts the student to discover that difference
themselves.

## Skill Type
- **Type:** instructional
- **Course Focus:** Both

## When to Trigger
- Student expresses confusion between two specific consonants
  (e.g. " can't tell [θ] and [f] apart", "why is it [s] and not [z]?")
- Student gives a wrong answer on a place/manner/voicing classification
  question and their answer suggests they've confused the target sound
  with a neighboring one
- Student asks "what's the difference between X and Y?" about two IPA
  symbols

---
# INSTRUCTIONAL SKILLS:

## Tutor Stance
- Never name the differing feature first. The student names it through
  questioning.
- Anchor questions in the student's own body when possible: "put your
  fingers on your throat," "hold a hand in front of your mouth," "say it
  slowly and notice where your tongue is."
- One feature at a time. If two sounds differ on multiple features
  (e.g. [p] vs [z]), pick the most salient single feature and probe that
  one; address the others only if the student brings them up.
- Acknowledge warmly when the student gets it — this is a moment of real
  learning and should feel like one.

## Flow
### Step 1 — Identify the pair
If the student has named two specific sounds, confirm them. If they've
described sounds without naming IPA symbols ("the sound at the start of
*think*"), translate to IPA and confirm: "So you're asking about [θ] and
[ð], yes?"

### Step 2 — Look up the differing features
Call `logic.py` with the two symbols. It returns the list of features
where they differ. In the most common case, there is exactly one.

### Step 3 — Ask the Socratic question
Frame a question that points at the differing feature without naming it:

- If they differ in **voicing**: "Put your fingers on your throat and say
  [X], then [Y]. What do you feel?"
- If they differ in **place**: "Say [X] and [Y] slowly. Where does your
  tongue (or lips) end up each time?"
- If they differ in **manner**: "Try to hold out [X] for as long as you
  can. Now try to hold out [Y]. What's different?"

### Step 4 — Confirm and anchor
When the student articulates the difference, confirm it and name the
feature officially. "Right — that vibration is voicing. [X] is voiceless,
[Y] is voiced."

### Step 5 — Handoff
Return the conversation to whatever the student was doing. Don't lecture
further unless they ask.

## Safe Output Types
- Socratic questions pointing at one articulatory feature
- Brief anchoring confirmations once the student names the feature
- IPA symbol translations from description ("the sound at the start of
  *ship*" → [ʃ])

## Must Avoid
- Naming the differing feature before the student does
- Probing multiple features at once
- Giving a full classification table of either sound
- Moving on to another contrast before the current one is resolved
- Breaking into unprompted lecture about phonetic theory

## Example Exchange
> **Student:** I keep getting [θ] and [f] mixed up on the homework.
>
> **Tutor:** Okay — [θ] is the sound in *thing*, [f] is the sound in *fat*.
> Let's compare. Say *thing* very slowly and pay attention to where your
> tongue is at the very start. Now say *fat* the same way. What's
> different?
>
> **Student:** For *thing* my tongue is kind of between my teeth. For
> *fat* my bottom lip is touching my top teeth.
>
> **Tutor:** Exactly. That's the difference in place of articulation.
> [θ] is dental — tongue between or against the upper teeth. [f] is
> labiodental — lower lip against upper teeth. Voicing and manner are
> actually the same for both, so place is the one thing distinguishing
> them.

## Inputs Expected by logic.py
- `sym1` (str): an IPA symbol, e.g. `"θ"`
- `sym2` (str): another IPA symbol, e.g. `"f"`

## Outputs Returned by logic.py
A dict:
- `differing_features` (list of str): the feature names that differ,
  subset of `["place", "manner", "voicing"]`
- `sym1_features` (dict): full feature bundle for sym1
- `sym2_features` (dict): full feature bundle for sym2
- `primary_feature` (str or None): the single most salient differing
  feature, for skills that want a single-feature handoff

## Notes for Reusers
This skill is consonant-focused. Vowel contrasts would need a parallel
module (`ipa_vowels.py`) and potentially a separate skill. The
`primary_feature` field prioritizes voicing > manner > place when
multiple features differ, on the pedagogical grounds that voicing is the
easiest for students to feel in their own body.