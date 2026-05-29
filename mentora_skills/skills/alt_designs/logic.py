# logic.py — alt-designs
# Granular skill in Phase 3 (form-critique). Tracks whether the student has
# proposed at least one specific, feasible design change that addresses a
# prior critique with a defensible predicted claim_movement. Pure function;
# no side effects.

# VALID_METHODS reads from metadata.yaml.course_context.research_methods at
# module load. Hard-coded POLI SCI 210 defaults are used as a defensive
# fallback when metadata is unreadable, missing, or malformed. Adopters
# customize the method set by editing metadata.yaml only. See
# docs/audits/cross-cutting.md entry CC-2.
def _load_valid_methods():
    _DEFAULT = (
        "theory-data", "inference", "surveys", "experiments",
        "large-n", "small-n", "machine-learning",
    )
    try:
        import yaml
        from pathlib import Path
        md_path = Path(__file__).parent.parent.parent / "metadata.yaml"
        if not md_path.is_file():
            return _DEFAULT
        with open(md_path) as f:
            md = yaml.safe_load(f) or {}
        methods = (md.get("course_context") or {}).get("research_methods")
        if not isinstance(methods, list) or not methods:
            return _DEFAULT
        ids = []
        for m in methods:
            if isinstance(m, str):
                ids.append(m)
            elif isinstance(m, dict) and isinstance(m.get("id"), str):
                ids.append(m["id"])
            else:
                return _DEFAULT
        return tuple(ids) if ids else _DEFAULT
    except Exception:
        return _DEFAULT
    except Exception:
        return _DEFAULT


VALID_METHODS = _load_valid_methods()
MIN_ALTERNATIVES = 1
TARGET_ALTERNATIVES = 2

MIN_CHANGE_WORDS = 6
MIN_FEASIBILITY_WORDS = 4
MIN_CLAIM_MOVEMENT_WORDS = 6
MIN_TIE_WORDS = 4

GENERIC_CHANGE_CUES = (
  "be more careful",
  "be more rigorous",
  "use better methods",
  "collect more data",
  "use better data",
  "do more research",
  "improve the study",
  "better analysis",
)


def _is_generic_change(value):
  v_low = (value or "").strip().lower()
  if not v_low:
    return True
  return any(c in v_low for c in GENERIC_CHANGE_CUES)


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  change = (entry.get("change") or "").strip()
  addresses = (entry.get("addresses_critique") or "").strip()
  feasibility = (entry.get("feasibility") or "").strip()
  claim_movement = (entry.get("expected_claim_movement") or "").strip()
  if len(change.split()) < MIN_CHANGE_WORDS:
    return False
  if _is_generic_change(change):
    return False
  if len(addresses.split()) < MIN_TIE_WORDS:
    return False
  if len(feasibility.split()) < MIN_FEASIBILITY_WORDS:
    return False
  if len(claim_movement.split()) < MIN_CLAIM_MOVEMENT_WORDS:
    return False
  return True


