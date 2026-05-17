"""
id-natural-class / logic.py

Catalog data + run() entry point for the Identify Natural Class skill.

Scaffolds finding the narrowest exhaustive natural class of a set of
sounds, with emphasis on the exhaustiveness test.
"""

# ──────────────────────────────────────────────────────────────────────
# Flow steps
# ──────────────────────────────────────────────────────────────────────

FLOW_STEPS = [
    {
        "step": 1,
        "name": "List the sounds",
        "tutor_prompt": "Write out the sounds in the set explicitly. What's "
                        "in your set?",
        "advance_when": "student has the set written out",
    },
    {
        "step": 2,
        "name": "Identify shared features",
        "tutor_prompt": "Walk through feature dimensions one at a time. "
                        "For each, ask: are all the sounds in the set the "
                        "same on this feature?",
        "advance_when": "student has identified which features are shared",
    },
    {
        "step": 3,
        "name": "Compose the candidate class",
        "tutor_prompt": "Combine the shared features into a class label. "
                        "What do we call sounds with these features?",
        "advance_when": "student names a candidate class",
    },
    {
        "step": 4,
        "name": "Test exhaustiveness",
        "tutor_prompt": "Are there any sounds in the language that share "
                        "these features but are NOT in your set?",
        "if_yes": "Class is too broad — narrow it. Return to Step 2.",
        "if_no":  "Class is exhaustive. Move to Step 5 to confirm narrowness.",
        "advance_when": "student determines whether class is exhaustive",
    },
    {
        "step": 5,
        "name": "Confirm narrowness",
        "tutor_prompt": "Is there a tighter (narrower) feature description "
                        "that also exhausts the set?",
        "advance_when": "student confirms or revises to narrowest exhaustive class",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Feature dimensions for each inventory type
# ──────────────────────────────────────────────────────────────────────

FEATURE_DIMENSIONS = {
    "consonants": {
        "place": ["bilabial", "labiodental", "interdental", "alveolar",
                  "post-alveolar", "palatal", "velar", "glottal"],
        "manner": ["stop", "fricative", "affricate", "nasal", "lateral",
                   "approximant", "tap", "trill"],
        "voicing": ["voiced", "voiceless"],
        "macro_classes": {
            "obstruents":  "stops + fricatives + affricates",
            "sonorants":   "nasals + liquids + glides + vowels",
            "coronals":    "alveolar + post-alveolar + (sometimes interdental)",
            "labials":     "bilabial + labiodental",
            "dorsals":     "palatal + velar + uvular",
            "continuants": "fricatives + approximants + vowels (no full closure)",
        },
    },
    "vowels": {
        "height": ["high", "mid", "low"],
        "backness": ["front", "central", "back"],
        "rounding": ["rounded", "unrounded"],
        "tense_lax": ["tense", "lax"],
        "macro_classes": {
            "high_vowels":  "[i, ɪ, u, ʊ]",
            "low_vowels":   "[æ, ɑ, a]",
            "front_vowels": "[i, ɪ, e, ɛ, æ]",
            "back_vowels":  "[u, ʊ, o, ɔ, ɑ]",
            "lax_vowels":   "[ɪ, ɛ, æ, ʊ, ʌ, ə, ɔ]",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
# Hint ladders per step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "list_sounds": [
        "Write the sounds in the set, separated by commas.",
        "Make sure you have ALL of them — easy to skip one. The set should "
        "match exactly what was given in the data or question.",
        "If the question gives a paradigm, the sounds in the set are usually "
        "the ones triggering an alternation, or the ones in the conditioning "
        "environment.",
    ],
    "find_features": [
        "Pick one feature dimension at a time. For consonants: place, manner, "
        "voicing. For vowels: height, backness, rounding, tense/lax.",
        "Go through ALL the sounds for each feature. If they're all the same, "
        "that feature is shared. If even one differs, that feature isn't shared.",
        "It's possible no single feature unites the set — that's evidence the "
        "set isn't a natural class.",
    ],
    "compose_class": [
        "Combine the features you found. If they all share place=alveolar, the "
        "class is 'alveolars.' If they share voice=voiceless and manner=stop, "
        "it's 'voiceless stops.'",
        "Use one feature label if one suffices. Use a conjunction of features "
        "if multiple are needed (e.g., 'high front lax vowels').",
        "Macro-class labels (obstruents, sonorants, coronals) are often the "
        "right answer when a single dimension covers the set.",
    ],
    "test_exhaustiveness": [
        "Pick one sound NOT in your set. Does it have the features you said "
        "the class shares? If yes, your class includes it — but it shouldn't.",
        "Common failure: picking a class that's true of the set but ALSO true "
        "of more sounds. 'Voiced sounds' is too broad if your set is just "
        "voiced stops.",
        "If you find any sound outside your set that fits the class description, "
        "the class is too broad. Find a feature that excludes that outsider.",
    ],
    "confirm_narrowness": [
        "Is there a more specific description that still includes every sound "
        "in your set?",
        "Wider features are less informative. 'Coronals' beats 'consonants' "
        "even when both technically work.",
        "Don't confuse narrow with restrictive — narrow means the smallest "
        "feature description that still covers the whole set.",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Common errors
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "NC1",
        "trigger_phrases": ["it's voiced consonants", 
                            "it's just sonorants",
                            "they're all alveolar"],
        "description": "Class is too broad — includes targets but also non-targets",
        "redirect": "Test it: is there any sound in the language with that "
                    "feature that's NOT in your set? If yes, the class is too "
                    "broad. Find a tighter description.",
    },
    {
        "id": "NC2",
        "trigger_phrases": ["this is a natural class because they share",
                            "they're a class because"],
        "description": "Treating shared features alone as sufficient (skipping exhaustiveness)",
        "redirect": "Sharing features is necessary but not sufficient. The "
                    "class also has to include every sound in the language with "
                    "those features. Have you checked?",
    },
    {
        "id": "NC3",
        "trigger_phrases": ["[p, l, w] are a natural class",
                            "any group of sounds can be a natural class"],
        "description": "Treating arbitrary lists as natural classes",
        "redirect": "What feature do they share? If you can't find one that "
                    "exhausts these three and excludes other sounds, this isn't "
                    "a natural class.",
    },
    {
        "id": "NC4",
        "trigger_phrases": ["i'll just list the sounds",
                            "the rule fires for [p], [t], [k]"],
        "description": "Listing segments in a rule environment instead of using class label",
        "redirect": "Those three sounds share a feature. What is it? Use the "
                    "class label — it's why we have natural classes in the first "
                    "place.",
    },
    {
        "id": "NC5",
        "trigger_phrases": ["narrow class is bad",
                            "wider is more general",
                            "i should use the most general class"],
        "description": "Inverted preference — picking widest class instead of narrowest",
        "redirect": "Narrowest exhaustive class is the right answer. Wider "
                    "classes overgenerate (rule applies where it shouldn't). "
                    "Narrower exhaustive classes are more informative.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Example natural class identifications
# ──────────────────────────────────────────────────────────────────────

EXAMPLE_CLASSES = [
    {
        "set": ["p", "t", "k"],
        "class": "voiceless stops",
        "reasoning": "All voiceless, all stops. No voiceless stops missing "
                     "from the set in English. Exhaustive.",
        "wrong_answers": [
            ("voiceless consonants", "too broad — includes /s, f, ʃ, θ, h/"),
            ("stops",                "too broad — includes /b, d, g/"),
        ],
    },
    {
        "set": ["m", "n", "ŋ"],
        "class": "nasals",
        "reasoning": "All nasals; English has exactly these three nasals. Exhaustive.",
        "wrong_answers": [
            ("voiced consonants", "too broad — includes voiced stops/fricatives/liquids"),
            ("sonorants",          "too broad — includes liquids and glides"),
        ],
    },
    {
        "set": ["i", "ɪ", "u", "ʊ"],
        "class": "high vowels",
        "reasoning": "All [+high]. English has exactly these four high vowels.",
        "wrong_answers": [
            ("vowels",     "too broad — includes mid and low"),
            ("tense vowels", "doesn't match — /ɪ/ and /ʊ/ are lax"),
        ],
    },
    {
        "set": ["i", "ɪ", "e", "ɛ", "æ"],
        "class": "front vowels",
        "reasoning": "All [+front]. English has exactly these five front vowels.",
        "wrong_answers": [
            ("unrounded vowels", "too broad — includes central and back unrounded"),
            ("vowels",            "too broad"),
        ],
    },
    {
        "set": ["t", "d", "s", "n"],
        "class": "coronals (specifically alveolar non-laterals)",
        "reasoning": "All alveolar. /l/ is also alveolar but is a lateral; "
                     "the class 'coronals' (in some feature systems excluding "
                     "lateral approximants) gets the four targets exactly. "
                     "For LING 250 purposes, 'coronals' is the expected answer.",
        "wrong_answers": [
            ("alveolars",     "includes /l/ which isn't in the set"),
            ("voiced consonants", "doesn't fit — /t/ and /s/ are voiceless"),
            ("obstruents",    "doesn't fit — /n/ is a sonorant"),
        ],
        "note": "HW5 Part B Maltese problem — Lucille missed this on the original test.",
    },
    {
        "set": ["b", "d", "g"],
        "class": "voiced stops",
        "reasoning": "All voiced and all stops. No voiced stops missing.",
        "wrong_answers": [
            ("stops",     "too broad — includes voiceless"),
            ("voiced",    "too broad — includes voiced fricatives, sonorants"),
        ],
    },
    {
        "set": ["s", "z", "ʃ", "ʒ"],
        "class": "sibilants",
        "reasoning": "All have high-frequency noise concentration. Sometimes "
                     "called 'strident coronals.' English has exactly these "
                     "four sibilants in the standard analysis.",
        "wrong_answers": [
            ("fricatives",   "too broad — includes /f, v, θ, ð, h/"),
            ("alveolars",    "doesn't include /ʃ, ʒ/ which are post-alveolar"),
        ],
    },
    {
        "set": ["p", "l", "w"],
        "class": "NOT A NATURAL CLASS",
        "reasoning": "No single feature or feature combination exhausts these "
                     "three. /p/ is a voiceless bilabial stop, /l/ is a voiced "
                     "alveolar lateral, /w/ is a voiced labio-velar approximant. "
                     "They share no exhaustive feature description.",
        "wrong_answers": [
            ("consonants", "too broad — most of the language is in this class"),
        ],
        "note": "Useful counterexample for what a natural class is NOT.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Tutor reminders
# ──────────────────────────────────────────────────────────────────────

TUTOR_REMINDERS = [
    "The student identifies the class. Scaffold the procedure.",
    "Narrowness AND exhaustiveness — both required. Class is too broad if it "
    "includes sounds not in the data.",
    "The exhaustiveness test is the key move — never skip it.",
    "Some sets aren't natural classes. That's a legitimate finding.",
    "Wider features are less informative. 'Coronals' beats 'consonants' even "
    "when both technically cover the set.",
    "If student is stuck on feature recall, hand off to validate-prereqs.",
]


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """Orchestrator entry point. Returns structured guidance."""
    return {
        "skill_id": "id-natural-class",
        "skill_name": "Identify Natural Class",
        "version": "0.1.0",
        "flow": FLOW_STEPS,
        "feature_dimensions": FEATURE_DIMENSIONS,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "example_classes": EXAMPLE_CLASSES,
        "tutor_reminders": TUTOR_REMINDERS,
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "id-natural-class"
    assert len(result["flow"]) == 5
    assert "consonants" in result["feature_dimensions"]
    assert "vowels" in result["feature_dimensions"]
    assert len(result["common_errors"]) >= 4
    assert len(result["example_classes"]) >= 5
    print("id-natural-class/logic.py self-test passed.")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['feature_dimensions'])} inventory types")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
    print(f"  {len(result['example_classes'])} example natural classes")
