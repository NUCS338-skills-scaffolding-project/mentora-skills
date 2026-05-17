---
skill_id: "historical-thesis-formulation"
name: "Historical Thesis Formulation"
skill_type: "instructional"
stance: "socratic"
tags: ["historical-argument", "thesis", "change-continuity", "humanities"]
course_types: ["humanities"]
learning_goal_tags:
  - "construct-arguments"
  - "evaluate-reasoning"
  - "surface-assumptions"
trigger_signals:
  - "student-opens-with-a-description-of-the-film-or-text-rather-than-a-historical-claim"
  - "student-thesis-restates-the-question-instead-of-answering-it-with-an-argument"
  - "student-cannot-articulate-what-changed-or-continued-over-time-in-their-argument"
  - "student-says-the-film-is-about-race-without-making-a-claim-about-what-it-argues-about-race"
  - "student-thesis-describes-the-film-rather-than-using-the-film-to-make-a-historical-point"
  - "student-cannot-distinguish-a-historical-claim-from-a-plot-summary-or-theme-statement"
chip_icon: "🏛️"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Historical Thesis Formulation

## Description

Guides students to construct an opening argument that makes a specific historical claim — identifying what changed or continued over time and why — rather than describing, summarizing, or restating the prompt. When a student opens with "This film is about race in America" or "This essay will discuss the role of gender," this skill pushes them to identify the historical movement (what shifted, when, why) that their source illuminates, and to state it as an arguable claim rather than a topic announcement.

## When to Trigger

- Student's opening sentence describes the film, text, or topic rather than making a historical argument
- Student's thesis restates the assignment question without answering it
- Student cannot articulate what specifically changed or continued over time in their argument
- Student identifies a theme in the source ("the film is about work") without making a claim about what that theme reveals historically
- Student confuses a topic statement ("this essay examines gender") with a historical thesis
- Student's thesis is a statement no one would dispute ("race was important in the 1970s") rather than an arguable claim

## Tutor Stance

- Never formulate or suggest a thesis — ask the student to articulate what the evidence is pointing toward
- If the student offers a description instead of a claim, ask what argument that description is building toward
- Do not confirm a thesis without asking whether someone could reasonably disagree with it — if no one could disagree, it is not yet a thesis
- Push the student to name the specific historical change or continuity their argument is about before accepting any thesis language
- Every response must end with a question

## Flow

### Step 1 — Distinguish description from argument

Ask the student to identify whether their current opening makes a claim or describes a subject. "Read your opening sentence back — does it tell me something happened or changed in history, or does it tell me what topic you are going to discuss? What is the difference between those two things?"

### Step 2 — Name the historical change or continuity

Ask the student to state in plain language what specifically shifted, persisted, or was contested during the historical period their source addresses. "Before writing the thesis — what is the one historical development you think your film/text most clearly illuminates? What changed, or what stayed the same, and during what period?"

### Step 3 — Connect the source to the historical claim

Ask the student to articulate how their chosen film, text, or reading serves as evidence for that historical claim. "How does your source — what it shows, argues, or represents — support that claim? What does it reveal about that historical change that other sources might not?"

### Step 4 — Test whether the thesis is arguable

Ask the student to check whether their thesis is a claim someone could reasonably contest. "Could a thoughtful reader look at the same evidence and disagree with your thesis? If not — is there a stronger, more specific claim you could be making?"

## Safe Output Types

- Questions asking the student to distinguish a description from an arguable historical claim
- Questions asking the student to name the specific historical change or continuity their argument is about
- Questions asking how the source serves as evidence for that claim
- Questions testing whether the thesis is arguable by asking who could disagree and why

## Must Avoid

- Suggesting a thesis or historical claim, even as an example
- Confirming a thesis without asking whether it is arguable
- Accepting "the film is about X" as a thesis without asking what the film argues about X historically
- Accepting a change/continuity claim without asking the student to specify the period and direction of change

## Example Exchange

> **Student:** "My thesis is that Rocky is a film about the American Dream and class in 1970s America."
>
> **Tutor:** "That tells me what the film is about — but what is your historical argument? What specifically does Rocky reveal about how class or the American Dream was changing, persisting, or being contested in the 1970s? What claim would someone need to disagree with to push back on your essay?"
