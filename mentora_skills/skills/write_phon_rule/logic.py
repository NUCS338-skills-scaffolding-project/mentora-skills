"""
write-phon-rule / logic.py

Catalog data + run() entry point for the Write Phonological Rule skill.

Scaffolds writing an alternation in formal /A/ → [B] / X __ Y notation,
with focus on natural-class generalization in the environment and
proper slashes/brackets discipline.
"""

# ──────────────────────────────────────────────────────────────────────
# Flow steps
# ──────────────────────────────────────────────────────────────────────

FLOW_STEPS = [
    {
        "step": 1,
        "name": "Identify the target",
        "tutor_prompt": "What sound is changing in this alternation? What's "
                        "the underlying form being transformed?",
        "advance_when": "student names the target with /slash/ notation",
    },
    {
        "step": 2,
        "name": "Identify the result",
        "tutor_prompt": "What does the target turn into on the surface?",
        "advance_when": "student names the result with [bracket] notation",
    },
    {
        "step": 3,
        "name": "Identify the environment",
        "tutor_prompt": "In every form where the change happens, what's to "
                        "the left of the target? What's to the right?",
        "advance_when": "student lists left and right contexts from the data",
    },
    {
        "step": 4,
        "name": "Generalize using natural classes",
        "tutor_prompt": "Look at the contexts you just listed. What do they "
                        "have in common? Can we describe them with a single "
                        "feature or class?",
        "advance_when": "student states a natural-class generalization",
    },
    {
        "step": 5,
        "name": "Notation check + verification",
        "tutor_prompt": "Now write the full rule using /A/ → [B] / X __ Y "
                        "format. Then verify: does your rule derive every "
                        "surface form in the data? Does it produce any forms "
                        "NOT in the data?",
        "advance_when": "rule is verified against the dataset",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Notation reference
# ──────────────────────────────────────────────────────────────────────

NOTATION_REFERENCE = {
    "target_form": {
        "notation": "/X/",
        "meaning":  "Underlying / phonemic representation",
    },
    "result_form": {
        "notation": "[X]",
        "meaning":  "Surface / phonetic representation",
    },
    "environment_position": {
        "notation": "__",
        "meaning":  "Where the target sits in the environment",
    },
    "word_boundary": {
        "notation": "#",
        "meaning":  "Word boundary (initial: # __; final: __ #)",
    },
    "natural_class_features": {
        "notation": "[+feature]",
        "meaning":  "Feature-based class (e.g., [+voice], [+nasal])",
    },
    "shorthand_classes": {
        "V":  "any vowel",
        "C":  "any consonant",
        "N":  "any nasal",
        "G":  "any glide",
        "L":  "any liquid",
    },
    "null": {
        "notation": "Ø",
        "meaning":  "Empty / nothing (used in epenthesis Ø → X / __ Y or deletion X → Ø / __ Y)",
    },
    "common_environments": [
        ("V __ V",         "intervocalic"),
        ("__ #",           "word-final"),
        ("# __",           "word-initial"),
        ("[+voice] __",    "after voiced"),
        ("[+nasal] __",    "after nasal"),
        ("__ [-voice]",    "before voiceless"),
        ("[+sibilant] __", "after sibilant"),
        ("σ[ __",          "syllable-onset"),
        ("__ ]σ",          "syllable-coda"),
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Hint ladders per step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "identify_target": [
        "What sound appears in the underlying forms but changes on the surface?",
        "Look at the alternation: which form is the 'starting point' that gets "
        "transformed? That's the target.",
        "The target uses /slash/ notation because it's underlying. So if /b/ "
        "becomes [β], your target is /b/.",
    ],
    "identify_result": [
        "When the target sound shows up on the surface in the conditioning "
        "context, what does it look like?",
        "Surface forms always use [bracket] notation, not /slash/. The result "
        "of the rule is the surface variant.",
        "Spanish: /b/ becomes [β] between vowels. The result is [β].",
    ],
    "identify_environment": [
        "In your data, list every word where the target changes. For each one, "
        "what's the sound directly before the target? What's the sound directly "
        "after?",
        "Do you see a pattern? Are the sounds-before all similar? Are the "
        "sounds-after all similar?",
        "Word boundaries count too — if the target is at the start of a word, "
        "the left context is # (word boundary).",
    ],
    "generalize_with_features": [
        "List the specific sounds in the environment. Now: what feature do "
        "they share?",
        "If your environment is /a/, /e/, /i/, /o/, /u/ — what's the natural "
        "class? Vowels, abbreviated as V.",
        "If it's /m/, /n/, /ŋ/ — that's the nasal class, [+nasal] or N. The "
        "rule should use the class label, not the segment list.",
    ],
    "notation_check": [
        "Walk through your rule. Are the target and result using the right "
        "slash/bracket conventions? /target/ → [result]?",
        "Does the environment use __ to mark the position of the target?",
        "Test the rule against every form in the data. Does it derive every "
        "surface form? Does it overproduce (yield forms NOT in the data)?",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Common errors
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "WR1",
        "trigger_phrases": ["/[b,d,g]/ →", "/{b,d,g}/", "the rule is for b, d, and g"],
        "description": "Listing segments where natural class features should be used",
        "redirect": "Your rule lists [b, d, g] but those three sounds share a "
                    "feature. What is it? Use that class label instead of the list.",
    },
    {
        "id": "WR2",
        "trigger_phrases": ["/[X]/", "[X] →", "→ /Y/"],
        "description": "Mixing slashes and brackets for target and result",
        "redirect": "Slashes /X/ are underlying, brackets [X] are surface. "
                    "What's underlying in your rule? What's surface? Each gets "
                    "its own notation.",
    },
    {
        "id": "WR3",
        "trigger_phrases": ["the rule is about how X sounds", 
                            "the rule describes the articulation"],
        "description": "Treating rules as physical descriptions",
        "redirect": "Phonological rules are abstract symbolic mappings between "
                    "underlying and surface forms. They look like physical "
                    "events but operate on representations.",
    },
    {
        "id": "WR4",
        "trigger_phrases": ["/X/ → [Y] / [+voice] [+voice] __",
                            "the environment is too specific"],
        "description": "Environment too narrow — misses cases the rule should cover",
        "redirect": "Test your rule against every form. Are there surface forms "
                    "with [Y] that your rule doesn't derive? If so, the "
                    "environment is too specific.",
    },
    {
        "id": "WR5",
        "trigger_phrases": ["the wider class is always better",
                            "i'll just use [+sonorant]"],
        "description": "Environment too broad — overgenerates surface forms",
        "redirect": "Is there any sound in [+sonorant] that does NOT trigger "
                    "the rule in your data? If so, the class is too wide. "
                    "Narrow it to the smallest exhaustive class.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Example rules from instructor materials
# ──────────────────────────────────────────────────────────────────────

EXAMPLE_RULES = [
    {
        "language": "Spanish",
        "rule": "/b/ → [β] / V __ V",
        "description": "Voiced stop lenition between vowels",
        "process": "lenition",
    },
    {
        "language": "English",
        "rule": "V → [+nasal] / __ [+nasal]",
        "description": "Vowel nasalization before nasal consonants",
        "process": "assimilation (manner)",
    },
    {
        "language": "English",
        "rule": "/-z/ → [-s] / [-voice] __",
        "description": "Plural suffix devoicing after voiceless consonants",
        "process": "voicing assimilation",
    },
    {
        "language": "English",
        "rule": "Ø → [ə] / [+sibilant] __ /-z/",
        "description": "Plural epenthesis after sibilants",
        "process": "epenthesis",
    },
    {
        "language": "Swampy Cree",
        "rule": "/p/ → [b] / V __ V",
        "description": "Stop voicing between vowels",
        "process": "lenition (parallel to Spanish)",
    },
    {
        "language": "Hungarian",
        "rule": "/[+obs]/ → [α voice] / __ [α voice +obs]",
        "description": "Obstruent voicing assimilation",
        "process": "voicing assimilation",
    },
    {
        "language": "Korean",
        "rule": "/l/ → [r] / __ V",
        "description": "Lateral becomes flap before vowel (in onset)",
        "process": "positional alternation (syllable-conditioned)",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Tutor reminders
# ──────────────────────────────────────────────────────────────────────

TUTOR_REMINDERS = [
    "The student writes the rule. Scaffold the parts; don't write the rule.",
    "Notation discipline: /X/ for underlying, [X] for surface. Always.",
    "Natural classes, not segment lists. Always ask 'what feature unites these?'",
    "Narrowest exhaustive class for the environment. Too broad overgenerates.",
    "Verify against the data: does the rule cover every relevant form? Does it "
    "produce forms not in the data?",
    "If the student is fundamentally unsure what's changing, return to analyze-dist.",
]


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """Orchestrator entry point. Returns structured guidance."""
    return {
        "skill_id": "write-phon-rule",
        "skill_name": "Write Phonological Rule",
        "version": "0.1.0",
        "flow": FLOW_STEPS,
        "notation_reference": NOTATION_REFERENCE,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "example_rules": EXAMPLE_RULES,
        "tutor_reminders": TUTOR_REMINDERS,
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "write-phon-rule"
    assert len(result["flow"]) == 5
    assert "target_form" in result["notation_reference"]
    assert len(result["common_errors"]) >= 4
    assert len(result["example_rules"]) >= 5
    print("write-phon-rule/logic.py self-test passed.")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['notation_reference'])} notation reference categories")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
    print(f"  {len(result['example_rules'])} example rules")
