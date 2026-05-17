---
skill_id: "read-waveform"
name: "Read Waveform"
skill_type: "instructional"
stance: "socratic"
tags: ["phonetics", "acoustics", "waveform", "segment-boundaries", "vot", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "identify-evidence"
  - "interpret-evidence"
  - "decompose-arguments"
trigger_signals:
  - "student-cant-mark-segment-boundary"
  - "student-asks-where-segment-starts"
  - "student-confuses-stop-phases"
  - "student-cant-locate-vot"
  - "wrong-answer-misreads-amplitude-as-segment-edge"
  - "student-asks-how-to-read-waveform"
  - "student-cant-tell-voiced-from-voiceless-on-waveform"
chip_icon: "〰️"
version: "0.1.0"
python_entry: "logic.py"
---

# Read Waveform

## Description
Scaffolds reading a waveform (amplitude over time) — locating segment
boundaries, identifying voiced vs voiceless regions by periodicity,
recognizing the three-phase anatomy of stop consonants (closure → burst
→ release/aspiration), and measuring VOT. Targets HW3 Q18 specifically
(14 sub-questions, weighted at 14 points), plus midterm 1 acoustic
description questions. Stateless — the orchestrator tracks which task
the student is on (segmentation, VOT measurement, voicing identification).

## When to Trigger

### Fires when:
- Student is asked to mark segment boundaries on a waveform
- Student asks "where does this segment start/end?"
- Student can't distinguish closure from release on a stop
- Student needs to locate VOT or measure it
- Wrong answer treats amplitude changes as segment boundaries without
  considering segment type
- Student can't tell voiced from voiceless regions visually
- Student asks "how do I read this waveform?"

### Does NOT fire when:
- Student is reading a spectrogram (use `read-spectrogram`)
- Student is reading a spectral slice (use `interpret-spectrum`)
- Student is on a transcription question without a waveform image
  (HW1/HW2)
- Student is doing distributional analysis (use `analyze-dist`)

### Boundary cases:
- **Two waveforms shown for comparison**: walk through each separately,
  then ask the student to compare. Don't try to read both simultaneously.
- **Word/phrase-level segmentation**: at the level of fluent speech,
  word boundaries are perceptual not acoustic — there's no clear visual
  cue between most consecutive words. Students who try to mark word
  boundaries on a waveform often get confused. Redirect: "you're
  marking segment boundaries, not word boundaries — they're different."
- **Sonorant-vowel transitions**: approximants and nasals blur into
  adjacent vowels in the waveform. The skill scaffolds finding the
  best edge but acknowledges that some boundaries are inherently fuzzy.

## Tutor Stance
- The student finds the boundary. The skill scaffolds the visual cues:
  what to look for, what to ignore.
- Type of segment dictates the cue. A stop has a silent closure phase;
  a fricative has aperiodic noise; a vowel has periodic high-amplitude
  oscillation. Match the cue to the segment type.
- Periodicity = voicing. A periodic (regular wave-cycle pattern)
  region indicates vocal fold vibration. An aperiodic region is
  voiceless (or a non-sonorous gap).
- Stops have three phases. Closure (silence) → burst (vertical spike)
  → aspiration (aperiodic noise, may or may not be present). The
  segment "starts" at the closure onset and "ends" at the next
  segment's onset.
- Don't confuse amplitude changes with segment boundaries. A loud-to-quiet
  transition within a vowel is NOT a segment boundary. The boundary
  is where the segment TYPE changes.

## Flow

### Step 1 — Identify axes
Confirm the student knows: x-axis is time (left to right), y-axis is
amplitude (positive and negative around zero). Each cycle of the
waveform is one period of vocal fold vibration if periodic.

### Step 2 — Identify the segment type at each region
Walk through the waveform region by region. At each region, ask:
- Periodic, high amplitude → vowel
- Periodic, lower amplitude → sonorant consonant (nasal, liquid, glide)
- Aperiodic noise → voiceless fricative (or stop release/aspiration)
- Silence (no amplitude) → stop closure
- Periodic + aperiodic → voiced fricative

### Step 3 — Locate stop phases
For stops specifically, identify:
- Closure: a silent gap (or near-silent, depending on voicing)
- Burst: a sudden vertical spike at the moment of release
- Aspiration: aperiodic noise after the burst, before voicing
  resumes (only for aspirated stops)

### Step 4 — Mark segment boundaries
The boundary between two segments is where the visual cue changes.
- Vowel → stop: where the periodic pattern stops and silence/closure begins
- Stop → vowel: where the burst happens, OR where periodic vowel
  amplitude resumes (depends on aspiration)
- Vowel → fricative: where periodic pattern transitions to aperiodic
  noise
- Sonorant → vowel: amplitude increases; periodicity continues. This
  edge is fuzzy.

### Step 5 — Measure VOT (if asked)
For VOT specifically:
- Find the burst (vertical spike)
- Find the start of vowel voicing (where regular periodic cycles
  resume)
- Measure the time interval between them
- Positive (long-lag) = aspirated voiceless
- Zero / short-lag = unaspirated (English voiced word-initial, OR
  voiceless after [s])
- Negative = prevoiced (rare in English word-initial; common
  intervocalically and in Spanish)

## Safe Output Types
- Axis-identification prompts ("what's on the x-axis here? the y-axis?")
- Region-classification prompts ("at this point in the waveform, is the
  pattern periodic or aperiodic? high or low amplitude?")
- Phase-identification prompts for stops ("can you find the closure?
  the burst? any aspiration?")
- Boundary-marking prompts ("at what point does the pattern change
  from [type 1] to [type 2]?")
- VOT-measurement prompts ("where's the burst? where does voicing
  begin?")
- Acknowledgments when the student correctly identifies a feature
- Redirects when the student treats amplitude changes as boundaries

## Must Avoid
- Reading the waveform for the student
- Marking segment boundaries on behalf of the student
- Measuring VOT for the student
- Letting the student call any amplitude change a segment boundary
- Skipping the periodicity check when classifying a region
- Treating word boundaries as acoustic events on a waveform of fluent
  speech (they're perceptual, not visual)
- Continuing waveform-reading scaffolding when the student lacks the
  prerequisite acoustic vocabulary (return to `validate-prereqs`)
- Mixing waveform reading with spectrogram reading — they're different
  representations and require different mental models

## Example Exchange
> **Student:** I'm on HW3 Q18 and I need to mark where [s] ends and
> [t] begins in *stop*. The waveform shows [s] then [t] then a vowel.
> Where's the boundary?
>
> **Tutor:** Let's work through it visually. First, what does an [s]
> look like on a waveform — periodic or aperiodic? High or low
> amplitude?
>
> **Student:** Aperiodic, kind of medium amplitude — it's friction
> noise.
>
> **Tutor:** Right. And what does a [t] look like, specifically the
> closure phase before the release?
>
> **Student:** Silent? Like, no amplitude.
>
> **Tutor:** Exactly — closure is a silent gap. So the boundary
> between [s] and [t] is where the aperiodic noise of [s] stops and
> the silence of [t]'s closure begins. Look at the waveform: where
> does the medium-amplitude noise transition into a flat line?
>
> **Student:** I see a place around 0.4 seconds where the noise drops
> off and there's basically nothing.
>
> **Tutor:** That's your boundary. The end of [s] / start of [t]'s
> closure phase.

## Disambiguation from Other Skills
- `read-spectrogram` reads frequency over time with formants and
  consonant signatures. **This skill** reads amplitude over time —
  different visual representation, different cues.
- `interpret-spectrum` reads amplitude over frequency at one moment.
  **This skill** reads amplitude over time. Different axes.
- `analyze-dist` does distributional analysis on phonological data.
  **This skill** is about acoustic interpretation, not pattern analysis.
- `repair-miscon` fires on misconceptions like "voiceless fricatives
  have no waveform" or "amplitude changes are segment boundaries."
  **This skill** assumes the student understands the basic acoustic
  vocabulary.

## Inputs Expected by logic.py
- `waveform_image` (str, optional): reference to a waveform image being
  shown to the student
- `target_word` (str, optional): the word being analyzed (e.g.,
  "stop", "cat", "boy")
- `task` (str, optional): which task — "segmentation",
  "vot_measurement", "voicing_id", "stop_phases"
- `current_step` (int, optional): which step of the flow the student
  is on. 0 or absent defaults to Step 1.

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `segment_signatures` (dict): visual cues per segment type
- `vot_categories` (dict): VOT range definitions and English distribution
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill targets HW3 Q18 directly (14 sub-questions on segment
boundaries, weighted heaviest in HW3). It also covers VOT measurement
which appears on midterm 1 acoustic-description questions.

The segment_signatures catalog is the central reference. Each segment
type has distinct visual cues; the orchestrator can match the student's
target to the right cue when scaffolding.

For boundary-marking on fluent speech (phrases like *cats and dogs*),
some boundaries are inherently fuzzy. Don't force precision; the skill
explicitly acknowledges sonorant-vowel transitions can't be sharply
marked.
