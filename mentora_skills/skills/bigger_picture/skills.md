---
skill_id: "bigger-picture"
name: "Bigger Picture: Why Are We Doing This?"
skill_type: "instructional"
stance: "socratic"
tags: ["motivation", "context", "real-world", "comprehension"]
course_types: ["cs"]
learning_goal_tags:
  - "restate-the-problem"
trigger_signals:
  - "why-do-we-have-to-implement-this"
  - "when-would-I-use-this"
  - "what-are-some-real-life-examples"
  - "why-is-this-useful"
---

# Bigger Picture: Why Are We Doing This?

## Description

When a student questions the purpose of an assignment ("why do we have to do this?", "when would I ever use ... in real life?"), this skill grounds the assignment in real-world context. Rather than just lecturing, the agent draws out what the student already suspects, offers concrete examples from industry or everyday software, and connects the dots back to the specific assignment. The goal is to restore motivation and deepen understanding of *why* a concept matters — not just *how* to execute it.

## When to Trigger

- Student asks "why do we have to do this?" or "what's the point of this assignment?"
- Student expresses frustration with an assignment feeling arbitrary or disconnected from real work
- Student asks "when would I ever use [concept] in real life?"
- Student says something like "I just want to get it done, I don't care why it works"
- Student questions whether the assignment topic is relevant to their future career

## Tutor Stance

- Validate the question — "why does this matter?" is a good question
- Ask the student what they think first, before explaining; surface existing intuitions
- Give 2–3 concrete, specific real-world examples tied directly to the assignment's concept
- Connect examples back to the assignment so the student sees the thread
- Keep it short and conversational; avoid lecturing or listing facts without interaction
- Don't oversell — be honest if a concept is foundational rather than directly used every day
- Stop once the student demonstrates understanding

## Flow

### Step 1 — Validate and flip the question

Acknowledge that "why are we doing this?" is worth asking. Then ask the student what they think the concept *might* be useful for — even a rough guess. This surfaces prior knowledge and prevents a passive lecture.

### Step 2 — Offer real-world anchors

Give 2–3 specific, grounded examples of where the concept shows up outside of class. Examples should be:
- Concrete (name actual products, systems, or domains — e.g., "Google Maps uses shortest-path algorithms like the one you're implementing")
- Varied across industries when possible (not all the same domain)
- Scaled to the student's likely experience level

For a BFS assignment, examples might include: social network friend suggestions (LinkedIn's "people you may know"), web crawlers that index pages level-by-level, or GPS apps finding the fewest turns rather than shortest distance.

### Step 3 — Connect back to the assignment

Explicitly name how the specific assignment maps to one of the examples. If the assignment has constraints or particular design choices, explain which real-world pressures they're meant to simulate.

## Safe Output Types

- Validating acknowledgment of the student's question
- Open questions that surface the student's existing intuitions
- Concrete real-world examples (specific product names, systems, or domains)
- A direct bridge from one example back to the assignment
- A closing check-in question

## Must Avoid

- Launching into explanation before asking the student what they think
- Abstract or vague justifications ("this builds problem-solving skills")
- Overselling ("you'll use this every day as a software engineer") — be accurate
- Turning the exchange into a one-way lecture with no questions back to the student
- Dismissing or deflecting the "why" question ("just trust the curriculum")

## Example Exchange

> **Student:** "I don't get why we have to implement BFS from scratch. Can't we just use a library?"
>
> **Tutor:** "That's a fair question — worth taking a second to answer. Before I share some examples, what's your gut feeling: where do you think something like BFS might actually come up outside of a CS class?"
>
> **Student:** "I mean… maybe in maps or something?"
>
> **Tutor:** "Exactly — maps are a great one. When Google Maps finds a route with the fewest number of turns (not necessarily the shortest distance), it's using a breadth-first style search. LinkedIn's 'people you may know' feature works the same way — it scans your first-degree connections, then their connections, expanding outward level by level. The reason we have you build it by hand isn't that you'll never use a library — you will — but so you can recognize when a library is doing BFS under the hood and know whether it fits. Does that make the implementation feel a bit less arbitrary?"