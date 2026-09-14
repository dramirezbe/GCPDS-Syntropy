Act as a university Python/NumPy laboratory designer focused on IQ signals and as a generator of reproducible Jupyter notebooks.

Your task is to CREATE EXACTLY EIGHT `.ipynb` files, corresponding exclusively to:

**Pre-M0 — Python through IQ (W1)**

All eight notebooks MUST be created under:

`@notebooks/`

Every generated notebook MUST satisfy and pass:

`@prompts/nb-pass-criterion.txt`

You must read and strictly obey `@prompts/nb-pass-criterion.txt` before creating the notebooks.

Do not create a single notebook with eight sections.

You must generate **EIGHT independent notebooks**, each executable individually from top to bottom.

============================================================
SOURCE OF TRUTH FOR THE PASS CRITERION
======================================

The mandatory pass criterion is defined by:

`@prompts/nb-pass-criterion.txt`

You must treat that file as the authoritative source of truth.

The required outcome is:

1. The student must be able to explain array axes INDEPENDENTLY.
2. The student must be able to correct an injected axis swap.
3. Power must agree with a direct calculation using complex magnitude.

These three requirements are mandatory in **EACH of the eight notebooks**.

A notebook cannot be considered passing if any of these three requirements lacks evidence or its corresponding gate is not satisfied.

============================================================
GENERAL PRE-M0 OBJECTIVE
========================

Close the initial programming gap using IQ signals as a familiar context.

Cover only:

* functions;
* indexing;
* slicing;
* broadcasting;
* dtypes;
* file loading;
* plotting;
* joint IQ power.

Defer custom classes until they are actually needed.

============================================================
REQUIRED OUTPUT FILES
=====================

Create exactly these eight notebooks under `@notebooks/`:

1. `pre_m0_1_python_functions_for_iq.ipynb`

2. `pre_m0_2_numpy_iq_arrays_axes_and_dtypes.ipynb`

3. `pre_m0_3_iq_indexing_and_slicing.ipynb`

4. `pre_m0_4_iq_broadcasting_and_vectorized_operations.ipynb`

5. `pre_m0_5_loading_and_inspecting_iq_files.ipynb`

6. `pre_m0_6_iq_time_traces_and_constellations.ipynb`

7. `pre_m0_7_joint_iq_power_and_complex_magnitude.ipynb`

8. `pre_m0_8_iq_axes_power_and_capstone_check.ipynb`

Do not change these filenames.

Also create:

`pre_m0_generation_report.json`

The final set of deliverables must contain exactly these nine files.

============================================================
COMMON IQ CONTRACT
==================

Whenever possible, use the canonical layout:

`X.shape == (N, 2, L)`

Expected interpretation:

* axis 0 -> examples
* axis 1 -> I/Q components
* axis 2 -> time samples

An individual example must have:

`sample.shape == (2, L)`

where:

`sample[0] = I`

`sample[1] = Q`

Prefer:

`dtype = np.float32`

Use small, pedagogical datasets.

When generating synthetic data, use:

`SEED = 42`

and reproducible mechanisms.

============================================================
STRICT GLOBAL RESTRICTIONS
==========================

DO NOT include:

* custom classes;
* object-oriented programming as course content;
* PyTorch;
* TensorFlow;
* Keras;
* autograd;
* training;
* optimizers;
* CNN;
* MLP;
* DataLoader;
* GPU;
* CUDA;
* ONNX;
* deployment;
* streaming;
* RTL-SDR acquisition;
* STFT;
* spectrograms;
* PSD;
* filtering;
* demodulation;
* SNR estimation;
* RF calibration;
* dBm;
* 50-ohm conversion;
* content belonging to M0 or later modules.

Use primarily:

```python
import numpy as np
```

and, only where appropriate:

```python
import matplotlib.pyplot as plt
from pathlib import Path
```

Do not add unnecessary dependencies.

============================================================
COMMON PEDAGOGICAL ARCHITECTURE
===============================

Each notebook must follow this logical order:

1. Title.
2. Unit objective.
3. What the student should learn.
4. IQ data used.
5. Guided development of the specific concept.
6. Small examples.
7. Student exercises.
8. Pass Criterion Challenge.
9. Automatic validations.
10. Manual evaluation of axis explanation.
11. Final PASS/WAIT report.

Use Markdown before introducing new concepts.

Avoid excessively long cells.

