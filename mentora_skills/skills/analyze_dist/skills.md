---
skill_id: "analyze-dist"
name: "Analyze Distribution"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "phonemic-analysis", "distributional-analysis", "allophone", "allomorph", "methodology", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "interpret-evidence"
  - "decompose-arguments"
  - "identify-evidence"
  - "surface-assumptions"
trigger_signals:
  - "student-shown-language-data"
  - "student-asks-phonemic-status"
  - "student-asks-allophone-status"
  - "student-must-classify-phoneme-vs-allophone"
  - "student-asks-how-to-analyze-data"
  - "student-uncertain-about-distribution"
  - "data-shown-with-two-target-sounds"
  - "wrong-answer-from-incomplete-environment-listing"

version: "0.1.0"
python_entry: "logic.py"
---

# Analyze Distribution

## Description
Walks the student through the five-step distributional analysis methodology
that runs through phonemic analysis (HW4), allomorph selection (HW4 + HW5),
and syllable-conditioned alternations (HW5). Given a dataset of forms
containing two target sounds (or two allomorphs of a morpheme), the skill
scaffolds the procedure: look for minimal pairs, list environments, classify
the distribution, check phonetic similarity, choose the underlying
representation by simplicity. The student does the analysis; the skill
provides scaffolding prompts, catches common errors, and surfaces parallel
problems when stuck. Stateless — the orchestrator tracks which step the
student is on.

## When to Trigger

### Fires when:
- Student is given linguistic data (forms in IPA from any language) and
  must determine the phonemic status of two sounds
- Student must determine which allomorph of a morpheme appears in what
  context
- Student must identify a phonological rule from a paradigm of alternations
- Student says things like "are these phonemes or allophones?", "how do
  I figure out the rule?", "what's the underlying form?", or shows data
  and asks for help analyzing it
- Wrong answer reveals incomplete environment listing or jumped-to-
  conclusion analysis

### Does NOT fire when:
- Student is on a transcription question with no analysis to do (HW1/HW2
  territory)
- Student is reading a spectrogram (use `read-acoustic-trace`)
- Student needs help identifying a single natural class (use
  `id-natural-class`)
- Student has already done the analysis and just needs to formalize the
  rule (use `write-phon-rule`)
- Student's confusion is about what two sounds *sound* like, not how
  they distribute (use `contrastive-hint`)

### Boundary cases:
- **Student names two sounds but no data given**: ambiguous between this
  skill and `contrastive-hint`. If the student is asking about
  classification ("are X and Y allophones?") and the assignment is
  HW4/HW5, prefer this skill. If they're asking about feature differences
  ("how is X different from Y?"), prefer contrastive-hint.
- **Student stuck on a single step**: this skill scaffolds the whole
  procedure but each step has its own hint ladder. Re-call the skill
  with the relevant `current_step` to get step-specific scaffolding.
- **Student tries to apply English categorizations to non-English data**:
  fire alongside `repair-miscon` for the [i]/[ɪ] cross-linguistic
  projection error.

## Tutor Stance
- Methodological discipline. The student does the analysis; the skill
  scaffolds the procedure. Never classify the sounds before the student
  has compared environments. Never propose the UR before the student has
  considered both candidates. Never name the rule before the student has
  identified the change.
- Each language stands on its own. Don't appeal to English categorizations
  to settle non-English data questions.
- Insist on completeness. The discipline of writing out *every* environment
  is what catches the analysis. Don't accept partial lists.
- Phonetic similarity is required, not optional. Even with complementary
  distribution, students must check similarity (the English [h]/[ŋ] case
  is the textbook reminder).
- Two URs analyzed in parallel, not in sequence. When choosing UR by
  simplicity, the student should consider both candidates and count the
  rules each requires.

## Flow

### Step 1 — Frame the question
Confirm the student knows the trinary choice they're determining: separate
phonemes, allophones of one phoneme, or free variation. If they don't know,
redirect to `validate-prereqs` for a phonemic-principle refresher before
continuing.

### Step 2 — Look for minimal pairs
Ask: "Can you find a pair of words in the data that differ ONLY in [X]
vs [Y]?" If yes → strong evidence for separate phonemes. If no → "Absence
of minimal pairs is not proof of allophony — let's check distribution."
Move to Step 3.

### Step 3 — List environments
Have the student list every left-and-right environment where each sound
appears. Insist on completeness — every form, both contexts. This is the
discipline that catches the analysis.

### Step 4 — Classify distribution
Ask: "Looking at your two lists, is there ANY context where both [X] and
[Y] appear?" Yes → overlapping → separate phonemes. No → complementary
→ likely allophones. Proceed to Step 4b.

### Step 4b — Phonetic similarity check
Critical: complementary distribution alone is NOT sufficient. Ask "What
features do [X] and [Y] share?" If they share most features (place, manner,
voicing for consonants), proceed to Step 5. If they're radically different
(English [h]/[ŋ] case), they're separate phonemes despite complementary
distribution.

### Step 5 — Choose UR + write rule
For allophones: ask the student to consider both candidate URs in parallel.
"If [X] is the UR, what rule(s) would you need? Now if [Y] is the UR,
what rule(s) would you need?" The simpler analysis wins. Hand off to
`write-phon-rule` if the student needs help with formal notation.

