"""
read-waveform / logic.py

Catalog data + run() entry point for the Read Waveform skill.

Scaffolds reading amplitude-over-time waveforms: identifying segments,
locating segment boundaries, measuring VOT, distinguishing voiced from
voiceless regions.
"""

# ──────────────────────────────────────────────────────────────────────
# Flow steps
# ──────────────────────────────────────────────────────────────────────

FLOW_STEPS = [
    {
        "step": 1,
        "name": "Identify axes",
        "tutor_prompt": "On a waveform, what's on the x-axis? The y-axis?",
        "advance_when": "student names time on x and amplitude on y",
    },
    {
        "step": 2,
        "name": "Identify segment type at each region",
        "tutor_prompt": "At this region, is the pattern periodic or aperiodic? "
                        "High or low amplitude? What segment type does that "
                        "match?",
        "advance_when": "student classifies regions by segment type",
    },
    {
        "step": 3,
        "name": "Locate stop phases (if applicable)",
        "tutor_prompt": "For the stop, can you find the closure (silent gap), "
                        "the burst (vertical spike), and the aspiration "
                        "(aperiodic noise) if present?",
        "advance_when": "student locates closure, burst, and any aspiration",
    },
    {
        "step": 4,
        "name": "Mark segment boundaries",
        "tutor_prompt": "At what point does the visual pattern change from one "
                        "segment type to another? That's the boundary.",
        "advance_when": "student marks the boundary correctly",
    },
    {
        "step": 5,
        "name": "Measure VOT (if asked)",
        "tutor_prompt": "Find the burst. Find the start of voicing (regular "
                        "periodic cycles). The interval between them is the VOT.",
        "advance_when": "student measures VOT and classifies it (negative / "
                        "zero / long-lag)",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Segment signatures on waveforms
# ──────────────────────────────────────────────────────────────────────

SEGMENT_SIGNATURES = {
    "vowel": {
        "periodicity": "periodic (regular wave cycles)",
        "amplitude":   "high",
        "duration":    "longer than most consonants",
        "diagnostic":  "regular oscillation around zero, large amplitude",
    },
    "voiceless_stop": {
        "phases": [
            "closure: silence (flat line at zero amplitude)",
            "burst: vertical spike at release",
            "aspiration (if aspirated): aperiodic noise after burst",
        ],
        "diagnostic":  "silence followed by a sharp burst",
    },
    "voiced_stop": {
        "phases": [
            "closure: low-amplitude periodic activity (voicing during closure)",
            "burst: vertical spike at release",
            "no aspiration in English",
        ],
        "diagnostic":  "low-amplitude periodicity in closure, then burst",
    },
    "voiceless_fricative": {
        "periodicity": "aperiodic (random pattern)",
        "amplitude":   "medium",
        "duration":    "moderate to long",
        "diagnostic":  "noise-like pattern with no clear cycles",
    },
    "voiced_fricative": {
        "periodicity": "periodic + aperiodic (mixed)",
        "amplitude":   "medium",
        "diagnostic":  "noise overlaid on regular cycles",
    },
    "nasal": {
        "periodicity": "periodic (voiced)",
        "amplitude":   "low to medium (lower than vowels)",
        "diagnostic":  "regular cycles but smaller amplitude than adjacent vowels",
    },
    "liquid_or_glide": {
        "periodicity": "periodic (voiced)",
        "amplitude":   "medium (between nasal and vowel)",
        "diagnostic":  "vowel-like but lower amplitude; transitions blur into vowels",
    },
    "silence_or_pause": {
        "diagnostic":  "flat line at zero amplitude (no activity)",
    },
}

# ──────────────────────────────────────────────────────────────────────
# VOT categories and ranges (in milliseconds)
# ──────────────────────────────────────────────────────────────────────

VOT_CATEGORIES = {
    "negative": {
        "range_ms": "-150 to -10",
        "label":    "prevoiced",
        "description": "voicing begins BEFORE stop release",
        "english_context": "intervocalic voiced stops (less reliable phrase-initial)",
        "other_languages": "Spanish, French word-initial voiced stops",
    },
    "zero_or_short_lag": {
        "range_ms": "0 to 30",
        "label":    "unaspirated",
        "description": "voicing begins at or just after stop release",
        "english_context": "/b d g/ word-initial; /p t k/ after [s] (e.g., 'spy', 'sty', 'sky')",
    },
    "long_lag": {
        "range_ms": "30 to 100",
        "label":    "aspirated voiceless",
        "description": "voicing begins well after stop release; aspiration noise fills the gap",
        "english_context": "/pʰ tʰ kʰ/ word-initial / stressed-syllable-initial",
    },
}

# ──────────────────────────────────────────────────────────────────────
# Hint ladders per step
# ──────────────────────────────────────────────────────────────────────

HINT_LADDERS = {
    "identify_axes": [
        "Look at the bottom of the waveform. What's it labeled?",
        "It's time, usually in seconds or milliseconds. The y-axis is amplitude — "
        "shows the size of the wave (positive and negative around zero).",
        "If you see numbers like 0.0, 0.2, 0.4 on the x-axis, those are seconds. "
        "On the y-axis, the wave swings above and below zero.",
    ],
    "classify_region": [
        "Look at one region of the waveform. Is the pattern regular and "
        "repeating, or random?",
        "Regular and repeating = periodic = voicing. Random = aperiodic = "
        "voiceless or fricative noise.",
        "Now check amplitude. High amplitude periodic = vowel. Low amplitude "
        "periodic = sonorant consonant (nasal, liquid). Aperiodic = voiceless "
        "fricative or stop release.",
    ],
    "find_stop_phases": [
        "Look for a silent gap in the waveform — flat line at zero. That's "
        "the closure phase of a stop.",
        "After the silent gap, you should see a sudden vertical spike — that's "
        "the burst (release of the stop).",
        "After the burst, if there's aperiodic noise before voicing resumes, "
        "that's aspiration. If voicing starts immediately, no aspiration.",
    ],
    "mark_boundary": [
        "What kind of segment is to the LEFT of the boundary you're looking "
        "for? What kind is to the RIGHT?",
        "The boundary is where the visual cue changes — periodic to silence, "
        "noise to periodic, etc.",
        "Don't get distracted by amplitude changes WITHIN a segment (a vowel "
        "can swell and quiet without ending). The boundary is where the segment "
        "TYPE changes.",
    ],
    "measure_vot": [
        "Find the burst (the sharp vertical spike at stop release).",
        "Find where regular periodic cycles begin — that's voicing onset.",
        "Measure the time from burst to voicing onset. Positive (long) = "
        "aspirated. Zero or near-zero = unaspirated. Negative (voicing before "
        "burst) = prevoiced.",
    ],
}

# ──────────────────────────────────────────────────────────────────────
# Common errors
# ──────────────────────────────────────────────────────────────────────

COMMON_ERRORS = [
    {
        "id": "WV1",
        "trigger_phrases": ["the boundary is where amplitude changes",
                            "this loud part is one segment, this quiet part is another"],
        "description": "Treating amplitude changes within a segment as boundaries",
        "redirect": "Amplitude can change WITHIN a segment (vowels swell and "
                    "quiet, fricatives vary in intensity). The boundary is "
                    "where the segment TYPE changes — periodic to silence, "
                    "noise to periodic, etc.",
    },
    {
        "id": "WV2",
        "trigger_phrases": ["voiceless fricatives have no waveform",
                            "[s] has no signal"],
        "description": "Misconception that voiceless fricatives are silent",
        "redirect": "Voiceless fricatives have a clear waveform — it's just "
                    "aperiodic. The friction noise creates a noise-like pattern "
                    "with medium amplitude.",
    },
    {
        "id": "WV3",
        "trigger_phrases": ["the stop is one block",
                            "i can't see the closure"],
        "description": "Treating stops as a single homogeneous region",
        "redirect": "Stops have THREE phases: silent closure, burst spike, "
                    "and (sometimes) aspiration noise. Look for each one "
                    "separately.",
    },
    {
        "id": "WV4",
        "trigger_phrases": ["all english voiced stops are prevoiced",
                            "english /b/ has negative VOT"],
        "description": "Overgeneralizing prevoicing",
        "redirect": "In English, /b d g/ word-initial typically have ZERO or "
                    "short-lag VOT, not negative. Prevoicing is more reliable "
                    "intervocalically. Spanish /b d g/ ARE prevoiced word-initial — "
                    "different language, different pattern.",
    },
    {
        "id": "WV5",
        "trigger_phrases": ["i'll mark word boundaries",
                            "where does each word end?"],
        "description": "Trying to mark word boundaries on fluent speech",
        "redirect": "Word boundaries in fluent speech are perceptual, not "
                    "acoustic. There's often no visual gap between words. "
                    "Mark SEGMENT boundaries, not word boundaries.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# Tutor reminders
# ──────────────────────────────────────────────────────────────────────

TUTOR_REMINDERS = [
    "The student finds the boundary. Scaffold the visual cues.",
    "Periodicity = voicing. Always check periodicity first.",
    "Stops have THREE phases (closure, burst, aspiration). Don't conflate.",
    "Boundary = where segment TYPE changes, not where amplitude changes.",
    "Word boundaries on fluent speech are perceptual, not acoustic.",
    "If student lacks acoustic vocabulary (period, periodic, amplitude), "
    "hand off to validate-prereqs.",
]


# ──────────────────────────────────────────────────────────────────────
# Skill entry point
# ──────────────────────────────────────────────────────────────────────

def run(input):
    """Orchestrator entry point. Returns structured guidance."""
    return {
        "skill_id": "read-waveform",
        "skill_name": "Read Waveform",
        "version": "0.1.0",
        "flow": FLOW_STEPS,
        "segment_signatures": SEGMENT_SIGNATURES,
        "vot_categories": VOT_CATEGORIES,
        "hint_ladders": HINT_LADDERS,
        "common_errors": COMMON_ERRORS,
        "tutor_reminders": TUTOR_REMINDERS,
    }


# ──────────────────────────────────────────────────────────────────────
# Self-test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run({})
    assert result["skill_id"] == "read-waveform"
    assert len(result["flow"]) == 5
    assert "vowel" in result["segment_signatures"]
    assert "voiceless_stop" in result["segment_signatures"]
    assert "long_lag" in result["vot_categories"]
    assert len(result["common_errors"]) >= 4
    print("read-waveform/logic.py self-test passed.")
    print(f"  {len(result['flow'])} flow steps")
    print(f"  {len(result['segment_signatures'])} segment signatures")
    print(f"  {len(result['vot_categories'])} VOT categories")
    print(f"  {len(result['hint_ladders'])} hint ladders")
    print(f"  {len(result['common_errors'])} cataloged errors")
