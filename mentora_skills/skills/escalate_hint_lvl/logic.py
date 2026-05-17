"""
logic.py for escalate-hint-level-gradually

Given a current hint level and a hint type (or a custom ladder),
returns the next hint in the ladder. Stateless — the orchestrator
tracks current_level across turns.

Design philosophy: hint ladders go from abstract/metacognitive to
concrete/body-anchored, but never reach the answer. When the student
is stuck at max level, that's a signal to switch skills, not to hint
harder.
"""

# Hint ladders for common HW1 question types.
# Each list goes from level 1 (most abstract) to level N (most specific)
# but always stops short of revealing the answer.
HINT_LADDERS = {
    "feature_classification": [
        # Level 1: metacognitive
        "This is a good one to work through carefully. What do you "
        "already know about this sound? Say it out loud a couple of "
        "times and notice what happens.",
        # Level 2: invoke the framework
        "Every consonant can be described with three features: place of "
        "articulation, manner of articulation, and voicing. Which of "
        "the three is the question asking you to figure out?",
        # Level 3: focused observation
        "Focus on just that feature. If it's voicing, put your hand on "
        "your throat. If it's place, notice where your tongue or lips "
        "are. If it's manner, notice what the airflow is doing — "
        "stopped, friction, or free.",
        # Level 4: narrow to a comparison
        "Try contrasting with a sound you already know well. What does "
        "this sound have in common with [s] or [t] or [m]? What's "
        "different?",
    ],
    "midsagittal_diagram": [
        # Level 1: general orientation
        "Take a moment with the diagram. What's the first thing you "
        "notice — where is something constricted or closed?",
        # Level 2: framework
        "A midsagittal diagram encodes three things: where the "
        "constriction is (place), how tight it is (manner), and "
        "whether the vocal folds are vibrating (voicing). Can you "
        "identify each one on this diagram?",
        # Level 3: focus on place
        "Start with place. Where is the narrowest or most complete "
        "constriction? Lips pressed together? Tongue tip at the "
        "alveolar ridge? Tongue body at the velum?",
        # Level 4: focus on manner
        "Now manner. Is there complete closure (a stop), a narrow "
        "channel with airflow (a fricative), an open passage (an "
        "approximant), or a lowered velum sending air through the nose "
        "(a nasal)?",
        # Level 5: focus on voicing
        "Finally voicing. Is there a mark at the vocal folds "
        "indicating vibration? If yes, voiced. If no, voiceless.",
    ],
    "ipa_transcription": [
        # Level 1: the general principle
        "Say each IPA symbol out loud, slowly, one at a time. Then try "
        "blending them. What English word does the sequence sound like?",
        # Level 2: setting aside spelling
        "Don't try to match letters — match sounds. The IPA symbols tell "
        "you exactly what sounds to produce, and English spelling is "
        "often misleading.",
        # Level 3: symbol-by-symbol
        "Go symbol by symbol. What's the first sound? What's the "
        "second? Just name each one, then put them together.",
        # Level 4: tricky symbols
        "If there's a symbol you don't recognize, here are some "
        "common ones: [ʃ] is the 'sh' sound, [ʒ] is the 'zh' (as in "
        "measure), [θ] is 'th' (voiceless, as in thing), [ð] is 'th' "
        "(voiced, as in this), [ŋ] is the 'ng' in sing, [ʔ] is the "
        "glottal stop in uh-oh.",
    ],
    "multi_select_feature": [
        # Level 1: parse the question
        "Let's break this down. What feature, or combination of "
        "features, are they asking you to find?",
        # Level 2: one word at a time
        "Go through the list one word at a time. For each word, focus "
        "only on the sound at the position the question asks about — "
        "beginning, end, or somewhere in the middle.",
        # Level 3: feature test
        "For each word, ask: does the target sound match *all* of the "
        "features the question named? All of them have to match — if "
        "even one feature is off, that word doesn't belong.",
        # Level 4: stuck on a specific word
        "If you're stuck on a particular word, say the target sound in "
        "isolation. Feel for each feature one at a time — throat for "
        "voicing, airflow for manner, mouth position for place.",
    ],
    "feature_to_symbol_q11": [
        # Q11-specific ladder: given a formal description, find the IPA
        # symbol. Highest-stakes question on HW1 (10 of 40 points).
        # Level 1: decompose the description
        "Take the description apart. If they say 'voiceless "
        "post-alveolar fricative,' that's three pieces of information. "
        "What is each piece telling you?",
        # Level 2: filter by one feature at a time
        "Use the description to narrow the field. Start with manner — "
        "the manner alone usually narrows you to a small set (only "
        "two or three English consonants share most manners). Then "
        "use place to narrow further. Then voicing picks one.",
        # Level 3: identify the candidate set
        "Suppose the description is 'voiced bilabial stop.' Bilabial "
        "stops in English are [p] and [b]. One is voiceless, one is "
        "voiced. Which one matches?",
        # Level 4: when manner is ambiguous
        "If you can't remember the manner term, anchor it: 'fricative' "
        "= friction sound (s/z/f/v/θ/ð/ʃ/ʒ/h), 'stop' = complete "
        "closure (p/b/t/d/k/g/ʔ), 'nasal' = air through nose (m/n/ŋ), "
        "'affricate' = stop+fricative (tʃ/dʒ), 'approximant' = open "
        "passage (ɹ/j/w), 'lateral' = around the sides (l).",
    ],
    "symbol_to_description": [
        # Inverse direction: given a symbol, produce the formal
        # description. Used in matching questions and definition
        # questions (e.g., HW1 Q4: "What is the manner of [θ]?").
        # Level 1: name the three features
        "When you describe a consonant formally, you name three "
        "things. What are they? (Hint: one is about the vocal folds.)",
        # Level 2: one feature at a time
        "Take it feature by feature. Start with voicing — say the "
        "sound with a hand on your throat. Vibrating or not?",
        # Level 3: place
        "Now place. Say the sound slowly and notice where the "
        "constriction is. Lips? Tongue tip and upper teeth? Tongue "
        "tip and the ridge behind your teeth? Tongue body and the "
        "roof? Back of the tongue and the velum?",
        # Level 4: manner
        "Now manner. What is the airflow doing at that constriction? "
        "Completely blocked (stop)? Squeezed through a narrow channel "
        "with friction (fricative)? Going through the nose (nasal)? "
        "Flowing freely past the articulators (approximant)?",
        # Level 5: omitted features convention
        "Last thing: predictable features get left out. Nasals are "
        "always voiced in English, so for [m] you'd say 'bilabial "
        "nasal' — not 'voiced bilabial nasal stop.' Are any of your "
        "features predictable from the others?",
    ],
    "chart_navigation": [
        # For when the student can't find a symbol on the IPA chart or
        # doesn't know how to use the chart as a lookup tool.
        # Level 1: orient
        "The IPA chart isn't a list — it's a 2D grid. What do you "
        "think the rows and columns mean?",
        # Level 2: name the axes
        "Columns = place of articulation, organized front-of-mouth on "
        "the left to back-of-mouth on the right. Rows = manner of "
        "articulation. Where on the grid would you start looking for "
        "the sound you want?",
        # Level 3: navigate to the right cell
        "Suppose you're looking for [s]. [s] is alveolar (place) and "
        "fricative (manner). Find the alveolar column, the fricative "
        "row. The cell where they meet has [s] and [z].",
        # Level 4: read voicing pairs
        "When two symbols share a cell, they differ only in voicing. "
        "By convention, voiceless is on the left, voiced is on the "
        "right. So if you're looking for the voiceless one, take the "
        "left symbol; voiced, take the right.",
    ],
}


