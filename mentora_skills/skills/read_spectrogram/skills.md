---
skill_id: "read-spectrogram"
name: "Read Spectrogram"
skill_type: "instructional"
stance: "socratic"
tags: ["phonetics", "acoustics", "spectrogram", "formants", "transitions", "place-of-articulation", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "identify-evidence"
  - "interpret-evidence"
  - "decompose-arguments"
trigger_signals:
  - "student-cant-read-spectrogram"
  - "student-cant-locate-formants"
  - "wrong-answer-inverts-f1-height"
  - "student-asks-which-spectrogram-matches"
  - "student-cant-identify-place-from-transitions"
  - "student-asks-how-to-find-f1-f2"
  - "student-confuses-darkness-with-frequency"
chip_icon: "📊"
version: "0.1.0"
python_entry: "logic.py"
---

# Read Spectrogram

## Description
Scaffolds reading a spectrogram (frequency over time, with darkness
indicating amplitude) — locating formants F1 and F2, mapping them to
vowel features (F1↔height, F2↔backness, both INVERSE for height),
identifying consonant signatures (stops, fricatives, nasals,
sonorants), and reading formant transitions for stop place of
articulation. Targets HW3 Q4-Q5 (axes/terminology), Q16
(spectrogram-to-phrase matching, 6 points, the highest-weighted HW3
question), and any spectrogram-based midterm 1 question. Stateless —
the orchestrator tracks which task the student is on.

## When to Trigger

### Fires when:
- Student is given a spectrogram and asked to identify what it shows
- Student asks "where's F1 / F2?"
- Student inverts F1↔height (says "high vowels have high F1")
- Student is matching spectrograms to phrases (HW3 Q16 task)
- Student can't identify consonant place from formant transitions
- Wrong answer reads spectrogram axes incorrectly (darkness as
  frequency, etc.)
- Student needs help locating consonant signatures (stops,
  fricatives, nasals)

### Does NOT fire when:
- Student is reading a waveform (use `read-waveform`)
- Student is reading a spectral slice (use `interpret-spectrum`)
- Student is on a transcription question without a spectrogram image
  (HW1/HW2)
- Student is doing distributional analysis (use `analyze-dist`)

### Boundary cases:
- **Multiple spectrograms shown for matching**: walk through each one
  separately to identify features (vowels, consonants, transitions),
  then ask the student to match to phrases by feature density and
  pattern.
- **Cross-speaker comparisons**: different speakers produce different
  absolute formant values for "the same" vowel. Compare within-speaker
  patterns or formant-relative-to-formant ratios, not absolute Hz
  values.
- **Praat formant tracker overlay**: if the student is in Praat with
  the formant tracker on, warn that the tracker can mislabel —
  always cross-check by visual inspection.

## Tutor Stance
- The student reads the spectrogram. The skill scaffolds: identify
  axes, locate formants, map to features.
- F1 ↔ height (INVERSE: high vowel = LOW F1). F2 ↔ backness (front
  vowel = HIGH F2). The inverse direction for F1 is the most-confused
  mapping in the course.
- Count formants from the bottom up. F1 is the lowest, then F2, F3, etc.
- Darkness = amplitude. Frequency is on the y-axis. Darkness shows how
  much energy is at that frequency at that time.
- For consonant place, read the FORMANT TRANSITIONS of the adjacent
  vowel, not the consonant itself. Counterintuitive but essential.
- Identify segment categories before specific sounds. "This is a
  stop" before "this is /p/." Most HW3 questions only require category
  identification.

## Flow

### Step 1 — Identify axes
Confirm: x-axis is time (seconds), y-axis is frequency (Hz, low at
bottom and high at top), darkness = amplitude (intensity at that
frequency at that time).

### Step 2 — Locate formants
For vowel regions, identify the dark horizontal bands. The lowest is
F1, then F2, then F3. Count from the bottom. F1 is usually below
1000 Hz; F2 is between F1 and ~3000 Hz.

### Step 3 — Map formants to vowel features
F1 ↔ height (INVERSE: low F1 = high vowel; high F1 = low vowel). F2
↔ backness (high F2 = front vowel; low F2 = back vowel). Apply the
inverse for height carefully — it's the most-confused mapping.

### Step 4 — Identify consonant signatures
- Stops: silence in the closure, vertical spike at burst, possibly
  aspiration noise after
- Fricatives: random aperiodic noise, varying frequency concentration
  by place ([s, z]: high-frequency 5000-6000 Hz; [ʃ, ʒ]: 2500 Hz;
  [f, v, θ, ð]: diffuse; [h]: tracks adjacent vowel formants)
- Nasals: abrupt amplitude drop at nasal onset; nasal formants ~200
  and ~2000 Hz
- Sonorants: vowel-like formants but lower amplitude; [l] has low F2;
  [ɹ] has very low F3 (the diagnostic for English r); [w], [j] like
  [u] and [i]

### Step 5 — Read formant transitions for stop place of articulation
For stops, the place is read from the ADJACENT VOWEL'S formant
transitions:
- Labial (/p, b, m/): all formant edges point DOWN going into the
  consonant (closure lowers all resonances)
- Alveolar (/t, d, n/): F2 points UP toward ~1700 Hz (the alveolar
  locus)
- Velar (/k, g, ŋ/): F2 and F3 converge ('velar pinch')

## Safe Output Types
- Axis-identification prompts ("what's on the y-axis? what does
  darkness represent?")
- Formant-locating prompts ("can you find the lowest dark band? that's
  F1. What's above it?")
- Feature-mapping prompts ("F1 is at about 700 Hz here — high or low?
  And what does that tell you about vowel height?")
- Consonant-category prompts ("at this region, do you see silence?
  noise? formant patterns?")
- Place-from-transition prompts ("look at how F2 moves into the
  consonant — does it go up, down, or pinch with F3?")
- Acknowledgments and corrections of inversion errors
- Transitions to `interpret-spectrum` if the student wants to verify
  formant values via spectral slice

## Must Avoid
- Reading the spectrogram for the student
- Naming the vowel before walking through F1 and F2
- Letting F1↔backness or F1↔height-direct stand without correction
- Reading consonant place from the consonant itself instead of from
  formant transitions
- Treating absolute formant Hz values as cross-speaker constants
- Mixing waveform and spectrogram reading (different representations)
- Reading darkness as frequency or vice versa
- Continuing spectrogram scaffolding when the student lacks vocabulary
  (return to `validate-prereqs`)

## Example Exchange
> **Student:** I'm looking at a spectrogram of a vowel. There's a dark
> band around 300 Hz and another around 2200 Hz. What vowel is this?
>
> **Tutor:** Let's work through it. First, those two bands — which is
> F1 and which is F2?
>
> **Student:** F1 is the lower one, so 300 Hz. F2 is 2200 Hz.
>
> **Tutor:** Right. Now, what does F1 of 300 Hz tell you about height?
>
> **Student:** Low F1 means... low vowel?
>
> **Tutor:** Careful — F1↔height is INVERSE. Low F1 means HIGH vowel
> (small mouth opening, larger pharynx). High F1 means LOW vowel.
>
> **Student:** So 300 Hz F1 = high vowel.
>
> **Tutor:** Right. And F2 of 2200 Hz?
>
> **Student:** High F2 = front vowel?
>
> **Tutor:** Right. So you have a high front vowel. What two English
> vowels are high front?
>
> **Student:** [i] and [ɪ].
>
> **Tutor:** Right. F1 of 300 Hz is at the lower end of the high range,
> which fits [i] (which is the higher of the two). [ɪ] would have
> slightly higher F1 (because it's slightly less high). So this is
> probably [i].

## Disambiguation from Other Skills
- `read-waveform` reads amplitude over time. **This skill** reads
  frequency over time. Different axes, different cues.
- `interpret-spectrum` reads amplitude over frequency at one moment
  (a vertical slice). **This skill** reads time-varying frequency
  patterns.
- `id-natural-class` identifies natural classes of sounds. **This
  skill** reads acoustic data; doesn't classify abstract groups.
- `repair-miscon` fires on misconceptions like "F1 is backness" or
  "high vowels have high F1." **This skill** assumes the student has
  the correct mappings or refers to repair-miscon to fix them.

## Inputs Expected by logic.py
- `spectrogram_image` (str, optional): reference to the spectrogram
  being shown
- `target_word_or_phrase` (str, optional): what the spectrogram is of
- `task` (str, optional): "vowel_id", "consonant_id", "phrase_match",
  "place_from_transition"
- `current_step` (int, optional): which step the student is on. 0 or
  absent defaults to Step 1.

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps
- `axes` (dict): spectrogram axis conventions
- `formant_to_feature` (dict): F1↔height inverse, F2↔backness mappings
- `consonant_signatures` (dict): visual cues per consonant category
- `formant_transitions_by_place` (dict): place diagnostics
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill is the heaviest acoustic-interpretation skill — HW3 Q16
alone is 6 points (highest single question in HW3). Spectrogram
reading shows up on midterm 1 too.

The F1↔height INVERSE is the single most-confused mapping in the
course. Students inherit the wrong mnemonic ("high vowel, high F1")
and the inverse direction needs deliberate repair. Pair with
repair-miscon when the student persists in the wrong direction.

The formant transitions catalog is the central reference for
consonant place. Many students don't know that consonant place is read
from the adjacent vowel's transitions; teaching this explicitly is a
core function of the skill.
