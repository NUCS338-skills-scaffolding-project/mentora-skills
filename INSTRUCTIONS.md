# Using mentora-skills

`mentora-skills` is the master skills package for the Mentora tutoring system.
You do **not** develop skills here — you develop them in your own team repo.
This repo is read-only for teams.

---

## What this repo is for

- It is the single source of truth for all skills across all teams.
- It is automatically updated every 6 hours by syncing from each team repo.
- It is pip-installable so you can import and test your skills locally.

---

## Your workflow

1. **Write your skill** in your team repo under `skills/<skill-name>/skills.md` (and `logic.py` if it's a code skill).
2. **Push to your repo.** The sync runs automatically and picks up your changes within 6 hours.
3. **Test locally** by installing `mentora-skills` as a package (see below).

You never push directly to this repo. If your skill doesn't show up after a sync cycle, check the validation errors in the sync action logs.

---

## Installing as a package

Add this to your team repo's `requirements.txt`:

```
mentora-skills @ git+https://github.com/your-org/mentora-skills.git@main
```

Then install:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install git+https://github.com/your-org/mentora-skills.git@main
```

---

## Testing your skill locally

Once installed, you can import your skill directly:

```python
# Instructional skill — load the raw .md for inspection
from pathlib import Path
import mentora_skills

skills_root = Path(mentora_skills.__file__).parent / "skills"
md = (skills_root / "your_skill_name" / "skills.md").read_text()
print(md)
```

```python
# Code skill — run logic.py directly
from mentora_skills.skills.your_skill_name import logic

result = logic.run({
    "signature": "def foo(x: int) -> int",
    "n": 5
})
print(result)
```

Note: skill directory names use underscores (`your_skill_name`), even if your repo uses hyphens (`your-skill-name`). This is standard Python package naming.

---

## Skill ID collisions

If two teams use the same `skill_id`, only the first one wins. The second is rejected and logged in the sync report. If this happens to your skill:

1. Check the sync action logs in this repo for the rejection message.
2. Rename your skill's `skill_id` in `skills.md` to something unique.
3. Push the fix — it will be picked up on the next sync.

---

## Questions

If your skill isn't appearing after a sync cycle or you hit a validation error you can't resolve, reach out to the course staff.
