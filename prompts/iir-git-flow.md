# Prompt: Git Flow

## Prompt

```
Explain the Gitflow workflow for a Python/Jupyter notebook project.

Cover:
- main vs develop branches
- feature/*, refactor/*, docs/* branches
- push, pull, fetch
- merge, rebase
- Pull Requests
- Branch naming conventions
- Admin vs user roles

Show the complete workflow with actual commands.
```

## Reference

Source: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

## Key Concepts

### Branches

| Branch | Purpose | Merges into |
|--------|---------|-------------|
| `main` | Production-ready releases | — |
| `develop` | Integration branch | `main` |
| `feature/*` | New features | `develop` |
| `docs/*` | Documentation | `develop` |
| `refactor/*` | Code restructuring | `develop` |
| `hotfix/*` | Production patches | `main` + `develop` |

### Workflow

1. `develop` is created from `main`
2. `feature` branches are created from `develop`
3. When feature is complete → merge to `develop`
4. When `develop` is stable → create `release` branch
5. When `release` is ready → merge to `main` + tag
6. For urgent fixes → `hotfix` from `main` → merge to both

### Commands

```bash
# Create feature branch
git checkout develop
git checkout -b feature/iir-filter-notebook

# Work and commit
git add .
git commit -m "feat: add IIR filter notebook"

# Push and create PR
git push origin feature/iir-filter-notebook
gh pr create --title "Add IIR Filter Notebook"

# After review, merge to develop
git checkout develop
git merge feature/iir-filter-notebook
git push origin develop

# Delete feature branch
git branch -d feature/iir-filter-notebook
```
