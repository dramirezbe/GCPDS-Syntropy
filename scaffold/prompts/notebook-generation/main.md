# Notebook Generation Prompts — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Describe the prompt pair that defines the exact eight-notebook Pre-M0 curriculum and its mandatory learner evidence.

## Tech stack & conventions
- Notebook output is raw `.ipynb` content under `notebooks/`.
- Each notebook is independent and executable from top to bottom.
- Scope excludes classes, ML frameworks, SDR hardware, filtering, demodulation, and advanced spectral work.

## Structure
```text
prompts/
├── create-nbs.md          # ★ ENTRY POINT: complete generation specification
└── pass-criterion.txt     # Compact authoritative acceptance contract
```

## Entry points
- `prompts/create-nbs.md` -> enumerates filenames, pedagogy, and required evidence.
- `prompts/pass-criterion.txt` -> resolves acceptance questions when other wording is ambiguous.

## Key interactions
- **Pass criterion -> generation prompt:** three outcomes are expanded into PC-1, PC-2, and PC-3 gates.
- **Generation prompt -> report:** `notebooks/pre_m0_generation_report.json` records produced files and compliance.

## Common tasks & gotchas
- Do not collapse the curriculum into one notebook; exactly eight independent files are required.
- Manual axis reasoning cannot be replaced with only a Boolean computed from code.
- Keep topics within Pre-M0 scope even when IQ examples suggest more advanced SDR material.

## Open questions / TODO
- `create-nbs.md` refers to `prompts/nb-pass-criterion.txt`, while the tracked file is `prompts/pass-criterion.txt`; align the filename before regeneration.
