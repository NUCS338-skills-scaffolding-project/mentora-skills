---
skill_id: "dx-prereq-gaps"           
name: "Diagnose Prerequisite Gaps"              
skill_type: "instructional"
stance: "socratic"                    
tags: ["phonetics", "diagnostic", "prerequisites", "gaps", "remediation"]
course_types: ["humanities"]         
learning_goal_tags:                  
  - "detect-ambiguity"
  - "surface-assumptions"
  - "request-targeted-help"
  - "reflect-on-progress"
trigger_signals:
  - "validate-prereqs-fail"
  - "cannot-localize-stuck-point"
  - "repeated-restart-without-progress"
  - "vague-references-to-named-concepts"
  - "hint-failed-to-unblock"
  - "remediation-plan-requested"
chip_icon: "🔍"                      
version: "0.1.0"                     
python_entry: "logic.py"
---

# Diagnose Prerequisite Gaps

## Description
When a student is stuck or has failed a pre-knowledge probe, identifies
which specific sub-concept of a prerequisite is missing from their
mental model. For each HW1 prerequisite concept, provides a small
sequence of targeted diagnostic probes that isolate sub-concepts (e.g.
for "place of articulation": does the student understand constriction?
Can they locate it in the vocal tract? Can they name a specific place?).
The orchestrator judges each response and returns a structured gap
report indicating what the student does and doesn't yet know.

## When to Trigger

### Fires when:
- `validate-prereqs` returned `fail` for a concept
- Student is stuck mid-assignment in a way that suggests a foundational
  gap (not a misconception, not just a hint-worthy stuck moment)
- Tutor needs to plan a remediation session and wants to know exactly
  which sub-concepts to cover

### Does NOT fire when:
- Student has a wrong mental model rather than a missing one — use
  `repair-miscon` instead
- Student is stuck on a specific question within a concept they
  otherwise grasp — use `escalate-hint-lvl` instead
