---
skill_id: "preemption-event-reasoning"
name: "Preemption Event Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["scheduling", "os", "preemption", "context-switch", "cs"]
course_types: ["cs"]
learning_goal_tags:
  - "trace-execution"
  - "identify-invariants"
  - "handle-edge-cases"
trigger_signals:
  - "student-cannot-explain-when-preemption-fires-vs-when-the-running-job-continues"
  - "student-does-not-check-whether-a-newly-arrived-job-should-preempt-the-current-job"
  - "student-confuses-a-preemptive-and-non-preemptive-variant-of-the-same-policy"
  - "student-places-preemption-at-the-wrong-tick-without-reasoning-about-the-trigger-event"
  - "student-cannot-identify-what-happens-to-the-preempted-job-and-what-runs-next"
  - "student-treats-quantum-expiry-and-job-arrival-as-equivalent-preemption-triggers"
chip_icon: "⚡"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Preemption Event Reasoning

## Description

Guides students to reason about when a preemption event fires, what specific event triggers it, and what the scheduler does at the exact moment of preemption — distinguishing preemptive from non-preemptive policy variants and identifying what runs next after the interrupted job returns to the ready queue. When a student's schedule has preemption at the wrong tick, misses that a new job arrival should trigger a preemption check, conflates quantum expiry with arrival-triggered preemption, or cannot explain what the scheduler selects after kicking out the running job, this skill builds the event-driven reasoning chain from trigger to next-job selection.

## When to Trigger

- Student cannot state whether the policy is preemptive or non-preemptive, or what that distinction means
- Student does not check whether a newly arrived job's selection criterion beats the currently running job's criterion
- Student confuses a preemptive variant of a policy (e.g., SRPT) with its non-preemptive variant (e.g., SJF)
- Student places a preemption event at the wrong tick without tracing back to the event that should have triggered it
- Student cannot explain what happens to the preempted job (where it goes) and what the scheduler selects to run next
- Student treats all preemption triggers as equivalent (e.g., treats a quantum expiry the same as a new-arrival preemption check)

## Tutor Stance

- Never state whether the policy is preemptive or what triggers preemption — ask the student to derive it from the policy description
- If the student's preemption timing is wrong, ask them to identify the specific event (arrival, completion, quantum expiry) that should trigger a scheduling decision at the tick in question
- Do not confirm that a preemption fires correctly without asking the student to compare the running job's criterion to the arriving or ready job's criterion at that exact tick
- Push the student to trace what happens to the preempted job (it rejoins the ready queue) and what the scheduler selects next before moving on
- Every response must end with a question

## Flow

### Step 1 — Establish whether the policy is preemptive

Ask the student to state whether the policy interrupts a running job and under what condition, before any workload trace. "Before tracing — is [SRPT / Priority / RR] a preemptive policy? What does that mean: under what condition is a running job interrupted before it finishes its burst?"

### Step 2 — Identify the preemption trigger event

Ask the student to name the specific event type that causes the scheduler to re-evaluate which job should run. "What kind of event triggers the scheduler to check whether the current job should be preempted — a new job arriving, a quantum expiring, a job unblocking, or some combination? Walk through each event type and say whether it triggers a preemption check for this policy."

### Step 3 — Trace the exact moment of preemption

Ask the student to work through a specific preemption moment tick by tick: compare criteria, decide whether preemption fires, and identify the next job. "At t=[tick], Job B arrives with [criterion value] while Job A is running with [criterion value]. According to the policy — does Job B preempt Job A at this tick? Walk through the comparison the scheduler makes."

### Step 4 — Resolve what runs next

Ask the student to identify where the preempted job goes and what the scheduler selects immediately after preemption. "Job A is preempted — where does it go? And now that the ready queue has changed, what does the policy select to run at t=[tick+1]? Apply the selection rule to the current queue state."

## Safe Output Types

- Questions asking whether the policy is preemptive and what condition triggers preemption
- Questions asking what specific event type (arrival, quantum expiry, unblock) triggers a scheduling decision for this policy
- Questions asking the student to compare the running job's criterion to the arriving job's criterion at a specific tick
- Questions asking where the preempted job goes and what the scheduler selects next

## Must Avoid

- Stating whether the policy is preemptive or what triggers it
- Confirming a preemption event without asking the student to compare the running and arriving jobs' criterion values
- Accepting "it gets preempted" without asking the student to identify the specific event and verify the criterion comparison
- Moving past a preemption moment before the student has identified both what happens to the preempted job and what runs next

## Example Exchange

> **Student:** "My SRPT schedule is almost right but the completion times are off — I think it has something to do with when jobs arrive."
>
> **Tutor:** "Let's check a specific moment — at t=1, Job B arrives with remaining burst 2 while Job A (burst 4) is running. According to SRPT, what comparison does the scheduler make at this exact tick? Does Job B preempt Job A, and how do you decide?"
