# Project Guidance — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: none
> Last audited: 2026-09-14 @ commit `27696d6`

## Purpose
Document the repository-level files that govern agent behavior, environment setup, available local skills, and pending exercises.

## Tech stack & conventions
- `AGENTS.md` is the authoritative repository instruction file.
- Local reusable skills live under `.agents/skills/<skill>/SKILL.md`.
- `.atl/skill-registry.md` is generated indexing metadata, not a replacement for each skill contract.
- Conventional commits must not contain AI attribution or `Co-Authored-By` trailers.

## Structure
```text
./
├── AGENTS.md                         # ★ ENTRY POINT: agent and environment rules
├── .agents/harness-tasks.md          # Harness task tracking
├── .agents/skills/
│   ├── project-scaffold/             # Three-layer navigation workflow
│   ├── git-flow/                     # Branch strategy, PR workflow, divergence checks
│   ├── pseudocode-specific/          # Detailed educational pseudocode workflow
│   ├── pseudocode-general/           # High-level code flow description
│   └── python-notebook/              # Raw notebook JSON generation workflow
├── .atl/skill-registry.md            # Generated skill index
└── .gitignore                        # Ignored local artifacts
```

## Entry points
- `AGENTS.md` -> read before running GNU Radio-dependent Python or modifying the project.
- `.agents/skills/project-scaffold/SKILL.md` -> maintain this scaffold.
- `.agents/skills/git-flow/SKILL.md` -> branch strategy and PR workflow.
- `.agents/harness-tasks.md` -> discover unfinished project exercises.

## Key interactions
- **AGENTS.md -> scaffold:** directs agents through the scaffold before source inspection.
- **Skill registry -> SKILL.md:** the registry locates skills; the skill file supplies the actual contract.
- **GNU Radio -> virtual environment:** apt-installed Python modules require `python3 -m venv --system-site-packages .venv`.
- **Post-Task Gate:** verification checklist run after completing any task.
- **Dynamic packages:** agent detects and installs packages as needed, never hardcodes requirements.txt.

## Common tasks & gotchas
- First run `python3 -c "import gnuradio"`; install packages only if verification fails.
- Never create the project environment with an isolated `python3 -m venv .venv`.
- Refresh the skill registry after adding or changing skills; do not hand-edit generated registry content.
- Do NOT hardcode `requirements.txt`; detect and install packages dynamically per AGENTS.md.
- `develop` branch must never be deleted; it is the permanent integration branch.

## Open questions / TODO
- Consider adding notebook execution tests to CI pipeline.
- Refresh the generated skill registry only if skill files changed.
