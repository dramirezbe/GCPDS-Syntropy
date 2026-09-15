```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FIRST ITERATION                                │
└─────────────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼
                           ┌─────────────────────┐
                           │     ML NOTEBOOK     │
                           │                     │
                           │ User's experiment   │
                           └──────────┬──────────┘
                                      │
                                      ▼
═══════════════════════════════════════════════════════════════════════════════
                           GATE 1 — NOTEBOOK HEALTH
                         DETERMINISTIC / NO AI / NO EXEC
═══════════════════════════════════════════════════════════════════════════════

                           ┌──────────────────────────┐
                           │          nbQA            │
                           │                          │
                           │ Notebook structure       │
                           │ nbformat / JSON health   │
                           │ Syntax errors             │
                           │ Undefined variables      │
                           │ Imports / static issues  │
                           │ Linting                  │
                           │ Formatting               │
                           │ Cell integrity           │
                           └────────────┬─────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                       PASS                           FAIL
                         │                             │
                         │                             ▼
                         │                    ┌─────────────────┐
                         │                    │   SUGGEST FIX   │
                         │                    │                 │
                         │                    │ Auto-fix only   │
                         │                    │ deterministic   │
                         │                    │ / mechanical    │
                         │                    │ problems        │
                         │                    └────────┬────────┘
                         │                             │
                         │                             ▼
                         │                         ML NOTEBOOK
                         │                             │
                         │                      Feedback 1 ↺
                         │
                         ▼
═══════════════════════════════════════════════════════════════════════════════
                    NORMALIZATION + CONTEXT EXTRACTION
                    DETERMINISTIC / NO EXPERIMENT EXECUTION
═══════════════════════════════════════════════════════════════════════════════

                         ┌────────────────────────────────┐
                         │            NORMALIZER           │
                         │                                │
                         │ Normalize notebook structure   │
                         │ Normalize code representation  │
                         │ Preserve cell ordering         │
                         └────────────────┬───────────────┘
                                          │
                                          ▼
                         ┌────────────────────────────────┐
                         │       CONTEXT EXTRACTION        │
                         │                                │
                         │ AST                            │
                         │ Symbol table                   │
                         │ Cell dependencies              │
                         │ Data Flow Graph                │
                         │ Variables / DataFrames         │
                         │ ML operations                  │
                         │ fit / transform / split / CV  │
                         └────────────────┬───────────────┘
                                          │
                                          ▼
═══════════════════════════════════════════════════════════════════════════════
                       GATE 2 — ML METHODOLOGICAL AUDIT
                            AI / NO CODE EXECUTION
═══════════════════════════════════════════════════════════════════════════════

                         ┌─────────────────────────────────────────┐
                         │             AUDIT ENGINE AI             │
                         │                                         │
                         │     3 AXES / 7 AUDIT DIMENSIONS        │
                         │                                         │
                         │ ┌─────────────────────────────────────┐ │
                         │ │  1. DATA INTEGRITY                  │ │
                         │ │                                     │ │
                         │ │  • Leakage                          │ │
                         │ │  • Splitting                        │ │
                         │ │  • Data Quality                     │ │
                         │ └─────────────────────────────────────┘ │
                         │                                         │
                         │ ┌─────────────────────────────────────┐ │
                         │ │  2. EVALUATION INTEGRITY            │ │
                         │ │                                     │ │
                         │ │  • Validation                       │ │
                         │ │  • Metrics                          │ │
                         │ └─────────────────────────────────────┘ │
                         │                                         │
                         │ ┌─────────────────────────────────────┐ │
                         │ │  3. EXPERIMENT INTEGRITY             │ │
                         │ │                                     │ │
                         │ │  • Reproducibility                  │ │
                         │ │  • Experiment Integrity              │ │
                         │ └─────────────────────────────────────┘ │
                         └──────────────────────┬──────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │                           │                           │
                   PASS                        FAIL                    UNVERIFIABLE
                    │                           │                           │
                    │                           │                           │
                    │                           ▼                           ▼
                    │                 ┌───────────────────┐       ┌──────────────────┐
                    │                 │    REMEDIATION    │       │ HUMAN / CONTEXT   │
                    │                 │                   │       │ REVIEW REQUIRED   │
                    │                 │ Finding           │       │                  │
                    │                 │ Evidence          │       │ Insufficient      │
                    │                 │ Impact            │       │ information to    │
                    │                 │ Suggested fix     │       │ establish PASS    │
                    │                 │                   │       │ or FAIL           │
                    │                 │ No blind          │       └─────────┬────────┘
                    │                 │ auto-correction   │                 │
                    │                 └─────────┬─────────┘                 │
                    │                           │                           │
                    │                           └──────────────┬────────────┘
                    │                                          │
                    │                                          ▼
                    │                                    ML NOTEBOOK
                    │                                          │
                    │                                   Feedback 2 ↺
                    │
                    ▼
═══════════════════════════════════════════════════════════════════════════════
                     METHODOLOGICAL PRE-MLOPS APPROVAL
═══════════════════════════════════════════════════════════════════════════════

                         ┌────────────────────────────────┐
                         │         GATE 2 PASS            │
                         │                                │
                         │ Methodologically acceptable    │
                         │ for experimental execution     │
                         │                                │
                         │ Gate 1 = PASS                  │
                         │ Gate 2 = PASS                  │
                         └────────────────┬───────────────┘
                                          │
                                          ▼
═══════════════════════════════════════════════════════════════════════════════
                      GATE 3 — EXPERIMENT EXECUTION
                      CONTROLLED EXECUTION / NO AI AUDIT
═══════════════════════════════════════════════════════════════════════════════

                         ┌────────────────────────────────┐
                         │          EXPERIMENT RUN         │
                         │                                │
                         │ Execute notebook / experiment  │
                         │                                │
                         │ Capture:                       │
                         │ • Runtime errors               │
                         │ • Execution success            │
                         │ • Outputs                      │
                         │ • Metrics                      │
                         │ • Artifacts                    │
                         │ • Runtime reproducibility      │
                         │ • Resource/runtime information │
                         └────────────────┬───────────────┘
                                          │
                              ┌───────────┴───────────┐
                              │                       │
                           SUCCESS                  FAILURE
                              │                       │
                              │                       ▼
                              │             ┌─────────────────────┐
                              │             │   EXECUTION ERROR   │
                              │             │                     │
                              │             │ Diagnose / report   │
                              │             │ Suggested correction│
                              │             └──────────┬──────────┘
                              │                        │
                              │                        ▼
                              │                    ML NOTEBOOK
                              │                        │
                              │                 Feedback 3 ↺
                              │
                              ▼
═══════════════════════════════════════════════════════════════════════════════
                         PRE-MLOPS EXPERIMENT GATE
═══════════════════════════════════════════════════════════════════════════════

                         ┌────────────────────────────────┐
                         │       GATE 3 PASS              │
                         │                                │
                         │ Experiment successfully       │
                         │ executed under controlled      │
                         │ conditions                     │
                         └────────────────┬───────────────┘
                                          │
                                          ▼
═══════════════════════════════════════════════════════════════════════════════
                                  MLOps
═══════════════════════════════════════════════════════════════════════════════

                         ┌────────────────────────────────┐
                         │             MLOps              │
                         │                                │
                         │ Experiment tracking            │
                         │ Data / artifact versioning     │
                         │ Reproducible training          │
                         │ Model versioning                │
                         │ Model registry                  │
                         │ Training pipelines              │
                         │ Deployment                      │
                         │ Monitoring                      │
                         │ Retraining                      │
                         │ Governance                      │
                         └────────────────────────────────┘
```

