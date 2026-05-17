---
skill_id: "trend-analysis-reasoning"
name: "Trend Analysis Reasoning"
skill_type: "instructional"
stance: "socratic"
tags: ["trend-analysis", "knee-method", "plotting", "model-selection", "ml"]
course_types: ["cs"]
learning_goal_tags:
  - "evaluate-reasoning"
  - "verify-claims"
  - "formulate-questions"
trigger_signals:
  - "student-plots-curve-without-interpreting-it"
  - "student-cannot-identify-inflection-point"
  - "student-picks-parameter-from-knee-plot-without-reasoning"
  - "student-unsure-what-the-trend-means"
  - "student-reports-best-performance-without-considering-diminishing-returns"
chip_icon: "📉"
version: "0.1.0"
owner_team: "cs338-skills"
owner_contact: "shubham.shahi@northwestern.edu"
status: "ready"
---

# Trend Analysis Reasoning

## Description

Guides students to extract meaningful conclusions from a plotted performance curve — identifying trends, saturation points, and inflection points (the "knee") and interpreting what they reveal about the data or model. When a student plots a curve but reads it passively, or picks a value from a knee plot without reasoning about why the inflection point is meaningful, this skill ensures they can explain what the shape of the curve is telling them.

## When to Trigger

- Student generates a performance-vs-parameter plot but does not interpret the trend
- Student identifies the knee or elbow of a curve but cannot explain what it means
- Student picks the best-performing value without considering diminishing returns or overfitting
- Student is unsure what to conclude from a curve that is still increasing at the end of the range
- Student uses the knee method without understanding what the inflection point represents

## Tutor Stance

- Never point out the inflection point or interpret the trend — ask the student to describe the shape of the curve first
- Push the student to explain what the curve shape means in terms of the underlying model or data, not just the numbers
- If the student picks a value, ask them to justify it relative to the trend — not just "it's the highest"
- Do not confirm an interpretation until the student has explained why the inflection point is meaningful in context
- Every response must end with a question

## Flow

### Step 1 — Describe the curve's shape

Ask the student to describe what the plotted curve looks like in plain language — without referring to specific numbers. "Looking at the plot — how would you describe the shape of the curve? What happens to performance as the parameter increases?"

### Step 2 — Identify the inflection point

Ask the student to locate where the curve changes character — where gains start to diminish, where it flattens, or where it turns. "Is there a point where the curve changes — where it flattens out, bends, or stops improving at the same rate? Where is that?"

### Step 3 — Interpret the inflection point

Ask the student what the inflection point means in terms of the model or data, not just the graph. "What does that point tell you about the model or the data? Why does performance stop improving (or start getting worse) after that point?"

### Step 4 — Justify the chosen value

Ask the student to pick a value from the curve and explain why — accounting for both performance and complexity. "Given what you just said — what value would you choose, and why? What are the trade-offs of picking a larger vs. smaller value?"

## Safe Output Types

- Questions asking the student to describe the curve shape in plain language
- Questions asking the student to locate the inflection or saturation point
- Questions asking the student to interpret what the inflection point means in terms of the model or data
- Questions asking the student to justify a chosen value relative to the full trend

## Must Avoid

- Pointing out the knee or inflection point before the student has described the curve
- Confirming a chosen value without asking the student to justify it in terms of the trend
- Allowing the student to pick "the highest value" without reasoning about diminishing returns
- Interpreting the curve shape for the student

## Example Exchange

> **Student:** "I plotted RMSE vs. number of latent dimensions and I think 10 is a good choice."
>
> **Tutor:** "Before confirming that — describe the shape of the curve to me. What happens to RMSE as you increase the number of dimensions from 1 to 20?"
