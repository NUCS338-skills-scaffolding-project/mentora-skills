---
skill_id: "id-natural-class"
name: "Identify Natural Class"
skill_type: "instructional"
stance: "socratic"
tags: ["phonology", "phonetics", "natural-class", "features", "methodology", "ling250"]
course_types: ["humanities"]
learning_goal_tags:
  - "interpret-evidence"
  - "surface-assumptions"
  - "decompose-arguments"
trigger_signals:
  - "student-asks-what-features-unite-set"
  - "student-picks-too-broad-class"
  - "student-cant-name-shared-feature"
  - "wrong-answer-uses-non-exhaustive-class"
  - "student-confuses-natural-class-with-arbitrary-list"
  - "student-asks-if-set-is-natural-class"
  - "student-cant-describe-class-with-features"
chip_icon: "🎯"
version: "0.1.0"
python_entry: "logic.py"
---

# Identify Natural Class

## Description
Scaffolds identifying the **narrowest exhaustive natural class** of a
set of sounds — the smallest feature-defined group that includes every
sound in the set AND excludes every sound that's not in the set. A
natural class isn't just "sounds that share a feature"; it's "sounds
that share a feature, and ALL sounds with that feature are in the set."
The skill guides the student through listing the sounds, identifying
shared features (place, manner, voicing for consonants; height, backness,
rounding, tense for vowels), and testing exhaustiveness. Used by HW4
rule writing and HW5 Part B (Maltese coronals). Stateless — the
orchestrator tracks the current step.

## When to Trigger

### Fires when:
- Student is given a set of sounds and asked to name the natural class
  uniting them
- Student writes a phonological rule whose environment is a list of
  segments where a feature-class would be more accurate
- Student picks a class that includes the targets but is too broad
  (e.g., "sonorants" when the data is just coronals)
- Student claims a set IS a natural class without demonstrating the
  feature relationship
- Student claims a set is NOT a natural class without checking all
  features
