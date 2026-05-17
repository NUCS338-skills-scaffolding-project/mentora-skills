---
skill_id: "apply-phon-rule"
name: "Apply Phonological Rule"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "phonological-rules", "derivation", "forward-application", "methodology", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "extract-requirements"
  - "verify-claims"
  - "surface-assumptions"
trigger_signals:
  - "student-given-ur-and-rule"
  - "student-asks-how-to-apply-rule"
  - "student-stuck-deriving-surface-form"
  - "wrong-answer-applies-rule-where-environment-doesnt-match"
  - "wrong-answer-fails-to-apply-rule-where-environment-matches"
  - "student-confuses-rule-reading-with-rule-application"
  - "student-asks-what-rule-produces"
chip_icon: "▶️"
version: "0.1.0"
python_entry: "logic.py"
---

# Apply Phonological Rule

## Description
Scaffolds applying a given phonological rule forward — deriving the
surface form from an underlying representation. The student is given a
UR (e.g., `/apa/`) and a rule (e.g., `/p/ → [b] / V __ V`) and must
produce the surface form (`[aba]`). Forward derivation is mechanical
once the student understands rule-reading: parse the rule (target,
result, environment), scan the UR for environment matches, apply the
change at each match. Tested explicitly on Midterm 2 (review problems
C2-C3) but rarely on HW4. Stateless — the orchestrator tracks which
step the student is on and which loci have been checked.

## When to Trigger

### Fires when:
- Student is given a UR and a rule and must derive the surface form
- Student attempts to apply a rule and gets the wrong answer
- Student asks "how do I use this rule?" or "what does this rule
  produce on /X/?"
- Student applies the rule incorrectly (in the wrong context, or fails
  to apply where the context matches)
- Student treats rule-application as the same operation as rule-reading

### Does NOT fire when:
- Student is writing a rule from observed data (use `write-phon-rule` —
  the inverse operation)
- Student is doing distributional analysis (use `analyze-dist`)
- Student is identifying a natural class (use `id-natural-class`)
- Student is on a transcription question (HW1/HW2)

### Boundary cases:
- **Multiple rule applications in one form**: scan left-to-right and
  apply the rule at every matching context. Example: rule `/p/ → [b] /
  V _ V` applied to `/apapa/` yields `[ababa]`, not `[abapa]` — both
  /p/'s match the environment.
- **Rule order matters**: when two rules interact, the order can change
  the output. This skill handles single-rule application. For ordered
  rule sets, scaffold each rule application in turn.
- **Rule doesn't apply at all**: if the UR doesn't match the rule's
  environment anywhere, the surface form equals the UR. Students
  sometimes try to "force" rule application — redirect.

## Tutor Stance
- The student does the derivation. The skill scaffolds the procedure.
- Application is mechanical, not creative. Given a UR and a rule, the
  surface form is fully determined. The student's job is to check
  matches systematically, not to interpret.
- Read every rule completely before applying. Target → result, then
  environment. Then scan.
- Scan every position. Don't stop at the first match — there may be
  multiple loci.
- Match the environment exactly. If the rule says `V __ V`, both
  contexts must be vowels. A consonant on either side disqualifies
  that locus.
- If no locus matches, the rule doesn't apply. Surface = UR.

## Flow

### Step 1 — Parse the rule
Read the rule into its three parts: target (what gets transformed),
result (what it becomes), environment (where the change happens). Have
the student identify each part out loud.

### Step 2 — Scan the UR for the target
Find every position where the target sound appears in the UR. Mark each
as a candidate locus. (Rules can apply multiple times in one form.)

### Step 3 — Check the environment at each locus
At each candidate position, check whether the environment matches.
Walk through left context and right context separately. If any part
of the environment doesn't match, the rule doesn't apply at that locus.

### Step 4 — Apply the change at matching loci
At every locus where the environment matches, replace the target with
the result. Loci where the environment doesn't match stay unchanged.

### Step 5 — Output the surface form
Read the resulting form. This is the surface representation. Use brackets
`[X]` for the surface form, slashes `/X/` for the original UR.

