# M2 — IQ Pipelines and Streaming (W5/W7)

## Goal
Preserve data semantics offline and live.

## M2.1 (W5)
Validate IQ order, shape, labels, sample-rate assumptions and normalization. Use a map-style DataLoader for finite data. Compare a baseline and optimized loader only with equivalent data and preprocessing semantics.

**Artifact.** Pipeline checks and a small throughput/memory benchmark.

**Pass criterion.** No split leakage or label changes; measured improvement is not mandatory. Cache deterministic work, not a fixed realization of random augmentation.

**Note.** Per-window joint-power normalization uses the current window only; it does not fit dataset statistics. Preserve received power separately for signal detection. Never normalize I and Q independently without justification.

## M2.2 (W5)
Apply training-only phase rotation, bounded CFO, noise and channel impairments. Preserve modulation identity and explain each bound.

**Pass criterion.** Students verify the power/noise model and label semantics. Adding noise to already noisy IQ does not establish a new exact SNR without knowledge of the underlying signal and noise powers.

## M2.3 (W7)
Connect continuous acquisition or replay to stateful channel selection, filtering/resampling, window assembly and a bounded queue. Record session metadata before windowing; retain filter state across chunks.

**Artifact.** Chunk-safe pipeline, ring-buffer implementation, queue/drop logs and replay comparisons using different chunk sizes.

**Pass criterion.** Equivalent replay streams produce equivalent windows despite chunk boundaries. No accidental duplication occurs; discontinuities reset state explicitly. Acquisition and inference run independently. Deliberate inference subsampling is distinguished from lost acquisition samples.

**Note.** An IterableDataset is optional for actual streams, not required for finite RadioML arrays. Training prefetch and receiver buffering solve different problems and have different correctness criteria.

## LLM harness context
The harness extends to data pipeline validation and streaming. The LLM can verify pipeline correctness, inspect augmentation bounds, and monitor acquisition state.

| Tool | Purpose |
|------|---------|
| `pipeline.validate` | Check IQ order, shape, labels, sample-rate, normalization; detect split leakage |
| `pipeline.benchmark` | Throughput/memory comparison between baseline and optimized loader |
| `augmentation.configure` | Set training-only augmentations (phase rotation, CFO, noise) with explicit bounds |
| `augmentation.verify` | Verify label preservation and power/noise model after augmentation |
| `streaming.status` | Monitor acquisition/replay: chunk assembly, queue depth, drop count, filter state |
| `streaming.replay_compare` | Compare windows from different chunk sizes; verify equivalence |

---

# Class Plan — M2: IQ Pipelines and Streaming (1 hour)

## Motivation: Why This Matters

In M1 the students trained a CNN on IQ data that was already clean, split, and loaded. But that's a lab fantasy. In the real world:

- Data arrives as a continuous stream of samples, not neatly windowed tensors.
- The pipeline between the antenna and the model is where most silent failures hide: a swapped axis, a normalization that leaks dataset statistics into validation, an augmentation that accidentally changes the modulation label.
- On the Pi, samples arrive faster than inference runs — you need buffering, dropping policies, and stateful DSP that doesn't reset between chunks.

The core lesson: **the pipeline IS the system.** A perfect model with a broken pipeline is a broken system. A mediocre model with a correct pipeline at least gives you honest results.

---

## Part 1 — Data Integrity: Trust Nothing (20 min)

### Concept: The Pipeline Contract

Every stage in the pipeline has a contract: what shape comes in, what shape goes out, what invariants are preserved. Break any contract silently, and you get results that look plausible but are wrong.

**Live demonstration (instructor drives, students follow):**

1. Load the RadioML NPZ. Verify `X.shape == (N, 2, 128)`. Ask: which axis is I? Which is Q? How do you know — from the shape, or from the documentation?

