# Project Guidance — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: none
> Last audited: 2026-09-12 @ commit `ce73307`

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
├── tasks.md                          # Informal backlog
├── .agents/skills/
│   ├── project-scaffold/             # Three-layer navigation workflow
│   ├── pseudocode/                   # Educational pseudocode workflow
│   └── python-notebook/              # Raw notebook JSON generation workflow
├── .atl/skill-registry.md            # Generated skill index
└── .gitignore                        # Ignored local artifacts
```

## Entry points
- `AGENTS.md` -> read before running GNU Radio-dependent Python or modifying the project.
- `.agents/skills/project-scaffold/SKILL.md` -> maintain this scaffold.
- `tasks.md` -> discover unfinished project exercises; verify before treating items as requirements.

## Key interactions
- **AGENTS.md -> scaffold:** directs agents through the scaffold before source inspection.
- **Skill registry -> SKILL.md:** the registry locates skills; the skill file supplies the actual contract.
- **GNU Radio -> virtual environment:** apt-installed Python modules require `python3 -m venv --system-site-packages .venv`.

## Common tasks & gotchas
- First run `python3 -c "import gnuradio"`; install packages only if verification fails.
- Never create the project environment with an isolated `python3 -m venv .venv`.
- Refresh the skill registry after adding or changing skills; do not hand-edit generated registry content.
- `tasks.md` is a planning note and includes items that may already be partially completed.

## Open questions / TODO
- Clarify which `tasks.md` items remain current and which are historical.
- Refresh the generated skill registry only if scaffold creation is meant to be indexed as a skill change; no skill changed in this operation.
