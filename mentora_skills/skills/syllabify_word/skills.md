---
skill_id: "syllabify-word"
name: "Syllabify Word"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "syllable-structure", "mop", "sonority", "phonotactics", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "extract-requirements"
  - "verify-claims"
  - "decompose-arguments"
trigger_signals:
  - "student-asks-how-to-syllabify"
  - "student-applies-mop-without-phonotactic-check"
  - "student-counts-letters-not-vowels"
  - "student-cant-place-cluster-in-onset-or-coda"
  - "wrong-answer-creates-illegal-onset"
  - "student-asks-where-syllable-boundary-is"
  - "student-confuses-spelling-with-syllabification"
chip_icon: "📑"
version: "0.1.0"
python_entry: "logic.py"
---

# Syllabify Word

## Description
Scaffolds dividing a word into syllables using two principles: the
**Maximum Onset Principle** (MOP — assign as many consonants to the
following onset as possible) and **phonotactic legality** (the resulting
onsets and codas must be permissible in the language). The skill walks
the student through counting syllables (= counting vowels), placing
intervocalic consonants by MOP, and checking that the proposed onsets
are legal English onsets via the Sonority Sequencing Principle (SSP).
Targets HW5 Q16 (English syllabification, 8 points). Stateless — the
orchestrator tracks which step the student is on.

## When to Trigger

### Fires when:
- Student is asked to syllabify a word (e.g., *aluminum*, *constraint*,
  *atlas*)
- Student asks "how do I syllabify this?"
- Student applies MOP without checking phonotactic legality (creates
  illegal onsets like *.tla.*)
- Student counts letters or syllables incorrectly (e.g., 4 syllables
  for *aluminum* which has 4 vowel sounds)
- Student gives onset or coda assignment that's clearly wrong by SSP
- Wrong answer reveals confusion between spelling and pronunciation
  (e.g., counting silent letters)
- Student can't place a consonant cluster in onset vs coda

### Does NOT fire when:
- Student is doing distributional analysis (use `analyze-dist`)
- Student is on a transcription question without syllabification
  (HW1/HW2)
- Student is identifying a natural class (use `id-natural-class`)
- Student is reading acoustic data (use the read-* skills)

### Boundary cases:
- **Ambisyllabic consonants**: in some words (e.g., *better*), a
  consonant arguably belongs to both syllables. For LING 250 purposes,
  apply MOP and assign to the onset of the following syllable.
- **Stress-conditioned syllabification**: stress can sometimes shift
  syllabification. The HW5 problems don't test this — use MOP and
  phonotactics, ignore stress.
- **Loanwords with non-English clusters**: words like *psychology*
  have spelling-only consonant clusters that aren't pronounced. Always
  syllabify based on PRONUNCIATION (the phonemic form), not spelling.

## Tutor Stance
- The student syllabifies. The skill scaffolds the procedure: count,
  place, check.
- Vowels count syllables. Each vowel SOUND (not vowel letter) is one
  syllable nucleus. Diphthongs count as one. Silent letters don't count.
- MOP assigns intervocalic consonants. Push as many consonants into
  the following onset as legality permits. Then assign leftovers to
  the preceding coda.
