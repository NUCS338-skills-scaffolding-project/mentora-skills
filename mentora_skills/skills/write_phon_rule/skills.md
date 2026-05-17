---
skill_id: "write-phon-rule"
name: "Write Phonological Rule"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "phonological-rules", "formal-notation", "natural-classes", "methodology", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "construct-arguments"
  - "extract-requirements"
  - "verify-claims"
trigger_signals:
  - "student-cant-formalize-rule"
  - "student-mixes-slashes-and-brackets"
  - "student-lists-segments-instead-of-features"
  - "student-asks-how-to-write-rule"
  - "wrong-answer-rule-misses-natural-class"
  - "wrong-answer-rule-includes-extra-context"
  - "student-asks-what-to-put-in-environment"
chip_icon: "✏️"
version: "0.1.0"
python_entry: "logic.py"
---

# Write Phonological Rule

## Description
Scaffolds writing a phonological alternation in formal notation:
`/A/ → [B] / X __ Y`. The student has typically completed distributional
analysis (via `analyze-dist`) and identified an alternation, and now
needs to formalize it — including expressing the conditioning environment
in natural-class features rather than listing specific segments. The
skill walks the student through four parts: target (what changes), result
(what it becomes), environment (where the change occurs), and the
slashes/brackets distinction that maintains the underlying-vs-surface
level. Stateless — the orchestrator tracks which part the student is on.

## When to Trigger

### Fires when:
- Student has identified an alternation pattern and is asked to express
  it as a formal rule
- Student writes a rule that lists specific segments where natural-class
  features should be used
- Student mixes slashes and brackets (e.g., `/X/ → /Y/ / __ [Z]/`)
- Student asks "how do I write this as a rule?"
- Student writes a rule whose environment is missing a relevant context
  or includes irrelevant ones
- Wrong answer reveals environment is too narrow or too broad

### Does NOT fire when:
- Student is still doing distributional analysis (use `analyze-dist`)
- Student is given a rule and asked to apply it forward (use
  `apply-phon-rule`)
- Student is identifying the natural class of a set of sounds (use
  `id-natural-class`; this skill *uses* that internally)
- Student is on a transcription question (HW1/HW2)

### Boundary cases:
- **Student wants to use individual segments in environment**: this is
  a teachable moment, not a hard error. Walk them through
  feature-generalization with `id-natural-class` as a sub-task.
- **Student writes a rule that captures the data exactly but is overly
  specific**: ask "could the rule be simpler? Are there sounds in the
  environment that could be grouped together?"
- **Multi-rule alternations**: some alternations require ordered rules
  (e.g., English plural). The student should write each rule separately
  and consider order if relevant.

## Tutor Stance
- The student writes the rule. The skill scaffolds piece by piece: what
  changes, what it becomes, in what environment.
- Notation discipline matters. `/X/` is the underlying form (the
  phoneme), `[X]` is the surface form. Mixing them in a single rule
  signals level-of-representation confusion that should be addressed.
- Natural classes, not segment lists. If the environment includes
  multiple specific sounds, ask "what feature do they share? Can we use
  that instead?"
- The narrowest exhaustive class is the right answer for the environment.
  Too broad = the rule overgenerates. Too narrow = the rule misses cases.
- Stay anchored to the data. The rule must derive every surface form in
  the dataset and not produce surface forms that aren't there.

## Flow

### Step 1 — Identify the target
What sound changes? This is the `/A/` slot. It's the underlying form
that the rule will transform. Ask: "Which sound is being affected — what's
the input to the rule?"

### Step 2 — Identify the result
What does the target become on the surface? This is the `[B]` slot. Ask:
"When the rule applies, what does [A] turn into?"

### Step 3 — Identify the environment
Where does the change happen? Walk through the contexts in the data:
"In every form where [A] becomes [B], what's to the left? What's to the
right?" Identify left context, right context, word boundaries.

### Step 4 — Generalize the environment using natural classes
The contexts identified in Step 3 are concrete sounds. Now generalize:
"What do all the left contexts have in common? Can we describe them
using one feature or class?" Hand off to `id-natural-class` if the
student needs scaffolding here. Common environments: `V _ V`, `[+voice] _`,
`__ #`, `[+nasal] __`.