Code must be readable for students with introductory Python knowledge.

Do not hide pedagogically important operations inside overly complex functions.

============================================================
FUNDAMENTAL RULE ABOUT STUDENT ANSWERS
======================================

The assessment requires the student to explain the axes INDEPENDENTLY.

Therefore:

DO NOT immediately reveal the answers to exercises evaluating:

* axis meaning;
* injected axis swap.

There must first be a section titled:

`STUDENT ATTEMPT`

containing incomplete cells and/or questions.

If a solution is provided, it must appear only afterward in a separate section titled:

`OPTIONAL SOLUTION — REVEAL ONLY AFTER ATTEMPT`

Do not use the optional solution automatically to complete the student's exercise.

============================================================
COMMON PASS CRITERION FOR ALL 8 NOTEBOOKS
=========================================

Every notebook MUST contain all three of the following tests.

---

## PC-1 — INDEPENDENT AXIS EXPLANATION

Include a section titled:

`STUDENT AXIS EXPLANATION`

The student must answer in Markdown, at minimum:

1. What does axis 0 represent?
2. What does axis 1 represent?
3. What does axis 2 represent?
4. Why does one axis have size 2?
5. Where are I and Q located?
6. Where are the temporal samples located?

DO NOT automatically evaluate this by string comparison.

Explicitly create:

```python
AXES_EXPLANATION_VERIFIED = False
```

and explain:

> This variable must only be manually changed to `True` by the student/instructor after the independent explanation has been reviewed.

The notebook MUST NOT emit final PASS while:

```python
AXES_EXPLANATION_VERIFIED == False
```

---

## PC-2 — INJECTED AXIS SWAP

Starting from the correct array:

```python
X.shape == (N, 2, L)
```

deliberately create:

```python
X_swapped = np.transpose(X, (0, 2, 1))
```

so that:

```python
X_swapped.shape == (N, L, 2)
```

The inversion must be presented as a deliberately injected error.

DO NOT show the correction before the student attempt.

The student must:

1. inspect `X_swapped.shape`;
2. identify which axis should contain I/Q;
3. explain why the new shape is incorrect;
4. write the corrective operation;
5. produce `X_fixed`;
6. demonstrate that `X_fixed` exactly recovers the original.

Mandatory validation:

```python
axis_swap_corrected = (
    X_fixed.shape == X.shape
    and X_fixed.dtype == X.dtype
    and np.array_equal(X_fixed, X)
)
```

Also use:

```python
assert X_fixed.shape == X.shape
assert X_fixed.dtype == X.dtype
assert np.array_equal(X_fixed, X)
```

Display:

`AXIS SWAP CHECK: PASS`

only when the correction is true.

Otherwise display:

`AXIS SWAP CHECK: WAIT`

---

## PC-3 — IQ POWER AGREEMENT

Calculate power through TWO independent paths.

Method A — real components:

```python
I = ...
Q = ...

P_iq = np.mean(I**2 + Q**2)
```

Method B — direct complex magnitude:

```python
z = I + 1j*Q

P_complex = np.mean(np.abs(z)**2)
```

The two paths MUST be implemented independently.

One function must not call the other.

Validate using explicit tolerances, for example:

```python
POWER_RTOL = 1e-5
POWER_ATOL = 1e-7

power_consistency = np.allclose(
    P_iq,
    P_complex,
    rtol=POWER_RTOL,
    atol=POWER_ATOL
)

assert power_consistency
```

Display:

```text
POWER COMPONENT METHOD = ...
POWER COMPLEX METHOD   = ...
ABSOLUTE DIFFERENCE    = ...
POWER CHECK: PASS
```

only when the check is true.

============================================================
COMMON FINAL PASS GATE
======================

Every notebook must end with a section titled:

`PASS CRITERION GATE`

At minimum:

```python
automatic_checks = {
    "axis_swap_corrected": axis_swap_corrected,
    "power_consistency": power_consistency,
}

automatic_pass = all(automatic_checks.values())

final_pass = (
    automatic_pass
    and AXES_EXPLANATION_VERIFIED
)
```

Display individually:

```text
AXES EXPLANATION: PASS/WAIT
AXIS SWAP CHECK: PASS/WAIT
POWER CHECK: PASS/WAIT
```

The notebook may print:

`PRE-M0.X FINAL STATUS: PASS`

only when:

