# Context — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: [audit](./audit/main.md)
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
House reference documents, design artifacts, audit workflow materials, and published PDFs that inform the project's ML notebook audit methodology and pedagogical design.

## Tech stack & conventions
- LaTeX sources compile with `latexmk -pdf`; output lands in `context/audit/`.
- Excalidraw diagrams are hand-drawn architecture sketches (JSON format).
- PDFs are published reference papers and design documents.
- Markdown files are human-readable summaries of workflows and findings.
- HTML files are standalone rendered views of diagrams or reports.

## Structure
```text
context/
├── audit/                                # ML notebook audit workflow
│   ├── Audit-ML-Notebook.tex             # ★ LaTeX source with TikZ flowchart
│   ├── Audit-ML-Notebook.pdf             # Compiled audit document (4 pages)
│   ├── ML-Audit-flow.md                  # Source ASCII flow diagram
│   ├── ML-audit-html.html                # Rendered HTML version of audit flow
│   ├── ML-audit-block-diagrams.html      # Block-diagram rendering of the audit flow
│   ├── NBQA_USAGE.md                     # ruff/nbqa/black/yapf pipeline reference
│   └── diagram-audit.excalidraw          # Excalidraw audit diagram
├── 00 ProductionPipelinePCG.pdf          # Production pipeline reference
├── 01_Concept.pdf                        # Concept document
├── 02 PromptTL.pdf                       # Prompt transfer learning reference
├── Arco_Pedagogico_Neural_Operators...   # Pedagogical arc for FNO/Bochner/RFF
├── diagram-harness.excalidraw            # Harness architecture diagram
├── pseudocode.pdf                        # Pseudocode reference document
├── pseudocode.tex                        # Pseudocode LaTeX source
├── prompt01Lap1.tex                      # Prompt LaTeX source
├── SANDBOX.md                            # Sandbox documentation
├── SANDBOX.pdf                           # Compiled sandbox document
└── SANDBOX.tex                           # Sandbox LaTeX source
```

## Entry points
- `context/audit/Audit-ML-Notebook.tex` -> main audit document; compile with `latexmk -outdir=context/audit -pdf`.
- `context/audit/NBQA_USAGE.md` -> quick reference for notebook linting pipeline.
- `context/audit/ML-Audit-flow.md` -> source ASCII diagram for the audit workflow.

## Key interactions
- **audit/ML-Audit-flow.md -> audit/Audit-ML-Notebook.tex:** ASCII flow is the source of truth; TikZ diagram renders it visually.
- **audit/NBQA_USAGE.md -> examples/nbqa-playground/:** documents the linting pipeline tested by fail-nb.ipynb.
- **PDFs -> project design:** reference papers inform the pedagogical and audit methodology.
- **LaTeX sources -> PDFs:** `latexmk -pdf` compiles `.tex` to `.pdf`.

## Common tasks & gotchas
- Compile audit document: `latexmk -outdir=context/audit -pdf context/audit/Audit-ML-Notebook.tex`.
- Clean aux files: `latexmk -outdir=context/audit -c context/audit/Audit-ML-Notebook.tex`.
- TikZ flowchart uses `\resizebox{\textwidth}{!}{...}` to fit the page width.
- PDFs in this directory are tracked in git; do not regenerate without reason.

## Open questions / TODO
- Context directory contains mixed file types (PDF, TeX, MD, HTML, Excalidraw) — consider sub-directory reorganization.
- Some PDFs lack clear naming conventions; consider renaming for discoverability.
