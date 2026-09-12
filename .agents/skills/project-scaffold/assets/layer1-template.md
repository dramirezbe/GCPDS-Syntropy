# {Section Name} — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: [{sub1}](./{sub1}/main.md), [{sub2}](./{sub2}/main.md)
> Last audited: YYYY-MM-DD @ commit <SHORT_SHA>

## Purpose
{One-paragraph description of what this section does in the system.}

## Tech stack & conventions
- {Language / framework} ^{version}
- {Key dependencies}
- {Build tool}
- {Testing framework}
- {Container / deployment tech}

## Structure
```
{section}/
├── {file}              # ★ ENTRY POINT: what it does
├── {dir}/
│   ├── {file}          # {purpose}
│   └── {file}          # {purpose}
├── Dockerfile          # {build strategy}
├── package.json        # {note if relevant}
└── ...
```

## Entry points
- `{path}` -> {what happens on startup / import}
- `{path}` -> {secondary entry point}

## Key interactions
- **{Consumer} -> {This section}:** {how they call it}
- **{This section} -> {Downstream}:** {what it calls}
- **{Shared resource}:** {database, message queue, file system}

## Common tasks & gotchas
- {Task 1}
- {Known issue 1}
- {Convention to follow}

## Open questions / TODO
- {Question 1}
- {Planned refactor}
