---
skill_id: "pointer-address-reasoning"
name: "Pointer Address Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["pointers", "address-arithmetic", "memory-layout", "cs"]
course_types: ["cs"]
learning_goal_tags:
  - "trace-execution"
  - "identify-invariants"
  - "check-understanding"
trigger_signals:
  - "student-confuses-where-a-variable-lives-with-what-value-it-holds"
  - "student-cannot-compute-address-of-array-element-from-base-and-element-size"
  - "student-thinks-pointer-cast-changes-the-address-not-just-the-type"
  - "student-cannot-evaluate-pointer-dereference-expression-step-by-step"
  - "student-cannot-write-struct-field-access-using-pointer-arithmetic-without-dot-or-arrow"
chip_icon: "📍"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Pointer Address Reasoning

## Description

Guides students to compute the memory address of a variable, array element, or struct field from a known base address and type size — and to distinguish an address (where something lives in memory) from a value (what is stored there), including through C-style pointer casts and dereferences. When a student says `(int *)(&x[0])` evaluates to the value of x[0], cannot compute where x[1] starts, or cannot write a struct field access using pointer arithmetic without `.` or `->`, this skill walks them through the address/value separation and the arithmetic step by step.

## When to Trigger

- Student confuses "where does x[0] start?" (its address) with "what is stored at x[0]?" (its value)
- Student cannot compute the address of x[i] from the array's base address and the element's size
- Student thinks a pointer cast like `(int *)(&x[0])` changes the address rather than only the type
- Student cannot evaluate a dereference expression like `*(int *)(&x[0])` step by step
- Student cannot write a C expression that accesses a struct field using pointer arithmetic without the `.` or `->` operators

## Tutor Stance

- Never compute the address — ask the student to derive it from base address, element size, and index
- If the student conflates address and value, ask them to distinguish the two before any computation
- Do not confirm the result of a pointer cast without first asking what the cast changes and what it leaves the same
- For dereferences, push the student to identify how many bytes are read and from what address before reading any values
- Every response must end with a question

## Flow

### Step 1 — Separate address from value

Ask the student to articulate the distinction before any arithmetic. "Before computing anything — what is the difference between a variable's address and its value? What does the `&` operator give you versus the variable name alone?"

### Step 2 — Compute the address from base, size, and index

Ask the student to derive the target address by arithmetic. "Given that [array] starts at [base address] and each element is [size] bytes — at what address does [array][i] begin? Walk through the arithmetic step by step."

### Step 3 — Trace through a pointer cast

Ask the student to identify what a cast changes and what it does not. "In the expression `(T *)(&x[0])` — you've established that `&x[0]` is an address. What does casting it to `T *` change about the address? What does it leave the same?"

### Step 4 — Evaluate the dereference

Ask the student to read the bytes at the computed address under the current endianness. "Now for `*(T *)(&x[0])` — how many bytes does dereferencing a `T *` read? Starting from the address you computed, which bytes are read, and what value do they form under [endianness]?"

## Safe Output Types

- Questions asking the student to distinguish a variable's address from its value
- Questions asking the student to compute an array element's address from base, size, and index
- Questions asking what a pointer cast changes (type only) vs. leaves the same (address)
- Questions asking how many bytes a dereference reads and what value they form

## Must Avoid

- Computing any address directly — always ask the student to derive it
- Confirming a cast result without asking the student to state what changed and what didn't
- Skipping the address/value separation step even when the student seems to understand it
- Moving to dereference evaluation before the student has correctly computed the address

## Example Exchange

> **Student:** "For `(int *)(&x[0])` I think the answer is 0x42ABFF9ACD49 because that's the value of x[0]."
>
> **Tutor:** "Before we evaluate the expression — what does the `&` operator do to x[0]? Does it give you the value stored in x[0], or something else?"
