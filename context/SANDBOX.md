# SDR/ML Algorithm Sandbox

> A collaborative toolbox for testing SDR and ML algorithms across a team.

---

## What Is the Sandbox?

The **sandbox** is an integrated pipeline where a team can:

1. Express an algorithm idea (pseudocode or free-form).
2. Generate a runnable Jupyter notebook automatically.
3. Follow a documented structure so every notebook is consistent.
4. Audit the notebook for correctness before merging.
5. Version-control everything through a disciplined git flow.

It combines **five tools** into a single workflow:

| Tool | Role |
|------|------|
| pseudocode-general | High-level flow description (language-agnostic) |
| pseudocode-specific | Detailed algorithm design with control flow |
| python-notebook | Generates valid notebook JSON from a description |
| project-scaffold | 3-layer documentation for agent navigation |
| git-flow | Branch strategy, PR workflow, conventional commits |

---

## Git Flow --- Conceptual View

### Branch Hierarchy

```
main ────────────────── production, protected
  │
  └── develop ────────── integration branch
        ├── feature/<name> ── new work
        ├── fix/<name> ────── bug fixes
        ├── docs/<name> ───── documentation
        └── release/<ver> ── version bump
```

**Rules:**
- main is always deployable. Never push directly.
- All PRs target develop.
- Branches are never deleted after merge (audit history).
- Conventional commits: `feat(scope):`, `fix(scope):`, `docs(scope):`.

### Branch Lifecycle

```
main      •─────────────────────────────────•
           \                               /
feature    •───•───•───•───────────────────•  PR #1
                \                         /
fix          •───•───•───────────────────•  PR #2

            time ─────────────────────────>
```

---

## Flow Sandbox 1 --- Pseudocode-Driven

**Entry:** User provides general pseudocode.
**Exit:** Notebook merged via git flow.

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Input │────>│ Scaffold Explore │────>│ Follow Structure │────>│  Audit nb   │────>│  Git Flow   │
│ (pseudocode)│     │ + Create nb      │     │                  │     │             │     │ (PR develop)│
└─────────────┘     └──────────────────┘     └──────────────────┘     └──────┬──────┘     └─────────────┘
                                                                            │
                                                                            │ fail: fix
                                                                            │
                                                                     ┌──────▼──────┐
                                                                     │             │
                                                                     └─────────────┘
```

### Steps

1. **User Input** --- Provide general pseudocode (e.g., SDR monitoring pipeline).
2. **Scaffold Explore + Create nb** --- Agent explores scaffold documentation, generates notebook using python-notebook skill.
3. **Follow Structure** --- Notebook sections follow the scaffold; each section has its own specific pseudocode.
4. **Audit nb** --- Validate: notebook format, axis conventions (N, 2, L), power calculations, missing cells.
5. **Git Flow** --- Create feature branch, commit with conventional message, open PR to develop.

### Conceptual Example

```
Input:   Pseudocode (general)
            │
            ▼
Process: Explore scaffold ──> Create notebook ──> Each section has specific pseudocode
            │
            ▼
Output:  Runnable notebook
```

---

## Flow Sandbox 2 --- Idea-Driven

**Entry:** Team member has a test idea (no pseudocode yet).
**Exit:** Notebook merged via git flow.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌─────────────┐     ┌─────────────┐
│  Test Idea  │────>│  Create nb   │────>│ Follow Structure │────>│  Audit nb   │────>│  Git Flow   │
│ (free-form) │     │              │     │                  │     │             │     │ (PR develop)│
└─────────────┘     └──────────────┘     └──────────────────┘     └──────┬──────┘     └─────────────┘
                                                                        │
                                                                        │ fail: fix
                                                                        │
                                                                 ┌──────▼──────┐
                                                                 │             │
                                                                 └─────────────┘
```

### Steps

1. **Test Idea** --- Team member describes what they want to test (e.g., compare Welch vs periodogram for weak signals).
2. **Create nb** --- Agent generates notebook using python-notebook skill from the description.
3. **Follow Structure** --- Notebook follows scaffold conventions: IQ shape (N, 2, L), axis explanations, power formulas.
4. **Audit nb** --- Validate format, conventions, missing cells, correctness.
5. **Git Flow** --- Branch, commit, PR to develop.

### Conceptual Example

```
Input:   Test Idea (free-form)
            │
            ▼
Process: Create notebook ──> Follow structure
            │
            ▼
Output:  Runnable notebook
```

---

## What Is Missing

The sandbox is functional but incomplete. These components need to be built:

### 1. Dockerization

Reproducible environment for all team members.

```
┌─────────────────────────────────┐
│  Base Image (Python 3.10)       │
├─────────────────────────────────┤
│  System Packages (GNU Radio)    │
├─────────────────────────────────┤
│  Python Packages (numpy, etc.)  │
├─────────────────────────────────┤
│  Sandbox Code                   │
├─────────────────────────────────┤
│  Jupyter Lab (default CMD)      │
└─────────────────────────────────┘
```

