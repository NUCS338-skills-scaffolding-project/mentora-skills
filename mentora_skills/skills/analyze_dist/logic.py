"""
analyze_dist / logic.py

Catalog data + run() entry point for the Analyze Distribution skill.

The orchestrator may call run(input) when the skill is invoked. The data
structures here are also referenced by the orchestrator's prompt assembly
when this skill is selected, so they're written to be both
machine-consumable and human-readable.

Canonical data lives in utils/phonemic_analysis.py and utils/language_datasets.py.
This module holds a self-contained working subset so the skill is portable
even if utils/ aren't loaded.
"""

# ──────────────────────────────────────────────────────────────────────
# The five steps — compact form for runtime use
# ──────────────────────────────────────────────────────────────────────

DIAGNOSTIC_STEPS = [
    {
        "step": 1,
        "name": "Frame the question",
        "tutor_prompt": "What are we trying to figure out about [X] and [Y]? "
                        "Phonemes, allophones, or free variation?",
        "advance_when": "student articulates the trinary choice",
    },
    {
        "step": 2,
        "name": "Look for minimal pairs",
        "tutor_prompt": "Can you find a pair of words in the data that differ "
                        "ONLY in [X] vs [Y]?",
        "if_yes": "Strong evidence for separate phonemes. Move to confirm.",
        "if_no":  "Absence of minimal pairs is not proof of allophony. "
                  "Let's check distribution.",
        "advance_when": "student confirms presence/absence of minimal pairs",
    },
    {
        "step": 3,
        "name": "List environments",
        "tutor_prompt": "What's to the left and right of [X] in each form? "
                        "Make a list. Now do the same for [Y].",
        "advance_when": "student has produced a complete list for both",
        "common_pitfall": "skipping environments — insist on completeness",
    },
    {
        "step": 4,
        "name": "Classify distribution",
        "tutor_prompt": "Looking at your two lists, is there ANY context "
                        "where both [X] and [Y] appear?",
        "if_overlap":         "Overlapping → separate phonemes. Done.",
        "if_complementary":   "Complementary → likely allophones. "
                              "Check phonetic similarity next.",
        "advance_when": "student classifies the distribution",
    },
    {
        "step": "4b",
        "name": "Phonetic similarity check",
        "tutor_prompt": "What features do [X] and [Y] share? Are they "
                        "similar enough that one could be a variant of the "
                        "other?",
        "if_similar":    "Allophones confirmed. Move to UR selection.",
        "if_dissimilar": "NOT allophones (e.g., English [h]/[ŋ]). "
                         "Separate phonemes despite complementary distribution.",
        "advance_when": "student decides on similarity",
    },
    {
        "step": 5,
        "name": "Choose UR by simplicity",
        "tutor_prompt": "If [X] is the UR, what rule(s) would you need? "
                        "Now if [Y] is the UR, what rule(s) would you need? "
                        "Which analysis is simpler?",
        "advance_when": "student selects UR with rule-count justification",
    },
]


# ──────────────────────────────────────────────────────────────────────
# Hint ladders — used when the student is stuck at a step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "frame_the_question": [
        "What categories of phonological status do you know? Name them.",
        "There are three: separate phonemes, allophones of one phoneme, "
        "and free variation. Which one are you trying to determine?",
        "Let's look at the data and decide what evidence would push us "
        "toward each category.",
    ],
    "find_minimal_pairs": [
        "Look at each pair of words. Is there one that differs only in "
        "[X] vs [Y]?",
        "What does 'differ only in [X] vs [Y]' mean? The rest of the word "
        "is identical except for that one sound.",
        "Try comparing [WORD1] and [WORD2] — what's different about them?",
    ],
    "list_environments": [
        "Pick the first word containing [X]. What sound is to its left? "
        "What sound is to its right?",
        "Use # for word boundary, V for any vowel, C for any consonant. "
        "Or just write the actual sound.",
        "Have you done this for every word containing [X]? Now do the same "
        "for every word containing [Y].",
    ],
    "compare_distributions": [
        "Compare your two lists side by side. Are any of the contexts the "
        "same?",
        "Even ONE shared context = overlapping. Look carefully.",
        "If you see [X] in context A and [Y] in context A — that's overlap.",
    ],
    "phonetic_similarity": [
        "What place of articulation does [X] have? What place does [Y] have?",
        "What manner does each have? Voicing?",
        "If they share most features, they're plausible allophones. "
        "If they're radically different (like English h vs ŋ), they're not.",
    ],
    "choose_ur": [
        "Imagine [X] is the underlying form. What rule would derive [Y] in "
        "its environments?",
        "Now imagine [Y] is the underlying form. What rule would derive [X] "
        "in its environments?",
        "Count the rules each analysis requires. Which has fewer?",
        "The form with the BROADEST distribution (the elsewhere case) is "
        "usually the UR — yields the simplest rules.",
    ],
}


