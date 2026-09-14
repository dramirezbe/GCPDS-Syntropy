# IIR Workflow Prompts — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Map the prompts that explore an IIR low-pass IQ exercise through natural language, formal pseudocode, GNU Radio, and Git collaboration.

## Tech stack & conventions
- SciPy workflow: `scipy.signal.butter` and `scipy.signal.lfilter` along axis 2.
- GNU Radio workflow: system-installed modules accessed through a `--system-site-packages` virtual environment.
- Pseudocode uses `←` for assignment, `=` for comparison, explicit block endings, PascalCase algorithms, and camelCase variables.
- Git examples use conventional commit messages and topic branches.

## Structure
```text
prompts/
├── iir-plain-instructions-to-code.md  # SciPy design from prose
├── iir-pseudocode-to-code.md          # Formal algorithm then Python
├── iir-gnuradio-to-code.md            # Flowgraph-oriented implementation
├── iir-git-flow.md                    # Gitflow exercise
└── iir-scaffold.md                    # Scaffold trigger phrase
```

## Entry points
- `prompts/iir-plain-instructions-to-code.md` -> most concrete SciPy requirements.
- `prompts/iir-pseudocode-to-code.md` -> concept-first route using the local pseudocode skill.
- `prompts/iir-gnuradio-to-code.md` -> flowgraph route requiring environment verification.

## Key interactions
- **Plain prompt <-> pseudocode prompt:** both target `(5, 2, 1000)` data and compare power before and after filtering.
- **GNU Radio prompt -> AGENTS.md:** implementation depends on system GNU Radio visibility.
- **Gitflow prompt -> implementation artifacts:** explains how future work could move through topic branches and pull requests.

## Common tasks & gotchas
- `single_pole_iir_filter_ff` is float-valued while `vector_source_c` and `vector_sink_c` are complex; this proposed chain requires correction or separate I/Q paths.
- `single_pole_iir_filter_ff` is provided by `gnuradio.filter`, despite the original prompt placing it under `gnuradio.blocks`.
- Normalized cutoff conventions must be stated consistently when SciPy filter code is created.
- `iir-scaffold.md` is only an invocation prompt, not repository documentation itself.

## Open questions / TODO
- The Cristian notebook resolves GNU Radio stream types by splitting complex input into float I/Q paths, filtering each path, and recombining them.
- The pseudocode workflow is implemented and runtime-validated in `cristian-work/iir_pseudocode_to_code.ipynb`.
- The plain-instructions workflow is implemented and runtime-validated in `cristian-work/iir_plain_instructions_to_code.ipynb`.
- Decide whether Gitflow is normative for this repository or only instructional content.
