# Prompt: Pseudocode → Code (IIR Filter)

## Context

Topic: IIR filter applied to IQ dummy signal
Skill: `pseudocode` (from `.agents/skills/pseudocode/SKILL.md`)

## Skill to Use

Load the `pseudocode` skill first, then follow its activation contract.

## Prompt

```
Using the pseudocode skill, write pseudocode for an IIR low-pass filter applied to a synthetic IQ signal.

Requirements:
- Generate a synthetic IQ signal: X.shape == (N, 2, L) with SEED=42
- Design a 2nd-order IIR low-pass filter (Butterworth)
- Apply the filter along axis 2 (time samples) for each example
- Compute and compare power before and after filtering

Follow pseudocode conventions:
- Use ← for assignment
- Use = for comparison
- Close all blocks explicitly (END FOR, END IF, END FUNCTION)
- PascalCase for algorithms, camelCase for variables

Then translate the pseudocode to Python/NumPy code.
```

## Example Pseudocode Structure

```
FUNCTION DesignButterworthIIR(cutoff, sample_rate, order)
    DECLARE b AS ARRAY
    DECLARE a AS ARRAY
    ← compute filter coefficients
    RETURN (b, a)
END FUNCTION

FUNCTION ApplyIIRFilter(signal, b, a)
    DECLARE filtered AS ARRAY
    ← scipy.signal.lfilter(b, a, signal, axis=2)
    RETURN filtered
END FUNCTION

FUNCTION ComputePower(iq_array)
    DECLARE I, Q AS ARRAY
    ← extract components
    RETURN mean(I² + Q²)
END FUNCTION

--- Main ---
X ← GenerateSyntheticIQ(N=5, L=1000, seed=42)
(b, a) ← DesignButterworthIIR(cutoff=0.1, sample_rate=1.0, order=2)
X_filtered ← ApplyIIRFilter(X, b, a)
P_before ← ComputePower(X)
P_after ← ComputePower(X_filtered)
```

## Expected Output

1. Pseudocode block following conventions
2. Python/NumPy translation with `scipy.signal`
3. Validation that power changes after filtering
