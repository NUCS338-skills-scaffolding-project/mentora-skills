"""
mentora_skills — Master skills package for the Mentora tutoring system.

Install:
    pip install -e .

Usage in the orchestrator:
    # Load a skill's full .md for system prompt construction
    from pathlib import Path
    import mentora_skills
    skills_dir = Path(mentora_skills.__file__).parent / "skills"
    md = (skills_dir / "edge_case_gen" / "skills.md").read_text()

    # Import and run a code skill's logic directly
    from mentora_skills.skills.edge_case_gen import logic
    result = logic.run(inputs)
"""

__version__ = "0.1.0"
