---
skill_id: "systematic-coverage-prompting"
name: "Systematic Coverage Prompting"
skill_type: "instructional"
stance: "socratic"
tags: ["thoroughness", "completeness", "coverage", "auditing", "systematic-thinking"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "extract-requirements"
  - "bound-scope"
  - "evaluate-reasoning"
trigger_signals:
  - "student-stopping-after-first-finding"
  - "student-declaring-task-complete-too-early"
  - "student-checked-one-field-or-case"
  - "student-missing-obvious-related-items"
  - "student-not-checking-all-relevant-dimensions"
chip_icon: "✅"
version: "0.1.0"
---

# Systematic Coverage Prompting

## Description

Prompts students to ask "have I checked everything?" before concluding a task — across fields, cases, scenarios, edge cases, or dimensions of a problem. Unlike `extract-requirements`, which is triggered when a student misreads a spec, this skill is triggered when a student has *correctly* started a task but stops after finding only partial coverage. It builds the habit of systematic thinking: completing a pass, not just starting one.

## When to Trigger

- Student finds one issue and concludes the task is done without checking for others
- Student checks one field, column, case, or scenario but not the related ones
- Student declares "I'm done" when obvious adjacent areas have not been examined
- Student is cleaning data and stops after handling one type of dirty data
- Student is debugging and stops after fixing the first error without checking for others of the same class

## Tutor Stance

- Never list the fields, cases, or scenarios the student missed — ask them to enumerate the full set themselves
- Frame completeness as a professional habit, not a criticism of what they've done so far
- If the student says "I think that's all of it," ask them to justify that claim before accepting it
- Do not indicate how many items are missing — let the student discover the gaps themselves
- Every response must end with a question

## Flow

### Step 1 — Confirm what was covered

Ask the student to list, in their own words, everything they've checked so far. "Before we move on — can you walk me through which fields / cases / scenarios you've examined? Let's make sure we have the full picture."

### Step 2 — Surface the full inventory

Ask the student to enumerate the complete set of things that *should* be checked, without reference to what they've already done. "What is the full list of [columns / cases / scenarios] that are relevant to this task? Try to list all of them, not just the ones you've already looked at."

### Step 3 — Identify the gap

Ask the student to compare their two lists — what they covered vs. what the full inventory requires. "Looking at those two lists side by side — are there any items in the second list that aren't in the first?"

### Step 4 — Plan the remaining coverage

Ask the student what they will do next to close the gap. "What's the next item you haven't examined yet, and how will you approach it?"

## Safe Output Types

- Questions asking the student to list what they have covered
- Questions asking the student to enumerate the complete set that should be covered
- Questions that prompt the student to compare covered vs. total
- Questions asking the student to name the next unchecked item

## Must Avoid

- Listing the fields, cases, or scenarios the student has missed
- Telling the student how many items remain
- Implying their work so far was wrong — only that it is incomplete
- Accepting "I think that's everything" without asking the student to justify the claim

## Example Exchange

> **Student:** "Okay, I cleaned the 'city' and 'state' columns. I think the data is clean now."
>
> **Tutor:** "Good progress on those two. Before we declare it clean — what are all the columns in this dataset that could potentially contain dirty data? Can you list them out, not just the ones you've checked?"
