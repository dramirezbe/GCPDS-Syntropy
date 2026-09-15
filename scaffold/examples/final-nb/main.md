# Final Nb — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Hold validated final notebooks that serve as quality benchmarks: a reference implementation and a known-issue notebook for testing audit gates.

## Tech stack & conventions
- Jupyter Notebook with Python 3 kernels.
- `reference-nb.ipynb` is the canonical validated implementation.
- `issue-nb.ipynb` contains known issues for testing audit detection.
- `reference-nb-requirements.txt` pins exact dependencies for the reference notebook.

## Structure
```text
final-nb/
├── reference-nb.ipynb              # ★ Validated reference implementation
├── reference-nb-requirements.txt   # Pinned dependencies for reference notebook
└── issue-nb.ipynb                  # Known-issue notebook for gate testing
```

## Entry points
- `reference-nb.ipynb` -> the gold-standard notebook; should pass all audit gates.
- `issue-nb.ipynb` -> intentionally flawed; used to verify gate detection.

## Key interactions
- **reference-nb.ipynb -> audit gates:** should pass Gate 1 (health), Gate 2 (methodology), Gate 3 (execution).
- **issue-nb.ipynb -> audit gates:** should fail specific gates with known findings.
- **reference-nb-requirements.txt -> environment:** exact dependency versions for reproducibility.

## Common tasks & gotchas
- Do not modify `reference-nb.ipynb` without re-validating all three audit gates.
- `issue-nb.ipynb` failures are intentional; do not "fix" them unless the test scenario changes.

## Open questions / TODO
- Consider adding CI validation that `reference-nb.ipynb` passes all gates.
- Consider documenting which specific issues `issue-nb.ipynb` is designed to trigger.