### Flujo de estados

```text
ML Notebook
    │
    ▼
Gate 1
    │
    ├── FAIL ──► Suggest Fix ──► Notebook ↺
    │
    └── PASS
          │
          ▼
   Normalize + Context Extraction
          │
          ▼
        Gate 2
          │
          ├── FAIL ──► Remediation ──► Notebook ↺
          │
          ├── UNVERIFIABLE ──► Review / additional context ──► Gate 2 ↺
          │
          └── PASS
                │
                ▼
              Gate 3
                │
                ├── FAIL ──► Execution remediation ──► Notebook ↺
                │
                └── PASS
                      │
                      ▼
                    MLOps
```

### Principios incorporados

```text
GATE 1
→ "Is the notebook technically healthy?"
→ Deterministic
→ No AI
→ No code execution
→ Mechanical fixes may be suggested/applied

GATE 2
→ "Is the ML experiment methodologically sound?"
→ AI-assisted semantic analysis
→ No code execution
→ 3 axes / 7 dimensions
→ Evidence-based findings
→ PASS / FAIL / UNVERIFIABLE
→ Recommendations rather than blind automatic fixes

GATE 3
→ "Does the validated experiment actually execute?"
→ Real controlled execution
→ Runtime validation
→ Capture outputs, metrics and artifacts
→ No methodological judgment by execution itself

MLOps
→ "Can the validated experiment become an operational ML system?"
```

Queda establecido este flow como base. Espero tu feedback.
