---
skill_id: "probe-min-pair"
name: "Probe Minimal Pair"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "minimal-pair", "phonemic-analysis", "evidence", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "identify-evidence"
  - "interpret-evidence"
  - "verify-claims"
trigger_signals:
  - "student-asks-what-is-minimal-pair"
  - "student-claims-no-minimal-pair-found"
  - "student-confuses-minimal-pair-with-similar-pair"
  - "student-asks-if-pair-is-minimal"
  - "wrong-answer-conflates-near-miss-with-minimal-pair"
  - "student-asks-what-minimal-pair-proves"
chip_icon: "🔗"
version: "0.1.0"
python_entry: "logic.py"
---

# Probe Minimal Pair

## Description
Helps the student find, evaluate, or construct minimal pairs as evidence
for phonemic contrast. A minimal pair is two words that share every sound
and syllable position except for one sound — the contrast at that one
position is direct evidence that the two sounds are separate phonemes in
the language. The skill scaffolds three operations: testing whether a
candidate pair counts (criteria check), finding minimal pairs in given
data, and interpreting what their presence or absence means for phonemic
status. Stateless — the orchestrator tracks which operation the student
is on.

## When to Trigger

### Fires when:
- Student asks "what is a minimal pair?" or asks for a definition
- Student claims they can't find a minimal pair in given data
- Student claims absence of a minimal pair proves allophony (it doesn't)
- Student asks whether a candidate pair (e.g., *bear* / *fair*) qualifies
- Student needs help constructing a minimal pair from the data they have
- Wrong answer treats a near-miss (e.g., *cat* / *cap*, which differs in
  the final segment too) as a minimal pair without checking criteria

### Does NOT fire when:
- Student is doing the full distributional analysis (use `analyze-dist`;
  minimal-pair search is one step within that flow)
- Student is identifying feature differences between two sounds
  (`contrastive-hint`)
- Student is reading a spectrogram (`read-spectrogram`)
- Student already has clear evidence and just needs to formalize a rule
  (`write-phon-rule`)

### Boundary cases:
- **Student claims absence of minimal pair = allophones**: this is a
  cataloged misconception. Fire alongside `repair-miscon` so the
  orchestrator can address the underlying belief.
- **Cross-linguistic data**: minimal pairs in non-English data have the
  same status as minimal pairs in English. Don't let the student's
  English intuitions override the target language's evidence.
- **Near-miss pairs** (e.g., *bear* / *fair* — differ in initial AND
  final segment): these are NOT minimal pairs. The skill's flow
  explicitly tests this.

## Tutor Stance
- The student does the comparing. The tutor asks them to walk through
  the criteria one segment at a time.
- Absence of a minimal pair is not proof of anything. Always redirect
  "I can't find one" to "what does that fact tell us, and what does it
  not tell us?"
- Minimal pairs are the cleanest evidence type, but not the only one.
  Overlapping environments without strict minimal pairs (Hindi [b]/[b̤])
  are also valid evidence for phonemic contrast.
- Each language stands on its own. A minimal pair in Hindi proves
  something about Hindi, not about English.

## Flow

### Step 1 — Establish the criteria
If the student doesn't already know, scaffold the definition: a minimal
pair is two words of equal length where every sound is identical except
for one sound at one position, and the two words have different meanings.
Have the student state these criteria back before moving on.

### Step 2 — Test a candidate pair
Given two candidate words, walk the student through segment-by-segment
comparison. At each position, ask: "Is the sound at this position the
same in both words?" Count the differences. One difference + different
meanings = minimal pair. Zero or multiple differences = not a minimal
pair.

### Step 3 — Search given data for minimal pairs
If the student has a dataset and is looking for minimal pairs containing
two target sounds, scaffold the search: "Pick a word with [X]. Now look
for a word in the data that has the same length and structure, with [Y]
where [X] was. Found one?"

### Step 4 — Interpret the result
- **Found a minimal pair**: separate phonemes in this language.
- **Found no minimal pair after exhaustive search**: inconclusive.
  Move to distributional analysis (hand off to `analyze-dist`).
- **Found a near-miss**: the candidates aren't a minimal pair, but the
  fact that they differ in two positions doesn't disqualify the sounds
  from being phonemes — keep searching.

### Step 5 — Construct minimal pairs from the data
If the student is asked to provide a minimal pair (HW1/HW2 territory),
scaffold construction: pick a word with one of the target sounds,
substitute the other target sound at that position, ask whether the
result is a real word in the language.

## Safe Output Types
- Definitional scaffolding when the student doesn't know what a minimal
  pair is
- Segment-by-segment comparison prompts ("at position 1, what sound is
  in each word?")
- Search prompts ("which word in your data has the same structure but
  with [Y] in place of [X]?")
- Interpretation prompts ("you found a minimal pair — what does that
  prove about [X] and [Y] in this language?")
- Acknowledgments of correct identification or correct rejection
- Redirects when the student misclassifies near-misses as minimal pairs
- Transitions to `analyze-dist` when minimal pair search is exhausted
  without success

## Must Avoid
- Naming whether a candidate pair is a minimal pair before the student
  has walked through the segment-by-segment comparison
- Telling the student that absence of a minimal pair proves anything
  about phonemic status — it doesn't
- Pulling minimal pairs from outside the given data when the question
  is about a specific dataset
- Accepting "*bear* and *fair* differ in one sound" without questioning
  — they differ in two
- Treating English minimal pairs as evidence about non-English data
- Continuing minimal-pair search when distributional analysis is the
  more productive next step (transition to `analyze-dist`)

## Example Exchange
> **Student:** Are *think* and *sink* a minimal pair for [θ] and [s]?
>
> **Tutor:** Good candidate. Let's test it. Walk through position by
> position — what's the first sound in *think*?
>
> **Student:** [θ].
>
> **Tutor:** And in *sink*?
>
> **Student:** [s].
>
> **Tutor:** Different at position 1, good. Position 2?
>
> **Student:** [ɪ] in both.
>
> **Tutor:** Same. Position 3?
>
> **Student:** [ŋ] in both.
>
> **Tutor:** Same. Position 4?
>
> **Student:** [k] in both.
>
> **Tutor:** Same. So total differences across all positions: how many?
>
> **Student:** Just one — at position 1.
>
> **Tutor:** And the words have different meanings?
>
> **Student:** Yes.
>
> **Tutor:** Then this is a minimal pair. What does it tell us about [θ]
> and [s] in English?
>
> **Student:** They're different phonemes?
>
> **Tutor:** Right — separate phonemes, because swapping one for the
> other changes the word's identity.

## Disambiguation from Other Skills
- `analyze-dist` runs the full five-step phonemic analysis, of which
  minimal pair search is Step 2. **This skill** zooms in specifically
  on minimal pair reasoning when that's the focus of the question or
  the source of confusion.
- `contrastive-hint` produces a feature contrast between two sounds —
  what makes them different phonetically. **This skill** is about
  whether two sounds are phonemes by testing word-level evidence, not
  about how they differ articulatorily.
- `repair-miscon` fires on the cataloged misconception "no minimal
  pair = allophones." **This skill** scaffolds the search and
  evaluation; pair them when the student has the wrong belief.
- `write-phon-rule` formalizes alternations once analysis is done.
  **This skill** runs upstream of that.

## Inputs Expected by logic.py
- `target_sounds` (list of str, optional): the two IPA symbols, e.g.
  `["θ", "s"]`
- `candidate_pair` (tuple of str, optional): two words being tested,
  e.g. `("think", "sink")`
- `dataset` (list of dict, optional): forms in the language being
  analyzed, used for minimal-pair search
- `current_step` (int, optional): which step of the flow the student
  is on (1-5). 0 or absent defaults to Step 1.

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `criteria` (list): the three minimal-pair criteria as plain-language
  checks
- `hint_ladders` (dict): per-step hint progressions for stuck students
- `common_errors` (list): cataloged error patterns with redirects
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill is the focused complement to `analyze-dist`. Use it when
minimal-pair reasoning IS the question (HW1/HW2 transcription tasks,
Quiz 4 phonemic-status questions) and analyze-dist when the full
methodology is needed. The skills can also chain: if minimal-pair
search comes up empty, transition to analyze-dist.

The criteria are language-agnostic. The same three checks apply whether
the student is working with English, Hindi, Korean, or made-up data.
The example datasets in `utils/language_datasets.py` provide many
language-specific minimal pair examples for the orchestrator to draw
on when scaffolding searches.
