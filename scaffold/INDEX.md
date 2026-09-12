# Scaffold INDEX

> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Provide the layer-0 navigation map for agents working on the IQ-oriented Python/NumPy learning materials and their supporting prompts.

## Tech stack & conventions
- Jupyter Notebook with Python 3 kernels.
- NumPy `float32` tensors use the canonical shape `(N, 2, L)`.
- Axis 0 is examples, axis 1 is I/Q components, and axis 2 is time samples.
- Prompts and agent documentation are Markdown; scaffold metadata is JSON.

## Structure
```text
scaffold/
├── INDEX.md                         # ★ ENTRY POINT: repository map
├── notebooks/                       # Curriculum documentation
├── prompts/                         # Prompt documentation
├── project-guidance/                # Repository-operating guidance
└── _meta/                           # Manifest and raw exploration notes
```

### Section map
| Section | Purpose | Docs |
| --- | --- | --- |
| Notebooks | Eight sequential Pre-M0 labs teaching Python and NumPy through IQ signals | [notebooks/main.md](notebooks/main.md) |
| Prompts | Source instructions for notebook generation, IIR exercises, and Git workflow | [prompts/main.md](prompts/main.md) |
| Project guidance | Agent environment rules, local skills, registry, and work backlog | [project-guidance/main.md](project-guidance/main.md) |

## Entry points
- `AGENTS.md` -> mandatory operating and GNU Radio environment instructions.
- `notebooks/pre_m0_1_python_functions_for_iq.ipynb` -> start of the learner sequence.
- `prompts/create-nbs.md` -> generation contract for all eight notebooks.
- `tasks.md` -> project backlog and exercise ideas.

## Key interactions
```text
AGENTS.md -> scaffold/INDEX.md -> section docs -> repository files
prompts/create-nbs.md + prompts/pass-criterion.txt -> notebooks/*.ipynb
notebooks/*.ipynb -> notebooks/pre_m0_generation_report.json
.agents/skills/* -> agent workflows; .atl/skill-registry.md indexes them
```

## Common tasks & gotchas
- Start with this index rather than scanning the repository blindly.
- Update the relevant section docs and manifest whenever repository structure or contracts change.
- Notebook pass gates combine automatic checks with a manually verified axis explanation.
- GNU Radio requires a virtual environment created with `--system-site-packages`; see `AGENTS.md`.

## Open questions / TODO
- No dependency lockfile currently documents exact NumPy and Matplotlib versions.
- The IIR prompt set describes future code work, but no IIR implementation exists in the repository.
