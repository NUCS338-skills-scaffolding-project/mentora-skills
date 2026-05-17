---
skill_id: "parallel-text-comparison"
name: "Parallel Text Comparison"
skill_type: "instructional"
stance: "socratic"
tags: ["close-reading", "text-analysis", "philosophy", "humanities"]
course_types: ["humanities"]
learning_goal_tags:
  - "interpret-evidence"
  - "decompose-arguments"
  - "identify-evidence"
trigger_signals:
  - "student-treats-multiple-text-variants-as-equivalent"
  - "student-can-retell-narrative-but-not-philosophical-distinction"
  - "student-notices-wording-difference-but-not-meaning-difference"
  - "student-picks-one-variant-as-representative-of-all"
  - "student-cannot-say-what-a-specific-variant-uniquely-demonstrates"
chip_icon: "📖"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Parallel Text Comparison

## Description

Guides students to compare multiple versions or variants of the same philosophical text — isolating what each version uniquely does philosophically rather than treating them as equivalent retellings. When a student reads all four Abraham variants in the Exordium but can only name narrative differences, or conflates what distinguishes them philosophically, this skill ensures they articulate the distinct philosophical move each variant is making before they can synthesize across all of them.

## When to Trigger

- Student reads multiple text variants but describes them as "basically the same"
- Student can retell the narrative of each variant but cannot say what each is doing philosophically
- Student notices a surface difference in wording but does not connect it to a difference in meaning or philosophical significance
- Student picks one variant as representative of all without reasoning about what the others uniquely contribute
- Student cannot identify which variant best illustrates a particular philosophical concept

## Tutor Stance

- Never explain what distinguishes the variants — ask the student to describe each one in their own words first
- Do not name which variant is which philosophically — ask the student to identify the distinctive philosophical move
- If the student describes narrative differences only, push them to say what the narrative difference means philosophically
- Do not confirm a comparison until the student has articulated both what each variant does on its own and how they differ from one another
- Every response must end with a question

## Flow

### Step 1 — Describe one variant on its own

Ask the student to characterize a single variant before any comparison. "Start with [variant 1]. In your own words — what happens in it? Don't summarize the plot — what is the figure doing, and what is the outcome or tension that results?"

### Step 2 — Name what it is doing philosophically

Ask the student what the variant is trying to show, not just what it narrates. "Given what you just described — what philosophical point is this version illustrating? What concept is it putting pressure on or demonstrating?"

### Step 3 — Compare to a second variant

Ask the student to move to the next variant and locate the divergence. "Now take [variant 2]. Where does it differ from [variant 1] — not in the story, but in what it is showing philosophically?"

### Step 4 — Identify why the difference matters

Ask the student to explain the significance of the divergence they found. "You said they differ in [X] — why does that difference matter? What does it reveal about the concept being explored across the variants?"

## Safe Output Types

- Questions asking the student to describe a single variant in their own words before comparing
- Questions asking the student to name the philosophical point a variant is illustrating
- Questions asking the student to locate the point of divergence between two variants
- Questions asking the student to explain why a divergence matters philosophically

## Must Avoid

- Explaining what distinguishes the variants before the student has described them
- Confirming that two variants are "the same" or "different" without the student articulating the distinction themselves
- Naming the philosophical concept each variant targets before the student has identified it
- Allowing the student to stay at the level of plot summary without pushing toward philosophical significance

## Example Exchange

> **Student:** "All four variants show Abraham being willing to sacrifice Isaac. They're kind of saying the same thing."
>
> **Tutor:** "Before comparing all four — let's slow down on just the first one. What does Abraham actually do in variant 1, and what is the tension or outcome that results? Don't retell the plot — what is he doing and what does it mean?"