```python
AXES_EXPLANATION_VERIFIED == True
```

AND

```python
axis_swap_corrected == True
```

AND

```python
power_consistency == True
```

Otherwise it MUST print:

`PRE-M0.X FINAL STATUS: WAIT`

Replace `X` with the correct notebook number.

============================================================
NOTEBOOK 1
pre_m0_1_python_functions_for_iq.ipynb
======================================

UNIT FOCUS:

Python functions applied to IQ.

Cover only:

* `def`;
* parameters;
* `return`;
* local variables;
* calling functions;
* arrays as function arguments;
* shape/dtype inspection inside functions.

Implement at minimum:

```python
describe_array(x)
number_of_samples(x)
get_iq_components(x)
joint_iq_power(x)
complex_magnitude_power(x)
```

The student must clearly understand:

`input -> processing -> return value`

Include a specific exercise about the difference between:

```python
print(...)
```

and:

```python
return ...
```

The common Pass Criterion remains mandatory.

Do not turn this notebook into a general NumPy tutorial.

============================================================
NOTEBOOK 2
pre_m0_2_numpy_iq_arrays_axes_and_dtypes.ipynb
==============================================

UNIT FOCUS:

NumPy arrays, dimensions, axes, and dtypes.

Cover:

* `ndarray`;
* `shape`;
* `ndim`;
* `size`;
* `axis`;
* `float32`;
* `float64`;
* `complex64`;
* `complex128`;
* `astype`;
* `.real`;
* `.imag`;
* `I + 1j*Q`.

Build progressively:

```python
I.shape == (L,)
Q.shape == (L,)
sample.shape == (2, L)
X.shape == (N, 2, L)
```

Include a Markdown table:

| Object | Shape | ndim | dtype | Meaning of axes |
| ------ | ----- | ---- | ----- | --------------- |

Include exercises using:

`PREDICT THE SHAPE BEFORE RUNNING.`

The common Pass Criterion remains mandatory.

============================================================
NOTEBOOK 3
pre_m0_3_iq_indexing_and_slicing.ipynb
======================================

UNIT FOCUS:

Indexing and slicing.

Cover:

```python
X[0]

X[0:1]

X[:,0,:]

X[:,1,:]

X[0,0,:]

X[0,:,10:30]

X[:,:,::2]
```

Explicitly explain:

> Integer indexing can remove an axis.

and:

> Slicing can preserve an axis.

Compare shapes before and after each operation.

Include exercises where the student:

* selects one example;
* selects I;
* selects Q;
* extracts samples `20:40`;
* preserves the batch dimension;
* predicts output shapes.

The injected axis swap must be diagnosed specifically using knowledge of indexing and slicing.

The common Pass Criterion is mandatory.

============================================================
NOTEBOOK 4
pre_m0_4_iq_broadcasting_and_vectorized_operations.ipynb
========================================================

UNIT FOCUS:

Broadcasting and vectorized operations.

Cover:

* element-wise operations;
* scalar multiplication;
* broadcasting;
* compatible shapes;
* incompatible shapes;
* vectorization;
* channel-wise scaling.

Use, for example:

```python
X.shape == (N,2,L)

channel_scales.shape == (1,2,1)

scaled = X * channel_scales
```

Explain why broadcasting works.

Show an incompatible case and capture the error pedagogically.

Compare:

Python loop

versus

vectorized NumPy operation

and demonstrate with `np.allclose` that they produce the same result.

Relate the injected axis swap to a semantic broadcasting problem.

The common Pass Criterion is mandatory.

============================================================
NOTEBOOK 5
pre_m0_5_loading_and_inspecting_iq_files.ipynb
==============================================

UNIT FOCUS:

File loading and IQ inspection.

The notebook must be self-contained.

First create a small demonstrative NPZ file:

`demo_iq.npz`

containing:

```python
iq.shape == (N,2,L)
```

Then load it using:

```python
Path
np.load(..., allow_pickle=False)
```

Cover:

* `Path.exists()`;
* NPZ keys;
* shape;
* ndim;
* dtype;
* nbytes;
* safe loading.

Implement:

```python
inspect_iq_array(iq)
```

Include pedagogical examples of:

* nonexistent file;
* wrong key;
* wrong ndim;
* unexpected IQ axis.

Also create a deliberately axis-swapped file or variable and have the student diagnose it when loading.

The common Pass Criterion is mandatory.

=============