- The gap is already known (e.g. the student said "I've never heard
  of the IPA" — no diagnosis needed, just teach it)

### Boundary cases:
- **Multiple concepts may be shaky**: diagnose one at a time rather
  than running diagnostics on all five prerequisites simultaneously.
  Stacked diagnostics feel like interrogation.
- **Student gets the first sub-probe right but later ones wrong**:
  that's the gap being located. Stop once the gap is identified — no
  need to continue down the diagnostic ladder.
- **Student seems to know everything but still failed the initial
  probe**: the initial probe may have caught them on phrasing rather
  than substance. Note this and skip remediation.

## Tutor Stance
- Diagnostics are investigative, not punitive. Frame as "let me figure
  out where the sticking point is," not "let me find what you don't
  know."
- Ask ONE diagnostic probe at a time. Wait for the answer. Judge.
  Decide whether to continue.
- Stop as soon as the gap is located. If sub-probe 2 fails, you don't
  need to ask sub-probes 3 or 4 — you know where the gap is.
- Use the student's own words back to them when possible. "You said
  X — let's build on that" is more motivating than "okay, but you
  missed Y."
- When a gap is identified, hand off cleanly to remediation or to a
  concept refresher. The diagnostic itself is not teaching.

## Flow

### Step 1 — Identify the concept to diagnose
Usually driven by a prior `validate-prereqs` fail. Call
`run({"action": "get_probes", "concept": <concept_id>})` to retrieve
the ordered list of diagnostic sub-probes.

### Step 2 — Pose sub-probes one at a time
Ask the first sub-probe. Wait for the answer. The orchestrator judges
whether the student demonstrated understanding of that specific
sub-concept.

### Step 3 — Decide whether to continue
- If the student demonstrates the sub-concept → ask the next sub-probe
- If the student does NOT demonstrate it → stop. You've located the gap.

### Step 4 — Report the gap
Call `run({"action": "summarize", "concept": <concept_id>,
"sub_concepts_passed": [...], "sub_concept_failed": <id>})` to get a
structured gap report the orchestrator can use to plan remediation.

### Step 5 — Hand off
The gap report identifies what to teach. The orchestrator routes to a
concept refresher, a targeted mini-lesson, or (if the gap is very
narrow) a single corrective exchange. Do NOT use this skill to teach
— it only diagnoses.

## Safe Output Types
- One diagnostic sub-probe at a time, delivered conversationally
- A brief acknowledgment of the student's answer before the next probe
- A handoff line once the gap is identified ("got it — let's spend a
  minute on X")
- The structured gap report, for the orchestrator's planning (not
  shown to the student)

## Must Avoid
- Asking multiple sub-probes in a single message
- Continuing to probe after the gap has been located
- Diagnosing multiple concepts in parallel in one session
- Teaching within the diagnostic — this skill locates gaps; other
  skills or refreshers fill them
- Reading the gap report to the student
- Treating the diagnostic as a test or making the student feel
  examined

## Example Exchange
> *(Prior context: student failed validate-prereqs on
> "place_of_articulation")*
>
> **Tutor:** "Okay, let me figure out where the sticking point is —
> this'll just be a couple of small questions. First: when we talk
> about a consonant being 'constricted,' what do you think that means?"
>
> **Student:** "Like, the air is being squeezed or blocked off in some
> way?"
>
> *(Orchestrator judges: sub-probe 1 passed — student understands
> constriction)*
>
> **Tutor:** "Nice — that's exactly it. Next: if I make the sound [p],
> where in my mouth is the constriction happening?"
>
> **Student:** "Um... somewhere in the front? I don't really know."
>
> *(Orchestrator judges: sub-probe 2 failed — student can't locate
> constriction anatomically. Gap identified.)*
>
> **Tutor:** "Okay, I think I see the gap — you've got the concept of
> constriction but not yet the anatomy of where it happens. Let's
> spend two minutes on the parts of the mouth that matter for
> consonants, and then come back to the question."

## Disambiguation from Other Skills
- `validate-prereqs` asks one probe per concept and returns a
  coarse pass/weak/fail. **This skill** goes deeper — given a known
  weakness, it isolates *which specific sub-concept* is the gap.
- `repair-miscon` fires when the student has a confident wrong
  model. **This skill** fires when the student is missing (or hazy
  on) a piece.
- `escalate-hint-lvl` scaffolds a student through a
  specific stuck question. **This skill** steps out of the question to
  diagnose what's missing upstream.

## Inputs Expected by logic.py

For `action: "get_probes"`:
- `concept` (str): one of the concept IDs in the catalog (see
  `list_concepts()`)

For `action: "summarize"`:
- `concept` (str)
- `sub_concepts_passed` (list of str): sub-probe IDs the student
  demonstrated understanding of
- `sub_concept_failed` (str or None): the sub-probe ID where
  understanding broke down, or None if all passed

## Outputs Returned by logic.py

For `action: "get_probes"`:
- `action` = `"get_probes"`
- `concept` (str)
- `sub_probes` (list of dict): ordered sequence of diagnostic probes,
  each with:
    - `id` (str): stable identifier
    - `name` (str): short description of the sub-concept
    - `probe_question` (str): the question to ask
    - `what_to_listen_for` (str): orchestrator guidance on what a
      passing answer looks like
- `error` (str or None)

For `action: "summarize"`:
- `action` = `"summarize"`
- `concept` (str)
- `gap` (dict or None): `None` if all sub-probes passed; otherwise
  `{id, name, remediation_hint}`
- `strengths` (list of dict): sub-probes the student passed, with
  id/name
- `error` (str or None)

## Notes for Reusers
The `DIAGNOSTICS` catalog is HW1-specific and parallels the concepts
in `validate-prereqs`. Each diagnostic is a 2–4 step ladder from
most foundational to most specific. Adding a new concept requires:
the concept ID, an ordered list of sub-probes (foundational → specific),
and a remediation hint per sub-probe. Judgment is the orchestrator's
job — this skill holds structure, not scoring. Same design decision as
`validate-prereqs`.