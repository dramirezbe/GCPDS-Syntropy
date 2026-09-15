# Audit — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Document the ML notebook audit workflow: a three-gate quality pipeline that validates notebook health, ML methodological correctness, and experiment execution, with deterministic fixes and human-review escalation paths.

## Tech stack & conventions
- LaTeX with TikZ for the flowchart diagram; compiled via `latexmk`.
- Six references: Yang (2022), Subotic (2023), Kaufman (2022), Breck (2019), Sculley (2011), NIST (2023).
- Three gates: Gate 1 (Notebook Health), Gate 2 (ML Methodological Audit), Gate 3 (Experiment Execution).
- Two fix categories: deterministic (Gate 1, Gate 3) and human-review (Gate 2 UNVERIFIABLE).
- NBQA pipeline: `nbqa ruff` (fatal gate + style), `nbqa black` (formatting), `nbqa yapf` (alternative formatter).
- Ruff notes: E901 removed in modern ruff; F823 merged into F822; F822 is `__all__` undefined exports.

## Structure
```text
audit/
├── Audit-ML-Notebook.tex       # ★ LaTeX source: full document + TikZ flowchart
├── Audit-ML-Notebook.pdf       # Compiled output (4 pages, ~335 KB)
├── ML-Audit-flow.md            # Source ASCII flow diagram (human-readable)
├── ML-audit-html.html          # Rendered HTML version of audit flow
├── NBQA_USAGE.md               # ruff/nbqa/black/yapf pipeline reference
└── diagram-audit.excalidraw    # Excalidraw audit diagram
```

## Entry points
- `Audit-ML-Notebook.tex` -> compile with `latexmk -outdir=context/audit -pdf`.
- `NBQA_USAGE.md` -> quick reference for the notebook linting pipeline.
- `ML-Audit-flow.md` -> source ASCII flow; the TikZ diagram renders this visually.

## Key interactions
- **ML-Audit-flow.md -> Audit-ML-Notebook.tex:** ASCII flow is the source of truth; TikZ renders it.
- **NBQA_USAGE.md -> examples/nbqa-playground/fail-nb.ipynb:** documents the pipeline that fail-nb validates.
- **Gate 1:** deterministic health checks (ruff F821/F822, cell metadata, kernel spec).
- **Gate 2:** ML methodology audit; UNVERIFIABLE findings escalate to human review.
- **Gate 3:** experiment execution; deterministic fixes for runtime errors.

## Common tasks & gotchas
- Compile: `latexmk -outdir=context/audit -pdf context/audit/Audit-ML-Notebook.tex`
- Clean: `latexmk -outdir=context/audit -c context/audit/Audit-ML-Notebook.tex`
- TikZ diagram uses `\resizebox{\textwidth}{!}{...}` for page-width fitting.
- Feedback loops return to the notebook for re-validation after fixes.
- The `--ignore=F821` flag appears on both the fatal gate and style check in NBQA_USAGE.md.

## Open questions / TODO
- Consider adding Gate 3 execution results to the audit document.
- The HTML version (`ML-audit-html.html`) may drift from the LaTeX source; consider auto-generation.
