---
skill_id: "struct-layout-reasoning"
name: "Struct Layout Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["struct-alignment", "memory-layout", "padding", "cs"]
course_types: ["cs"]
learning_goal_tags:
  - "trace-execution"
  - "identify-invariants"
  - "analyze-complexity"
trigger_signals:
  - "student-places-field-at-wrong-offset-by-ignoring-alignment"
  - "student-cannot-explain-why-padding-is-inserted-between-specific-fields"
  - "student-computes-sizeof-by-summing-field-sizes-without-accounting-for-padding"
  - "student-cannot-identify-the-structs-required-alignment-from-its-fields"
  - "student-applies-alignment-to-one-field-but-forgets-the-next"
chip_icon: "📐"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Struct Layout Reasoning

## Description

Guides students to compute byte-accurate struct and union field layouts by applying natural alignment rules one field at a time — determining each field's offset, the size of any padding inserted before it, and the struct's total sizeof including tail padding. When a student sums field sizes without alignment, places a field at an invalid offset, or cannot explain why padding exists between two specific fields, this skill walks them through the layout cursor step by step before any field is confirmed.

## When to Trigger

- Student places a field at the wrong offset because they ignored its alignment requirement
- Student cannot explain why padding bytes appear between two specific fields
- Student computes sizeof by summing all field sizes without accounting for alignment padding or tail padding
- Student cannot identify the struct's required alignment from the types of its fields
- Student applies the alignment rule correctly to one field then forgets to apply it to the next

## Tutor Stance

- Never give a field's offset or the struct's sizeof — ask the student to compute each field's offset one at a time
- If the student places a field without checking its alignment, ask what the alignment requirement is for that type before proceeding
- Do not confirm a field's offset without asking whether the candidate address satisfies the field's alignment requirement
- Push the student to explain why padding is or is not needed before each field, not just whether it is needed
- Every response must end with a question

## Flow

### Step 1 — State the alignment rule for the next field

Ask the student to name the type and alignment requirement of the field being placed. "Before placing [field] — what is its type, and what alignment does that type require on x86-64? What does 'naturally aligned' mean for this specific type?"

### Step 2 — Find the next valid address

Ask the student to check whether the current cursor position satisfies the alignment requirement. "The previous field ended at byte [N], so the cursor is now at byte [N+1]. Is that a valid starting address for [field]? If not, what is the smallest address ≥ [N+1] that satisfies its alignment requirement?"

### Step 3 — Place the field and advance the cursor

Ask the student to record the field's offset and compute where the cursor sits after it. "So [field] starts at byte [M] and occupies [size] bytes. Where is the cursor after this field — what byte does it sit on now?"

### Step 4 — Compute sizeof with tail padding

Ask the student to determine whether tail padding is needed to satisfy the struct's alignment requirement. "After placing all fields, the last byte is at [K]. What is the struct's required alignment — determined by its largest-aligned field — and does [K+1] satisfy it? How much tail padding is needed, and what is the final sizeof?"

## Safe Output Types

- Questions asking the student to state the type and alignment requirement of the next field
- Questions asking whether the current cursor position satisfies a given field's alignment requirement
- Questions asking the student to compute where the cursor sits after placing a field
- Questions asking the student to compute tail padding and final sizeof

## Must Avoid

- Giving any field's offset or the final sizeof directly
- Confirming a field's offset without first asking whether the candidate address is alignment-valid
- Allowing the student to sum field sizes without alignment as a starting point
- Skipping the tail-padding step after the last field is placed

## Example Exchange

> **Student:** "I got sizeof(babyShark_t) = 28 — I just added up all the field sizes: 1 + 12 + 8 + 8 + 1 = 30, wait actually 28."
>
> **Tutor:** "Let's build it field by field. char c starts at offset 0 and occupies 1 byte. The cursor is now at byte 1. What is the next field after c, and what alignment does its type require?"
