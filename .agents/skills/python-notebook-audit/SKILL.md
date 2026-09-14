---
name: python-notebook-audit
description: "Trigger: audit notebook, review notebook, check notebook, notebook quality, notebook lint. Audit Jupyter notebooks against project standards and report violations."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use this skill when:
- a user asks to audit, review, or check a Jupyter notebook;
- a notebook needs quality validation before merge or presentation;
- comparing a notebook against the project reference standard;
- identifying structural, documentation, or style issues in notebooks.

Do not use for:
- generating new notebooks (use `python-notebook` skill);
- executing notebook cells or running code;
- fixing issues (this skill only reports them).

## Hard Rules

- **R1: Explore, don't reference.** Read the notebook file directly. Never reference external files like "reference-nb.ipynb" or "issue-nb.ipynb" in your report. Explain issues in terms of what the notebook contains, not what it should match.
- **R2: Report only, never edit.** This skill generates audit reports. Do NOT modify, fix, or rewrite the notebook. The agent must not call `edit`, `write`, or any file-modifying tool on the audited notebook.
- Report each violation with: cell index, issue type, the offending code/text, and a concrete fix suggestion.
- Group findings by severity: BLOCKER > WARNING > INFO.
- A notebook with zero BLOCKERs passes. Warnings are recommendations.

## Audit Rules

### Structure Rules

| ID | Rule | Severity |
|----|------|----------|
| S1 | Title cell must exist as first cell | BLOCKER |
| S2 | Title cell must contain general pseudocode (numbered steps) | BLOCKER |
| S3 | Title cell must contain pipeline flow diagram | WARNING |
| S4 | Every section must have a markdown cell before its code cell(s) | BLOCKER |
| S5 | Section markdown must contain Summary BEFORE pseudocode | BLOCKER |
| S6 | Section markdown pseudocode must use `pseudocode-specific` conventions | WARNING |

### Documentation Rules

| ID | Rule | Severity |
|----|------|----------|
| D1 | Every function must have a docstring | BLOCKER |
| D2 | Docstrings must use Sphinx style (`:param`, `:return`, `:type`, `:rtype`) | WARNING |
| D3 | Every parameter must be documented | BLOCKER |
| D4 | Return type must be documented | BLOCKER |

### Code Rules

| ID | Rule | Severity |
|----|------|----------|
| C1 | No magic numbers — use named constants | WARNING |
| C2 | No unused imports | WARNING |
| C3 | Imports must be at the top of the notebook, not scattered | WARNING |
| C4 | Import style must be consistent (e.g., `import numpy as np` everywhere) | WARNING |
| C5 | Functions must have type hints on parameters and return | WARNING |

### Pseudocode Rules

| ID | Rule | Severity |
|----|------|----------|
| P1 | Assignment must use `←` | WARNING |
| P2 | Comparison must use `=` | WARNING |
| P3 | Blocks must be closed (`END IF`, `END FOR`, `END FUNCTION`) | WARNING |
| P4 | Type declarations must use `DECLARE name AS TYPE` | WARNING |

## Execution Steps

1. Read the notebook file as JSON.
2. Parse all cells and classify as markdown or code.
3. Check Structure Rules (S1-S6) against cell ordering and content.
4. Check Documentation Rules (D1-D4) on every function in code cells.
5. Check Code Rules (C1-C5) across all code cells.
6. Check Pseudocode Rules (P1-P4) on all pseudocode blocks in markdown cells.
7. Group findings by severity and generate report.

## Output Contract

Return a structured audit report:

```
## Notebook Audit Report

**File:** {filename}
**Verdict:** PASS | FAIL (N blockers, M warnings)

### BLOCKERs
- [S1] Cell 0: Missing title cell. First cell must be a markdown cell with `# Title`.
- [S5] Cell 3: Section markdown has pseudocode before Summary. Move Summary above pseudocode.

### WARNINGs
- [C1] Cell 2: Magic number `2400000` — define `SAMPLE_RATE = 2.4e6` as a named constant.
- [D2] Cell 4: Docstring uses Google style (`Args:`) — convert to Sphinx style (`:param name: description`).

### INFOs
- [P3] Cell 3: Pseudocode block missing `END FUNCTION` closing.
```

## References

- `pseudocode-specific` skill — conventions for pseudocode syntax validation.
- `python-notebook` skill — valid notebook JSON structure requirements.
