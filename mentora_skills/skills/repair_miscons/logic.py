"""
logic.py for repair-misconceptions

Given a misconception ID (or a topic keyword), returns the structured
repair information the tutor needs to correct the misconception through
Socratic questioning. Mirror of the human-readable catalog in
context/misconceptions.md.
"""

MISCONCEPTIONS = {
    "spelling_reflects_pronunciation": {
        "title": "Spelling reflects pronunciation",
        "claim": "You can figure out how a word sounds from how it's spelled.",
        "why_wrong": (
            "English orthography is inconsistent. The same letter can "
            "spell different sounds (c in cat vs cell), the same sound "
            "can be spelled many ways (sh/ti/ci all spell [ʃ]), and "
            "sounds occur that aren't written (the glottal stop in "
            "uh-oh)."
        ),
        "correction_target": (
            "Ask the student to find two words where the same letter is "
            "pronounced differently, or the same sound is spelled "
            "differently."
        ),
        "related_concepts": ["orthography", "IPA", "one-sound-one-symbol"],
    },
    "th_is_one_sound": {
        "title": "\"Th\" is one sound",
        "claim": "The letters th represent a single sound.",
        "why_wrong": (
            "Th represents two different sounds: voiceless [θ] as in "
            "thing, and voiced [ð] as in this. They differ only in "
            "voicing."
        ),
        "correction_target": (
            "Ask the student to say thing and this with a hand on their "
            "throat and notice where they feel vibration."
        ),
        "related_concepts": ["voicing", "dental", "fricative"],
    },
    "ch_is_simple": {
        "title": "\"Ch\" is a simple sound",
        "claim": "Ch as in chip is a single consonant like [t] or [s].",
        "why_wrong": (
            "[tʃ] is an affricate — it begins as a complete stop closure "
            "([t]) and releases into a fricative ([ʃ]). Two articulations "
            "packaged into one symbol."
        ),
        "correction_target": (
            "Ask the student to say chip very slowly and notice what the "
            "tongue does at the very beginning versus what comes out "
            "after."
        ),
        "related_concepts": ["affricate", "post-alveolar", "manner"],
    },
    "y_is_always_vowel": {
        "title": "\"Y\" is always a vowel",
        "claim": "Y is a vowel (or \"sometimes a vowel\").",
        "why_wrong": (
            "The letter y can represent the vowel [i] (as in happy) or "
            "the consonant [j], a palatal approximant (as in yes). It's "
            "the sound that matters, not the letter."
        ),
        "correction_target": (
            "Ask the student to compare the beginning of yes with the "
            "beginning of in. What's different about what the tongue is "
            "doing?"
        ),
        "related_concepts": ["palatal", "approximant", "glide", "orthography"],
    },
    "nasals_only_in_nose": {
        "title": "Nasals only involve the nose",
        "claim": "Nasal sounds are produced only in the nose.",
        "why_wrong": (
            "Nasals involve a complete closure in the oral cavity AND a "
            "lowered velum. Air escapes through the nose because it "
            "can't escape through the mouth. The oral closure is what "
            "distinguishes [m] from [n] from [ŋ]."
        ),
        "correction_target": (
            "Ask the student what their lips, tongue tip, and tongue "
            "back are doing during [m], [n], and [ŋ]."
        ),
        "related_concepts": ["nasal", "velum", "place"],
    },
    "voiceless_means_silent": {
        "title": "Voiceless sounds are silent",
        "claim": "If a sound is \"voiceless,\" it means no sound is made.",
        "why_wrong": (
            "Voiceless means the vocal folds aren't vibrating. Plenty "
            "of audible sound is still produced — friction in "
            "fricatives, bursts in stops. Voiceless ≠ silent."
        ),
        "correction_target": (
            "Ask the student to whisper a sentence. Is it silent? "
            "What's producing the sound?"
        ),
        "related_concepts": ["voicing", "vocal folds"],
    },
    "ng_is_two_sounds": {
        "title": "[ŋ] is two sounds",
        "claim": "The ng at the end of sing is [n] followed by [g].",
        "why_wrong": (
            "[ŋ] is a single velar nasal. In words like sing, there's "
            "no [g] at all — just [ŋ]. (In words like finger, both [ŋ] "
            "and [g] are present.)"
        ),
        "correction_target": (
            "Ask the student to say sing and then finger slowly. Where "
            "is the tongue at the end of each?"
        ),
        "related_concepts": ["velar", "nasal", "orthography"],
    },
    "affricates_are_clusters": {
        "title": "Affricates are fast sequences of stop + fricative",
        "claim": "[tʃ] is just [t] followed quickly by [ʃ].",
        "why_wrong": (
            "The articulation is stop-then-fricative, but affricates "
            "behave as single units phonologically. They pattern like "
            "single consonants in syllable structure and timing, not "
            "like consonant clusters."
        ),
        "correction_target": (
            "Ask the student to compare catch it [kætʃ ɪt] with cat "
            "ship [kæt ʃɪp]. Do these sound different? Why?"
        ),
        "related_concepts": ["affricate", "cluster", "timing"],
    },
    "english_r_is_trill": {
        "title": "English 'r' is the IPA [r]",
        "claim": "The IPA symbol [r] is the English r sound in red, run, very.",
        "why_wrong": (
            "[r] in IPA is a trill — a series of rapid taps from the "
            "tongue tip against the alveolar ridge. English does NOT "
            "use the trill. The English r is the rhotic approximant "
            "[ɹ], a single approximation without contact. Spanish "
            "(rico), Italian (rosso), and Scottish (bright red) use [r]."
        ),
        "correction_target": (
            "Ask the student to say red in English, then try saying "
            "rico the way a native Spanish speaker would. What is the "
            "tongue doing differently?"
        ),
        "related_concepts": ["rhotic", "approximant", "trill",
                             "orthography", "transcription"],
    },
    "doubled_letters_doubled_sounds": {
        "title": "Doubled consonant letters are pronounced as the doubled letter",
        "claim": "The 'tt' in butter is pronounced [t] because that's the letter.",
        "why_wrong": (
            "In American English, butter is [bʌɾəɹ] with a tap [ɾ], "
            "not [t]. The tap appears between vowels when V1 is "
            "stressed and V2 is unstressed: butter, water, ladder, "
            "city, better. The spelling doesn't change — the "
            "environment does. Outside that environment (e.g., "
            "stressed V2 in attest) [t] surfaces."
        ),
        "correction_target": (
            "Ask the student to say butter and attest slowly, paying "
            "attention to what the tongue does at the middle "
            "consonant. Are they the same?"
        ),
        "related_concepts": ["tap", "flap", "alveolar", "environment",
                             "orthography"],
    },
    "ipa_chart_is_a_list": {
        "title": "The IPA chart is just a list",
        "claim": (
            "The IPA chart is a flat list of symbols you have to "
            "memorize one by one."
        ),
        "why_wrong": (
            "The chart is organized. Columns are place of "
            "articulation (front of mouth on the left, back on the "
            "right). Rows are manner. When two symbols share a cell, "
            "they differ only in voicing — voiceless on the left, "
            "voiced on the right. Knowing the structure lets you look "
            "up any consonant by its three features."
        ),
        "correction_target": (
            "Ask the student to find the cell for 'alveolar fricative' "
            "on the chart. What two symbols are there? What's the only "
            "difference between them?"
        ),
        "related_concepts": ["IPA", "chart", "place", "manner",
                             "voicing", "structure"],
    },
    "formal_description_names_all_features": {
        "title": (
            "The formal description of a consonant always names all "
            "three features"
        ),
        "claim": (
            "To describe a consonant formally, you always have to say "
            "voicing AND place AND manner — e.g., 'voiced bilabial "
            "nasal stop'."
        ),
        "why_wrong": (
            "Predictable features are conventionally omitted. Since "
            "all English nasals are voiced and have complete oral "
            "closure, [m] is 'bilabial nasal' — not 'voiced bilabial "
            "nasal stop'. Mention only the features that distinguish "
            "the sound from others sharing the same context."
        ),
        "correction_target": (
            "Ask: what does saying 'voiced' add to the description of "
            "[m]? Is there a voiceless [m] in English?"
        ),
        "related_concepts": ["formal description", "voicing", "place",
                             "manner", "convention"],
    },
}


