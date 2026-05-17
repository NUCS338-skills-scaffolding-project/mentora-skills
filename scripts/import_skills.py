"""
import_skills.py — One-time migration: clone team repos and import their skills.

Workflow:
  1. Read config/teams.yaml
  2. Clone each repo into clones/<team>/ (or pull if already cloned)
  3. Discover all skills.md files under the team's skills_path
  4. Validate each skill
  5. Detect skill_id collisions across teams → write collision_report.yaml
  6. Copy clean skills into mentora_skills/skills/ (hyphens → underscores)
  7. Add __init__.py only if logic.py is present

Usage:
    python scripts/import_skills.py
    python scripts/import_skills.py --resolve collision_report.yaml
    python scripts/import_skills.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT      = Path(__file__).parent.parent
TEAMS_CONFIG   = REPO_ROOT / "config" / "teams.yaml"
CLONES_DIR     = REPO_ROOT / "clones"
SKILLS_DST     = REPO_ROOT / "mentora_skills" / "skills"
COLLISION_FILE = REPO_ROOT / "collision_report.yaml"

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_skill_id(skills_md: Path) -> str | None:
    try:
        text = skills_md.read_text(encoding="utf-8")
        m = _FRONTMATTER_RE.match(text)
        meta = yaml.safe_load(m.group(1)) or {} if m else {}
        return meta.get("skill_id")
    except Exception:
        return None


def git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def clone_or_pull(team: dict) -> Path | None:
    path = CLONES_DIR / team["name"]
    if path.exists():
        print(f"  pulling {team['name']}...")
        r = git(["pull", "--ff-only"], cwd=path)
        if r.returncode != 0:
            print(f"  [WARN] pull failed: {r.stderr.strip()}")
    else:
        print(f"  cloning {team['name']}...")
        CLONES_DIR.mkdir(parents=True, exist_ok=True)
        r = git(["clone", "--depth", "1", "-b",
                 team.get("branch", "main"), team["repo"], str(path)])
        if r.returncode != 0:
            print(f"  [ERROR] clone failed: {r.stderr.strip()}")
            return None
    return path


def copy_skill(src: Path, skill_id: str, rename_to: str | None = None) -> None:
    """Copy a skill into mentora_skills/skills/ using underscore naming."""
    target_id = (rename_to or skill_id).replace("-", "_")
    dst = SKILLS_DST / target_id
    dst.mkdir(parents=True, exist_ok=True)

    shutil.copy2(src / "skills.md", dst / "skills.md")

    # If renaming, update skill_id in frontmatter
    if rename_to and rename_to != skill_id:
        text = (dst / "skills.md").read_text(encoding="utf-8")
        text = re.sub(rf'skill_id:\s*["\']?{re.escape(skill_id)}["\']?',
                      f'skill_id: "{rename_to}"', text, count=1)
        (dst / "skills.md").write_text(text, encoding="utf-8")

    if (src / "logic.py").exists():
        shutil.copy2(src / "logic.py", dst / "logic.py")
        (dst / "__init__.py").touch()


def write_collision_report(collisions: dict[str, list[dict]]) -> None:
    entries = [
        {
            "skill_id": sid,
            "status": "pending",
            "candidates": cands,
            "resolution": {
                "action": "keep",           # keep | rename | drop
                "keep": cands[0]["team"],
                "renames": {},              # {team: new_skill_id} when action=rename
                "notes": "",
            },
        }
        for sid, cands in collisions.items()
    ]
    COLLISION_FILE.write_text(
        yaml.dump({"collisions": entries}, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"\ncollision_report.yaml → {COLLISION_FILE}")
    print("Fill in each 'resolution' block, then re-run with --resolve collision_report.yaml")


def run(dry_run: bool = False, resolve_path: Path | None = None) -> None:
    teams = yaml.safe_load(TEAMS_CONFIG.read_text(encoding="utf-8")).get("teams", [])
    if not teams:
        sys.exit("No teams in config/teams.yaml")

    resolutions: dict = {}
    if resolve_path:
        data = yaml.safe_load(resolve_path.read_text(encoding="utf-8")) or {}
        resolutions = {c["skill_id"]: c for c in data.get("collisions", [])}

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from validate_skill import validate_skill_dir

    # ── Discover all skills across teams ──────────────────────────────
    print("\n── Cloning team repos ──────────────────────────────────────")
    all_skills: dict[str, list[dict]] = {}

    for team in teams:
        clone_path = clone_or_pull(team)
        if not clone_path:
            continue
        base = clone_path / team.get("skills_path", "skills/")
        if not base.exists():
            print(f"  [WARN] skills_path not found in {team['name']}")
            continue
        found = 0
        for skill_dir in sorted(d for d in base.iterdir()
                                 if d.is_dir() and (d / "skills.md").exists()):
            sid = parse_skill_id(skill_dir / "skills.md")
            if sid:
                all_skills.setdefault(sid, []).append({
                    "team": team["name"], "path": str(skill_dir),
                    "name": sid, "version": "0.1.0",
                })
                found += 1
        print(f"  {team['name']}: {found} skills found")

    # ── Detect collisions ─────────────────────────────────────────────
    print("\n── Checking collisions ─────────────────────────────────────")
    collisions = {sid: c for sid, c in all_skills.items() if len(c) > 1}
    if collisions and not resolutions:
        print(f"  {len(collisions)} collision(s): {', '.join(collisions)}")
        write_collision_report(collisions)
        print("\nImporting non-colliding skills only.")
    elif collisions:
        print(f"  {len(collisions)} collision(s) — applying resolutions")
    else:
        print("  No collisions.")

    # ── Copy skills ───────────────────────────────────────────────────
    print("\n── Importing skills ────────────────────────────────────────")
    imported = skipped_col = skipped_inv = 0

    for skill_id, candidates in all_skills.items():
        if len(candidates) > 1:
            if skill_id not in resolutions:
                skipped_col += 1
                continue
            res = resolutions[skill_id].get("resolution", {})
            action = res.get("action", "keep")
            if action == "drop":
                print(f"  drop   {skill_id}")
                continue
            elif action == "rename":
                for c in candidates:
                    new_id = res.get("renames", {}).get(c["team"])
                    if new_id:
                        print(f"  rename {skill_id} ({c['team']}) → {new_id}")
                        if not dry_run:
                            copy_skill(Path(c["path"]), skill_id, rename_to=new_id)
                            imported += 1
                continue
            else:
                keep = res.get("keep", candidates[0]["team"])
                candidates = [c for c in candidates if c["team"] == keep][:1]

        src = Path(candidates[0]["path"])
        result = validate_skill_dir(src)
        if not result.valid:
            print(f"  skip   {skill_id}  ({result.errors[0]})")
            skipped_inv += 1
            continue

        print(f"  import {skill_id}")
        if not dry_run:
            copy_skill(src, skill_id)
            imported += 1

    print(f"\nDone — imported: {imported}, skipped collisions: {skipped_col}, skipped invalid: {skipped_inv}")
    if dry_run:
        print("(dry run — nothing written)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import skills from team repos")
    parser.add_argument("--resolve", type=Path, metavar="REPORT")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run, resolve_path=args.resolve)


if __name__ == "__main__":
    main()
