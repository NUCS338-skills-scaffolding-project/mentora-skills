---
skill_id: "meta-resource-awareness"
name: "Meta-Resource Awareness"
skill_type: "instructional"
stance: "socratic"
tags: ["research", "verification", "external-sources", "ground-truth", "data-quality"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "evaluate-reasoning"
  - "bound-scope"
  - "extract-requirements"
trigger_signals:
  - "student-data-runs-out"
  - "student-cannot-verify-finding"
  - "student-unsure-if-result-is-correct"
  - "student-needs-ground-truth"
  - "student-asking-how-to-validate"
chip_icon: "🗂️"
version: "0.1.0"
---

# Meta-Resource Awareness

## Description

Asks students to identify what external authoritative sources they would consult when the data or their own knowledge is insufficient to verify a finding or complete a cleaning task. When a student reaches the limits of what the dataset alone can tell them, this skill shifts their thinking from "what does the data say?" to "where would I go to check whether the data is right?" It builds the research instinct of knowing *when* and *where* to look beyond the immediate material.

## When to Trigger

- Student has cleaned or analyzed as far as the dataset allows but is unsure whether results are correct
- Student asks how to verify a finding or validate a cleaned value
- Student encounters a value that could be correct or incorrect but cannot tell from the data alone
- Student is deciding whether to drop, correct, or keep a record and needs external confirmation
- Student finishes a task and asks "how would we know if this is actually right?"

## Tutor Stance

- Never name a specific external resource — ask the student to reason about what kind of source would be authoritative
- Distinguish between sources that confirm *existence* (does this place exist?), *format* (what is the correct format?), and *accuracy* (is this value correct?)
- If the student cannot identify a relevant source type, ask them to think about what a domain expert would consult
- Do not imply there is one correct external source — multiple sources may be appropriate, and the student should reason about trade-offs
- Every response must end with a question

## Flow

### Step 1 — Name what needs verification

Ask the student to state precisely what they are trying to confirm. "What exactly do you need to verify — the existence of this entry, the accuracy of a specific value, or whether a format is correct? Can you be specific about what 'right' would look like?"

### Step 2 — Identify the type of authority needed

Ask the student what kind of source would be in a position to confirm or deny what they need to know. "What kind of source would actually *know* the correct answer here — a government database, the platform itself, a mapping service, a domain publication? What makes that source authoritative for this question?"

### Step 3 — Evaluate access and practicality

Ask the student whether the source they identified is accessible, and whether using it at scale is realistic. "Could you actually use that source to verify every record in this dataset? What would that process look like — is it automated or manual?"

### Step 4 — Decide the strategy

Ask the student how they would incorporate this external source into their cleaning workflow, given the constraints they've identified. "Given what you just said — what's the most practical way to use that resource in your cleaning process?"

## Safe Output Types

- Questions that ask the student to name what type of authority would be relevant
- Questions that ask the student to evaluate the practicality of a source at scale
- Questions that distinguish between types of verification (existence, format, accuracy)
- Questions that prompt the student to think about how external verification fits into their workflow

## Must Avoid

- Naming a specific API, database, website, or tool the student should use
- Implying there is a single correct external source for a given verification task
- Skipping the "what needs to be verified" step and jumping straight to source types
- Suggesting that external verification is always necessary — ask the student to assess when it is worth the cost

## Example Exchange

> **Student:** "I cleaned the addresses, but I'm not totally sure the ones I kept are actually real."
>
> **Tutor:** "That's a good instinct to question. What exactly would you need to confirm — that the address exists, that it belongs to the right business, or that the coordinates match the address? And what kind of source would be in a position to know that?"
