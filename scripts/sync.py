"""
sync.py — Delta sync: pull new/changed skills from team repos.

Runs on every git pull from a team repo and only processes files
that actually changed, keeping it fast regardless of catalog size.

Usage:
    python scripts/sync.py
    python scripts/sync.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT    = Path(__file__).parent.parent
TEAMS_CONFIG = REPO_ROOT / "config" / "teams.yaml"
CLONES_DIR   = REPO_ROOT / "clones"
SKILLS_DST   = REPO_ROOT / "mentora_skills" / "skills"

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def parse_skill_id(skills_md: Path) -> str | None:
    try:
        text = skills_md.read_text(encoding="utf-8")
        m = _FRONTMATTER_RE.match(text)
        meta = yaml.safe_load(m.group(1)) or {} if m else {}
        return meta.get("skill_id")
    except Exception:
        return None


def pull_and_diff(clone_path: Path) -> tuple[list[str], list[str]]:
    """Pull latest, return (changed_paths, deleted_paths) relative to clone root."""
    git(["pull", "--ff-only"], cwd=clone_path)
    result = git(["diff", "--name-status", "ORIG_HEAD..HEAD"], cwd=clone_path)

    if result.returncode != 0 or not result.stdout.strip():
        # First sync or no ORIG_HEAD — treat everything as new
        ls = git(["ls-files", "--", "*/skills.md"], cwd=clone_path)
        return [f.strip() for f in ls.stdout.splitlines() if f.strip()], []

    changed, deleted = [], []
    for line in result.stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2 or not parts[1].endswith("skills.md"):
            continue
        status, path = parts[0].strip(), parts[1].strip()
        (deleted if status.startswith("D") else changed).append(path)

    return changed, deleted


def copy_skill(src: Path, skill_id: str) -> None:
    module = skill_id.replace("-", "_")
    dst = SKILLS_DST / module
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / "skills.md", dst / "skills.md")
    if (src / "logic.py").exists():
        shutil.copy2(src / "logic.py", dst / "logic.py")
        (dst / "__init__.py").touch()


def remove_skill(module_name: str) -> None:
    dst = SKILLS_DST / module_name
    if dst.exists():
        shutil.rmtree(dst)
        print(f"  removed {module_name}")


def run(dry_run: bool = False) -> None:
    teams = yaml.safe_load(TEAMS_CONFIG.read_text(encoding="utf-8")).get("teams", [])
    if not teams:
        sys.exit("No teams in config/teams.yaml")

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from validate_skill import validate_skill_dir

    total_updated = total_removed = 0

    for team in teams:
        clone_path = CLONES_DIR / team["name"]
        if not clone_path.exists():
            print(f"  [WARN] {team['name']} not cloned — run import_skills.py first")
            continue

        print(f"\n── {team['name']} ──────────────────────────────────────────")
        skills_base = clone_path / team.get("skills_path", "skills/")
        changed, deleted = pull_and_diff(clone_path)

        for rel in changed:
            skills_md = clone_path / rel
            if not skills_md.exists():
                continue
            skill_dir = skills_md.parent
            try:
                skill_dir.relative_to(skills_base)
            except ValueError:
                continue

            skill_id = parse_skill_id(skills_md)
            if not skill_id:
                print(f"  [WARN] no skill_id in {rel}")
                continue

            result = validate_skill_dir(skill_dir)
            if not result.valid:
                print(f"  [WARN] {skill_id}: {result.errors[0]}")
                continue

            print(f"  update {skill_id}")
            if not dry_run:
                copy_skill(skill_dir, skill_id)
                total_updated += 1

        for rel in deleted:
            module = Path(rel).parent.name.replace("-", "_")
            print(f"  remove {module} (deleted upstream)")
            if not dry_run:
                remove_skill(module)
                total_removed += 1

    print(f"\nSync complete — updated: {total_updated}, removed: {total_removed}")
    if dry_run:
        print("(dry run — nothing written)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync skills from team repos")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
