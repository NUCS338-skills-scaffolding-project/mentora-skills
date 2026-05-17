"""
logic.py for give-contrastive-hint

Given two IPA consonant symbols, identifies which articulatory features
differ between them and which feature is most pedagogically salient.
The calling tutor uses this output to generate a Socratic question
pointing at the right contrast.
"""

import sys
from pathlib import Path

# Make the repo root importable so we can pull from utils/
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from utils.ipa_consonants import get_features, features_that_differ


# Voicing first because it's the easiest for students to feel in their
# own body (hand on throat). Manner next — the articulatory gesture is
# usually visible. Place last — it requires introspecting on tongue
# position, which is the hardest.
FEATURE_PRIORITY = ["voicing", "manner", "place"]


def run(input):
    """
    Main entry point for the skill.

    :param input: dict with keys:
        - sym1 (str): first IPA consonant symbol
        - sym2 (str): second IPA consonant symbol
    :return: dict with keys:
        - differing_features (list[str]): features that differ
        - sym1_features (dict): full feature bundle for sym1
        - sym2_features (dict): full feature bundle for sym2
        - primary_feature (str | None): most pedagogically salient
          differing feature, or None if the symbols are identical or
          one isn't in the reference
        - error (str | None): human-readable error if lookup failed
    """
    sym1 = input.get("sym1")
    sym2 = input.get("sym2")

    f1 = get_features(sym1)
    f2 = get_features(sym2)

    if f1 is None or f2 is None:
        missing = sym1 if f1 is None else sym2
        return {
            "differing_features": [],
            "sym1_features": f1,
            "sym2_features": f2,
            "primary_feature": None,
            "error": f"Symbol not in reference: {missing!r}",
        }

    differing = features_that_differ(sym1, sym2)
    primary = _pick_primary(differing)

    return {
        "differing_features": differing,
        "sym1_features": f1,
        "sym2_features": f2,
        "primary_feature": primary,
        "error": None,
    }


def _pick_primary(differing_features):
    """Return the first feature in FEATURE_PRIORITY that differs, or None."""
    for feat in FEATURE_PRIORITY:
        if feat in differing_features:
            return feat
    return None


if __name__ == "__main__":
    # Sanity checks — run: python3 skills/give-contrastive-hint/logic.py
    result = run({"sym1": "p", "sym2": "b"})
    assert result["differing_features"] == ["voicing"]
    assert result["primary_feature"] == "voicing"
    assert result["error"] is None

    result = run({"sym1": "θ", "sym2": "f"})
    assert result["differing_features"] == ["place"]
    assert result["primary_feature"] == "place"

    result = run({"sym1": "p", "sym2": "z"})
    # p vs z differ on all three — primary picks voicing (highest priority)
    assert set(result["differing_features"]) == {"place", "manner", "voicing"}
    assert result["primary_feature"] == "voicing"

    result = run({"sym1": "p", "sym2": "p"})
    # identical
    assert result["differing_features"] == []
    assert result["primary_feature"] is None

    result = run({"sym1": "p", "sym2": "xyz"})
    # unknown symbol
    assert result["primary_feature"] is None
    assert result["error"] is not None

    print("give-contrastive-hint/logic.py: all checks passed ✓")