# ──────────────────────────────────────────────────────────────────────
# Common errors to flag (catalog for in-flight repair)
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "AD1",
        "trigger_phrases": ["these are allophones because they sound similar",
                            "they're allophones in english so they must be"],
        "description": "Projecting English categorizations onto another language",
        "redirect": "Each language has its own phonemic structure. Let's "
                    "look at the data given, not at English. What does THIS "
                    "data show?",
    },
    {
        "id": "AD2",
        "trigger_phrases": ["i think they're allophones",
                            "they look like allophones",
                            "obviously phonemes"],
        "description": "Jumping to a conclusion before doing the analysis",
        "redirect": "How did you get there? Have you listed the environments "
                    "for each sound? Let's do that first.",
    },
    {
        "id": "AD3",
        "trigger_phrases": ["they appear in different positions sometimes",
                            "mostly different contexts"],
        "description": "Using vague language for distributional classification",
        "redirect": "Complementary means NEVER the same context. Even one "
                    "shared context = overlapping. Be precise: are there "
                    "ANY shared contexts in your lists?",
    },
    {
        "id": "AD4",
        "trigger_phrases": ["they're complementary so they're allophones",
                            "complementary means allophones"],
        "description": "Skipping the phonetic similarity step",
        "redirect": "Complementary distribution alone isn't sufficient. "
                    "Are they phonetically similar? Think of English [h] and "
                    "[ŋ] — complementary but not allophones.",
    },
    {
        "id": "AD5",
        "trigger_phrases": ["the underlying form is the more common one",
                            "ur is whichever appears most"],
        "description": "Picking UR by frequency rather than broadest distribution",
        "redirect": "Frequency often correlates, but the diagnostic is "
                    "BROADEST distribution. Test both candidates: which "
                    "yields fewer rules?",
    },
    {
        "id": "AD6",
        "trigger_phrases": ["i can't find a pattern",
                            "there's no rule",
                            "this data is random"],
        "description": "Giving up without systematic environment listing",
        "redirect": "Have you listed every environment? Let's start over "
                    "with a clean list. Pick the first word with [X]. What's "
                    "to its left? What's to its right?",
    },
]


# ──────────────────────────────────────────────────────────────────────
# Compact dataset references (full data in utils/language_datasets.py)
# ──────────────────────────────────────────────────────────────────────

EXAMPLE_DATASETS = {
    "spanish_b_beta": {
        "language": "Spanish",
        "sounds": ("b", "β"),
        "status": "allophones",
        "rule": "/b/ → [β] / V _ V",
        "use_case": "introductory complementary-distribution example",
    },
    "korean_r_l": {
        "language": "Korean",
        "sounds": ("r", "l"),
        "status": "allophones",
        "rule": "/l/ → [r] / __ V (in onset)",
        "use_case": "syllable-position conditioning (advanced)",
    },
    "hindi_b_bh": {
        "language": "Hindi",
        "sounds": ("b", "b̤"),
        "status": "separate phonemes",
        "evidence": "overlapping distribution at # __ a, # __ i",
        "use_case": "shows overlap → phonemes without strict minimal pairs",
    },
    "english_h_ng": {
        "language": "English",
        "sounds": ("h", "ŋ"),
        "status": "separate phonemes",
        "evidence": "complementary BUT phonetically too dissimilar",
        "use_case": "counterexample to 'complementary = allophones'",
    },
    "swampy_cree_p_b": {
        "language": "Swampy Cree",
        "sounds": ("p", "b"),
        "status": "allophones",
        "rule": "/p/ → [b] / V _ V",
        "use_case": "canonical HW4 example, reused on Quiz 4",
    },
}


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """
    Orchestrator entry point. Returns a dict with structured guidance the
    orchestrator can incorporate into its prompt.

    Args:
        input: dict — typically contains the student's question, conversation
               history, and any detected target sounds. Schema is loose;
               we extract what's useful.

    Returns:
        dict with:
            - flow: list of diagnostic steps to walk through
            - hint_ladders: per-step hint progressions
            - common_errors: error patterns to watch for
            - example_datasets: parallel problems to suggest if stuck
            - tutor_reminders: high-priority stance reminders
    """
    return {
        "skill_id": "analyze_dist",
        "skill_name": "Analyze Distribution",
        "version": "0.1.0",
        "flow": DIAGNOSTIC_STEPS,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "example_datasets": EXAMPLE_DATASETS,
        "tutor_reminders": [
            "The student does the analysis. Scaffold the procedure.",
            "Never classify sounds before student has compared environments.",
            "Never propose UR before student has compared both candidates.",
            "Each language stands on its own — never appeal to English.",
            "Insist on listing EVERY environment — don't accept partial lists.",
            "Phonetic similarity check is REQUIRED for complementary case.",
        ],
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "analyze_dist"
    assert len(result["flow"]) == 6  # steps 1, 2, 3, 4, 4b, 5
    assert "spanish_b_beta" in result["example_datasets"]
    assert len(result["common_errors"]) >= 5
    print("analyze_dist/logic.py self-test passed.")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
    print(f"  {len(result['example_datasets'])} parallel datasets")

