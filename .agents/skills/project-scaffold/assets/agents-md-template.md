# AGENTS.md — {Project Name}

## Exploration Protocol (MANDATORY)

**Every AI agent MUST follow this order. No exceptions.**

### Step 1: Scaffold First (always)

Before touching any source code, read the scaffold:

1. `scaffold/INDEX.md` — full map of all sections and sub-sections
2. `scaffold/<section>/main.md` — Layer 1 overview of the section you need
3. `scaffold/<section>/<sub>/main.md` — Layer 2 detail of the specific sub-section

**Why:** The scaffold was built to let you understand structure without reading every file. It contains purpose, tech stack, file structure, entry points, key interactions, common tasks, and open questions for every section.

### Step 2: Source Code (only after scaffold)

Only after reading the relevant scaffold docs, use standard tools:
- `grep` / `rg` — find symbols, functions, patterns
- `find` / `glob` — find files by name
- `read` — read specific files for implementation details

**Never skip scaffold to go straight to grep.** You'll waste tokens and miss context.

### Step 3: Verify claims

If the scaffold says something and the code seems different, trust the code — but update the scaffold afterward.

## Repo Map

| Section | Purpose | Docs |
|---------|---------|------|
| {section} | {purpose} | [scaffold/{section}/main.md](scaffold/{section}/main.md) |

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and quick start |
| `scaffold/_meta/manifest.json` | Machine-readable scaffold index |
| `scaffold/_meta/exploration-log.md` | Raw exploration findings |
