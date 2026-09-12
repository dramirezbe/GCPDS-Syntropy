# Cristian's IIR Workspace

This directory contains Cristian's work developed on `feature/iir-cristian`. It is a personal workspace, not a section of the repository scaffold.

## Quick path

1. Verify the active branch with `git branch --show-current`.
2. Work only inside `cristian-work/` unless a shared file must be updated.
3. Keep generated notebooks reproducible and validate them before committing.

## Notebooks

| File | Purpose | Runtime status |
| --- | --- | --- |
| `iir_gnuradio_filter.ipynb` | GNU Radio IIR filtering for complex IQ | Static validation passed; GNU Radio runtime unavailable |
| `iir_pseudocode_to_code.ipynb` | Pseudocode translated to NumPy/SciPy | Execution passed |
| `iir_plain_instructions_to_code.ipynb` | Complete SciPy workflow with plots and NPZ output | Execution passed |

## Conventions

- IQ tensors use `(N, 2, L)`: examples, I/Q components, and time.
- Filtering operates on `axis=2`.
- Notebook outputs remain cleared in Git.
- Runtime-generated files such as `filtered_iq.npz` are not committed unless explicitly requested.

## Next step

Install GNU Radio according to `AGENTS.md` before executing `iir_gnuradio_filter.ipynb`.
