---
skill_id: "interpret-spectrum"
name: "Interpret Spectrum"
skill_type: "instructional"
stance: "socratic"
tags: ["phonetics", "acoustics", "spectrum", "harmonics", "formants", "source-filter", "f0", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "identify-evidence"
  - "interpret-evidence"
  - "surface-assumptions"
trigger_signals:
  - "student-confuses-f0-and-f1"
  - "student-cant-find-f0-from-spectrum"
  - "student-confuses-harmonics-with-formants"
  - "student-cant-locate-formant-peaks"
  - "wrong-answer-conflates-source-and-filter"
  - "student-asks-how-to-find-f0"
  - "student-asks-difference-between-spectrum-and-spectrogram"
chip_icon: "〽️"
version: "0.1.0"
python_entry: "logic.py"
---

# Interpret Spectrum

## Description
Scaffolds reading a spectral slice (amplitude over frequency at one
moment in time) — finding F0 from the spacing of harmonics, locating
formant peaks (the spectral envelope's high points), and maintaining
the source-filter distinction (harmonics come from the source / vocal
folds; formants come from the filter / vocal tract shape). Targets
HW3 Q7-Q15 (the spectrum-reading sequence) and any source-filter
question on midterm 1. Stateless — the orchestrator tracks which
quantity the student is finding.

## When to Trigger

### Fires when:
- Student is given a spectral slice and asked to find F0 or formants
- Student confuses F0 with F1 (the two are completely different
  quantities at different scales)
- Student treats harmonic peaks as formants (or vice versa)
- Student can't locate formant peaks
- Wrong answer conflates source (vocal fold vibration) with filter
  (vocal tract shape)
- Student asks "how do I find F0 from this?"
- Student asks "what's the difference between a spectrum and a
  spectrogram?"

### Does NOT fire when:
- Student is reading a waveform (use `read-waveform`)
- Student is reading a spectrogram (use `read-spectrogram`)
- Student is on a transcription question without spectral data
- Student is doing distributional analysis (use `analyze-dist`)

### Boundary cases:
- **Speaker variation**: F0 is determined by speaker (typical female
  ~200 Hz, typical male ~120 Hz, typical child ~300 Hz). Formants are
  also speaker-dependent in absolute terms but follow more constrained
  patterns. Don't expect cross-speaker constancy.
- **F0 from harmonic spacing vs. directly visible**: F0 is the
  spacing between adjacent harmonics, not a single labeled peak. The
  lowest harmonic IS at F0, but reading harmonic SPACING is the more
  reliable method.
- **Formant tracking errors**: spectral analyzers sometimes mislabel
  formants. Cross-check by visual inspection — formants are SLOWLY
  varying envelope peaks, not narrow spikes.

## Tutor Stance
- The student reads the spectrum. The skill scaffolds: identify axes,
  find F0 by harmonic spacing, locate formant peaks.
- Source vs filter is the core distinction. The vocal folds (source)
  produce harmonics — the regular spikes evenly spaced. The vocal
  tract (filter) shapes them — the envelope smooths over them, with
  peaks at the formants.
- F0 is found from harmonic spacing, not from a single peak. Adjacent
  harmonics are separated by F0 (Hz), so 10 Hz spacing means F0 = 10 Hz.
- Formants are envelope peaks. They sit ON the harmonics, but they're
  the SHAPE of the spectrum, not individual harmonic peaks.
- F0 (~100-300 Hz) and F1 (~300-900 Hz) are at different scales. They
  are NOT the same quantity at different names. F0 is source pitch;
  F1 is the lowest filter resonance.

## Flow

### Step 1 — Identify axes
Confirm: x-axis is frequency (Hz), y-axis is amplitude (dB). The
spectrum is a vertical "slice" through one instant of a spectrogram.

### Step 2 — Identify the harmonic structure
Count the regularly spaced peaks (the "comb" of vertical lines). They
are harmonics — integer multiples of F0. Spacing tells you F0.

### Step 3 — Find F0 from harmonic spacing
Measure the spacing between adjacent harmonics. That spacing IS F0.
Example: harmonics at 100, 200, 300, 400 Hz → F0 = 100 Hz. The lowest
harmonic is at F0 (the fundamental).

### Step 4 — Identify formant peaks
The spectral ENVELOPE (the smooth curve over the harmonic spikes) has
peaks. These peaks are formants. Find the envelope's high points —
they don't have to land on any single harmonic.

### Step 5 — Map to vowel features
Apply formant-to-feature mappings: F1↔height (INVERSE), F2↔backness.
Use the values from Step 4. (Same mappings as `read-spectrogram`.)

## Safe Output Types
- Axis-identification prompts ("what's on the x-axis here? the y-axis?")
- Harmonic-counting prompts ("how many regularly spaced peaks do you
  see? at what frequencies?")
- Spacing-measurement prompts ("the harmonics are at 200, 400, 600 Hz
  — what's the spacing?")
- F0-derivation prompts ("the spacing IS F0 — what's the answer?")
- Envelope-finding prompts ("now ignore the individual peaks and look
  at the SHAPE of the curve — where are the bumps?")
- Source-vs-filter clarifications when the student conflates them
- Acknowledgments when the student locates F0 and formants correctly
- Redirects when the student treats F0 and F1 as the same thing

## Must Avoid
- Reading the spectrum for the student
- Naming F0 directly without walking through harmonic spacing
- Letting F0/F1 conflation slide
- Treating individual harmonic peaks as formants
- Skipping the source-filter distinction when the student conflates them
- Mixing spectrum reading with spectrogram reading (different
  representations, different cues)
- Continuing spectrum-reading scaffolding when the student doesn't
  understand the source-filter framework (return to `validate-prereqs`)

## Example Exchange
> **Student:** I have a spectrum from HW3 Q9 and the question asks for
> F0. I see peaks at 200, 400, 600, 800, 1000 Hz. What's F0?
>
> **Tutor:** Good — you have the harmonic series. F0 isn't any single
> peak; it's the SPACING between harmonics. What's the spacing?
>
> **Student:** 200 Hz between each.
>
> **Tutor:** That spacing IS F0. F0 = 200 Hz. The lowest harmonic is
> also at 200 Hz (the fundamental), but in general you read F0 from
> the spacing — more reliable when the lowest harmonic is faint or
> the spectrum doesn't start at 0 Hz.
>
> **Student:** OK. The next question asks for F1. F1 is just F0, right?
>
> **Tutor:** Big trap to avoid. F0 and F1 are completely different.
> F0 is the rate of vocal fold vibration (source — what we perceive as
> pitch). F1 is the lowest formant — a resonance of the vocal tract
> shape (filter). They're at different scales: F0 is around 200 Hz
> here; F1 is more like 300-900 Hz depending on the vowel.
>
> **Student:** So how do I find F1 on this spectrum?
>
> **Tutor:** Look at the SHAPE of the spectrum, not individual peaks.
> The harmonics are spikes, but the overall ENVELOPE — the curve
> connecting the high points — has bumps. Those bumps are formants.
> F1 is the lowest envelope bump.

## Disambiguation from Other Skills
- `read-spectrogram` reads frequency over time. **This skill** reads
  amplitude over frequency at one instant — a different representation.
  Use spectrogram for time-varying analysis; spectrum for steady-state
  spectral content.
- `read-waveform` reads amplitude over time. **This skill** reads
  amplitude over frequency. Different axes.
- `repair-miscon` fires on misconceptions like "F0 and F1 are the same"
  or "harmonics ARE formants." **This skill** assumes the source-filter
  framework is intact; pair with repair-miscon when the conceptual
  model is broken.
- `validate-prereqs` covers source-filter theory at a conceptual level.
  **This skill** assumes the student knows what source and filter are
  separately, and helps them apply that knowledge to a specific spectrum.

## Inputs Expected by logic.py
- `spectrum_image` (str, optional): reference to a spectrum image
- `target_quantity` (str, optional): "f0", "f1", "f2", "vowel_id"
- `harmonic_frequencies` (list of int, optional): frequencies of
  visible harmonic peaks
- `current_step` (int, optional): which step the student is on. 0 or
  absent defaults to Step 1.

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps
- `axes` (dict): spectrum axis conventions
- `source_filter` (dict): theoretical framework distinguishing source
  (harmonics, F0) from filter (formants, vocal tract resonances)
- `f0_ranges_hz` (dict): typical F0 ranges by speaker type
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill targets HW3 Q7-Q15 (spectrum-reading sequence) and
embedded source-filter questions on midterm 1. The single most-confused
distinction in the course is F0 vs F1 — students often think they're
the same quantity. Always reinforce the source-filter framework.

The harmonic spacing technique for F0 is more reliable than reading
the lowest harmonic directly, because spectra sometimes start above
0 Hz or the lowest harmonic can be faint. Teach the spacing method.

For multi-instant analysis, hand off to `read-spectrogram` (which is
literally a stack of spectra over time).
