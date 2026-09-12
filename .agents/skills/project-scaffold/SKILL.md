---
name: project-scaffold
description: "Trigger: create scaffold, scaffold docs, project scaffold, setup scaffold, scaffold this repo. Generate and maintain a 3-layer documentation scaffold for AI agent navigation of monorepos."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use this skill when:
- an AI agent needs to explore or modify a codebase without reading every file;
- a monorepo lacks structured navigation docs;
- onboarding new agents to the project is expensive.

Do not use for:
- single-file projects;
- documentation intended primarily for humans (use README.md instead);
- one-off exploration that will not be reused.

## Hard Rules

- Create `scaffold/INDEX.md` first. No section main.md may exist without a parent index.
- Use exactly 3 layers: INDEX (layer 0), section main.md (layer 1), sub-section main.md (layer 2).
- Every `.md` must have: Purpose, Tech stack & conventions, Structure, Entry points, Key interactions, Common tasks & gotchas, Open questions / TODO.
- Maintain `scaffold/_meta/manifest.json` as a machine-readable mirror of the hierarchy.
- Maintain `scaffold/_meta/exploration-log.md` with raw findings; layer files synthesize from it.
- Never skip scaffold to go straight to grep — update the scaffold when code diverges from it.

## Decision Gates

| Situation | Action |
| --- | --- |
| Scaffold already exists | Update stale sections; do not recreate from scratch |
| Section has >3 sub-areas | Split into layer-2 sub-sections |
| Section is small and homogeneous | Stop at layer 1; no layer 2 |
| Code changed significantly | Audit the section and update its scaffold docs |
| New section added | Append to INDEX.md, create layer-1 main.md, then layer-2 if needed |

## Execution Steps

1. Read `assets/scaffold-index-template.md` and create `scaffold/INDEX.md` with the section map.
2. For each section, read `assets/layer1-template.md` and create `scaffold/<section>/main.md`.
3. For each heterogeneous section, read `assets/layer2-template.md` and create sub-section mains.
4. Read `assets/manifest-schema.json` and create `scaffold/_meta/manifest.json`.
5. Create `scaffold/_meta/exploration-log.md` with raw Phase 1 findings.
6. Add an `AGENTS.md` at repo root pointing to `scaffold/INDEX.md`.
7. After any code change that invalidates scaffold content, update the affected layer files.

## Output Contract

Return:
- Files created or modified (list every path);
- Layer coverage: which sections have layer 1 vs layer 2;
- Any ambiguities or TODOs that should be resolved in future sessions;
- Whether `manifest.json` needs a registry refresh.

## References

- `assets/scaffold-index-template.md` — INDEX.md template
- `assets/layer1-template.md` — Layer 1 section template
- `assets/layer2-template.md` — Layer 2 sub-section template
- `assets/manifest-schema.json` — manifest.json schema
- `assets/agents-md-template.md` — Root AGENTS.md template
