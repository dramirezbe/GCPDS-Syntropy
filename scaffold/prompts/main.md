# Prompts — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: [notebook-generation](./notebook-generation/main.md), [iir-workflows](./iir-workflows/main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Collect reusable instructions that generate the Pre-M0 notebooks or guide future IIR-filter implementation and Git workflow exercises.

## Tech stack & conventions
- Markdown prompt artifacts default to English.
- Paths prefixed with `@` identify repository inputs or output directories.
- `prompts/pass-criterion.txt` is authoritative for notebook acceptance.
- IIR prompts target Python, NumPy/SciPy, Matplotlib, GNU Radio, or pseudocode depending on the workflow.

## Structure
```text
prompts/
├── create-nbs.md                         # ★ ENTRY POINT: eight-notebook generation contract
├── pass-criterion.txt                    # Mandatory learner outcomes
├── iir-plain-instructions-to-code.md     # Natural language -> SciPy implementation
├── iir-pseudocode-to-code.md             # Pseudocode -> SciPy implementation
├── iir-gnuradio-to-code.md               # GNU Radio implementation prompt
├── iir-git-flow.md                       # Branching and collaboration exercise
└── iir-scaffold.md                       # Minimal scaffold invocation prompt
```

## Entry points
- `prompts/create-nbs.md` -> regenerate or audit the notebook curriculum contract.
- `prompts/iir-plain-instructions-to-code.md` -> begin a direct SciPy IIR exercise.
- `prompts/iir-scaffold.md` -> concise prompt that invokes repository scaffolding.

## Key interactions
- **`create-nbs.md` -> notebooks:** names and scopes exactly eight independent notebooks.
- **`pass-criterion.txt` -> `create-nbs.md`:** supplies the non-negotiable acceptance criteria.
- **IIR prompts -> future code:** describe alternative representations of the same filtering exercise; they do not themselves implement it.

## Common tasks & gotchas
- Update the generation report if the notebook contract or generated notebook inventory changes.
- The GNU Radio example mixes complex and float block names; verify block type compatibility before implementation.
- Treat Gitflow content as a learning prompt, not proof that the repository currently has those branches.

## Open questions / TODO
- Decide where generated IIR scripts and their tests should live.
- Reconcile exact GNU Radio block types before using the example as executable code.
