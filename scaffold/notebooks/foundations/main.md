# Notebook Foundations — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Document notebooks 1-5, which introduce functions, array representation, indexing, broadcasting, and safe IQ file inspection before visualization and synthesis.

## Tech stack & conventions
- NumPy is the core dependency; notebooks 3-4 also use Matplotlib for small demonstrations.
- Notebook 5 uses `pathlib.Path` and `np.load(..., allow_pickle=False)`.
- Integer indexing removes an axis while slicing preserves it.

## Structure
```text
notebooks/
├── pre_m0_1_python_functions_for_iq.ipynb              # Functions and return values
├── pre_m0_2_numpy_iq_arrays_axes_and_dtypes.ipynb       # Arrays, axes, and dtypes
├── pre_m0_3_iq_indexing_and_slicing.ipynb               # Index and slice semantics
├── pre_m0_4_iq_broadcasting_and_vectorized_operations.ipynb
└── pre_m0_5_loading_and_inspecting_iq_files.ipynb       # NPZ loading and validation
```

## Entry points
- `notebooks/pre_m0_1_python_functions_for_iq.ipynb` -> defines the first reusable IQ inspection and power functions.
- `notebooks/pre_m0_5_loading_and_inspecting_iq_files.ipynb` -> boundary between in-memory fundamentals and persisted IQ arrays.

## Key interactions
- **Functions -> later notebooks:** component extraction and power functions establish vocabulary reused throughout the sequence.
- **Axes/indexing -> broadcasting:** learners must understand shapes before component-wise vectorization.
- **File loading -> data contract:** loaded arrays are checked against dimensionality and I/Q-axis expectations.

## Common tasks & gotchas
- Prefer `X[0:1]` over `X[0]` when preserving the batch dimension matters.
- Broadcasting component scales requires shapes compatible with `(N, 2, L)`, commonly `(1, 2, 1)`.
- Never enable pickle merely to make an unknown NPZ file load.

## Open questions / TODO
- No shared Python module currently centralizes duplicated data-generation and validation helpers.