## Safe Output Types
- Rule-parsing prompts ("read the rule out loud — what's the target?
  what's the result? what's the environment?")
- Locus-finding prompts ("scan the UR — where does the target appear?")
- Environment-checking prompts ("at this locus, what's to the left? Is
  that the left context the rule requires?")
- Application acknowledgments ("right, the environment matches here, so
  the target becomes the result")
- Non-application acknowledgments ("the environment doesn't match here,
  so the target stays unchanged")
- Verification prompts after derivation ("read the surface form back —
  does it look right?")
- Redirects when the student tries to force application or misses a
  matching locus

## Must Avoid
- Deriving the surface form for the student
- Glossing over the environment check ("yeah it'll apply" without
  walking through left and right contexts)
- Letting the student stop at the first match when multiple loci exist
- Letting the student apply a rule whose environment doesn't actually
  match (a common error pattern)
- Mixing the slashes/brackets convention in modeled examples
- Treating multi-rule alternations as if a single rule covers everything —
  apply rules one at a time
- Continuing rule-application scaffolding when the student doesn't
  understand what the rule says (return to `write-phon-rule` for the
  notation, or `validate-prereqs` for rule conventions)

## Example Exchange
> **Student:** I have the rule /p/ → [b] / V __ V. The UR is /apapa/.
> What's the surface form?
>
> **Tutor:** Let's apply it together. First, read the rule out loud.
> What's the target?
>
> **Student:** /p/.
>
> **Tutor:** And what does it become?
>
> **Student:** [b].
>
> **Tutor:** And the environment?
>
> **Student:** Between two vowels.
>
> **Tutor:** Good. Now scan the UR /apapa/. Where does /p/ appear?
>
> **Student:** Position 2 and position 4.
>
> **Tutor:** Two loci. Let's check the environment at each. Locus 1 —
> what's to the left of the first /p/? What's to the right?
>
> **Student:** [a] on the left, [a] on the right.
>
> **Tutor:** Both vowels?
>
> **Student:** Yes.
>
> **Tutor:** So the environment matches. /p/ becomes [b] there. Now
> locus 2 — same check. What's left and right of the second /p/?
>
> **Student:** [a] on both sides too.
>
> **Tutor:** Both match. So both /p/'s become [b]. What's the surface
> form?
>
> **Student:** [ababa].
>
> **Tutor:** Right. Don't forget the brackets — surface forms use
> brackets, underlying forms use slashes.

## Disambiguation from Other Skills
- `write-phon-rule` writes a rule from observed data. **This skill**
  applies a given rule forward to derive surface from UR. They're
  inverse operations.
- `analyze-dist` runs the upstream distributional analysis. **This
  skill** is downstream of any analysis — the rule is already known.
- `id-natural-class` identifies the natural class of a set of sounds.
  **This skill** uses class memberships when checking whether a context
  matches a feature-based environment, but doesn't identify them.
- `repair-miscon` fires on cataloged misconceptions like "rule reading
  is the same as rule application" or "rules apply randomly." **This
  skill** assumes the student understands rules are deterministic
  symbolic mappings.

## Inputs Expected by logic.py
- `rule` (str, optional): the phonological rule in standard notation,
  e.g. `"/p/ → [b] / V __ V"`
- `ur` (str, optional): the underlying representation, e.g. `"/apapa/"`
- `current_step` (int, optional): which step the student is on (1-5).
  0 or absent defaults to Step 1.
- `loci_checked` (list of int, optional): positions in the UR already
  evaluated, used by orchestrator for multi-locus scaffolding

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `parsing_template` (dict): the structure for parsing a rule into
  target, result, and environment components
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `example_derivations` (list): canonical UR + rule → surface
  derivations for parallel examples
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill complements `write-phon-rule` — together they cover both
directions of rule operation. Forward application is tested on Midterm 2
(review problems C2-C3) and occasionally embedded in HW4 questions
that ask "what would this rule produce?"

The example derivations include cases where the rule applies once,
applies multiple times, and doesn't apply at all. Use these to
scaffold the student through edge cases that feel surprising.

For ordered rule sets (rare in LING 250 but appears in advanced phonology),
apply each rule in turn — this skill scaffolds one rule at a time.