**Benefit:** No more "works on my machine" --- every team member runs the same environment.

### 2. Dataset Generation (Simulated)

Synthetic IQ data for testing without hardware.

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Sine Wave   │     │                  │     │                  │
├──────────────┤     │                  │     │                  │
│  White Noise │────>│ Dataset Generator│────>│  IQ Tensor       │
├──────────────┤     │                  │     │  (N, 2, L)       │
│  Multi-tone  │     │                  │     │                  │
├──────────────┤     │                  │     │                  │
│Custom Signal │     │                  │     │                  │
└──────────────┘     └──────────────────┘     └──────────────────┘
```

**Benefit:** Test algorithms without SoapySDR hardware or live signals.

### 3. SoapySDR Skill

Skill for interacting with SDR hardware via SoapySDR.

```
┌──────────────────┐     ┌──────────────────┐
│  SDR Hardware    │     │  Setup Device    │
├──────────────────┤     ├──────────────────┤
│  SoapySDR Driver │────>│  Acquire IQ      │
└──────────────────┘     ├──────────────────┤
                         │  Configure Filters│
                         ├──────────────────┤
                         │  Continuous Mon.  │
                         └──────────────────┘
```

**Benefit:** Standardized way to acquire real IQ data from hardware.

### 4. Audit Skill

Automated notebook validation.

```
┌──────────────────┐
│    Notebook      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  nbformat valid  │
├──────────────────┤
│  IQ shape (N,2,L)│
├──────────────────┤
│  Axis explanation│
├──────────────────┤
│  Power calc      │
├──────────────────┤
│  Imports resolve │
├──────────────────┤
│  No hard paths   │
└────────┬─────────┘
         │
         ▼
    ┌────┴────┐
    │  Pass?  │
    └────┬────┘
    yes  │  no
    ▼    ▼
  PASS  FAIL
```

**Benefit:** Catch errors before PR review --- consistent quality.

### 5. Harness Logic / MCP Server

Orchestrate the full pipeline as a single command.

```
┌──────────────────┐
│  User Command    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Detect input    │
└────────┬─────────┘
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Flow 1 │ │ Flow 2 │
│pseudo  │ │free-for│
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌──────────────────┐
│  Audit notebook  │
├──────────────────┤
│  Create branch   │
├──────────────────┤
│  Commit + PR     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│     Done!        │
└──────────────────┘
```

**Benefit:** One command to go from idea to merged notebook.

---

## Sandbox Architecture --- Full View

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SANDBOX                                        │
│                                                                         │
│  ┌──────────────┐                                                       │
│  │ Pseudocode   │                                                       │
│  │ (general)    │──┐                                                    │
│  └──────────────┘  │                                                    │
│                    │    ┌──────────────────┐                             │
│  ┌──────────────┐  ├──>│ Scaffold Explore │                             │
│  │ Free-form    │──┘    └────────┬─────────┘                             │
│  │ Idea         │               │                                        │
│  └──────────────┘               ▼                                        │
│                        ┌──────────────────┐                              │
│                        │ Generate Notebook│                              │
│                        └────────┬─────────┘                              │
│                                 │                                        │
│                                 ▼                                        │
│                        ┌──────────────────┐                              │
│                        │ Follow Structure │                              │
│                        └────────┬─────────┘                              │
│                                 │                                        │
│                                 ▼                                        │
│                        ┌──────────────────┐                              │
│                        │ Audit Notebook   │──── fail ───> Fix Loop       │
│                        └────────┬─────────┘         │                    │
│                                 │ pass              │                    │
│                                 ▼                   │                    │
│                        ┌──────────────────┐         │                    │
│                        │ Git Flow (PR)    │<────────┘                    │
│                        └────────┬─────────┘                              │
│                                 │                                        │
│  ┌──────────────────────────────┼──────────────────────────────────┐    │
│  │  Supporting Infrastructure   │                                    │    │
│  │                              ▼                                    │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐│    │
│  │  │   Dataset    │ │    Docker    │ │  SoapySDR    │ │ Harness  ││    │
│  │  │  Generator   │ │              │ │    Skill     │ │   MCP    ││    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘│    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

| Component | Status | Purpose |
|-----------|--------|---------|
| pseudocode-general | Done | High-level flow description |
| pseudocode-specific | Done | Detailed algorithm design |
| python-notebook | Done | Generate notebook from description |
| project-scaffold | Done | 3-layer documentation navigation |
| git-flow | Done | Branch strategy, PR workflow |
| Dockerization | **Missing** | Reproducible team environment |
| Dataset Generation | **Missing** | Synthetic IQ data for testing |
| SoapySDR Skill | **Missing** | Hardware IQ acquisition |
| Audit Skill | **Missing** | Automated notebook validation |
| Harness / MCP | **Missing** | Orchestrate full pipeline |
