# Examples — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: [study-nbs](./study-nbs/main.md), [iir-nnbs](./iir-nnbs/main.md), [final-nb](./final-nb/main.md), [nbqa-playground](./nbqa-playground/main.md)
> Last audited: 2026-09-15 @ commit `5e9b936`

## Purpose
Organize all learning materials into four categories: foundational study notebooks, IIR exercise notebooks across multiple authors, final validated notebooks, and NBQA quality playground.

## Tech stack & conventions
- Jupyter Notebook with Python 3 kernels.
- NumPy `float32` tensors use the canonical shape `(N, 2, L)`.
- Axis 0 is examples, axis 1 is I/Q components, and axis 2 is time samples.
- Each author's IIR notebooks live in their own subdirectory under `iir-nnbs/`.
- NBQA validates notebooks with `nbqa ruff`, `nbqa black`, `nbqa yapf`.

## Structure
```text
examples/
├── study-nbs/                       # Eight-notebook Pre-M0 curriculum
│   ├── pre_m0_1_python_functions_for_iq.ipynb
│   ├── pre_m0_2_numpy_iq_arrays_axes_and_dtypes.ipynb
│   ├── pre_m0_3_iq_indexing_and_slicing.ipynb
│   ├── pre_m0_4_iq_broadcasting_and_vectorized_operations.ipynb
│   ├── pre_m0_5_loading_and_inspecting_iq_files.ipynb
│   ├── pre_m0_6_iq_time_traces_and_constellations.ipynb
│   ├── pre_m0_7_joint_iq_power_and_complex_magnitude.ipynb
│   ├── pre_m0_8_iq_axes_power_and_capstone_check.ipynb
│   ├── pre_m0_generation_report.json
│   └── prompts/
│       ├── create-nbs.md
│       └── pass-criterion.txt
├── iir-nnbs/                        # IIR exercise notebooks by author
│   ├── cristian/
│   ├── isa/
│   ├── Novoa/
│   ├── pisso/
│   ├── sebato/
│   └── prompts/
│       ├── iir-git-flow.md
│       ├── iir-gnuradio-to-code.md
│       ├── iir-plain-instructions-to-code.md
│       ├── iir-pseudocode-to-code.md
│       └── iir-scaffold.md
├── final-nb/                        # Validated final notebooks
│   ├── reference-nb.ipynb           # ★ Reference implementation
│   ├── reference-nb-requirements.txt
│   └── issue-nb.ipynb               # Known-issue notebook for testing
└── nbqa-playground/                 # NBQA quality validation sandbox
    └── fail-nb.ipynb                # Intentional ruff F821/F822 failures
```

## Entry points
- `examples/study-nbs/pre_m0_1_python_functions_for_iq.ipynb` -> begin the sequential curriculum.
- `examples/iir-nnbs/prompts/iir-pseudocode-to-code.md` -> pseudocode to SciPy implementation.
- `examples/iir-nnbs/cristian/WORKSPACE.md` -> Cristian's notebook map and conventions.
- `examples/final-nb/reference-nb.ipynb` -> validated reference implementation.
- `examples/nbqa-playground/fail-nb.ipynb` -> intentional failures for NBQA gate testing.

## Key interactions
- **Study notebooks:** sequential learning path from Python basics to IQ power analysis.
- **IIR notebooks:** parallel implementations of the same filtering exercise across authors.
- **Final notebooks:** validated reference and issue notebooks for quality benchmarks.
- **NBQA playground:** sandbox for testing ruff/black/yapf notebook linting pipelines.
- **Prompts:** generation contracts and implementation guides for both categories.

## Common tasks & gotchas
- Preserve `(N, 2, L)` shape convention; swapping axes 1 and 2 is intentional teaching defect.
- Use `np.mean(I**2 + Q**2)` and `np.mean(np.abs(I + 1j*Q)**2)` as equivalent power calculations.
- GNU Radio execution requires `--system-site-packages` virtual environment; see `AGENTS.md`.
- IIR notebooks use `scipy.signal.lfilter` along axis 2 and compare mean IQ power before/after filtering.
- `fail-nb.ipynb` triggers F821 (undefined name) and F822 (undefined in `__all__`) — used to validate the fatal gate.

## Open questions / TODO
- Add explicit environment or requirements file for notebook dependencies.
- Consider adding notebook execution tests to CI pipeline.
