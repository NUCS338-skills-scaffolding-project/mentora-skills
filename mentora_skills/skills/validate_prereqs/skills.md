---
skill_id: "validate-prereqs"
name: "Validate Pre-Knowledge"
skill_type: "instructional"
stance: "socratic"
tags: ["phonetics", "gating", "prerequisites", "assessment", "probe"]
course_types: ["humanities"]
learning_goal_tags:
  - "reflect-on-progress"
  - "restate-the-problem"
trigger_signals:
  - "assignment-starting"
  - "prereqs-not-yet-validated"
  - "student-asking-am-i-ready"
  - "student-claims-concept-mastery"
  - "concept-about-to-be-built-on"
python_entry: "logic.py"
---

# Validate Pre-Knowledge

## Description
Before the student begins an assignment, probes whether they can
articulate each prerequisite concept in their own words. Provides a
short open-response probe question per concept, plus the list of key
concepts a strong answer should cover. The orchestrator reads the
student's answer and makes the pass/weak/fail judgment, using the
skill's catalog as its reference.

## When to Trigger

### Fires when:
- Student is beginning an assignment and has not yet been validated on
  its prerequisite concepts
- Orchestrator is checking a specific concept the student claims to
  know before building on it
- Student explicitly asks whether they're ready to start (e.g. "am I
  ready for this?" or similar)

### Does NOT fire when:
- Student is already mid-question (use hinting or contrastive skills
  instead)
- Student has already been validated on the concept in this session
- Concept isn't in the probe catalog — orchestrator should supply a
  custom probe or skip

### Boundary cases:
- **Partial coverage**: answers that hit some but not all key concepts
  → `weak`. Orchestrator offers a brief refresher rather than failing
  the gate outright.
- **Correct answer in unfamiliar vocabulary**: the `key_concepts`
  entries include common synonyms, but natural language is open-ended.
  The orchestrator should judge the *substance* of the answer against
  the concepts — not require exact phrasing. If a correct answer uses
  vocabulary the catalog doesn't anticipate, the judgment is still
  `pass`; the catalog's synonym lists can be extended later.

## Tutor Stance
- Frame probes as "let me make sure we're on the same page," not as a
  quiz. The goal is to surface gaps before they cause struggle, not to
  test for its own sake.
- Give the student one real chance to answer before offering any
  scaffolding. Pre-emptive help defeats the purpose.
- On a `weak` verdict, offer a targeted refresher on the specific
  missing concept — don't re-explain the whole topic.
- On a `fail` verdict, do NOT just keep probing. Hand off to
  `dx-prereq-gaps` or a concept refresher. Repeated
  failures are a signal to change strategies.
- Never read the key concept list back at the student as a checklist.
  The catalog is for the tutor's judgment, not a fill-in-the-blank.
- Judge substance, not vocabulary. A student who explains voicing as
  "whether your voicebox is buzzing" has the concept even though
  "voicebox" and "buzzing" aren't in the catalog's synonym lists.

## Flow

### Step 1 — Identify the concept to probe
Orchestrator decides based on `assignment.md`'s Concepts Required. For
HW1 the likely probes are: voicing, place_of_articulation,
manner_of_articulation, ipa_principle, orthography_vs_pronunciation,
formal_consonant_description (the voicing+POA+manner format taught on
Day 3), and ipa_chart_navigation (how to read the IPA chart structure).

### Step 2 — Pose the probe
Call `run({"action": "probe", "concept": <concept_id>})` to retrieve
the probe question AND the key concepts catalog. Deliver the probe
conversationally — not as a quiz item.

### Step 3 — Judge the student's answer
The orchestrator reads the student's free-text response alongside the
`key_concepts` list and assigns a verdict:
- **pass** — answer substantively covers all key concepts, even with
  informal vocabulary
- **weak** — answer covers some but not all; one or more key concepts
  are missing or only partially addressed
- **fail** — answer doesn't engage the concept meaningfully (off-topic,
  empty, "I don't know")

### Step 4 — Branch on the verdict
- **pass** → acknowledge, move on
- **weak** → offer a targeted refresher on the specific missing
  concept(s), then continue. Do not re-probe.
- **fail** → hand off to `dx-prereq-gaps` or a concept
  refresher. Do not re-probe this concept this session.

## Safe Output Types
- The probe question, delivered conversationally
- Acknowledgment of the student's answer without announcing a verdict
- A short, specific refresher on a missing concept (for `weak`)
- A handoff line to remediation ("let's take a minute on X before we
  keep going") for `fail`

## Must Avoid
- Announcing the verdict or the key concept list to the student
- Reading the synonym list back at the student as a checklist
- Re-probing the same concept in one session
- Treating the probe as graded work
- Failing a student whose answer is substantively right but uses
  vocabulary the catalog didn't anticipate

## Example Exchange
> **Tutor:** "Before we jump into HW1, quick warm-up — in your own
> words, what is voicing, and how does it distinguish consonants?"
>
> **Student:** "Voicing is whether your vocal folds are vibrating.
> Like [z] has them buzzing but [s] doesn't."
>
> *(Orchestrator judges: pass — all three key concepts covered)*
>
> **Tutor:** "Nice — that's exactly it. Let's open HW1."

> **Tutor:** "Quick check before we start — what does 'place of
> articulation' mean?"
>
> **Student:** "Uh, like where the sound happens in your mouth?"
>
> *(Orchestrator judges: weak — got the location idea but missed
> "constriction/closure" and didn't name a specific place)*
>
> **Tutor:** "Close — you've got the general idea. One sharpening:
> place is specifically about where the airflow is *constricted* or
> *blocked*. Try saying [p] and [t] and notice where something is
> touching or closing off the airflow."

## Disambiguation from Other Skills
- `dx-prereq-gaps` runs *after* this skill returns a
  `fail` (or after mid-assignment stuckness) to figure out exactly
  what's missing. **This skill** does the initial check that raises
  the flag.
- `repair-miscon` handles confidently-held wrong models.
  **This skill** distinguishes "has the concept" from "doesn't have
  the concept" — not well-suited to catching a student who is
  confidently wrong in a coherent way.
- `escalate-hint-lvl` scaffolds during a specific
  question. **This skill** operates before questions begin.

## Inputs Expected by logic.py
- `action` (str): `"probe"` only (the orchestrator handles scoring)
- `concept` (str): one of the concept IDs in the catalog (see
  `list_concepts()`)

## Outputs Returned by logic.py
A dict:
- `action` = `"probe"`
- `concept` (str)
- `probe_question` (str): the warm-up question to pose
- `key_concepts` (list of dict): what a strong answer should cover,
  each with:
    - `name` (str): short name of the concept (e.g. "vocal fold
      vibration")
    - `synonyms` (list of str): common phrasings a student might use —
      illustrative, not exhaustive
    - `description` (str): what this concept captures, for the
      orchestrator's reference
- `example_strong_answer` (str): a reference answer the orchestrator
  can use as a substance benchmark (NOT shown to the student)
- `related_concepts` (list of str): concept tags this probe connects to
- `error` (str or None)

## Notes for Reusers
The `PROBES` catalog is HW1-specific (Days 1-3). To add a probe,
extend the catalog with: a `probe` question, a list of `key_concepts`
(each with name/synonyms/description), an `example_strong` answer, and
`related_concepts` tags. The skill deliberately does NOT score answers
— scoring is the orchestrator's job, because natural-language
judgment is what LLMs are good at and rigid substring matching would
wrongly penalize students who use novel but correct vocabulary.
