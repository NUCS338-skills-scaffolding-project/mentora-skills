"""
logic.py for validate-pre-knowledge

Single mode: returns a probe question AND the catalog of key concepts
a strong answer should cover. The orchestrator judges the student's
answer against these concepts natively, rather than relying on rigid
substring matching.

Design decision: scoring is NOT in this file. The catalog is the
skill's contribution; judgment is the orchestrator's job.
"""

# Prerequisite concept catalog for HW1 (Days 1-3).
# See assignment.md "Concepts Required" for the full list.
PROBES = {
    "voicing": {
        "probe": (
            "In your own words, what is voicing, and how does it "
            "distinguish consonants?"
        ),
        "key_concepts": [
            {
                "name": "vocal fold involvement",
                "synonyms": ["vocal folds", "vocal cords", "larynx",
                             "voicebox"],
                "description": (
                    "The student identifies that voicing is about the "
                    "vocal folds (or equivalent anatomical structure)."
                ),
            },
            {
                "name": "vibration mechanism",
                "synonyms": ["vibrate", "vibrating", "vibration",
                             "buzz", "buzzing"],
                "description": (
                    "The student identifies that the vocal folds are "
                    "vibrating (or not) — not just 'moving' or "
                    "'active,' but specifically vibrating."
                ),
            },
            {
                "name": "voiced vs voiceless distinction",
                "synonyms": ["voiced", "voiceless", "unvoiced"],
                "description": (
                    "The student uses the voiced/voiceless contrast, "
                    "or demonstrates the distinction by example "
                    "(e.g. [z] vs [s])."
                ),
            },
        ],
        "example_strong": (
            "Voicing is whether the vocal folds are vibrating during a "
            "sound. [z] is voiced — folds vibrating. [s] is voiceless "
            "— no vibration."
        ),
        "related_concepts": ["voicing", "vocal folds", "larynx"],
    },
    "place_of_articulation": {
        "probe": (
            "What does 'place of articulation' mean? Give one example "
            "if you can."
        ),
        "key_concepts": [
            {
                "name": "constriction or closure",
                "synonyms": ["constrict", "closure", "narrow", "block",
                             "obstruct"],
                "description": (
                    "The student identifies that something is being "
                    "constricted, closed, or blocked — not just "
                    "'where the sound is made,' but where the airflow "
                    "is narrowed or stopped."
                ),
            },
            {
                "name": "location in the vocal tract",
                "synonyms": ["vocal tract", "mouth", "tongue", "lips",
                             "teeth"],
                "description": (
                    "The student grounds place in physical anatomy — "
                    "somewhere in the vocal tract or oral cavity."
                ),
            },
            {
                "name": "specific example",
                "synonyms": ["bilabial", "alveolar", "velar", "dental",
                             "labiodental", "palatal", "glottal",
                             "post-alveolar", "labio-velar"],
                "description": (
                    "The student names at least one specific place of "
                    "articulation (e.g. bilabial for [p], alveolar "
                    "for [t])."
                ),
            },
        ],
        "example_strong": (
            "Place of articulation is where in the vocal tract the "
            "airflow is constricted or blocked. For example, bilabial "
            "sounds like [p] have constriction at both lips."
        ),
        "related_concepts": ["place", "articulation", "constriction"],
    },
    "manner_of_articulation": {
        "probe": (
            "What does 'manner of articulation' mean? How does it "
            "differ from place?"
        ),
        "key_concepts": [
            {
                "name": "type or shape of articulation",
                "synonyms": ["manner", "how", "type", "kind", "way"],
                "description": (
                    "The student conveys that manner is about the "
                    "*type* or *shape* of articulation, not the "
                    "location."
                ),
            },
            {
                "name": "airflow behavior",
                "synonyms": ["airflow", "air flow", "constrict",
                             "closure", "friction", "turbulence"],
                "description": (
                    "The student describes what the airflow is doing "
                    "— stopped, narrow with friction, free, etc."
                ),
            },
            {
                "name": "specific example",
                "synonyms": ["stop", "fricative", "nasal", "affricate",
                             "approximant", "lateral"],
                "description": (
                    "The student names at least one specific manner "
                    "(e.g. fricative, stop, nasal)."
                ),
            },
        ],
        "example_strong": (
            "Manner is how the airflow is shaped — complete closure "
            "(stops), narrow channel with friction (fricatives), open "
            "passage (approximants), etc. Place is where the "
            "constriction is; manner is what's happening there."
        ),
        "related_concepts": ["manner", "articulation", "airflow"],
    },
    "orthography_vs_pronunciation": {
        "probe": (
            "Why don't linguists use English spelling to describe "
            "sounds? Give an example."
        ),
        "key_concepts": [
            {
                "name": "spelling unreliability",
                "synonyms": ["inconsistent", "unreliable", "irregular",
                             "not reliable", "doesn't match",
                             "don't match", "misleading",
                             "different sounds"],
                "description": (
                    "The student conveys that English spelling "
                    "doesn't reliably reflect pronunciation."
                ),
            },
            {
                "name": "spelling system",
                "synonyms": ["spell", "letter", "orthograph",
                             "writing"],
                "description": (
                    "The student engages with spelling/orthography "
                    "as the relevant construct."
                ),
            },
            {
                "name": "sound system",
                "synonyms": ["sound", "pronunciation", "pronounc",
                             "phone"],
                "description": (
                    "The student engages with sound/pronunciation as "
                    "distinct from spelling."
                ),
            },
        ],
        "example_strong": (
            "English spelling is inconsistent — the same letter can "
            "spell different sounds (c in cat vs cell) and the same "
            "sound can be spelled many ways (sh/ti/ci all spell [ʃ]). "
            "That's why we use IPA instead."
        ),
        "related_concepts": ["orthography", "IPA", "spelling"],
    },
    "ipa_principle": {
        "probe": (
            "What's the core principle behind the IPA? What problem "
            "does it solve?"
        ),
        "key_concepts": [
            {
                "name": "one-to-one mapping",
                "synonyms": ["one sound", "one symbol", "one-to-one",
                             "unique", "distinct", "consistent"],
                "description": (
                    "The student conveys the one-symbol-per-sound "
                    "principle (or its inverse)."
                ),
            },
            {
                "name": "sounds as the unit",
                "synonyms": ["sound", "phone", "pronunciation"],
                "description": (
                    "The student identifies sounds (not letters) as "
                    "what IPA is representing."
                ),
            },
            {
                "name": "symbols as the representation",
                "synonyms": ["symbol", "letter", "character"],
                "description": (
                    "The student identifies symbols as what IPA uses "
                    "to stand for sounds."
                ),
            },
        ],
        "example_strong": (
            "The IPA uses one symbol per distinctive sound, and the "
            "same symbol always means the same sound — across words "
            "and across languages. It solves the inconsistency of "
            "spelling systems."
        ),
        "related_concepts": ["IPA", "one-sound-one-symbol", "transcription"],
    },
    "formal_consonant_description": {
        "probe": (
            "When a phonetician describes a consonant formally, what "
            "three features do they typically name, and in what order?"
        ),
        "key_concepts": [
            {
                "name": "the three features",
                "synonyms": ["voicing", "place", "manner",
                             "place of articulation",
                             "manner of articulation"],
                "description": (
                    "The student names voicing, place of articulation, "
                    "and manner of articulation as the three features."
                ),
            },
            {
                "name": "conventional order",
                "synonyms": ["voicing first", "voicing place manner",
                             "in that order", "voicing then place"],
                "description": (
                    "The student conveys the conventional order: "
                    "voicing → place → manner. (Order can be flexible "
                    "in casual description but voicing-first is the "
                    "textbook convention.)"
                ),
            },
            {
                "name": "predictable features can be omitted",
                "synonyms": ["omit", "implicit", "predictable",
                             "redundant", "leave out", "skip"],
                "description": (
                    "The student knows that predictable features are "
                    "conventionally left out — e.g., nasals are "
                    "predictably voiced, so [m] is described as "
                    "'bilabial nasal' rather than 'voiced bilabial "
                    "nasal stop'. (Bonus credit if the student gives "
                    "an example.)"
                ),
            },
        ],
        "example_strong": (
            "Three features, in order: voicing, place, manner. So [f] "
            "is a voiceless labiodental fricative. Predictable "
            "features are conventionally omitted — [m] is just a "
            "'bilabial nasal' because nasals are always voiced."
        ),
        "related_concepts": ["voicing", "place", "manner", "convention",
                             "Q11"],
    },
    "ipa_chart_navigation": {
        "probe": (
            "How is the IPA consonant chart organized? What does each "
            "row, column, and pair within a cell tell you?"
        ),
        "key_concepts": [
            {
                "name": "columns are place",
                "synonyms": ["columns", "column", "left to right",
                             "across", "horizontal"],
                "description": (
                    "The student identifies that columns map to place "
                    "of articulation, typically running front-of-mouth "
                    "(left) to back-of-mouth (right)."
                ),
            },
            {
                "name": "rows are manner",
                "synonyms": ["rows", "row", "top to bottom", "down",
                             "vertical"],
                "description": (
                    "The student identifies that rows map to manner of "
                    "articulation."
                ),
            },
            {
                "name": "voicing pairs within a cell",
                "synonyms": ["voicing", "voiceless", "voiced", "pair",
                             "left and right", "side by side"],
                "description": (
                    "The student identifies that when two symbols "
                    "share a cell, they differ only in voicing — "
                    "voiceless on the left, voiced on the right."
                ),
            },
        ],
        "example_strong": (
            "Columns are place (front to back of the mouth), rows are "
            "manner. Two symbols sharing a cell differ only in "
            "voicing — voiceless on the left, voiced on the right. "
            "So in the dental column, fricative row, you find [θ] "
            "(voiceless) and [ð] (voiced)."
        ),
        "related_concepts": ["IPA", "chart", "place", "manner",
                             "voicing"],
    },
}