def run(input):
    """
    Main entry point.

    If input has `misconception_id`, returns the full repair dict for that ID.
    If input has `topic`, returns a list of all misconceptions whose title
    or related_concepts include the topic as a substring (case-insensitive).

    :param input: dict with either "misconception_id" or "topic"
    :return: dict (for misconception_id) or list of dicts (for topic)
    """
    if "misconception_id" in input:
        mid = input["misconception_id"]
        entry = MISCONCEPTIONS.get(mid)
        if entry is None:
            return {
                "misconception_id": mid,
                "error": f"Unknown misconception_id: {mid}",
            }
        return {"misconception_id": mid, **entry, "error": None}

    if "topic" in input:
        topic = input["topic"].lower()
        matches = []
        for mid, entry in MISCONCEPTIONS.items():
            if topic in entry["title"].lower():
                matches.append({"misconception_id": mid, **entry})
                continue
            if any(topic in tag.lower() for tag in entry["related_concepts"]):
                matches.append({"misconception_id": mid, **entry})
        return matches

    return {"error": "Provide either misconception_id or topic in input."}


def list_misconceptions():
    """Return all misconception IDs with their titles. Useful for the orchestrator."""
    return [{"misconception_id": mid, "title": entry["title"]}
            for mid, entry in MISCONCEPTIONS.items()]


if __name__ == "__main__":
    # Lookup by ID
    result = run({"misconception_id": "th_is_one_sound"})
    assert result["misconception_id"] == "th_is_one_sound"
    assert "two different sounds" in result["why_wrong"]
    assert "hand on their throat" in result["correction_target"]
    assert result["error"] is None

    # Unknown ID
    result = run({"misconception_id": "not_a_real_id"})
    assert result["error"] is not None

    # Lookup by topic — title match
    results = run({"topic": "spelling"})
    assert any(r["misconception_id"] == "spelling_reflects_pronunciation"
               for r in results)

    # Lookup by topic — related_concepts match (voicing → th + voiceless)
    results = run({"topic": "voicing"})
    mids = [r["misconception_id"] for r in results]
    assert "th_is_one_sound" in mids
    assert "voiceless_means_silent" in mids

    # No match
    results = run({"topic": "klingon"})
    assert results == []

    # Missing input
    result = run({})
    assert "error" in result

    # list_misconceptions returns all 12
    all_mc = list_misconceptions()
    assert len(all_mc) == 12
    assert all("misconception_id" in m and "title" in m for m in all_mc)

    # Spot-check the new entries
    new_ids = {"english_r_is_trill", "doubled_letters_doubled_sounds",
               "ipa_chart_is_a_list", "formal_description_names_all_features"}
    existing_ids = {m["misconception_id"] for m in all_mc}
    assert new_ids.issubset(existing_ids)

    # English-r misconception is findable by topic search
    rhotic_results = run({"topic": "rhotic"})
    assert any(r["misconception_id"] == "english_r_is_trill"
               for r in rhotic_results)

    print("repair-misconceptions/logic.py: all checks passed ✓")
