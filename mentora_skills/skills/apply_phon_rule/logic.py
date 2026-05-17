"""
apply-phon-rule / logic.py

Catalog data + run() entry point for the Apply Phonological Rule skill.

Forward derivation: given UR + rule → surface form. Mechanical operation
broken into parse, scan, check, apply, output.
"""

# ──────────────────────────────────────────────────────────────────────
# Flow steps
# ──────────────────────────────────────────────────────────────────────

FLOW_STEPS = [
    {
        "step": 1,
        "name": "Parse the rule",
        "tutor_prompt": "Read the rule and identify three parts: target "
                        "(what changes), result (what it becomes), "
                        "environment (where the change happens).",
        "advance_when": "student names all three parts of the rule",
    },
    {
        "step": 2,
        "name": "Scan the UR for the target",
        "tutor_prompt": "Find every position in the UR where the target "
                        "sound appears. These are candidate loci for rule "
                        "application.",
        "advance_when": "student lists all positions of target in UR",
    },
    {
        "step": 3,
        "name": "Check environment at each locus",
        "tutor_prompt": "At each candidate locus, check both contexts: "
                        "what's to the left? What's to the right? Does each "
                        "match the rule's environment?",
        "advance_when": "student has classified each locus as match or no-match",
    },
    {
        "step": 4,
        "name": "Apply the change at matching loci",
        "tutor_prompt": "At every locus where the environment matches, "
                        "replace the target with the result. Loci where the "
                        "environment doesn't match stay unchanged.",
        "advance_when": "student has performed the substitution at all matches",
    },
    {
        "step": 5,
        "name": "Output the surface form",
        "tutor_prompt": "Read the resulting form. Use [brackets] because "
                        "this is the surface representation. The original UR "
                        "stays in /slashes/.",
        "advance_when": "student produces final surface form with bracket notation",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Rule parsing template
# ──────────────────────────────────────────────────────────────────────

PARSING_TEMPLATE = {
    "target": {
        "description": "The sound that changes; written in /slashes/",
        "find_in_rule": "left of the arrow",
        "example": "in '/p/ → [b] / V __ V', target is /p/",
    },
    "result": {
        "description": "What the target becomes; written in [brackets]",
        "find_in_rule": "right of the arrow, before the slash",
        "example": "in '/p/ → [b] / V __ V', result is [b]",
    },
    "environment": {
        "description": "The context where the change applies",
        "find_in_rule": "after the slash; '__' marks the target's position",
        "example": "in '/p/ → [b] / V __ V', environment is V __ V (between vowels)",
    },
}

# ──────────────────────────────────────────────────────────────────────
# Hint ladders per step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "parse_rule": [
        "Look at the rule. There's an arrow. What's to the LEFT of the arrow?",
        "Left of the arrow is the target. Right of the arrow (before any slash) "
        "is the result. Everything after the slash is the environment.",
        "In '/p/ → [b] / V __ V': /p/ is the target, [b] is the result, "
        "'V __ V' is the environment (between two vowels).",
    ],
    "scan_ur": [
        "Look at the UR character by character. Which characters match the "
        "target sound?",
        "Mark each position where the target appears. There can be one, "
        "multiple, or zero positions.",
        "Don't count just the first one — every occurrence is a candidate.",
    ],
    "check_environment": [
        "Pick the first candidate locus. What sound is immediately to its "
        "left? Is that what the rule requires?",
        "Now what's immediately to its right? Does it match?",
        "Both sides have to match for the rule to apply at that locus. If "
        "either side doesn't match, skip this locus and check the next.",
    ],
    "apply_change": [
        "At loci where the environment matched, swap the target for the result.",
        "At loci where the environment didn't match, leave the target alone.",
        "Don't apply the rule at non-matching loci just because the target "
        "appeared there. Environment is the gatekeeper.",
    ],
    "output_surface": [
        "Read the resulting string. That's your surface form.",
        "Wrap it in [brackets] to indicate it's a surface representation.",
        "If no locus matched the environment, the surface form equals the "
        "UR (just with brackets instead of slashes).",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Common errors
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "AR1",
        "trigger_phrases": ["i'll just apply it",
                            "the rule changes /p/ to [b] so /apapa/ becomes [abapa]"],
        "description": "Stopping at the first match instead of checking all loci",
        "redirect": "Did you check every position where the target appears? "
                    "Rules apply at every matching locus, not just the first one.",
    },
    {
        "id": "AR2",
        "trigger_phrases": ["the rule should apply", 
                            "the target is there so it changes"],
        "description": "Forcing application without environment match",
        "redirect": "The target appearing isn't enough — the environment also "
                    "has to match. What's the environment requirement? Does it "
                    "match here?",
    },
    {
        "id": "AR3",
        "trigger_phrases": ["the rule doesn't apply because i don't see the change",
                            "i don't think the rule fires"],
        "description": "Missing a locus where the environment matches",
        "redirect": "Walk through every position of the target. Are you sure "
                    "you checked the environment at every one? Easy to miss a "
                    "match.",
    },
    {
        "id": "AR4",
        "trigger_phrases": ["reading the rule and applying are the same",
                            "i know what the rule means so i can apply it"],
        "description": "Conflating rule reading with rule application",
        "redirect": "Reading and applying are different operations. Reading: "
                    "'/p/ → [b]' means '/p/ becomes [b].' Applying: given a "
                    "specific UR, derive the specific surface form. Walk through "
                    "the application steps.",
    },
    {
        "id": "AR5",
        "trigger_phrases": ["/abapa/", "[apapa]"],
        "description": "Mixing slashes and brackets in the answer",
        "redirect": "Surface forms use [brackets]. Underlying forms use "
                    "/slashes/. Which is your answer — surface or underlying? "
                    "It should use the right notation.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Example derivations
# ──────────────────────────────────────────────────────────────────────

EXAMPLE_DERIVATIONS = [
    {
        "rule": "/p/ → [b] / V __ V",
        "ur": "/apa/",
        "loci": [(1, "[a]_[a]", "match")],
        "surface": "[aba]",
        "note": "Single application — one match, one change.",
    },
    {
        "rule": "/p/ → [b] / V __ V",
        "ur": "/apapa/",
        "loci": [(1, "[a]_[a]", "match"), (3, "[a]_[a]", "match")],
        "surface": "[ababa]",
        "note": "Multiple applications — both /p/'s match, both change.",
    },
    {
        "rule": "/p/ → [b] / V __ V",
        "ur": "/pat/",
        "loci": [(0, "#_[a]", "no match — left context is # not V")],
        "surface": "[pat]",
        "note": "No application — rule doesn't fire because environment "
                "doesn't match. Surface = UR (in brackets).",
    },
    {
        "rule": "Ø → [e] / C __ CC",
        "ur": "/askp/",
        "loci": [(2, "[s]_[kp]", "match — C on left, CC on right")],
        "surface": "[asekp]",
        "note": "Epenthesis — Ø means insert. Inserts [e] between [s] and [kp].",
    },
    {
        "rule": "Ø → [e] / C __ CC",
        "ur": "/ask/",
        "loci": [],
        "surface": "[ask]",
        "note": "No application — UR doesn't have a CC sequence after a "
                "single C. Rule doesn't fire.",
    },
    {
        "rule": "/t/ → Ø / C __ #",
        "ur": "/kest/",
        "loci": [(3, "[s]_#", "match — C on left, # on right")],
        "surface": "[kes]",
        "note": "Deletion — target → Ø. Removes [t] from [kest].",
    },
    {
        "rule": "/t/ → Ø / C __ #",
        "ur": "/kesta/",
        "loci": [(3, "[s]_[a]", "no match — right context is V not #")],
        "surface": "[kesta]",
        "note": "No application — [t] is not word-final.",
    },
    {
        "rule": "/sk/ → [ks] / __ {C, #}",
        "ur": "/mask/",
        "loci": [(2, "_#", "match — right context is #")],
        "surface": "[maks]",
        "note": "Metathesis — two segments swap. /sk/ becomes [ks] before "
                "any consonant or word boundary.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Tutor reminders
# ──────────────────────────────────────────────────────────────────────

TUTOR_REMINDERS = [
    "Application is mechanical, not creative. UR + rule fully determines surface.",
    "Scan every locus where the target appears. Don't stop at the first match.",
    "Environment is the gatekeeper. Target alone isn't enough — environment "
    "must match too.",
    "If no locus matches, the rule doesn't apply. Surface = UR (in brackets).",
    "Use [brackets] for the output. Surface forms always use brackets.",
    "Reading a rule ≠ applying a rule. Application requires the systematic "
    "scan-and-check procedure.",
]


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """Orchestrator entry point. Returns structured guidance."""
    return {
        "skill_id": "apply-phon-rule",
        "skill_name": "Apply Phonological Rule",
        "version": "0.1.0",
        "flow": FLOW_STEPS,
        "parsing_template": PARSING_TEMPLATE,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "example_derivations": EXAMPLE_DERIVATIONS,
        "tutor_reminders": TUTOR_REMINDERS,
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "apply-phon-rule"
    assert len(result["flow"]) == 5
    assert "target" in result["parsing_template"]
    assert len(result["common_errors"]) >= 4
    assert len(result["example_derivations"]) >= 5
    print("apply-phon-rule/logic.py self-test passed.")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['parsing_template'])} parsing template parts")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
    print(f"  {len(result['example_derivations'])} example derivations")
