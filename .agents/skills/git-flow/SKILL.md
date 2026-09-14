---
name: git-flow
description: "Trigger: git flow, create branch, PR to develop, merge feature, git workflow, branch strategy. Enforce git flow with develop as integration branch and PR-based merges."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Activation Contract

Use this skill when:
- creating a new feature, fix, or docs branch;
- opening or reviewing a PR;
- merging into develop or main;
- checking branch hygiene or sync status.

Do not use for:
- direct commits to main (forbidden);
- one-off commits that do not belong to a feature;
- operations on forks.

## Prerequisites — gh CLI

Before any git-flow operation, verify `gh` is authenticated:

```bash
gh auth status
```

If not logged in:

```bash
gh auth login
# Select: GitHub.com → HTTPS → Login with a web browser → paste token
```

If `gh` is not installed:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y gh

# macOS
brew install gh
```

## Git Flow Logic

```
main ─────────────────────────── production (protected, no direct push)
  │
  └── develop ─────────────────── integration branch (all features land here)
        ├── feature/<name> ────── new work
        ├── fix/<name> ────────── bug fixes
        ├── docs/<name> ───────── documentation only
        └── release/<version> ── version bump + changelog
```

**Flow:**
1. `main` is always deployable. Never push directly.
2. `develop` is the integration branch. All PRs target `develop`.
3. Every change lives in its own branch, named `<type>/<short-description>`.
4. After PR merge, the source branch is NOT deleted (history preservation).
5. Periodically merge `develop` into `main` for releases.

## Hard Rules

### 1. Pull all branches and metadata before starting

```bash
git fetch origin --prune --tags
git pull origin main
git pull origin develop
```

**WARNING:** If `main` and `develop` diverge in time (main is older or newer than develop), STOP and report the drift:

```
⚠ DIVERGENCE DETECTED
  main last commit:   <date> — <hash> <msg>
  develop last commit: <date> — <hash> <msg>
  Action required: merge develop into main, or investigate.
```

Do not proceed until the operator resolves the divergence.

### 2. Always create a branch for new work

Never commit directly to `main` or `develop`. Branch naming:

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<short-desc>` | `feature/iir-welch-psd` |
| Fix | `fix/<short-desc>` | `fix/notebook-axis-label` |
| Docs | `docs/<short-desc>` | `docs/update-scaffold` |
| Release | `release/<version>` | `release/1.2.0` |

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<short-desc>
```

### 3. All PRs target develop

```bash
gh pr create \
  --base develop \
  --head feature/<short-desc> \
  --title "feat(scope): description" \
  --body "## What changed\n...\n## Why\n..."
```

Conventional commit titles required:
- `feat(scope):` — new feature
- `fix(scope):` — bug fix
- `docs(scope):` — documentation only
- `chore(scope):` — maintenance, deps, config

### 4. Do not delete branches after merge

After a PR is merged, leave the branch intact on the remote. This preserves audit history and makes bisection easier.

If a branch was accidentally deleted, recreate it from the merge commit:

```bash
git fetch origin
git checkout -b <branch-name> origin/<branch-name>
```

### 5. Merging develop into main

Only the repository owner merges `develop` into `main`:

```bash
git checkout main
git pull origin main
git merge develop
git push origin main
```

Or via PR:

```bash
gh pr create \
  --base main \
  --head develop \
  --title "release: merge develop into main" \
  --body "## Changes since last release\n..."
```

## Decision Gates

| Situation | Action |
| --- | --- |
| Need to start new work | `git checkout develop && git pull && git checkout -b feature/X` |
| Ready to merge | Open PR targeting `develop` with conventional commit title |
| main and develop diverge | STOP — report divergence, wait for resolution |
| Need to release | Create PR from `develop` to `main` |
| Accidentally committed to main | `git revert` the commit, do not force-push |
| Branch already deleted | Recreate from merge commit hash |

## Execution Steps

1. Run `gh auth status` — confirm authenticated, fallback to `gh auth login` tutorial.
2. Run `git fetch origin --prune --tags` — pull all branches and metadata.
3. Compare `main` and `develop` timestamps — warn if diverged.
4. Create feature branch from `develop`.
5. Do work, commit with conventional messages.
6. Push branch, open PR targeting `develop`.
7. After merge: do NOT delete the branch.
8. Periodically merge `develop` into `main` for releases.

## Output Contract

Return:
- gh auth status result;
- branch sync status (main vs develop timestamps);
- branch created (name, base);
- PR created (URL, title, target);
- any warnings about divergence or drift.

## References

- `AGENTS.md` — repository environment rules
- `scaffold/project-guidance/main.md` — project conventions