- Wrong answer reveals a non-exhaustive class (covers the targets but
  also covers other sounds that aren't in the data)

### Does NOT fire when:
- Student is doing distributional analysis (use `analyze-dist`)
- Student is constructing a rule but already knows the natural class
  (use `write-phon-rule`)
- Student is contrasting two sounds (use `contrastive-hint`)
- Student is on a transcription question (HW1/HW2)

### Boundary cases:
- **Multiple valid natural classes**: a set can sometimes be described
  by more than one class. The narrowest exhaustive one is the right
  answer. E.g., {p, t, k} can be "voiceless stops" (narrowest) or
  "voiceless obstruents" (too broad — includes voiceless fricatives).
- **Sounds that aren't a natural class**: not every set is a natural
  class. {p, l, w} share no exhaustive feature description. The skill
  scaffolds the testing; the answer can legitimately be "this isn't a
  natural class."
- **Vowels vs consonants**: the feature dimensions are different
  (height/backness/rounding for vowels; place/manner/voicing for
  consonants). Make sure the student knows which inventory they're
  working with.

## Tutor Stance
- The student identifies the class. The skill scaffolds the procedure:
  list, find shared features, test exhaustiveness.
- Narrowness matters. The right answer is the smallest exhaustive class.
  Don't accept "voiced sounds" when "voiced stops" is available.
- Exhaustiveness matters more. A class that includes the targets but
  also includes sounds NOT in the data is wrong, no matter how narrow
  it sounds.
- The exhaustiveness test is the key move: "is there any sound in the
  language that has these features but isn't in your data? If yes,
  your class is too broad."
- A natural class must (1) share features and (2) exhaust the
  language's sounds with those features. Both conditions are required.

## Flow

### Step 1 — List the sounds
Have the student write out the sounds in the set explicitly. This is
basic but essential — students sometimes try to identify a class without
fully recording what's in it.

### Step 2 — Identify shared features
Walk through feature dimensions one at a time. For consonants: place,
manner, voicing. For vowels: height, backness, rounding, tense/lax. At
each dimension, ask: "Are all the sounds in the set the same on this
feature? If yes, what value?"

### Step 3 — Compose the candidate class description
Combine the shared features into a class description. Examples:
- All voiceless + all stops → "voiceless stops"
- All coronal → "coronals"
- All high + all front → "high front vowels"
- All back + all rounded → "back rounded vowels"

### Step 4 — Test exhaustiveness
The critical step. Ask: "Are there any sounds in the language that
share these features but are NOT in your set?" If yes, the class is
too broad — back to Step 2 to find a narrower description. If no, the
class is exhaustive and you're done.

### Step 5 — Confirm narrowness
If multiple feature combinations describe the set exhaustively, pick
the narrowest one. Wider features are less informative. Example: if
{m, n, ŋ} could be "nasals" OR "voiced sounds," "nasals" wins because
it's tighter.

## Safe Output Types
- Listing prompts ("write out the sounds you're trying to classify")
- Feature-dimension prompts ("are they all the same on voicing? on
  place?")
- Composition prompts ("so they share [feature1] and [feature2] — what
  do we call that class?")
- Exhaustiveness-test prompts ("any other sounds in the language that
  share these features?")
- Narrowness checks ("is there a tighter description?")
- Acknowledgments when the class is correct
- Redirects when the class is too broad or non-exhaustive

## Must Avoid
- Naming the natural class for the student
- Accepting "they share a feature" without checking exhaustiveness
- Letting "voiced consonants" or "obstruents" stand when a tighter
  class is available
- Treating any list of sounds as a natural class without the feature
  test
- Skipping the exhaustiveness check on what looks like an obvious case
- Continuing the natural-class scaffolding when the student is
  fundamentally unclear on feature systems (return to `validate-prereqs`
  for IPA features)

## Example Exchange
> **Student:** For HW5 question 11, the sounds in Part B are /t, d, s,
> n/. What's the natural class?
>
> **Tutor:** Let's find out. First, write them out and walk through
> the feature dimensions. For consonants, the dimensions are place,
> manner, and voicing. Start with place — what's the place of /t/?
>
> **Student:** Alveolar.
>
> **Tutor:** /d/?
>
> **Student:** Alveolar.
>
> **Tutor:** /s/? /n/?
>
> **Student:** Both alveolar.
>
> **Tutor:** Great — they all share place. What about manner?
>
> **Student:** /t/ and /d/ are stops, /s/ is a fricative, /n/ is a
> nasal. Different.
>
> **Tutor:** So manner doesn't unite them. What about voicing?
>
> **Student:** /t/ and /s/ are voiceless, /d/ and /n/ are voiced.
> Mixed.
>
> **Tutor:** So voicing doesn't unite them either. The only feature
> they share is place — alveolar. So the candidate is "alveolars."
> Now test exhaustiveness: are there any other alveolars in English?
>
> **Student:** [l]?
>
> **Tutor:** Right. /l/ is alveolar but it's not in your set. So
> "alveolar" is too broad. What's narrower? Look at /t, d, s, n/ vs
> /l/ — what feature does /l/ have that the others don't?
>
> **Student:** /l/ is a lateral approximant.
>
> **Tutor:** Right. What's the broader feature for the others —
> coronal, alveolar minus the lateral approximants?
>
> **Student:** ... I'm not sure.
>
> **Tutor:** Try this: in the consonant chart, /t, d, s, n/ all sit on
> the alveolar column. What grouping covers them but excludes /l/ and
> the post-alveolars? Hint — coronal is the place class, and there's
> a feature that distinguishes lateral from non-lateral.
>
> **Student:** Coronals — but non-lateral?
>
> **Tutor:** Right. The narrowest exhaustive class for /t, d, s, n/ in
> English is "coronals" (some textbooks use "central coronals" or just
> "coronals" since lateral is a separate feature). For the LING 250
> intent, "coronals" is the expected answer.

## Disambiguation from Other Skills
- `analyze-dist` runs full distributional analysis. **This skill** is
  one operation that may be called inside that flow when the
  conditioning environment needs class-naming.
- `write-phon-rule` formalizes a rule. **This skill** identifies the
  class for the rule's environment. They chain — the user typically
  calls this skill while writing a rule.
- `contrastive-hint` distinguishes two specific sounds by feature.
  **This skill** finds shared features across a set of sounds.
- `repair-miscon` fires on misconceptions like "wider class is always
  better" or "any list of sounds is a natural class." **This skill**
  scaffolds the methodology; pair with repair-miscon when the student
  has the wrong belief.
- `validate-prereqs` covers IPA feature recall. **This skill** assumes
  the student knows feature dimensions; if they don't, hand off.

## Inputs Expected by logic.py
- `sounds` (list of str, optional): the IPA symbols in the set, e.g.
  `["t", "d", "s", "n"]`
- `inventory_type` (str, optional): "consonants" or "vowels", determines
  which feature dimensions to check
- `current_step` (int, optional): which step the student is on (1-5).
  0 or absent defaults to Step 1.
- `proposed_class` (str, optional): the student's candidate class label,
  used for exhaustiveness testing

## Outputs Returned by logic.py
A dict:
- `flow` (list): the 5 flow steps with tutor prompts
- `feature_dimensions` (dict): the feature dimensions for consonants
  and vowels
- `hint_ladders` (dict): per-step hint progressions
- `common_errors` (list): cataloged error patterns with redirects
- `example_classes` (list): canonical natural-class identifications
  with full reasoning
- `tutor_reminders` (list): high-priority stance reminders

## Notes for Reusers
This skill is the heart of HW5 Part B (Maltese coronal assimilation,
Q11) and embedded in many HW4 rule-writing questions. It also surfaces
in HW2 Q1-Q6 (multi-select feature identification — "find all the high
vowels") which is functionally a natural-class identification task at
the segment-list level.

The exhaustiveness test is the move students miss most often. Spend
time there. A common failure pattern: student picks a feature that's
correct for the set but is also true of other sounds in the language —
"too broad."

The example_classes catalog shows working through cases of varying
difficulty — from the obvious (high front vowels) to the nuanced
(coronals minus laterals).
