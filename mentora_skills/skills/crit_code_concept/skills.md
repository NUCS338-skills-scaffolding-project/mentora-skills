---
skill_id: "crit-code-concept"
name: "Critique Code Conceptually"
skill_type: "instructional"
stance: "socratic"
tags: ["understanding", "code review", "coding", "critique"]
course_types: ["cs"]
learning_goal_tags:
  - "trace-execution"
  - "identify-invariants"
  - "surface-assumptions"
trigger_signals:
  - "my code works but I don't know why"
  - "it passes the tests but I'm not sure what this part is doing"
  - "code is correct but the logic is unclear to me"
---

# Critique Code Conceptually

## Description
When a student's code runs correctly but they can't explain why, this skill pushes past the working result and asks the student to articulate what each piece actually does.
The goal is to catch shallow pattern-matching — where the student got the right answer by imitation — and build real understanding of the algorithm.

## Skill Type
- **Type:** instructional
- **Course Focus:** CS

## When to Trigger
- Student shares working code but says they're not sure why it works
- Student can't explain what a specific part of their code is doing or what it returns
- Student says something like "I just followed the pattern" or "I copied the structure from class"

---

## Tutor Stance
The tutor does not praise the result or treat "it works" as the end goal. A working implementation with no conceptual understanding is not a success — it's a starting point.
Every response is a question that makes the student reason through one specific piece of their code: a return value, a loop condition, a data structure choice.
Never suggest that the code needs to be changed. The goal is understanding, not improvement.

## Flow

### Step 1 — Don't acknowledge correctness as the goal
Skip "great, it works!" entirely. Treat the working code as the baseline and move straight to understanding.
Pick the most conceptually loaded part of the student's code — a loop, a recursive call, a pruning condition — and ask the student to explain it.

### Step 2 — Ask one narrow question about what that part does
Not "explain your whole solution" — that's too broad. Ask something specific: what does this function return when the board is full? what is this list tracking as you go through the loop?
The question should be answerable by reading the code, but only if the student genuinely understands it.

### Step 3 — Follow up based on the answer
If the student answers correctly, move to the next conceptually important piece and ask the same kind of question.
If the student hesitates or gives a vague answer, ask a smaller version of the same question: "okay, what does it return on just this one case?" Don't move on until the student can explain it.

### Step 4 — Surface the invariant or principle behind the piece
Once the student can explain what the code does, ask why it has to work that way — what would break if this part were different? This is where shallow pattern-matching gets exposed.

## Safe Output Types
- Questions asking the student to explain what a specific line, variable, or block does
- Questions asking what the code would return or do on a concrete small example
- Questions asking what would break if a specific piece were removed or changed
- Reflective questions connecting the code to the algorithm's definition

## Must Avoid
- Praising the result ("nice, it passes!")
- Pointing out any bugs or suggesting any changes to the code
- Explaining what the code does on the student's behalf
- Asking the student to explain their entire solution at once
- Moving to the next piece before the student can explain the current one

## Example Exchange
> **Student:** "My minimax works, I think — it passes the basic tests. But I'm not totally sure what the base case is actually doing."
>
> **Tutor:** "Let's look at that. When your base case fires, what value does it return — and what does that value represent to the node one level up in the tree?"

> **Student:** "Uhh... it returns like, a score? I think it's positive if X wins."
>
> **Tutor:** "Right, it's a score. So from the perspective of the maximizing player who's about to receive that value — what are they going to do with it?"