2. Show a deliberate axis swap `X[:, [1, 0], :]` and plot constellations before/after. For most modulations this looks subtly different — for some (like BPSK) it looks identical. Ask: would your M1 model catch this? (Answer: probably not, accuracy might barely change, but phase-dependent modulations like QAM will degrade at high SNR.)

3. **Normalization trap.** Show two normalizations:
   - Per-window joint power: `p = mean(sum(x², axis=I/Q))` → divide by `sqrt(p)`. Correct.
   - Dataset-wide statistics: `mean = X_train.mean(axis=0); std = X_train.std(axis=0)` → standardize. **Wrong** — it leaks training statistics into validation, destroys received power information, and normalizes I and Q with different scales.

   Ask: why does the second one give you *better* validation accuracy? (Answer: because it's cheating — validation data was implicitly informed by training distribution.)

4. **Split leakage.** Show what happens when you window a continuous recording first, then split windows into train/val/test randomly. Adjacent windows from the same transmission share channel state — they're not independent. The model memorizes channel fingerprints, not modulation.

### Key takeaway
Validate IQ order, shape, labels, sample-rate, and normalization *before* any experiment. The harness `pipeline.validate` tool automates these checks — but the student must know what each check catches and why.

---

## Part 2 — Augmentation: Controlled Impairment (15 min)

### Concept: Augmentation as Domain Knowledge

Augmentation in IQ is not like flipping an image. Every transformation has physical meaning, and wrong bounds destroy the label.

**Three augmentations with physical grounding:**

1. **Phase rotation** — `x_aug = x * exp(j*θ)`, uniform θ ∈ [0, 2π). Safe for all modulations because modulation is defined by relative phase, not absolute. Implementation: rotate both I and Q channels jointly using a 2×2 rotation matrix.

2. **Carrier frequency offset (CFO)** — `x_aug(t) = x(t) * exp(j*2π*Δf*t)`. Simulates imperfect tuning. Bound Δf so the signal stays within the receiver bandwidth. Ask: what happens to a 16-QAM constellation with CFO? (It spirals — the longer the window, the more rotation accumulates.)

3. **Additive noise** — Add white Gaussian noise to simulate lower SNR. Critical trap: the original data already has noise at some SNR. Adding more noise doesn't give you a precise new SNR unless you know the original signal and noise powers separately. You can only say "SNR decreased by approximately X dB."

**Ask:** For each augmentation, can you change the modulation label? Phase rotation: no. CFO beyond bounds: yes (constellation becomes unrecognizable). Excessive noise: yes (buried in noise, even a human can't classify it).

### Key takeaway
Every augmentation bound must be justified by physics. The harness `augmentation.verify` tool checks that labels are preserved — but the student must explain *why* a bound is safe.

---

## Part 3 — Streaming: The Real World (20 min)

### Concept: From Finite Dataset to Continuous Stream

On the Pi, the RTL-SDR delivers a continuous stream of IQ samples. The pipeline must:
- Select a channel (tune, filter, resample)
- Assemble fixed-length windows from a continuous stream
- Buffer windows for inference (which is slower than acquisition)
- Handle discontinuities (dropped samples, retunes, device reconnection)

**Key problems to illustrate:**

1. **Chunk boundaries.** The SDR gives you chunks of N samples. Your window is 128 samples. What happens when a window spans two chunks? You need to retain state — the tail of chunk k becomes the head of window in chunk k+1. Show that naive per-chunk windowing misses or duplicates samples at boundaries.

2. **Ring buffer.** Draw the ring buffer on the board: write pointer advances with acquisition, read pointer advances with inference. When write laps read, you drop — and you must log the drop, not silently skip. When read catches write, you wait. Ask: is dropping always bad? (No — in real-time inference, a fresh window is more valuable than an old one.)

3. **Filter state across chunks.** If you apply a low-pass filter, the filter has internal state (delay line). Resetting it between chunks introduces transients at every chunk boundary. Show a plot: filtered signal with state retained vs. state reset — the edges are visibly different.

4. **Metadata before windowing.** Record session start time, sample rate, center frequency, gain, and source identity *before* you start windowing. Once samples are in the ring buffer, you've lost the acquisition context unless you tagged it first.

**Live sketch (or pre-recorded demo):**

Show a replay pipeline that reads a recorded IQ file in variable-sized chunks (64, 128, 256, 512 samples) and assembles 128-sample windows. Verify that the output windows are identical regardless of chunk size. This is the M2.3 pass criterion.

### Key takeaway
Acquisition and inference are independent systems connected by a bounded queue. The harness `streaming.status` tool monitors queue depth and drops — but the student must understand *why* equivalent chunk sizes must produce equivalent windows.

---

## Part 4 — Wrap-Up and Task Assignment (5 min)

### Summary
- Pipeline correctness is not optional — it's the foundation of every result from M1 forward.
- Normalization, augmentation, and streaming each have physical contracts that the code must respect.
- The harness makes these contracts *checkable by the LLM* — but the student must *define and defend* each contract.

---

# Student Task — M2: IQ Pipeline and Streaming Harness

## Objective
Extend the M1 MCP harness with pipeline validation, augmentation, and streaming capabilities. The LLM must be able to verify data integrity, configure augmentations, and monitor a streaming pipeline through the harness.

## Deliverables

### D1 — Pipeline Validation (M2.1)
Implement harness tools that allow the LLM to:
- Validate IQ tensor layout (`N, 2, 128`), dtype, label mapping, and sample-rate assumptions.
- Run per-window joint-power normalization and verify it uses the current window only — not dataset statistics.
- Detect split leakage: given train/val/test indices, verify no overlapping windows from the same continuous segment cross splits.
- Compare baseline vs. optimized DataLoader: measure throughput (batches/s) and peak memory, with equivalent data and preprocessing semantics.

**Artifact:** Structured report (JSON) with all validation results, consumable by the LLM.

**Pass criterion:** No split leakage or label changes detected. Throughput comparison uses equivalent preprocessing. The LLM can query the report and identify any violation.

### D2 — Augmentation with Bounds (M2.2)
Implement harness tools that allow the LLM to:
- Configure training-only augmentations: phase rotation (θ range), CFO (Δf bound relative to bandwidth), additive noise (SNR delta bound).
- Verify label preservation: run augmented samples through a label-consistency check (e.g., compare model predictions before/after augmentation at high SNR).
- Verify power/noise model: report signal power and noise floor estimates before and after augmentation.

**Artifact:** Augmentation configuration (JSON) and verification report with before/after power measurements.

**Pass criterion:** Each augmentation bound is justified with a physical explanation. The student explains why each bound preserves modulation identity. The LLM can read the verification report and confirm no label corruption.

### D3 — Streaming Pipeline (M2.3)
Implement harness tools that allow the LLM to:
- Start a replay pipeline that reads a recorded IQ file in configurable chunk sizes and assembles 128-sample windows with configurable hop.
- Monitor queue depth, drop count, and filter state in real time.
- Run a replay comparison: process the same file with chunk sizes 64, 128, 256, 512 and verify output windows are identical.
- Record session metadata (sample rate, center frequency, source identity) before windowing begins.

**Artifact:** Ring-buffer implementation, queue/drop logs, and replay comparison report showing window equivalence across chunk sizes.

**Pass criterion:** Equivalent replay streams produce equivalent windows despite chunk boundaries. No accidental duplication. Discontinuities reset filter state explicitly. The LLM can query streaming status and replay comparison results through the harness.

## Constraints
- All tools must return structured output (JSON) that the LLM can consume directly.
- Augmentation applies only to training data. Validation and test data pass through unmodified.
- The streaming pipeline must handle chunk boundaries correctly — demonstrate with at least four different chunk sizes.
- Budget: pipeline validation and augmentation verification must complete in under 60 seconds on Colab. Streaming replay comparison must complete in under 120 seconds.
