---
skill_id: "escalate-support-level"
name: "Escalate Support Level"
skill_type: "instructional"
stance: "meta"
tags: ["scaffolding", "stuck", "support-intensity", "metacognition"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "manage-effort"
  - "request-targeted-help"
trigger_signals:
  - "student-stuck-after-socratic"
  - "student-not-responding-to-questions"
  - "multiple-failed-attempts"
  - "student-silence-persists"
  - "socratic-approach-stalling"
version: "0.1.0"
---

# Escalate Support Level

## Description

When Socratic questioning is no longer moving a stuck student forward, shifts the tutoring approach to more direct support — from asking back to giving targeted hints, examples, or scaffolding. Manages the intensity of tutoring intervention without jumping to answers. Recognizes when the student needs *direction* rather than *discovery*, and provides a pathway through escalating levels of support.

## When to Trigger

### Fires when:
- Student has received multiple Socratic questions but is still stuck (answering "I don't know," staying silent, or repeating the same wrong answer)
- The student's struggle has shifted from "I need to think harder" to "I need help understanding where to start"
- Probing and asking back has reached diminishing returns in the current turn or across multiple turns
- Student explicitly requests more direct help ("Can you just tell me...?")

### Does NOT fire when:
- Student is still actively thinking or attempting after a question — give them time first
- Student's wrong answer reveals a misconception that needs `repair-miscon`, not support escalation
- Student lacks prerequisite knowledge entirely — use `dx-prereq-gaps` instead
- Student needs emotional support or normalization of struggle — coordinate with `normalize-struggle`

### Boundary cases:
- **First escalation in a session**: Student has tried Socratic, it's not landing. Time to shift.
- **Multiple escalations across turns**: Orchestrator tracks which support level has been tried; this skill guides the next move up.
- **At max support level**: If direct hints and examples still don't unblock, consider switching skills entirely or acknowledging the need for a different kind of help.

## Tutor Stance

- **Acknowledge the shift explicitly.** Don't pretend you're still asking questions when you're pivoting to hints. "Let me be more direct here..."
- **Support is not surrender.** Escalating to hints doesn't mean giving the answer. It means being more specific about where to look or what to try.
- **Match intensity to struggle.** A student stuck on step 1 needs a lighter hint than a student stuck on step 5. Calibrate.
- **Normalize the pivot.** Frame escalating support as a natural next move, not a sign of failure. "This is a hard one — let me give you something more concrete to work with."
- **Preserve some cognitive work.** Even at higher support levels, the student should still be doing *something* — applying a hint, testing an example, filling in a gap — not passively receiving.
- **Don't layer hints.** One hint per turn. Let them try. If they're still stuck, escalate further next turn.
- **Know when to stop.** If max-level support (detailed example, structured scaffolding) doesn't move them, that's a signal to step back: either diagnose a gap, try a reframe, or acknowledge this isn't the right skill.

## Flow

### Step 1 — Recognize the stall
After a question or two, notice that Socratic is not landing:
- Student gives non-answers ("I don't know," "I'm not sure")
- Student repeats the same wrong answer despite probing
- Student goes silent or asks you to just tell them
- Multiple turns have passed with no progress

### Step 2 — Acknowledge the struggle and the shift
Explicitly name what's happening. Don't just suddenly switch tone.

Useful language:
- "I can see you're stuck. Let me shift approaches and give you something more concrete."
- "Asking questions isn't getting us there. Let me point you in a direction instead."
- "This is a tricky one. Rather than keep asking, let me show you where to focus."

Optionally weave in normalization:
- "Struggling here is normal — this is the kind of problem that needs some scaffolding."
- "You're in the right ballpark. Let me give you a firmer foothold."

### Step 3 — Deliver the first-level hint or scaffold
Move to a more direct form of support. This might be:
- A **directional hint** ("The answer involves X, not Y")
- A **structural scaffold** ("Break this into three parts: first do X, then Y, then Z")
- A **concrete example** from the domain ("Here's how you'd approach a similar problem...")
- A **focused observation** ("Notice that when you X, Y happens — what does that tell you?")

Do not give the answer. Do not explain the full solution. Give enough to unblock the next step.

### Step 4 — Set expectations for the next turn
Make clear that you're handing the work back to them:
- "Now try applying that to your problem."
- "See if that structure helps you organize your thinking."
- "Take another pass with that hint in mind."

### Step 5 — Wait for their attempt
Let them work with the hint. Don't add more support preemptively.

### Step 6 — If still stuck, escalate further
If the hint doesn't land:
- **Next escalation:** More specificity in the same direction (Step 3 hint → Step 4 hint)
- **Or:** Shift to a different form of support (directional hint → structured example)
- **Or:** Consider exiting the skill and trying a different approach (reframe, repair misconception, diagnose gap)

Use judgment: don't keep escalating the same hint ladder forever. After 2–3 escalation attempts with no progress, it's time to step back and try a different strategy.

## Safe Output Types

- Explicit acknowledgments of the shift in approach ("Let me be more direct...")
- Directional hints that point without solving
- Structural scaffolds (numbered steps, frameworks)
- Concrete examples or analogies from the domain
- Focused observations ("Have you noticed...?")
- Restatements of the problem in clearer terms
- Brief affirmations when the student makes progress with a hint
- Guidance on what to try next
- Transitions between support levels

## Must Avoid

- **Giving away the answer.** Even at max escalation, the student should do some work.
- **Jumping multiple levels at once.** If a light hint might work, don't jump to a full example. Escalate gradually.
- **Stacking multiple hints in one turn.** One hint, then wait. Let them try.
- **Pretending you're still asking questions when you're giving hints.** Be explicit about the shift in stance.
- **Escalating support on a misconception.** If the student's wrong answer reveals a flawed mental model, use `repair-miscon`, not escalating hints.
- **Continuing to escalate after max level.** If structured examples and scaffolding aren't unblocking, exit the skill. Try a different skill or acknowledge the need for a different kind of help.
- **Removing all cognitive work.** Even with direct hints, the student should still apply, test, or reason through something.

## Example Exchange

> **Student:** "I have no idea how to start this problem."
>
> **Tutor:** *(Socratic attempt)* "What do you notice about the structure of the input? What are the constraints telling you?"
>
> **Student:** "Um... I'm not sure. It's just confusing."
>
> **Tutor:** *(Second Socratic attempt)* "OK, let's narrow it down. Forget the whole problem for a second. What do you think the first step should be — reading the input, checking edge cases, or something else?"
>
> **Student:** "I really don't know where to even begin."
>
> **Tutor:** *(Recognize stall, escalate)* "I can see you're stuck at the starting line. Rather than keep asking, let me give you a structure to work with. Most problems like this break into three phases: (1) parse or understand the input, (2) identify the core logic, (3) build and test. Try reading through the problem and labeling which phase each sentence fits into. What do you find?"
>
> **Student:** "Oh, OK. So the first two sentences are about the input, the next paragraph is the logic, and the last bit is about output?"
>
> **Tutor:** "Exactly. Now that you've mapped the structure, what does the core logic paragraph actually ask you to do in plain English?"

---

## Disambiguation from Other Skills

- **`normalize-struggle`** acknowledges and validates the emotional experience of being stuck. **This skill** provides concrete support escalation. They work well together — normalize the struggle, then escalate support.
- **`repair-miscon`** fires when the student's stuckness is caused by a wrong mental model. **This skill** fires when the model is sound but the student needs direction. Check first: is it a gap or a misconception?
- **`dx-prereq-gaps`** fires when hints aren't landing because foundational knowledge is missing. **This skill** assumes prerequisites are in place; it's about intensity of tutoring, not filling knowledge gaps.
- **`reframe`** changes *how* the student thinks about the problem. **This skill** changes *how much help* they're getting. Different moves.
