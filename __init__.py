"""
mentora_skills — Master skills package for the Mentora tutoring system.

Provides:
  - A pip-installable catalog of all tutoring skills
  - catalog.load()  → list of slim skill dicts (for selection)
  - catalog.load_skill_md(skill_id) → raw skills.md text (for execution)
  - Direct import of code-skill logic modules, e.g.:
        from mentora_skills.skills.edge_case_gen import logic
        result = logic.run(inputs)
"""

__version__ = "0.1.0"
