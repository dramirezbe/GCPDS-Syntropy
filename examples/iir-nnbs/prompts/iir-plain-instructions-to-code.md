# Prompt: Plain Instructions → Code (IIR Filter)

## Context

Topic: IIR filter applied to IQ dummy signal
Goal: Generate code from natural language instructions

## Prompt

```
Write a Python script that applies an IIR low-pass filter to a synthetic IQ signal.

Requirements:
- Generate a synthetic IQ signal with 5 examples, 1000 time samples each
- Use the canonical layout: X.shape == (N, 2, L)
- Design a 2nd-order Butterworth IIR low-pass filter with cutoff frequency 0.1 (normalized)
- Apply the filter along the time axis (axis=2) for each I and Q component separately
- Compute power before and after filtering
- Plot time traces and constellations before and after filtering
- Save the filtered signal to an NPZ file

The script should:
1. Import numpy, scipy.signal, matplotlib.pyplot
2. Set SEED=42 for reproducibility
3. Create synthetic IQ data: sinusoidal components with noise
4. Design filter coefficients using scipy.signal.butter
5. Apply filter using scipy.signal.lfilter
6. Compute power: P = mean(I² + Q²)
7. Create 4 subplots: (a) I time trace, (b) Q time trace, (c) I/Q constellation, (d) power comparison
8. Save result to 'filtered_iq.npz'
9. Print verification: shape, dtype, power before, power after, power ratio

Expected output shape: X_filtered.shape == (5, 2, 1000)
```

## Expected Output

1. Complete Python script
2. Synthetic IQ generation
3. IIR filter design and application
4. Power computation and comparison
5. Visualization with matplotlib
6. File output