INPUT_SCHEMA: dict = {
    "week": "int",
    "method": "str",
    "article_path": "str",
    "prior_session_logs": "list[str] | None",
    "prior_in_phase_scratchpads": "dict[str, str] | None",
    "alternatives": "list | None",
}


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "alternatives": list[{
      "change": str,                      # specific design change
      "addresses_critique": str,          # which prior critique it addresses
      "feasibility": str,                 # what would be needed
      "expected_claim_movement": str,     # predicted direction
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "generic_change_indices": list[int],
    "next_prompt": str,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  method = input.get("method")
  if method not in VALID_METHODS:
    raise ValueError(f"method={method!r} must be one of {VALID_METHODS}")

  alternatives = input.get("alternatives") or []
  if not isinstance(alternatives, list):
    raise ValueError("alternatives must be a list")

  complete = [a for a in alternatives if _entry_complete(a)]
  incomplete = [a for a in alternatives if not _entry_complete(a)]
  generic_indices = [
    i for i, a in enumerate(alternatives) if _is_generic_change(a.get("change"))
  ]

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "ask_first_alternative"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if len((last.get("change") or "").split()) < MIN_CHANGE_WORDS or _is_generic_change(last.get("change")):
      next_prompt = "ask_change"
    elif len((last.get("addresses_critique") or "").split()) < MIN_TIE_WORDS:
      next_prompt = "ask_addresses_critique"
    elif len((last.get("feasibility") or "").split()) < MIN_FEASIBILITY_WORDS:
      next_prompt = "ask_feasibility"
    else:
      next_prompt = "ask_claim_movement"
  elif len(complete) < MIN_ALTERNATIVES:
    next_prompt = "ask_next_alternative"
  elif len(complete) < TARGET_ALTERNATIVES:
    next_prompt = "offer_second_alternative"
  else:
    next_prompt = "reconcile_and_exit"

  done = len(complete) >= MIN_ALTERNATIVES

  done_reasons = []
  if len(complete) >= MIN_ALTERNATIVES:
    done_reasons.append(f"{len(complete)} fully-filled, non-generic alternative(s) logged")
  if not generic_indices:
    done_reasons.append("no generic change strings in the list")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (need {MIN_ALTERNATIVES}, target {TARGET_ALTERNATIVES}).",
    f"Incomplete entries: {len(incomplete)}.",
  ]
  if generic_indices:
    observations.append(
      f"Generic change strings detected at indices {generic_indices} — push for specifics."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would verify the change actually addresses the
  # cited critique (rather than being plausible-sounding but unrelated), would
  # judge feasibility against the research question's actual constraints, and
  # would test that expected_claim_movement is a real direction prediction
  # rather than "we'd find out."
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "generic_change_indices": generic_indices,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }


def render_progress(observations: list[dict], scope: str) -> dict:
  """Score this student's alt-designs practice for the Progress tab.

  See poli_sci-210-skills/docs/superpowers/specs/2026-05-17-render-progress-rubrics.md.

  Coverage formula: per-assignment max(raw_diagnostic.complete_count),
  summed across assignments touched. PROFICIENT_AT = 4.

  Args:
    observations: rows from skill_observations (already filtered to this
      skill + student; either all rows for the course or all rows for
      one assignment, depending on scope).
    scope: 'course' or 'assignment'.

  Returns:
    scope='course':     {status, score, headline}
    scope='assignment': {status, score, insight=None}
  """
  PROFICIENT_AT = 4  # calibration: review after fall pilot
  THRESHOLDS = (0.30, 0.60, 0.85)

  # Group by assignment_id; for each, take the high-water complete_count.
  by_asg: dict = {}
  for o in observations:
    diag = o.get("raw_diagnostic") or {}
    cc = diag.get("complete_count")
    if not isinstance(cc, (int, float)) or isinstance(cc, bool):
      continue  # missing or non-numeric → treat as 0
    asg = o.get("assignment_id")
    if asg is None:
      continue
    by_asg[asg] = max(by_asg.get(asg, 0), int(cc))

  if scope == "course":
    cumulative = sum(by_asg.values())
    score = min(1.0, cumulative / PROFICIENT_AT)
  else:  # 'assignment'
    cumulative = max(by_asg.values()) if by_asg else 0
    score = min(1.0, cumulative / PROFICIENT_AT)

  if score >= THRESHOLDS[2]:
    status = "proficient"
  elif score >= THRESHOLDS[1]:
    status = "advanced"
  elif score >= THRESHOLDS[0]:
    status = "developing"
  else:
    status = "learning"

  if scope == "course":
    return {
      "status": status,
      "score": score,
      "headline": f"{cumulative} of 4 design alternatives proposed",
    }
  else:
    return {
      "status": status,
      "score": score,
      "insight": None,  # caller falls back to _default_insight
    }