def run(input):
    """
    Main entry point.

    :param input: dict with `current_level` (int, required) and either
                  `hint_type` (str) or `custom_ladder` (list of str).
    :return: dict with next_level, hint_text, is_max_level, total_levels, error
    """
    current_level = input.get("current_level")
    if current_level is None:
        return _error("current_level is required (use 0 for first hint).")
    if not isinstance(current_level, int) or current_level < 0:
        return _error(f"current_level must be a non-negative integer, got {current_level!r}")

    # Resolve the ladder: custom_ladder wins if both are present
    if "custom_ladder" in input and input["custom_ladder"]:
        ladder = input["custom_ladder"]
        if not isinstance(ladder, list) or not all(isinstance(h, str) for h in ladder):
            return _error("custom_ladder must be a list of strings.")
    elif "hint_type" in input:
        hint_type = input["hint_type"]
        ladder = HINT_LADDERS.get(hint_type)
        if ladder is None:
            return _error(
                f"Unknown hint_type: {hint_type!r}. "
                f"Known types: {list(HINT_LADDERS.keys())}. "
                f"Or pass custom_ladder."
            )
    else:
        return _error("Provide either hint_type or custom_ladder.")

    total_levels = len(ladder)
    next_level = current_level + 1

    if next_level > total_levels:
        # Already at or past the end of the ladder
        return {
            "next_level": current_level,
            "hint_text": None,
            "is_max_level": True,
            "total_levels": total_levels,
            "error": None,
        }

    return {
        "next_level": next_level,
        "hint_text": ladder[next_level - 1],
        "is_max_level": (next_level == total_levels),
        "total_levels": total_levels,
        "error": None,
    }


