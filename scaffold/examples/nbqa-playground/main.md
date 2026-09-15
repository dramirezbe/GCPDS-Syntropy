# Nbqa Playground — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Provide a sandbox for testing the NBQA notebook linting pipeline with intentional failures that validate the fatal gate and style checks.

## Tech stack & conventions
- `nbqa ruff` — primary linter; detects F821 (undefined name) and F822 (undefined in `__all__`).
- `nbqa black` — code formatter for notebook cells.
- `nbqa yapf` — alternative formatter.
- Ruff notes: E901 removed in modern ruff; F823 merged into F821; F822 is `__all__` exports.
- `--ignore=F821` appears on both fatal gate and style check in `context/audit/NBQA_USAGE.md`.

## Structure
```text
nbqa-playground/
└── fail-nb.ipynb    # ★ Intentional ruff F821/F822 failures
```

## Entry points
- `fail-nb.ipynb` -> triggers F821 (undefined `nonexistent_func`) and F822 (undefined in `__all__`).

## Key interactions
- **fail-nb.ipynb -> NBQA pipeline:** validates that `nbqa ruff` correctly detects and reports F821/F822.
- **fail-nb.ipynb -> Gate 1:** should fail the notebook health gate with deterministic findings.
- **NBQA_USAGE.md -> fail-nb.ipynb:** documents the pipeline that this notebook tests.

## Common tasks & gotchas
- Run `nbqa ruff examples/nbqa-playground/fail-nb.ipynb` to verify detection.
- The failures in `fail-nb.ipynb` are intentional; do not fix them.
- `fail-nb.ipynb` was originally at `examples/fail-nb.ipynb` before being moved here.

## Open questions / TODO
- Consider adding more intentional failures for other ruff rules (e.g., F401 unused imports).
- Consider adding a `pass-nb.ipynb` that should pass all checks.
