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

- **HR1: Explore, don't reference.** Read the notebook file directly. Never reference external files like "reference-nb.ipynb" or "issue-nb.ipynb" in your report. Explain issues in terms of what the notebook contains, not what it should match.
- **HR2: Report only, never edit.** This skill generates audit reports. Do NOT modify, fix, or rewrite the notebook. The agent must not call `edit`, `write`, or any file-modifying tool on the audited notebook.
- Report each violation with: cell index, issue type, the offending code/text, and a concrete fix suggestion.
- Group findings by severity: BLOCKER > WARNING > INFO.
- A notebook with zero BLOCKERs passes. Warnings are recommendations.

## Audit Rules

### Structure Rules

| ID | Rule | Severity |
|----|------|----------|
| R1 | Title cell must exist as first cell | BLOCKER |
| R2 | Title cell must contain general pseudocode (numbered steps) | BLOCKER |
| R3 | Title cell must contain pipeline flow diagram | WARNING |
| R4 | Every section must have a markdown cell before its code cell(s) | BLOCKER |
| R5 | Section markdown must contain Summary BEFORE pseudocode | BLOCKER |
| R6 | Section markdown pseudocode must use `pseudocode-specific` conventions | WARNING |

### Documentation Rules

| ID | Rule | Severity |
|----|------|----------|
| R7 | Every function must have a docstring | BLOCKER |
| R8 | Docstrings must use Sphinx style (`:param`, `:return`, `:type`, `:rtype`) | WARNING |
| R9 | Every parameter must be documented | BLOCKER |
| R10 | Return type must be documented | BLOCKER |

### Code Rules

| ID | Rule | Severity |
|----|------|----------|
| R11 | No magic numbers — use named constants | WARNING |
| R12 | No unused imports | WARNING |
| R13 | Imports must be at the top of the notebook, not scattered | WARNING |
| R14 | Import style must be consistent (e.g., `import numpy as np` everywhere) | WARNING |
| R15 | Functions must have type hints on parameters and return | WARNING |

### Pseudocode Rules

| ID | Rule | Severity |
|----|------|----------|
| R16 | Assignment must use `←` | WARNING |
| R17 | Comparison must use `=` | WARNING |
| R18 | Blocks must be closed (`END IF`, `END FOR`, `END FUNCTION`) | WARNING |
| R19 | Type declarations must use `DECLARE name AS TYPE` | WARNING |

### ML-Specific Rules (skip if no ML code detected)

ML code is detected when imports include `sklearn`, `torch`, `tensorflow`, `keras`, `xgboost`, `lightgbm`, or cells contain model training/evaluation patterns.

#### 1.1 Workflow Structure

| ID | Rule | Severity |
|----|------|----------|
| R20 | Standard ML order must be followed: Data Loading → Preprocessing → Feature Engineering → Model Training → Evaluation → Inference → Model Saving | BLOCKER |

#### 1.2 Top-to-Bottom Execution Order

| ID | Rule | Severity |
|----|------|----------|
| R21 | Every cell must depend only on state produced by earlier cells | BLOCKER |
| R22 | No hidden dependencies on later cells | BLOCKER |

#### 1.3 Code Readability

| ID | Rule | Severity |
|----|------|----------|
| R23 | Variable names must be meaningful | WARNING |
| R24 | Complex one-liners must be avoided | WARNING |
| R25 | Style must be consistent throughout | WARNING |

#### 2.1 Environment Variables

| ID | Rule | Severity |
|----|------|----------|
| R26 | Configuration values that should be env vars must not be hardcoded | WARNING |

#### 2.2 Reliable Data Handling

| ID | Rule | Severity |
|----|------|----------|
| R27 | File paths must not be hardcoded | WARNING |
| R28 | Raw data must be treated as immutable (never modified in place) | BLOCKER |
| R29 | Data acquisition must be explicit and repeatable | WARNING |

#### 2.4 Reproducibility Controls

| ID | Rule | Severity |
|----|------|----------|
| R30 | Random seeds must be set for numpy, python random, torch, tf, sklearn | BLOCKER |
| R31 | Deterministic flags must be set (PYTHONHASHSEED, torch.use-deterministic-algorithms) before any split, init, or training | WARNING |

#### 2.5 Fast Reruns / Caching

| ID | Rule | Severity |
|----|------|----------|
| R32 | Expensive steps must use caching (joblib.Memory, pickle, parquet) | WARNING |
| R33 | Training checkpoints must be saved | WARNING |

## Execution Steps

1. Read the notebook file as JSON.
2. Parse all cells and classify as markdown or code.
3. Check Structure Rules (R1-R6) against cell ordering and content.
4. Check Documentation Rules (R7-R10) on every function in code cells.
5. Check Code Rules (R11-R15) across all code cells.
6. Check Pseudocode Rules (R16-R19) on all pseudocode blocks in markdown cells.
7. Detect if notebook contains ML code (imports or patterns).
8. If ML code detected, check ML-Specific Rules (R20-R33).
9. Group findings by severity and generate report.

## Output Contract

Return a structured audit report:

```
## Notebook Audit Report

**File:** {filename}
**Verdict:** PASS | FAIL (N blockers, M warnings)

### BLOCKERs
- [R1] Cell 0: Missing title cell. First cell must be a markdown cell with `# Title`.
- [R5] Cell 3: Section markdown has pseudocode before Summary. Move Summary above pseudocode.

### WARNINGs
- [R11] Cell 2: Magic number `2400000` — define `SAMPLE_RATE = 2.4e6` as a named constant.
- [R8] Cell 4: Docstring uses Google style (`Args:`) — convert to Sphinx style (`:param name: description`).

### INFOs
- [R18] Cell 3: Pseudocode block missing `END FUNCTION` closing.
```

## References

- `pseudocode-specific` skill — conventions for pseudocode syntax validation.
- `python-notebook` skill — valid notebook JSON structure requirements.