### Step 5 — Notation check
Verify slashes vs brackets. The target and result use different notations:
target is `/A/` (underlying), result is `[B]` (surface). Environment uses
brackets for natural classes (`[+voice]`) and `#` for word boundary, `__`
for the position of the target. Walk through each piece of the student's
rule and confirm the conventions are followed.

## Safe Output Types
- Scaffolding prompts at each part of the rule (target, result,
  environment, generalization)
- Acknowledgments when a piece is correct ("right, the target is /p/")
- Redirects when the student lists segments where features are needed
- Notation-correction prompts ("you wrote `/[X]/` — what's the
  difference between `/X/` and `[X]`?")
- Pointers to `id-natural-class` when the environment needs class
  identification
- Verification prompts after the rule is written ("does your rule
  derive every surface form in the data? Does it produce any forms NOT
  in the data?")

## Must Avoid
- Writing the rule for the student
- Naming the natural class of the environment before the student has
  identified shared features
- Accepting `/[b/d/g]/` or any segment list when feature-based
  generalization is possible
- Letting slashes/brackets confusion slide
- Skipping the verification step (does the rule cover the data without
  overgenerating?)
- Listing specific sounds in the environment when the student has
  already produced them — instead, ask "what feature unites these?"
- Continuing rule-writing scaffolding when the student is fundamentally
  unsure what's changing (return to `analyze-dist`)

## Example Exchange
> **Student:** I figured out that Spanish [b] becomes [β] between vowels.
> How do I write that as a rule?
>
> **Tutor:** Good — you've done the analysis. Let's formalize it. First,
> what's changing? In your rule, what's the target sound?
>
> **Student:** /b/.
>
> **Tutor:** Slashes or brackets — which one for the target?
>
> **Student:** Slashes, because it's the underlying form.
>
> **Tutor:** Right. And the result — what does /b/ turn into?
>
> **Student:** [β].
>
> **Tutor:** Brackets, because it's the surface form. Now the
> environment. In your data, what's to the left of [β]? And to the
> right?
>
> **Student:** Vowels on both sides.
>
> **Tutor:** So the environment is "between vowels." How would you
> notate that?
>
> **Student:** V __ V?
>
> **Tutor:** That's the standard convention. Put it all together.
>
> **Student:** /b/ → [β] / V __ V.
>
> **Tutor:** Perfect. One last check — does this rule cover every [β]
> in your data? And does it produce any [β]s where the data has [b]?

## Disambiguation from Other Skills
- `analyze-dist` runs the upstream methodology (find the alternation,
  identify the conditioning). **This skill** assumes the alternation is
  identified and helps formalize it.
- `apply-phon-rule` runs the rule forward (UR + rule → surface).
  **This skill** writes the rule from observed alternations. They're
  inverse operations.
- `id-natural-class` identifies the narrowest exhaustive class for a
  set of sounds. **This skill** uses that operation when generalizing
  the environment in Step 4.
- `repair-miscon` fires on cataloged misconceptions like "rules are
  about physical articulation" or "wider class is always better."
  **This skill** assumes the conceptual model is intact.

## Inputs Expected by logic.py
- `target_sound` (str, optional): the underlying form being transformed
- `result_sound` (str, optional): the surface realization
- `dataset` (list of dict, optional): forms in the language being
  analyzed
- `current_step` (int, optional): which step the student is on (1-5).
  0 or absent defaults to Step 1.
- `student_rule_attempt` (str, optional): the student's rule-writing
  attempt for verification feedback

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `notation_reference` (dict): formal notation conventions (slashes,
  brackets, environment marks, common abbreviations)
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `example_rules` (list): canonical phonological rules for parallel
  examples
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill pairs tightly with `analyze-dist` (upstream) and
`id-natural-class` (concurrent for the environment). Together they
implement HW4's core operation: data → analysis → formal rule.

The notation reference includes the most common environment patterns
(intervocalic, word-final, after-nasal, etc.). The orchestrator can
use these as parallel examples when the student is stuck on environment
generalization.

For multi-rule alternations like English plural [-z]/[-s]/[-əz], this
skill scaffolds each rule separately. Rule ordering is out of scope —
treat that as a separate question if it arises.
