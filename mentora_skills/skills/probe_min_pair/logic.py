"""
probe-min-pair / logic.py

Catalog data + run() entry point for the Probe Minimal Pair skill.

The skill scaffolds three operations: testing whether a candidate pair
counts as a minimal pair, finding minimal pairs in given data, and
interpreting what their presence or absence means for phonemic status.
"""

# ──────────────────────────────────────────────────────────────────────
# The three minimal-pair criteria
# ──────────────────────────────────────────────────────────────────────

MINIMAL_PAIR_CRITERIA = [
    {
        "id": 1,
        "criterion": "Equal length / parallel structure",
        "test": "Both words have the same number of segments in the same positions.",
    },
    {
        "id": 2,
        "criterion": "Differ at exactly one position",
        "test": "Going position by position, exactly one segment differs.",
    },
    {
        "id": 3,
        "criterion": "Different meanings",
        "test": "The two words denote different things (not synonyms, not the same word).",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Flow steps
# ──────────────────────────────────────────────────────────────────────

FLOW_STEPS = [
    {
        "step": 1,
        "name": "Establish the criteria",
        "tutor_prompt": "What's the definition of a minimal pair? "
                        "Walk me through what makes two words count.",
        "advance_when": "student states all three criteria",
    },
    {
        "step": 2,
        "name": "Test a candidate pair",
        "tutor_prompt": "Let's go position by position. At position 1, "
                        "what's the sound in each word?",
        "advance_when": "student has compared every position and counted differences",
    },
    {
        "step": 3,
        "name": "Search the data",
        "tutor_prompt": "Pick a word with [X]. Now look for a word in the "
                        "data with the same length and structure, but with "
                        "[Y] where [X] was.",
        "advance_when": "student finds a candidate or has searched exhaustively",
    },
    {
        "step": 4,
        "name": "Interpret the result",
        "tutor_prompt": "What does what you found (or didn't find) tell us "
                        "about the phonemic status of [X] and [Y]?",
        "if_found":     "Separate phonemes in this language.",
        "if_not_found": "Inconclusive — minimal pair absence is not proof of "
                        "allophony. Distributional analysis next.",
        "advance_when": "student articulates the correct interpretation",
    },
    {
        "step": 5,
        "name": "Construct from data (if asked)",
        "tutor_prompt": "Pick a word with one target sound. Substitute the "
                        "other target sound at that position. Is the result a "
                        "real word in the language?",
        "advance_when": "student produces a candidate or determines none exists",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Hint ladders per step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "establish_criteria": [
        "What does 'minimal' mean in 'minimal pair'?",
        "It means MINIMUM possible difference — the smallest possible change "
        "between two words. How small? Think about how many sounds differ.",
        "Exactly one sound differs. Now what about the rest of the word? And "
        "what about the meanings?",
    ],
    "test_candidate": [
        "Compare the two words sound by sound. Are they the same length?",
        "If they're the same length, go through position 1, position 2, "
        "position 3, etc. At each position, are the sounds the same or "
        "different?",
        "Count the positions where they differ. If it's exactly one, AND the "
        "words have different meanings, AND they're the same length — minimal "
        "pair confirmed.",
    ],
    "search_data": [
        "Pick the first word with [X]. What sounds are around the [X]?",
        "Now scan the data for a word with the same surrounding sounds but "
        "[Y] in the [X] position.",
        "If you don't find one, try a different word with [X] as your starting "
        "point. The minimal pair (if it exists) might use any [X]-word as the "
        "anchor.",
    ],
    "interpret_result": [
        "What's the contrast between separate phonemes vs allophones again?",
        "If two sounds occur in identical contexts and the words mean different "
        "things, what does that prove? What does it not prove?",
        "Found pair → separate phonemes (in this language). No pair found → "
        "inconclusive; you need distributional analysis next.",
    ],
    "construct_pair": [
        "Pick any word in the data with [X]. Now substitute [Y] for [X] at the "
        "same position — what would that produce?",
        "Is the resulting form a real word in the language? Check the data.",
        "If not, try a different starting word. If no substitution yields a "
        "real word, there may not be a minimal pair available in this dataset.",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Common errors
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "MP1",
        "trigger_phrases": ["i can't find a minimal pair so they must be allophones",
                            "no minimal pair means they're allophones"],
        "description": "Treating absence of minimal pair as proof of allophony",
        "redirect": "Absence of a minimal pair is inconclusive, not proof of "
                    "allophony. Hindi [b] and [b̤] are separate phonemes shown "
                    "by overlapping distribution, not strict minimal pairs. "
                    "Move to distributional analysis next.",
    },
    {
        "id": "MP2",
        "trigger_phrases": ["bear and fair are a minimal pair for b and f",
                            "they differ in one sound"],
        "description": "Treating near-miss pairs as minimal pairs",
        "redirect": "Walk through position by position. *Bear* is [bɛɹ] and "
                    "*fair* is [fɛɹ]. How many positions actually differ?",
    },
    {
        "id": "MP3",
        "trigger_phrases": ["these are allophones in english",
                            "i know they're allophones"],
        "description": "Projecting English categorizations onto non-English data",
        "redirect": "We're working with [LANGUAGE] data. The minimal pair, if "
                    "one exists in this dataset, will be in [LANGUAGE], not "
                    "English. What does the data show?",
    },
    {
        "id": "MP4",
        "trigger_phrases": ["minimal pairs aren't necessary",
                            "i don't need a minimal pair"],
        "description": "Skipping minimal pair search entirely when it's possible",
        "redirect": "You're right that minimal pairs aren't strictly required, "
                    "but they're the cleanest evidence when available. Have "
                    "you actually checked whether one exists in the data?",
    },
    {
        "id": "MP5",
        "trigger_phrases": ["this pair has different meanings so it's minimal",
                            "different meanings means minimal pair"],
        "description": "Applying meaning criterion alone, without segment check",
        "redirect": "Different meanings is one criterion of three. The other "
                    "two: equal length, and exactly one position differs. "
                    "Have you checked all three?",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Example minimal pairs by language
# ──────────────────────────────────────────────────────────────────────

EXAMPLE_MINIMAL_PAIRS = {
    "english_consonants": [
        ("pat", "bat",   ("p", "b"), "voicing on initial stop"),
        ("tip", "dip",   ("t", "d"), "voicing on initial stop"),
        ("think", "sink", ("θ", "s"), "place of articulation"),
        ("fish", "fizz", ("ʃ", "z"), "place + voicing"),
        ("cat", "cab",   ("t", "b"), "final consonant"),
    ],
    "english_vowels": [
        ("beat", "bit",  ("i", "ɪ"), "tense/lax high front"),
        ("seat", "sit",  ("i", "ɪ"), "tense/lax high front"),
        ("boot", "book", ("u", "ʊ"), "tense/lax high back"),
        ("bait", "bet",  ("eɪ", "ɛ"), "diphthong/monophthong mid front"),
    ],
    "hindi_overlapping_not_minimal": [
        ("bara",  "b̤ari", ("b", "b̤"), "near-overlap, not strict minimal"),
        ("bina",  "b̤ir",  ("b", "b̤"), "different word lengths"),
    ],
    "korean_complementary_no_minimal": {
        "note": "Korean [r] and [l] are in complementary distribution. "
                "No minimal pair exists. This is a textbook case where "
                "absence of minimal pair is informative — combined with "
                "complementary distribution, it points to allophones.",
    },
}

# ──────────────────────────────────────────────────────────────────────
# Tutor reminders
# ──────────────────────────────────────────────────────────────────────

TUTOR_REMINDERS = [
    "The student does the comparing. Walk them through criteria, don't apply.",
    "Absence of a minimal pair is NOT proof of allophony — always redirect this.",
    "Each language stands on its own; don't appeal to English categorizations.",
    "Near-miss pairs (two differences) are NOT minimal pairs.",
    "Minimal pairs are the cleanest evidence type, but overlapping environments "
    "(without strict minimal pairs) also prove phonemic contrast.",
    "Hand off to analyze-dist when minimal-pair search is exhausted.",
]


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """Orchestrator entry point. Returns structured guidance."""
    return {
        "skill_id": "probe-min-pair",
        "skill_name": "Probe Minimal Pair",
        "version": "0.1.0",
        "criteria": MINIMAL_PAIR_CRITERIA,
        "flow": FLOW_STEPS,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "example_minimal_pairs": EXAMPLE_MINIMAL_PAIRS,
        "tutor_reminders": TUTOR_REMINDERS,
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "probe-min-pair"
    assert len(result["criteria"]) == 3
    assert len(result["flow"]) == 5
    assert len(result["common_errors"]) >= 4
    assert "english_consonants" in result["example_minimal_pairs"]
    print("probe-min-pair/logic.py self-test passed.")
    print(f"  {len(result['criteria'])} criteria")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
