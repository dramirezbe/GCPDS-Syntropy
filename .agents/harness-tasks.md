# Harness Tasks

> Last updated: 2026-09-14

## P0 - Critical (blocks quality)

### 1. Notebook Tester Skill
- [ ] Create `.agents/skills/notebook-tester/SKILL.md`
- [ ] Execute notebooks with `nbconvert --execute`
- [ ] Validate output shapes `(N, 2, L)`
- [ ] Check for errors in code cells
- [ ] Generate test reports

### 2. Audit Workflow Skill
- [ ] Create `.agents/skills/audit-workflow/SKILL.md`
- [ ] Compare scaffold vs actual files
- [ ] Detect missing/extra files
- [ ] Update `manifest.json` automatically
- [ ] Report drift to user

## P1 - Important (improves workflow)

### 3. GitHub Actions CI
- [ ] Create `.github/workflows/ci.yml`
- [ ] On PR to develop: lint, test, validate
- [ ] Notebook execution tests
- [ ] Scaffold consistency checks

### 4. Pre-commit Hooks
- [ ] Create `.pre-commit-config.yaml`
- [ ] Notebook metadata validation
- [ ] YAML/JSON lint
- [ ] Conventional commit format

## P2 - Nice to have

### 5. PR Template
- [ ] Create `.github/pull_request_template.md`
- [ ] Structured PR descriptions

### 6. Issue Templates
- [ ] Create `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] Create `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] Structured bug reports

## Completed

- [x] Git flow skill (2026-09-14)
- [x] Pseudocode skills (2026-09-14)
- [x] Project scaffold (2026-09-14)
- [x] Python notebook skill (2026-09-14)
- [x] Post-task gate (2026-09-14)
- [x] Required packages section (2026-09-14)
