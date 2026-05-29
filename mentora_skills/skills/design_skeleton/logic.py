# logic.py — design-skeleton
# Granular skill in Phase 2 (map-design). Tracks whether the
# student has filled in the seven canonical research-design fields with
# substance. n/a-with-rationale counts as filled. Pure function; no side
# effects.

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
FIELDS = [
  "research_question",
  "unit_of_analysis",
  "sample",
  "iv_or_treatment",
  "dv_or_outcome",
  "identification_strategy",
  "comparison",
]

MIN_FILLED = 5
MIN_FIELD_WORDS = 4
MIN_NA_RATIONALE_WORDS = 4

GENERIC_IDENT_CUES = ("regression", "experiment", "survey", "analysis", "study", "research")


def _field_filled(value):
  """A field is 'filled' if it's substantive prose OR an n/a with rationale."""
  if value is None:
    return False
  v = str(value).strip()
  if not v:
    return False
  v_low = v.lower()
  if v_low.startswith("n/a"):
    rationale = v.split("—", 1)[-1] if "—" in v else v.split("-", 1)[-1] if "-" in v else ""
    return len(rationale.strip().split()) >= MIN_NA_RATIONALE_WORDS
  return len(v.split()) >= MIN_FIELD_WORDS


def _identification_is_generic(value):
  if not value:
    return False
  v_low = str(value).strip().lower()
  if v_low.startswith("n/a"):
    return False
  word_count = len(v_low.split())
  cue_hit = any(c in v_low for c in GENERIC_IDENT_CUES)
  return cue_hit and word_count <= 4


INPUT_SCHEMA: dict = {
    "week": "int",
    "method": "str",
    "article_path": "str",
    "prior_session_logs": "list[str] | None",
    "prior_in_phase_scratchpads": "dict[str, str] | None",
    "design": "dict | None",
}


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "design": {
      "research_question": str | None,
      "unit_of_analysis": str | None,
      "sample": str | None,
      "iv_or_treatment": str | None,             # may be "n/a — <reason>"
      "dv_or_outcome": str | None,
      "identification_strategy": str | None,
      "comparison": str | None,                  # may be "n/a — <reason>"
    } | None,
  }
  :return: {
    "filled_fields": list[str],
    "missing_fields": list[str],
    "identification_generic": bool,
    "next_field": str | None,                    # next field to ask about, in order
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

  design = input.get("design") or {}
  if not isinstance(design, dict):
    raise ValueError("design must be a dict")

  filled = [f for f in FIELDS if _field_filled(design.get(f))]
  missing = [f for f in FIELDS if not _field_filled(design.get(f))]
  ident_generic = _identification_is_generic(design.get("identification_strategy"))

  next_field = missing[0] if missing else None

  ident_filled = "identification_strategy" in filled
  done = (
    len(filled) >= MIN_FILLED
    and ident_filled
    and not ident_generic
  )

  done_reasons = []
  if len(filled) >= MIN_FILLED:
    done_reasons.append(f"{len(filled)} of {len(FIELDS)} fields are substantively filled")
  if ident_filled:
    done_reasons.append("identification_strategy is filled")
  if ident_filled and not ident_generic:
    done_reasons.append("identification_strategy is method-specific (not 'regression'/'experiment'/'study')")

  observations = [
    f"Method: {method}.",
    f"Filled: {len(filled)}/{len(FIELDS)} ({', '.join(filled) or 'none'}).",
    f"Missing: {len(missing)} ({', '.join(missing) or 'none'}).",
  ]
  if ident_generic:
    observations.append(
      "identification_strategy reads as generic — push for the specific identifying logic."
    )
  if next_field:
    observations.append(f"Next field to ask about: {next_field}.")
  else:
    observations.append("All fields filled — go to reconcile-and-exit.")

  # LLM stub: a semantic check would verify each field's substance is
  # method-appropriate (e.g., catching a survey paper whose
  # identification_strategy is described in pure regression-only terms with no
  # mention of sampling logic).
  return {
    "filled_fields": filled,
    "missing_fields": missing,
    "identification_generic": ident_generic,
    "next_field": next_field,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }


def render_progress(observations: list[dict], scope: str) -> dict:
  """Score this student's design-skeleton practice for the Progress tab.

  See poli_sci-210-skills/docs/superpowers/specs/2026-05-17-render-progress-rubrics.md.

  Coverage formula (fractional model): per-assignment
  max(len(filled_fields) / 7), summed across assignments touched.
  PROFICIENT_AT = 3 (equivalent to 3 fully-completed skeletons).

  Args:
    observations: rows from skill_observations (already filtered to this
      skill + student; either all rows for the course or all rows for
      one assignment, depending on scope).
    scope: 'course' or 'assignment'.

  Returns:
    scope='course':     {status, score, headline}
    scope='assignment': {status, score, insight=None}
  """
  PROFICIENT_AT = 3  # calibration: review after fall pilot
  THRESHOLDS = (0.30, 0.60, 0.85)

  # Group by assignment_id; for each, take the high-water fractional fill.
  by_asg: dict = {}
  for o in observations:
    diag = o.get("raw_diagnostic") or {}
    filled_fields = diag.get("filled_fields") or []
    cc = len(filled_fields) / 7
    asg = o.get("assignment_id")
    if asg is None:
      continue
    by_asg[asg] = max(by_asg.get(asg, 0.0), cc)

  if scope == "course":
    cumulative = sum(by_asg.values())
    score = min(1.0, cumulative / PROFICIENT_AT)
  else:  # 'assignment'
    cumulative = max(by_asg.values()) if by_asg else 0.0
    score = min(1.0, cumulative / PROFICIENT_AT)

  if score >= THRESHOLDS[2]:
    status = "proficient"
  elif score >= THRESHOLDS[1]:
    status = "advanced"
  elif score >= THRESHOLDS[0]:
    status = "developing"
  else:
    status = "learning"

  # For headline, show cumulative as a rounded count of skeletons-worth.
  cumulative_display = round(cumulative, 2)
  if scope == "course":
    return {
      "status": status,
      "score": score,
      "headline": f"{cumulative_display} of 3 design skeletons completed",
    }
  else:
    return {
      "status": status,
      "score": score,
      "insight": None,  # caller falls back to _default_insight
    }
