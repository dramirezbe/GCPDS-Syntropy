# Notebooks — Layer 1

> Parent: [../INDEX.md](../INDEX.md)
> Children: [foundations](./foundations/main.md), [visualization-and-assessment](./visualization-and-assessment/main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Deliver an eight-notebook Pre-M0 learning sequence that closes foundational Python and NumPy gaps using familiar in-memory IQ signals.

## Tech stack & conventions
- Python 3 Jupyter notebooks using NumPy and, where visualization is needed, Matplotlib.
- Reproducibility uses `SEED = 42` or an equivalent deterministic NumPy generator.
- Canonical data contract: `X.shape == (N, 2, L)`, `float32`, with I at index 0 and Q at index 1.
- Each notebook contains PC-1 axis explanation, PC-2 injected axis-swap recovery, and PC-3 power-equivalence evidence.
- Notebook outputs are cleared in the tracked files.

## Structure
```text
notebooks/
├── pre_m0_1_python_functions_for_iq.ipynb
├── pre_m0_2_numpy_iq_arrays_axes_and_dtypes.ipynb
├── pre_m0_3_iq_indexing_and_slicing.ipynb
├── pre_m0_4_iq_broadcasting_and_vectorized_operations.ipynb
├── pre_m0_5_loading_and_inspecting_iq_files.ipynb
├── pre_m0_6_iq_time_traces_and_constellations.ipynb
├── pre_m0_7_joint_iq_power_and_complex_magnitude.ipynb
├── pre_m0_8_iq_axes_power_and_capstone_check.ipynb
└── pre_m0_generation_report.json    # Machine-readable generation inventory
```

## Entry points
- `notebooks/pre_m0_1_python_functions_for_iq.ipynb` -> begin the sequential curriculum.
- `notebooks/pre_m0_generation_report.json` -> inspect titles, focuses, cell counts, gates, and restrictions.

## Key interactions
- **Generation prompt -> notebooks:** `prompts/create-nbs.md` defines exact filenames and learning scope.
- **Pass criterion -> notebooks:** `prompts/pass-criterion.txt` supplies the three mandatory outcomes repeated in every notebook.
- **Notebook 1-5 -> notebook 6-8:** foundations prepare learners for visualization, power reasoning, and capstone assessment.

## Common tasks & gotchas
- Preserve `(N, 2, L)`; swapping axes 1 and 2 is an intentional teaching defect, not a new convention.
- Use `np.mean(I**2 + Q**2)` and `np.mean(np.abs(I + 1j*Q)**2)` as equivalent power calculations.
- Notebook 5 creates a temporary `demo_iq.npz` while demonstrating safe loading.
- PC-1 remains intentionally manual; an automated run alone cannot certify the learner explanation.

## Open questions / TODO
- Add an explicit environment or requirements file for notebook dependencies.
- Decide whether generated runtime artifacts should always be written to a dedicated temporary directory.
