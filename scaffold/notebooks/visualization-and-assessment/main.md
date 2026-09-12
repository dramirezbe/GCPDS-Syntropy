# Notebook Visualization and Assessment — Layer 2

> Parent: [../main.md](../main.md)
> Last audited: 2026-09-12 @ commit `ce73307`

## Purpose
Document notebooks 6-8, which apply the established IQ contract to time traces, constellations, power equivalence, and a final capstone check.

## Tech stack & conventions
- NumPy generates deterministic synthetic signals.
- Matplotlib renders time traces, constellation scatter plots, and power comparisons.
- Power checks use `rtol=1e-5` and `atol=1e-7` according to the generation report.

## Structure
```text
notebooks/
├── pre_m0_6_iq_time_traces_and_constellations.ipynb     # Visualization
├── pre_m0_7_joint_iq_power_and_complex_magnitude.ipynb  # Power proof and exercises
├── pre_m0_8_iq_axes_power_and_capstone_check.ipynb      # Cumulative assessment
└── pre_m0_generation_report.json                        # Scope and gate inventory
```

## Entry points
- `notebooks/pre_m0_6_iq_time_traces_and_constellations.ipynb` -> first visualization-focused lab.
- `notebooks/pre_m0_8_iq_axes_power_and_capstone_check.ipynb` -> terminal assessment and pass-gate summary.

## Key interactions
- **Canonical tensor -> plots:** component slices become time traces and I/Q scatter coordinates.
- **Real representation -> complex representation:** `I**2 + Q**2` is validated against `abs(I + 1j*Q)**2`.
- **Prior notebooks -> capstone:** axes, indexing, broadcasting, plotting, and power are evaluated together.

## Common tasks & gotchas
- A constellation plots Q against I; it does not use the time axis as a plotted coordinate.
- Keep reductions explicit so per-example power and global power are not confused.
- Do not mark the manual PC-1 gate true without an independently reviewed learner explanation.

## Open questions / TODO
- The repository has no automated notebook execution test proving Restart & Run All behavior.
