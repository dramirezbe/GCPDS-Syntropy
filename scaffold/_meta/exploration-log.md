# Exploration Log

> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Preserve raw Phase 1 repository findings used to synthesize the scaffold hierarchy.

## Tech stack & conventions
- Findings are evidence snapshots, not higher-authority replacements for repository files.
- Dates and audited commit IDs identify when observations were verified.
- Future exploration should append or revise findings when source structure changes.

## Structure
```text
Repository findings
├── Root guidance and backlog
├── Notebook curriculum and report
├── Prompt contracts
└── Local skill metadata
```

## Entry points
- `scaffold/INDEX.md` -> synthesized navigation derived from these findings.
- `scaffold/_meta/manifest.json` -> machine-readable hierarchy produced from the same audit.

## Key interactions
- **Raw findings -> layer docs:** section documents summarize the verified evidence below.
- **Source changes -> new audit:** stale claims must be corrected in both this log and affected scaffold documents.

## Common tasks & gotchas
- Do not treat prompt examples as implemented code.
- Hidden directories contain project skills and generated registry information that matter to agent navigation.

## Open questions / TODO
- Verify future notebook execution in a clean environment if reproducibility becomes part of the scaffold audit.

## Phase 1 findings — 2026-09-12
- Git branch `main` matched `origin/main`; audited commit was `ce73307`; working tree was clean before scaffold creation.
- No scaffold directory existed.
- Root contained `AGENTS.md`, `tasks.md`, `.gitignore`, three local skills, a generated skill registry, eight notebooks, one generation report, and seven prompt/criterion files.
- The notebook generation report declares all eight notebooks complete and records canonical IQ shape `(N, 2, L)`, `float32`, and seed 42.
- All tracked notebooks had zero stored outputs at audit time.
- Notebook dependencies observed from code were NumPy, Matplotlib, and standard-library `pathlib`.
- Notebook 5 can create `demo_iq.npz`; no tracked data files exist.
- `prompts/create-nbs.md` references `prompts/nb-pass-criterion.txt`, but the tracked criterion is `prompts/pass-criterion.txt`.
- The GNU Radio prompt proposes a complex source, a float IIR block, and a complex sink; block signatures need verification before execution.
- The repository has no README, dependency lockfile, automated notebook execution suite, or implemented IIR script.
