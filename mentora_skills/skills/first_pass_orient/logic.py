# logic.py — first-pass-orient
# Granular skill in Phase 1 (orient-paper). Tracks whether the student
# has produced a clean one-sentence puzzle and one-sentence answer in their
# own words. Pure function; no side effects.

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
MAX_SENTENCE_WORDS = 30
TOPIC_RESTATEMENT_CUES = ("they study", "this paper studies", "this paper is about", "they look at")


def _word_count(s):
  return len(s.split())


def _looks_like_topic_restatement(s):
  s_low = s.lower().strip()
  return any(s_low.startswith(c) for c in TOPIC_RESTATEMENT_CUES)


INPUT_SCHEMA: dict = {
    "week": "int",
    "method": "str",
    "article_path": "str",
    "prior_session_logs": "list[str] | None",
    "puzzle": "str | None",
    "answer": "str | None",
    "abstract_overlap_high": "bool | None",
}


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,    # from main orchestrator (empty for Phase 1)
    "puzzle": str | None,                      # student's one-sentence puzzle
    "answer": str | None,                      # student's one-sentence answer
    "abstract_overlap_high": bool | None,      # heuristic flag from tutor (or LLM stub)
  }
  :return: {
    "puzzle_ok": bool,
    "answer_ok": bool,
    "next_prompt": str,                        # which step the tutor should run next
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

  puzzle = (input.get("puzzle") or "").strip()
  answer = (input.get("answer") or "").strip()
  parrot = bool(input.get("abstract_overlap_high"))

  puzzle_ok = bool(puzzle) and _word_count(puzzle) <= MAX_SENTENCE_WORDS and not parrot
  answer_ok = (
    bool(answer)
    and _word_count(answer) <= MAX_SENTENCE_WORDS
    and not parrot
    and not _looks_like_topic_restatement(answer)
  )

  if not puzzle:
    next_prompt = "ask_puzzle"
  elif not puzzle_ok:
    next_prompt = "redo_puzzle"
  elif not answer:
    next_prompt = "ask_answer"
  elif not answer_ok:
    next_prompt = "redo_answer"
  else:
    next_prompt = "reconcile_and_exit"

  done = puzzle_ok and answer_ok
  done_reasons = []
  if puzzle_ok:
    done_reasons.append("puzzle is one short sentence and not abstract-parroting")
  if answer_ok:
    done_reasons.append("answer is one short sentence, not parroting, not a topic restatement")

  observations = [
    f"Method: {method}.",
    f"Puzzle: {'present' if puzzle else 'missing'}{' (over length)' if puzzle and _word_count(puzzle) > MAX_SENTENCE_WORDS else ''}.",
    f"Answer: {'present' if answer else 'missing'}{' (over length)' if answer and _word_count(answer) > MAX_SENTENCE_WORDS else ''}.",
  ]
  if parrot:
    observations.append("Abstract-overlap flag is HIGH — student is parroting the abstract.")
  if answer and _looks_like_topic_restatement(answer):
    observations.append("Answer reads as a topic restatement, not a finding ('they study...').")
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would compare puzzle/answer against the
  # abstract for paraphrased parroting (rather than verbatim overlap), and
  # would also verify the answer names a finding rather than a topic.
  return {
    "puzzle_ok": puzzle_ok,
    "answer_ok": answer_ok,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }


def render_progress(observations: list[dict], scope: str) -> dict:
  """Score this student's first-pass-orient practice for the Progress tab.

  See poli_sci-210-skills/docs/superpowers/specs/2026-05-17-render-progress-rubrics.md.

  Coverage formula: count of distinct assignments where any row has
  raw_diagnostic['done'] == True. PROFICIENT_AT = 4.

  Args:
    observations: rows from skill_observations (already filtered to this
      skill + student; either all rows for the course or all rows for
      one assignment, depending on scope).
    scope: 'course' or 'assignment'.

  Returns:
    scope='course':     {status, score, headline}
    scope='assignment': {status, score, insight=None}
  """
  PROFICIENT_AT = 4
  THRESHOLDS = (0.30, 0.60, 0.85)

  # Group by assignment_id; for each, 1 if any row has done=True, else 0.
  by_asg: dict = {}
  for o in observations:
    diag = o.get("raw_diagnostic") or {}
    cc = 1 if diag.get("done") else 0
    asg = o.get("assignment_id")
    if asg is None:
      continue
    by_asg[asg] = max(by_asg.get(asg, 0), cc)

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
      "headline": f"{cumulative} of 4 papers oriented",
    }
  else:
    return {
      "status": status,
      "score": score,
      "insight": None,  # caller falls back to _default_insight
    }
