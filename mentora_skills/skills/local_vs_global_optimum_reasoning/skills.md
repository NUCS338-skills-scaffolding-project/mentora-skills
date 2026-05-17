---
skill_id: "local-vs-global-optimum-reasoning"
name: "Local vs Global Optimum Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["search", "local-search", "hill-climbing", "optimality", "ai"]
course_types: ["cs"]
learning_goal_tags:
  - "evaluate-reasoning"
  - "identify-invariants"
  - "compare-strategies"
trigger_signals:
  - "student-thinks-hill-climbing-always-finds-the-best-solution"
  - "student-conflates-no-better-neighbor-with-the-problem-being-solved"
  - "student-does-not-understand-why-the-algorithm-returns-false-when-stuck"
  - "student-cannot-construct-a-case-where-hill-climbing-fails-to-find-a-solution"
  - "student-cannot-explain-the-difference-between-a-local-minimum-and-a-global-minimum"
  - "student-does-not-connect-the-boolean-return-value-to-whether-a-solution-was-found"
chip_icon: "⛰️"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Local vs Global Optimum Reasoning

## Description

Guides students to understand the distinction between a local optimum — a state with no better neighbors — and a global optimum — the actual best solution — and to reason about why hill-climbing and greedy local search can get stuck at local optima that are not solutions. When a student thinks a "no better neighbor" termination means the algorithm succeeded, or cannot construct a case where the algorithm fails, this skill builds the reasoning from the algorithm's termination condition to its correctness guarantee.

## When to Trigger

- Student believes hill-climbing always finds the globally optimal solution
- Student conflates "no better neighbor exists" with "the problem is solved"
- Student does not understand why the algorithm returns False (or equivalent failure signal) when it terminates without a solution
- Student cannot construct or describe a concrete case where hill-climbing fails to find a solution
- Student cannot explain the difference between a local minimum and a global minimum in their specific problem
- Student does not connect the boolean return value to whether an actual solution was reached

## Tutor Stance

- Never construct the counterexample for the student — ask them to find a configuration where hill-climbing gets stuck
- If the student thinks hill-climbing always succeeds, ask what the algorithm does when no neighbor improves the score
- Do not confirm the student understands the distinction until they can state what condition must hold for the termination state to be a solution
- Push the student to connect the theoretical limitation to what it means for their specific problem and return value
- Every response must end with a question

## Flow

### Step 1 — Distinguish termination from success

Ask the student to state what hill-climbing's termination condition is and whether it guarantees a solution. "When does your hill-climbing algorithm stop? And when it stops — does that mean it found a solution, or just that it can't improve anymore? What is the difference between those two things?"

### Step 2 — Define local vs global optimum

Ask the student to define a local minimum in terms of their specific problem. "In your problem — what would a local minimum look like? What would make a state a dead end for the algorithm even though it's not the goal?"

### Step 3 — Construct a failing case

Ask the student to find or construct a concrete configuration where hill-climbing gets stuck without solving the problem. "Can you draw or describe a specific board configuration — or a small example — where your algorithm would terminate but the answer is False? Where would it get stuck and why?"

### Step 4 — Connect to the return value

Ask the student to explain what the boolean return value means in light of local optima. "Given that hill-climbing can get stuck — what should your algorithm return when it terminates? And how do you know, at the termination state, whether you're at a solution or a local minimum that isn't one?"

## Safe Output Types

- Questions asking the student to distinguish the termination condition from a success condition
- Questions asking the student to define a local minimum in their specific problem
- Questions asking the student to construct a concrete case where hill-climbing fails
- Questions connecting the termination state to the boolean return value

## Must Avoid

- Constructing the counterexample or failing configuration for the student
- Accepting "the algorithm finds the best solution" without asking what happens at a local minimum
- Explaining the local vs global distinction without first asking the student to reason through the termination condition
- Confirming understanding without asking the student to connect it to the return value in their code

## Example Exchange

> **Student:** "My hill-climbing stops when no queen move reduces the number of attacks, so it's at the minimum."
>
> **Tutor:** "It's at a minimum — but what kind of minimum? Can you describe a queen configuration where no single move reduces attacks, but the board still isn't a valid solution? What would your algorithm return in that case?"
