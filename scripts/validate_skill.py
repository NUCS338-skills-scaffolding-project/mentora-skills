"""
validate_skill.py — Validates a skill directory before it enters the package.

Checks:
  1. skills.md exists with valid YAML frontmatter
  2. Required fields present: skill_id, name, skill_type, tags, trigger_signals
  3. Field values are correct types
  4. For code skills: logic.py is present
  5. Collision detection across a batch

Usage:
    # Single skill
    python scripts/validate_skill.py mentora_skills/skills/bound_scope

    # All skills
    python scripts/validate_skill.py --all mentora_skills/skills/
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REQUIRED_FIELDS  = ["skill_id", "name", "skill_type", "tags", "trigger_signals"]
VALID_TYPES      = {"instructional", "code"}
VALID_STATUSES   = {"ready", "stub", "broken"}
VALID_STANCES    = {"socratic", "hint", "reframe", "meta"}
_FRONTMATTER_RE  = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


@dataclass
class ValidationResult:
    skill_id: str = ""
    path: str = ""
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.valid = False
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def __str__(self) -> str:
        icon = "✓" if self.valid else "✗"
        lines = [f"{icon} {self.skill_id or self.path}"]
        for e in self.errors:
            lines.append(f"    ERROR: {e}")
        for w in self.warnings:
            lines.append(f"    WARN:  {w}")
        return "\n".join(lines)


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    return yaml.safe_load(m.group(1)) or {} if m else {}


def validate_skill_dir(skill_dir: Path) -> ValidationResult:
    result = ValidationResult(path=str(skill_dir))

    skills_md = skill_dir / "skills.md"
    if not skills_md.exists():
        result.fail("skills.md not found")
        return result

    try:
        text = skills_md.read_text(encoding="utf-8")
        m = _FRONTMATTER_RE.match(text)
        if not m:
            result.fail("No YAML frontmatter found (missing --- delimiters)")
            return result
        meta = yaml.safe_load(m.group(1)) or {}
    except Exception as exc:
        result.fail(f"Failed to parse frontmatter: {exc}")
        return result

    # Required fields
    for f in REQUIRED_FIELDS:
        if f not in meta or meta[f] is None:
            result.fail(f"Missing required field: '{f}'")
    if result.errors:
        return result

    skill_id = str(meta["skill_id"])
    result.skill_id = skill_id

    # skill_id should use underscores (new convention)
    if "-" in skill_id:
        result.warn(f"skill_id '{skill_id}' uses hyphens — use underscores instead")

    # Directory name should match skill_id (underscored)
    expected = skill_id.replace("-", "_")
    if skill_dir.name != expected:
        result.warn(f"Directory '{skill_dir.name}' does not match skill_id '{skill_id}' (expected '{expected}')")

    # Type
    skill_type = meta["skill_type"]
    if skill_type not in VALID_TYPES:
        result.fail(f"'skill_type' must be one of {VALID_TYPES}, got '{skill_type}'")

    # Tags and trigger_signals
    if not isinstance(meta["tags"], list) or len(meta["tags"]) == 0:
        result.fail("'tags' must be a non-empty list")
    if not isinstance(meta["trigger_signals"], list) or len(meta["trigger_signals"]) == 0:
        result.fail("'trigger_signals' must be a non-empty list")

    # Optional fields
    if "status" in meta and meta["status"] not in VALID_STATUSES:
        result.fail(f"'status' must be one of {VALID_STATUSES}, got '{meta['status']}'")
    if "stance" in meta and meta["stance"] not in VALID_STANCES:
        result.fail(f"'stance' must be one of {VALID_STANCES}, got '{meta['stance']}'")

    # Code skill: logic.py must exist
    if skill_type == "code" and not (skill_dir / "logic.py").exists():
        result.fail("skill_type is 'code' but logic.py is missing")

    # Instructional skill: warn if no Flow section
    if skill_type == "instructional" and "## Flow" not in text:
        result.warn("No '## Flow' section found in skills.md")

    return result


def validate_directory(skills_dir: Path) -> tuple[list[ValidationResult], list[str]]:
    """Validate all skills in a directory, also checking for skill_id collisions."""
    results: list[ValidationResult] = []
    seen: dict[str, str] = {}
    collisions: list[str] = []

    for skill_dir in sorted(d for d in skills_dir.iterdir()
                            if d.is_dir() and not d.name.startswith(("_", "."))):
        result = validate_skill_dir(skill_dir)
        results.append(result)

        if result.valid and result.skill_id:
            if result.skill_id in seen:
                result.fail(f"skill_id '{result.skill_id}' already used by '{seen[result.skill_id]}'")
                collisions.append(result.skill_id)
            else:
                seen[result.skill_id] = str(skill_dir)

    return results, collisions


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate skill directories")
    parser.add_argument("path", type=Path)
    parser.add_argument("--all", action="store_true",
                        help="Validate all skills under path")
    args = parser.parse_args()

    if args.all:
        results, collisions = validate_directory(args.path)
        for r in results:
            print(r)
        passed = sum(1 for r in results if r.valid)
        failed = len(results) - passed
        print(f"\n{passed} passed, {failed} failed", end="")
        if collisions:
            print(f", {len(collisions)} collision(s): {', '.join(collisions)}", end="")
        print()
        sys.exit(0 if failed == 0 else 1)
    else:
        result = validate_skill_dir(args.path)
        print(result)
        sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