## Safe Output Types
- Scaffolding prompts that ask the student to produce the next analytical
  step (list environments, identify shared contexts, propose a rule)
- Acknowledgments of student progress at each step ("right, that's
  complementary distribution — now let's check similarity")
- Redirects when the student skips ahead ("hold on — have you listed
  every environment?")
- Pointers to parallel problems from the EXAMPLE_DATASETS catalog when
  the student is stuck and an analogy would unblock
- Step-specific hints from the HINT_LADDERS at increasing levels of
  specificity
- Transition lines when handing off to a partner skill ("now that you've
  identified the rule, let's formalize the notation")

## Must Avoid
- Performing the analysis for the student (the central failure mode)
- Classifying the sounds (phonemes vs allophones) before the student has
  done the distributional comparison
- Naming the natural class of the conditioning environment (that's
  `id-natural-class`'s job)
- Writing the formal rule notation (that's `write-phon-rule`'s job)
- Appealing to English categorizations to settle non-English data
- Accepting partial environment lists — students who skip environments
  miss patterns
- Proposing the UR before both candidates have been compared
- Skipping the phonetic similarity check after complementary distribution
- Continuing to scaffold when the student is fundamentally missing a
  prerequisite (switch to `dx-prereq-gaps`)
- Mixing slashes and brackets in modeled examples (the level distinction
  must be maintained)

## Example Exchange
> **Student:** I have data from a language with [b] and [β]. Are they the
> same phoneme or different phonemes?
>
> **Tutor:** Good question. Before we look at the data, what are we trying
> to figure out — separate phonemes, allophones of one phoneme, or free
> variation?
>
> **Student:** Phonemes vs allophones I think.
>
> **Tutor:** Right. Step one — can you find a pair of words in your data
> that differ ONLY in [b] vs [β]?
>
> **Student:** I see [bino] "wine" and [laβa] "lava"... but those are
> different words about different things.
>
> **Tutor:** Those aren't a minimal pair — they don't share most of their
> structure. That's okay; absence of minimal pairs isn't proof of allophony.
> Let's list contexts. Start with [b]: in your data, what sound comes
> before and after each [b]?
>
> **Student:** [b] is at the start of *bino* and *bonito*. There's [m]
> before [b] in *ambos*.
>
> **Tutor:** Good. So [b] appears word-initially and after [m]. Now do
> the same for [β]: where does it appear?
>
> **Student:** [β] is between two vowels in *laβa* and *saβer*.
>
> **Tutor:** So [b] in some contexts, [β] in others. Look at your two
> lists side by side. Are there any contexts where BOTH [b] and [β]
> appear?
>
> **Student:** No, they're in different positions every time.
>
> **Tutor:** Right — that's complementary distribution. One more check
> before we conclude allophones: are [b] and [β] phonetically similar?
> What features do they share?

## Disambiguation from Other Skills
- `contrastive-hint` produces a *contrast* between two sounds —
  what features distinguish them. **This skill** scaffolds *analysis*
  of how two sounds *distribute* across data.
- `id-natural-class` identifies the natural class of a set of sounds.
  **This skill** identifies the *distributional pattern* of two sounds
  in data; it may *use* `id-natural-class` for the conditioning
  environment in the rule.
- `write-phon-rule` formalizes a known alternation in formal notation.
  **This skill** runs *upstream* of that — figuring out whether there
  IS an alternation to formalize.
- `repair-miscon` fires when the student's reasoning is caught on a
  cataloged misconception (e.g., projecting English [i]/[ɪ] phonemic
  status onto another language). **This skill** assumes the student's
  conceptual model is intact and just needs methodological scaffolding.
- `dx-prereq-gaps` fires when scaffolding isn't landing because the
  student lacks the phonemic principle itself. **This skill** assumes
  the principle is understood and helps the student apply it.

## Inputs Expected by logic.py
- `target_sounds` (list of str, optional): the IPA symbols under analysis,
  e.g. `["b", "β"]`
- `current_step` (int, optional): which diagnostic step the student is on
  (1-5, or "4b"). 0 or absent means the skill defaults to Step 1.
- `student_response` (str, optional): the student's most recent utterance,
  used by the orchestrator to detect when to advance steps or trigger
  error catches

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 6 diagnostic steps with tutor prompts and advance
  conditions
- `hint_ladders` (dict): keyed by step name, each value is a 3-level hint
  progression
- `common_errors` (list): cataloged error patterns with trigger phrases
  and redirect responses
- `example_datasets` (dict): 5 canonical analyses (Spanish, Korean,
  Hindi, English h-ŋ, Cree) for parallel-problem suggestion
- `tutor_reminders` (list): high-priority stance reminders for the
  orchestrator's prompt assembly

## Notes for Reusers
This skill is the workhorse for HW4 and HW5 phonemic-analysis questions.
It pairs upstream of `id-natural-class` (when the conditioning environment
needs class identification), `write-phon-rule` (when the analysis is done
and the student needs formal notation), and `probe-min-pair` (when minimal
pair reasoning is the focus).

The `EXAMPLE_DATASETS` catalog is intentionally short — full
cross-linguistic data lives in `utils/language_datasets.py`. The skill's
local copy is for portability if utils aren't loaded.