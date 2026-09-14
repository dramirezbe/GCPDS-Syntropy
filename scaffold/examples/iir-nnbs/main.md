# IIR Notebooks — Layer 2

> Parent: [../main.md](../main.md)
> Children: none
> Last audited: 2026-09-14 @ commit `27696d6`

## Purpose
Document IIR filter exercise notebooks implemented by multiple authors, each following the same filtering exercise with different approaches.

## Tech stack & conventions
- Python 3 Jupyter notebooks using NumPy, SciPy, and optionally GNU Radio.
- IIR low-pass filter applied to synthetic IQ signals.
- Canonical data contract: `X.shape == (N, 2, L)`, `float32`.
- Each author implements three variants: GNU Radio, plain instructions, pseudocode-to-code.

## Structure
```text
examples/iir-nnbs/
├── cristian/
│   ├── WORKSPACE.md
│   ├── iir_gnuradio_filter.ipynb
│   ├── iir_plain_instructions_to_code.ipynb
│   └── iir_pseudocode_to_code.ipynb
├── isa/
│   ├── iir_gnuradio.ipynb
│   ├── iir_plain_to_code.ipynb
│   └── iir_pseudocode_to_code.ipynb
├── Novoa/
│   ├── iir_gnuradio_filter.ipynb
│   ├── iir_plain_instructions_to_code.ipynb
│   ├── iir_pseudocode_to_code.ipynb
│   ├── filtered_iq.npz
│   └── filtered_iq_from_pseudocode.npz
├── pisso/
│   ├── iir_gnuradio_filter.ipynb
│   ├── iir_plain_instructions.ipynb
│   └── iir_pseudocode_to_code.ipynb
├── sebato/
│   ├── iir_gnuradio_iq_filter.ipynb
│   ├── iir_plain_instructions_to_code.ipynb
│   └── iir_pseudocode_to_code.ipynb
└── prompts/
    ├── iir-git-flow.md
    ├── iir-gnuradio-to-code.md
    ├── iir-plain-instructions-to-code.md
    ├── iir-pseudocode-to-code.md
    └── iir-scaffold.md
```

## Entry points
- `examples/iir-nnbs/cristian/WORKSPACE.md` -> Cristian's notebook map and conventions.
- `examples/iir-nnbs/prompts/iir-pseudocode-to-code.md` -> pseudocode to SciPy implementation.
- `examples/iir-nnbs/prompts/iir-gnuradio-to-code.md` -> GNU Radio implementation prompt.

## Key interactions
- **Prompts -> notebooks:** each prompt describes an alternative representation of the same filtering exercise.
- **GNU Radio notebooks:** require system packages and `--system-site-packages` virtual environment.
- **Plain instructions notebooks:** direct SciPy implementation with plots and NPZ output.
- **Pseudocode notebooks:** algorithm design then Python translation.

## Common tasks & gotchas
- GNU Radio execution requires the system dependency described in `AGENTS.md`.
- IIR notebooks use `scipy.signal.lfilter` along axis 2 and compare mean IQ power before/after filtering.
- The GNU Radio example mixes complex and float block names; verify block type compatibility before implementation.
- Treat Gitflow content as a learning prompt, not proof that the repository currently has those branches.

## Open questions / TODO
- Reconcile exact GNU Radio block types before using the example as executable code.
- Consider adding notebook execution tests for IIR exercises.
