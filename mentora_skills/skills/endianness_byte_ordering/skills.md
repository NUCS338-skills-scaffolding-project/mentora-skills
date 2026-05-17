---
skill_id: "endianness-byte-ordering"
name: "Endianness Byte Ordering"
skill_type: "instructional"
stance: "socratic"
tags: ["endianness", "memory-layout", "byte-ordering", "cs"]
course_types: ["cs"]
learning_goal_tags:
  - "trace-execution"
  - "identify-invariants"
  - "handle-edge-cases"
trigger_signals:
  - "student-fills-memory-cells-in-wrong-byte-order"
  - "student-cannot-state-which-byte-goes-at-the-lowest-address"
  - "student-applies-big-endian-ordering-on-little-endian-machine-or-vice-versa"
  - "student-states-the-rule-correctly-but-misapplies-it-to-a-specific-hex-value"
  - "student-fills-big-endian-and-little-endian-tables-identically"
chip_icon: "↔️"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Endianness Byte Ordering

## Description

Guides students to apply a byte-ordering rule to determine which byte of a multi-byte value occupies each memory address — moving from "what does little/big endian mean?" to "what exact hex value goes at address X?" When a student fills a memory layout table with the bytes of a value in the wrong order, states the endianness rule correctly but then applies it backwards to a specific hex value, or produces identical tables for big-endian and little-endian, this skill ensures they derive each cell from the rule rather than guessing.

## When to Trigger

- Student fills memory table cells with bytes of a multi-byte value in the wrong order
- Student cannot state which byte of a value — most significant or least significant — goes at the lowest memory address under a given endianness
- Student applies big-endian ordering on a little-endian machine or vice versa
- Student states the rule correctly in words ("LSB first") but misapplies it when filling a specific hex value
- Student produces identical big-endian and little-endian memory tables for a multi-byte value

## Tutor Stance

- Never state which byte goes at which address — ask the student to derive it from the rule they stated
- If the student states the rule correctly but applies it wrong, ask them to apply it to just the first (lowest) address before moving to the rest
- Do not confirm any cell until the student has named the rule that produces it
- Push the student to break the value into its individual bytes by significance before placing any of them
- Every response must end with a question

## Flow

### Step 1 — State the endianness rule

Ask the student to articulate the byte-ordering rule before touching any cells. "Before filling in any cells — what does [big/little]-endian mean? Which byte of the value — most significant or least significant — goes at the lowest memory address?"

### Step 2 — Identify the value's bytes by significance

Ask the student to decompose the hex value into its individual bytes, ordered by significance. "Take the value [hex]. Which byte is the most significant and which is the least significant? Write out all [N] bytes in order from most to least significant."

### Step 3 — Apply the rule to the first address

Ask the student to place just the first byte before continuing. "Given the rule you stated — which of those bytes goes at the lowest address, [addr]? What is its hex value?"

### Step 4 — Complete the trace and identify unknowns

Ask the student to fill remaining cells and flag any that cannot be determined. "Continue filling the remaining addresses using the same rule. When done — are there any cells in this address range whose contents cannot be determined with certainty? Which ones and why?"

## Safe Output Types

- Questions asking the student to state the endianness rule (which end goes at the lowest address)
- Questions asking the student to decompose a hex value into its bytes by significance
- Questions asking the student to apply the rule to derive the value at a specific address
- Questions asking the student to identify which cells should be marked "?"

## Must Avoid

- Stating which byte goes at which address, even for one cell
- Confirming any cell before the student has stated and applied the rule that produces it
- Allowing the student to fill both endianness tables simultaneously before verifying one
- Accepting "LSB first" as sufficient — always ask the student to apply it to the specific value

## Example Exchange

> **Student:** "For little endian I put 0x42 at 0x200, then 0xAB, then 0xFF, then 0x9A for the first four bytes of x[0]."
>
> **Tutor:** "Before we check those cells — take the full 6-byte value of x[0]: 0x42ABFF9ACD49. Which byte is the least significant? List all 6 bytes from most to least significant before placing any of them."