def run(input):
    """
    Main entry point.

    :param input: dict with `action` ("probe") and `concept`.
    :return: dict with probe_question, key_concepts, example_strong_answer,
             related_concepts, error.
    """
    action = input.get("action")
    concept = input.get("concept")

    if action != "probe":
        return _error(
            action, concept,
            "action must be 'probe'. Scoring is handled by the orchestrator."
        )

    if concept is None:
        return _error(action, concept, "concept is required.")

    entry = PROBES.get(concept)
    if entry is None:
        return _error(
            action, concept,
            f"Unknown concept: {concept!r}. Known: {list(PROBES.keys())}"
        )

    return {
        "action": "probe",
        "concept": concept,
        "probe_question": entry["probe"],
        "key_concepts": entry["key_concepts"],
        "example_strong_answer": entry["example_strong"],
        "related_concepts": entry["related_concepts"],
        "error": None,
    }


def list_concepts():
    """Return all prerequisite concept IDs with their probe questions."""
    return [{"concept": c, "probe": entry["probe"]}
            for c, entry in PROBES.items()]


def _error(action, concept, msg):
    return {
        "action": action,
        "concept": concept,
        "error": msg,
    }


if __name__ == "__main__":
    # Basic probe
    r = run({"action": "probe", "concept": "voicing"})
    assert r["action"] == "probe"
    assert r["concept"] == "voicing"
    assert "voicing" in r["probe_question"].lower()
    assert isinstance(r["key_concepts"], list)
    assert len(r["key_concepts"]) == 3
    assert all("name" in kc and "synonyms" in kc and "description" in kc
               for kc in r["key_concepts"])
    assert "vocal folds" in r["example_strong_answer"]
    assert r["error"] is None

    # Key concept shape
    vocal_concept = r["key_concepts"][0]
    assert vocal_concept["name"] == "vocal fold involvement"
    assert "vocal cords" in vocal_concept["synonyms"]
    assert "voicebox" in vocal_concept["synonyms"]

    # Each of the 7 probes works
    for concept_id in ["voicing", "place_of_articulation",
                       "manner_of_articulation",
                       "orthography_vs_pronunciation", "ipa_principle",
                       "formal_consonant_description",
                       "ipa_chart_navigation"]:
        r = run({"action": "probe", "concept": concept_id})
        assert r["error"] is None
        assert len(r["key_concepts"]) >= 2
        assert r["probe_question"]
        assert r["example_strong_answer"]

    # Unknown concept
    r = run({"action": "probe", "concept": "vowel_harmony"})
    assert r["error"] is not None

    # Invalid action — no scoring anymore
    r = run({"action": "score", "concept": "voicing"})
    assert r["error"] is not None
    assert "orchestrator" in r["error"].lower()

    # Missing action
    r = run({"concept": "voicing"})
    assert r["error"] is not None

    # Missing concept
    r = run({"action": "probe"})
    assert r["error"] is not None

    # list_concepts returns all 7
    all_probes = list_concepts()
    assert len(all_probes) == 7
    assert all("concept" in p and "probe" in p for p in all_probes)

    # New Day-3 probes are present and have the right shape
    new_concepts = {"formal_consonant_description", "ipa_chart_navigation"}
    existing_concepts = {p["concept"] for p in all_probes}
    assert new_concepts.issubset(existing_concepts)

    print("validate-pre-knowledge/logic.py: all checks passed ✓")