def list_hint_types():
    """Return all known hint_type keys with their ladder lengths."""
    return [{"hint_type": k, "total_levels": len(v)}
            for k, v in HINT_LADDERS.items()]


def _error(msg):
    return {
        "next_level": None,
        "hint_text": None,
        "is_max_level": False,
        "total_levels": 0,
        "error": msg,
    }


if __name__ == "__main__":
    # First hint on a known type
    r = run({"hint_type": "feature_classification", "current_level": 0})
    assert r["next_level"] == 1
    assert r["hint_text"] is not None
    assert "sound" in r["hint_text"].lower()
    assert r["is_max_level"] is False
    assert r["total_levels"] == 4
    assert r["error"] is None

    # Mid-ladder escalation
    r = run({"hint_type": "feature_classification", "current_level": 2})
    assert r["next_level"] == 3
    assert r["is_max_level"] is False

    # Hit max level
    r = run({"hint_type": "feature_classification", "current_level": 3})
    assert r["next_level"] == 4
    assert r["is_max_level"] is True

    # Past max — returns None hint, flags max
    r = run({"hint_type": "feature_classification", "current_level": 4})
    assert r["hint_text"] is None
    assert r["is_max_level"] is True

    # Midsagittal ladder has 5 levels
    r = run({"hint_type": "midsagittal_diagram", "current_level": 0})
    assert r["total_levels"] == 5

    # Unknown hint_type
    r = run({"hint_type": "not_a_type", "current_level": 0})
    assert r["error"] is not None
    assert "Unknown hint_type" in r["error"]

    # Custom ladder
    custom = ["try harder", "think about the frog", "which frog though"]
    r = run({"custom_ladder": custom, "current_level": 0})
    assert r["hint_text"] == "try harder"
    assert r["total_levels"] == 3
    r = run({"custom_ladder": custom, "current_level": 2})
    assert r["hint_text"] == "which frog though"
    assert r["is_max_level"] is True

    # Missing current_level
    r = run({"hint_type": "feature_classification"})
    assert r["error"] is not None

    # Invalid current_level
    r = run({"hint_type": "feature_classification", "current_level": -1})
    assert r["error"] is not None

    # Missing ladder source
    r = run({"current_level": 0})
    assert r["error"] is not None

    # list_hint_types
    types = list_hint_types()
    assert len(types) == 7
    assert all("hint_type" in t and "total_levels" in t for t in types)

    # New Day-3 ladders are present
    type_names = {t["hint_type"] for t in types}
    assert {"feature_to_symbol_q11", "symbol_to_description",
            "chart_navigation"}.issubset(type_names)

    # Spot-check a Q11 hint at level 1
    r = run({"hint_type": "feature_to_symbol_q11", "current_level": 0})
    assert r["error"] is None
    assert r["next_level"] == 1
    assert "description" in r["hint_text"].lower() or \
           "feature" in r["hint_text"].lower()

    # symbol_to_description has 5 levels (omitted-features step)
    r = run({"hint_type": "symbol_to_description", "current_level": 0})
    assert r["total_levels"] == 5

    print("escalate-hint-level-gradually/logic.py: all checks passed ✓")