- Phonotactics is the gatekeeper. *atlas* → *.at.las.* not *.a.tlas.*
  because */tl/* is not a legal English onset.
- SSP is the filter. Legal onsets rise in sonority from edge to nucleus.
  Legal codas fall in sonority from nucleus to edge. Use SSP to check
  borderline cases.
- Always work from the phonemic form, not spelling. *Psychology* is
  /saɪ.kɑ.lə.dʒi/ — four syllables, not five.

## Flow

### Step 1 — Convert spelling to phonemic form
Make sure the student is working with phonemic representation, not
spelling. /saɪˈkɑlədʒi/ for *psychology*, not the orthographic form.
Silent letters don't count.

### Step 2 — Count syllables (= count vowel nuclei)
The number of syllables equals the number of vowel sounds in the
phonemic form. Diphthongs count as one nucleus.

### Step 3 — Place intervocalic consonants by MOP
For each block of consonants between two vowels, push as many as
possible into the FOLLOWING syllable's onset. Remaining consonants
go to the preceding syllable's coda.

### Step 4 — Check phonotactic legality of onsets
For each proposed onset, verify it's a legal English onset:
- Single C: always legal
- CC: must rise in sonority (e.g., /pl/, /tr/, /sm/) AND be in the
  English-licensed list. */tl/, */dl/, */pw/, */mr/* are NOT legal
- CCC: must start with /s/, then voiceless stop, then sonorant
  (/spl, str, skr, spr/, etc.)
- If the proposed onset is illegal, move one consonant back to the
  previous coda.

### Step 5 — Verify with SSP
The Sonority Sequencing Principle: sonority rises from syllable edge
to nucleus, then falls. Walk through each syllable: does sonority
rise across the onset? Fall across the coda? If not, re-check.

## Safe Output Types
- Phonemic-conversion prompts ("what's the phonemic form? we don't
  syllabify spelling")
- Vowel-counting prompts ("how many vowel SOUNDS are in /aluminum/?")
- MOP application prompts ("between these two vowels, how many
  consonants are there? Try pushing all of them into the next onset
  first.")
- Legality-check prompts ("is /tl/ a legal English onset? When did
  you last see a word starting with /tl/?")
- SSP verification prompts ("walk through the sonority of this onset
  — does it rise from edge to nucleus?")
- Acknowledgments and corrections
- Redirects when spelling and pronunciation diverge

## Must Avoid
- Syllabifying for the student
- Counting orthographic vowels instead of phonemic vowels (silent
  letters trap)
- Letting MOP override phonotactic legality
- Skipping the legality check (it's the difference between a 50% and
  a 100% answer)
- Treating diphthongs as two syllables
- Letting spelling-induced syllabification stand (e.g., *fa-ther*
  vs phonemically /fɑ.ðɚ/)
- Continuing syllabification scaffolding when the student doesn't know
  what a syllable is (return to `validate-prereqs`)

## Example Exchange
> **Student:** How do I syllabify *aluminum*?
>
> **Tutor:** Let's start with the phonemic form. How is *aluminum*
> pronounced?
>
> **Student:** /əˈluːmɪnəm/.
>
> **Tutor:** Good. Now count the vowel sounds — that's the number of
> syllables.
>
> **Student:** /ə/, /uː/, /ɪ/, /ə/. Four.
>
> **Tutor:** Right, four syllables. Now place the consonants between
> vowels using MOP. Between /ə/ and /uː/, what consonant is there?
>
> **Student:** /l/.
>
> **Tutor:** One consonant — push it into the following onset. So we
> have /ə.luː/ so far. Between /uː/ and /ɪ/?
>
> **Student:** /m/.
>
> **Tutor:** Push /m/ to the next onset: /ə.luː.mɪ/. Between /ɪ/ and
> the final /ə/?
>
> **Student:** /n/.
>
> **Tutor:** Same — push to next onset: /ə.luː.mɪ.nəm/.
>
> **Student:** Wait, where did the last /m/ go?
>
> **Tutor:** It's the coda of the last syllable — there's no following
> vowel for it to be the onset of, so it must be the coda. Final
> answer: /ə.luː.mɪ.nəm/. Now check phonotactic legality. Are /l/, /m/,
> /n/ all legal English onsets?
>
> **Student:** Yeah, all single consonants are legal.
>
> **Tutor:** Right. Done.

## Disambiguation from Other Skills
- `id-natural-class` identifies feature-based groups of sounds. **This
  skill** divides words into syllables — different operation.
- `analyze-dist` does distributional analysis. **This skill** is about
  syllable structure, not phonemic status.
- `apply-phon-rule` derives surface forms from URs. **This skill** is
  about syllable boundaries within a single form.
- `validate-prereqs` covers basic syllable structure (onset, nucleus,
  coda definitions, sonority hierarchy). **This skill** assumes those
  are known and helps apply MOP and SSP.
- `repair-miscon` fires on misconceptions like "syllabification follows
  spelling" or "MOP always wins over phonotactics." **This skill**
  scaffolds the procedure; pair with repair-miscon when the conceptual
  model is wrong.

## Inputs Expected by logic.py
- `word_phonemic` (str, optional): the phonemic form, e.g.
  `"/əˈluːmɪnəm/"`
- `word_orthographic` (str, optional): the spelled form for reference
- `current_step` (int, optional): which step the student is on. 0 or
  absent defaults to Step 1.
- `proposed_syllabification` (str, optional): the student's attempt
  for verification feedback

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `mop` (dict): Maximum Onset Principle definition + procedure
- `english_onsets` (dict): legal English onsets categorized by length
  and structure
- `english_codas` (dict): legal English codas
- `sonority_hierarchy` (list): the standard sonority ranking
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `example_syllabifications` (list): worked examples of varying
  difficulty
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill targets HW5 Q16 (8 points) directly. Syllabification also
appears as a sub-task in some allomorph-conditioning rules in HW5
(e.g., when stress-related allomorphs depend on syllable structure).

The English onsets/codas catalogs are rule-based but include the most
common edge cases. /tl/ and /dl/ are particularly tricky — students
think they're legal because of words like *atlas* and *paddle*, but
those words are syllabified */æt.ləs/* and */pæ.dl̩/* (or
*/pæd.l̩/*) precisely BECAUSE the cluster doesn't form a legal onset.

The example syllabifications include the HW5 problem set words:
*pumpkin, atlas, constraint, athletic, photograph, restaurant,
distract, monstrous*. Each shows the MOP + legality interaction.
