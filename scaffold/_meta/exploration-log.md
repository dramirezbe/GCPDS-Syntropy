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

## Workspace update — 2026-09-12
- The active branch was verified as `feature/iir-cristian`, tracking `origin/feature/iir-cristian`.
- `cristian-work/` is a personal workspace rather than a scaffold section.
- Its local guide is `cristian-work/WORKSPACE.md`; no `scaffold/cristian-work/` mirror is maintained.

## GNU Radio notebook update — 2026-09-12
- `cristian-work/iir_gnuradio_filter.ipynb` implements the GNU Radio IIR prompt as a tutorial notebook.
- The prompt's direct complex-source to float-IIR connection is type-incompatible; the notebook splits I and Q into float streams, filters them independently, then recombines them.
- `single_pole_iir_filter_ff` belongs to `gnuradio.filter`, not `gnuradio.blocks`; the notebook uses the verified module namespace.
- GNU Radio was absent from the environment. `python3-venv` was installed, but GNU Radio installation could not proceed because `sudo` required interactive authentication.
- Notebook JSON and static cell contracts were validated; runtime execution remains pending until GNU Radio is installed.

## Pseudocode-to-code notebook update — 2026-09-12
- `cristian-work/iir_pseudocode_to_code.ipynb` implements the pseudocode prompt with explicit declarations, assignment symbols, comparisons, and block endings.
- The Python translation uses a second-order SciPy Butterworth low-pass filter and `lfilter(..., axis=2)` on deterministic `(5, 2, 1000)` float32 IQ data.
- Sequential clean-namespace execution passed: shape remained `(5, 2, 1000)` and power changed from `1.254055` to `1.001605` (ratio `0.798693`).
- `nbclient` executed all six code cells successfully in a clean kernel; the tracked notebook intentionally retains empty outputs.

## Plain-instructions notebook update — 2026-09-12
- `cristian-work/iir_plain_instructions_to_code.ipynb` implements the complete NumPy/SciPy workflow with four requested plots and compressed NPZ persistence.
- Clean sequential execution ran all seven code cells and created a temporary 37,858-byte `filtered_iq.npz` outside the repository.
- Runtime verification preserved `(5, 2, 1000)` float32 data and changed joint power from `1.207514` to `0.927528` (ratio `0.768130`).
- `nbclient` execution was unavailable because the environment has no registered `python3` kernelspec; clean-namespace sequential execution was used instead.
