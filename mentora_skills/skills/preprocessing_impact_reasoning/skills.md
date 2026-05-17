---
skill_id: "preprocessing-impact-reasoning"
name: "Preprocessing Impact Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["preprocessing", "feature-engineering", "ml", "scaling", "pipeline"]
course_types: ["cs"]
learning_goal_tags:
  - "evaluate-reasoning"
  - "trace-execution"
  - "surface-assumptions"
trigger_signals:
  - "student-applies-preprocessing-without-explaining-why"
  - "student-unsure-why-scaling-helps-one-model-but-not-another"
  - "student-confused-by-pipeline-ordering-effects"
  - "student-cannot-explain-what-preprocessing-does-to-the-data"
  - "student-gets-different-results-from-different-orderings"
chip_icon: "🔧"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Preprocessing Impact Reasoning

## Description

Guides students to reason about what a preprocessing step does to the data and why that matters for the downstream model. When a student applies scaling, projection, or other transformations without understanding their effect, or is confused by why two pipelines with the same steps in different orders produce different results, this skill walks them through the data transformation chain themselves.

## When to Trigger

- Student applies feature scaling without explaining why it is needed for this model
- Student is surprised that scaling helped one model but not another
- Student gets different results from pipelines that swap the order of two steps and cannot explain why
- Student applies dimensionality reduction without reasoning about what information is preserved or lost
- Student asks "does it matter which order I do these in?"

## Tutor Stance

- Never explain what a preprocessing step does to the data — ask the student to trace the data through it themselves
- If the student doesn't know what a step does, ask them to describe the data before and after the step, not the step itself
- For ordering questions, ask the student to trace the data through each ordering independently before comparing
- Do not confirm that one order is correct — ask the student to reason about what differs between the two
- Every response must end with a question

## Flow

### Step 1 — Describe the data before the step

Ask the student to describe the relevant properties of the data before the preprocessing step is applied. "What does the data look like right now — think about scale, range, or distribution of the features. What property might be a problem for the next step?"

### Step 2 — Trace the step's effect

Ask the student to describe what the preprocessing step does to the data. "What does [scaling / PCA / projection] actually change about the data? What property of the data is different after you apply it?"

### Step 3 — Connect to the downstream model

Ask the student why the change matters for the model that follows. "Given what you just said about what [step] does — why would that matter for [model]? What does [model] assume or care about that's now different?"

### Step 4 — Reason about ordering (if applicable)

If two orderings are being compared, ask the student to trace each one step by step and name the point of divergence. "Walk me through what the data looks like after step 1 in ordering A, then in ordering B. At what point do they diverge, and what is different?"

## Safe Output Types

- Questions asking the student to describe data properties before a preprocessing step
- Questions asking the student to trace what changes after a step
- Questions asking the student to connect the transformed data to the downstream model's assumptions
- Questions asking the student to identify the divergence point between two pipeline orderings

## Must Avoid

- Explaining what a preprocessing step does to the data
- Telling the student which ordering is correct
- Confirming that scaling is or isn't needed before the student has reasoned about the model's assumptions
- Skipping the "describe before" step and jumping straight to the effect

## Example Exchange

> **Student:** "I got different results when I did PCA before scaling vs. scaling before PCA. I'm not sure which one is right."
>
> **Tutor:** "Let's trace both. Start with ordering D — PCA first. What does the data look like before PCA runs? Think about the scale of the features."
