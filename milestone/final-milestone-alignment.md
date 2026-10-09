# Final Milestone Alignment — Harness as AI Middleware

> **Harness definition**: middleware that sits between the human operator, the computational tools (training, inference, acquisition), and an LLM — enabling the LLM to drive, monitor, and reason about the tools while the human retains strategic control.
>
> Implementation vehicles: MCP servers, Claude Code skills, agent toolkits, or any protocol that exposes structured tool interfaces to an LLM.

---

## Pre-M0 — Python/NumPy through IQ (W1)

### Goal
Close the programming gap using familiar signals.

### Pre-M0.1
Functions, indexing, slicing, broadcasting, dtypes, file loading, plotting and joint IQ power. Defer custom classes until needed.

**Artifact.** Notebook loading IQ, plotting time traces and constellations, computing power and documenting dimensions; one-paragraph capstone description.

**Pass criterion.** Students independently explain array axes and correct an injected axis swap. Power agrees with a direct complex-magnitude calculation.

### M0.1
Validate the Colab environment with a short computation; check Pi connectivity and acquire a short IQ recording. Log hardware and versions.

**Artifact.** Environment report and readable capture with acquisition metadata.

**Pass criterion.** The computation produces finite outputs and the recording is readable. A GPU check is not a guarantee of future Colab availability.

### M0.2
Train a small IQ-feature MLP using tensor operations, autograd and explicit SGD updates. Inspect gradient shapes and perform finite differences.

**Artifact.** Training loop, chain-rule explanation and one manual parameter count.

**Pass criterion.** Loss decreases; selected gradients match finite differences within declared tolerances; parameter shapes and count are correct.

### M0.3
Reproduce the toy model using a minimal nn.Module and optimizer. Introduce only the class syntax needed for this model.

**Pass criterion.** Identical weights and batches produce matching forward outputs and one controlled SGD update.

### LLM harness context
**First harness seed (optional at this stage).** An MCP tool or skill can expose environment validation (GPU check, determinism probe, version audit) so the LLM can verify the setup and diagnose failures. The student must understand what each check means — the harness reports, the student interprets.

| Tool | Purpose |
|------|---------|
| `environment.validate` | Run determinism probe, GPU benchmark, version lock — return structured report |
| `environment.diagnose` | Given a failing check, suggest root cause |

---

## M1 — Training and Baselines (W3–W4; export W6)

### Goal
Create one observable experiment path.

### M1.1 (W3)
A minimal harness reads one configuration, logs training and validation metrics, and saves epoch-boundary checkpoints. A supplied compact CNN separates training-loop learning from architecture design.

**Artifact.** Configuration, learning curves, checkpoint and short recovery test.

**Pass criterion.** Resume restores model, optimizer, completed epoch and random state. Validation uses evaluation mode without parameter updates. Arbitrary mid-batch interruption equivalence is not required.

### M1.2 (W3/W4)
Overfit one batch, then change one factor at a time: learning rate, regularization or training SNR distribution. Keep evaluation fixed.

**Artifact.** Sanity-check result and a bounded ablation table with runtime.

**Pass criterion.** Single-batch classification succeeds with low loss and finite gradients; interpretations distinguish SNR-stratified evaluation from changing the training distribution. Failed experiments receive a controlled diagnosis.

### M1.3 (W4)
Train a two-channel RadioML Conv1D baseline and compare against a DSP-feature classifier using identical splits. Predeclare architecture, metric, budget and validation target. Choose capstone classes and live labels.

**Artifact.** Class map, split indices, tensor/parameter summary, per-SNR metrics, confusion matrices and a capstone input/label contract.

**Pass criterion.** Run stays within budget and is compared fairly with the baseline. Do not require arbitrary universal accuracy across low-SNR examples. Test data remain locked until final selection.

### M1.4 (W6)
Export the baseline in evaluation mode to ONNX and run fixed recorded examples on both the training host and Pi CPU.

**Pass criterion.** Logits match within declared absolute/relative tolerances, the Pi client needs no training-model definition, and batch-one latency is measured.

### LLM harness context
**This is the milestone where the harness becomes the central artifact.** The MCP server (or equivalent) wraps the training loop so the LLM can configure, launch, monitor, and analyze experiments. Every pass criterion above still requires the student to produce and understand the scientific result.

| Tool | M1 sub | Purpose |
|------|--------|---------|
| `training.configure` | M1.1 | Accept architecture and hyperparameter config (JSON); validate against budget constraints (250K params, 7200s, batch 256, 20 epochs) |
| `training.run` | M1.1 | Start a training run; save epoch-boundary checkpoints with model, optimizer, epoch, and RNG state |
| `training.status` | M1.1 | Return current epoch, train/val loss, accuracy, elapsed time, system metrics |
| `training.stop` | M1.1 | Early stopping or manual halt |
| `training.resume` | M1.1 | Restore from checkpoint — must restore model, optimizer, completed epoch, and random state |
| `training.overfit_check` | M1.2 | Run single-batch overfit sanity check; report loss and gradient finiteness |
| `training.ablation` | M1.2 | Run one-factor-at-a-time ablation with fixed evaluation; return comparative table with runtime |
| `training.report` | M1.1–M1.3 | Generate structured report: learning curves, per-SNR metrics, confusion matrices, parameter summary, budget usage |
| `model.export_onnx` | M1.4 | Export in eval mode to ONNX; run parity check against training host |
| `model.verify_parity` | M1.4 | Compare logits on fixed recorded examples between training host and Pi CPU; report tolerances |

---

## M2 — IQ Pipelines and Streaming (W5/W7)

### Goal
Preserve data semantics offline and live.

### M2.1 (W5)
Validate IQ order, shape, labels, sample-rate assumptions and normalization. Use a map-style DataLoader for finite data. Compare a baseline and optimized loader only with equivalent data and preprocessing semantics.

**Artifact.** Pipeline checks and a small throughput/memory benchmark.

**Pass criterion.** No split leakage or label changes; measured improvement is not mandatory. Cache deterministic work, not a fixed realization of random augmentation.

**Note.** Per-window joint-power normalization uses the current window only; it does not fit dataset statistics. Preserve received power separately for signal detection. Never normalize I and Q independently without justification.

### M2.2 (W5)
Apply training-only phase rotation, bounded CFO, noise and channel impairments. Preserve modulation identity and explain each bound.

**Pass criterion.** Students verify the power/noise model and label semantics. Adding noise to already noisy IQ does not establish a new exact SNR without knowledge of the underlying signal and noise powers.

### M2.3 (W7)
Connect continuous acquisition or replay to stateful channel selection, filtering/resampling, window assembly and a bounded queue. Record session metadata before windowing; retain filter state across chunks.

**Artifact.** Chunk-safe pipeline, ring-buffer implementation, queue/drop logs and replay comparisons using different chunk sizes.

**Pass criterion.** Equivalent replay streams produce equivalent windows despite chunk boundaries. No accidental duplication occurs; discontinuities reset state explicitly. Acquisition and inference run independently. Deliberate inference subsampling is distinguished from lost acquisition samples.

**Note.** An IterableDataset is optional for actual streams, not required for finite RadioML arrays. Training prefetch and receiver buffering solve different problems and have different correctness criteria.

### LLM harness context
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

## M3 — RF Representations (W8; optional extension W9)

### Goal
Compare representations within deployment limits.

### M3.1
Refine the compact real two-channel Conv1D baseline with small kernels and global pooling. Explain receptive field and parameter cost.

### M3.2
Compare with a small Conv2D on two-sided complex-STFT log power. Fix FFT length, window, hop, centering, scaling and frequency ordering.

**Artifact.** Matched-data comparison of per-SNR metrics, parameters, training time, preprocessing cost and Pi inference time.

**Pass criterion.** Use identical source examples/splits and declared budgets. Discuss discarded phase information; a spectrogram need not outperform IQ. Do not concatenate unrelated benchmark windows into fictitious continuous signals.

### M3.3 (Optional)
Implement tied real convolutions representing complex multiplication. Compare with unconstrained real two-channel convolution.

**Pass criterion.** Verify shapes and gradients, explain weight coupling, and check export support. This extension cannot displace required capture evaluation.

### LLM harness context
The harness enables fair comparison experiments. The LLM uses the same training tools to run matched experiments on different representations.

| Tool | Purpose |
|------|---------|
| `representation.configure` | Switch between IQ Conv1D and STFT Conv2D with matched data/splits |
| `representation.compare` | Generate matched comparison: per-SNR metrics, parameters, training time, preprocessing cost, Pi inference time |
| `stft.configure` | Set FFT length, window, hop, centering, scaling, frequency ordering |

---

## M4 — Capture-Domain Evaluation (W9)

### Goal
Measure and address synthetic-to-real mismatch.

### M4.1
Evaluate candidate models on independently labeled captures. Keep source/session groups separate; inspect gain, bandwidth, sample-rate, frequency-offset and channel differences. Do not infer ground truth from model output.

**Artifact.** Synthetic-versus-capture validation report and documented acquisition conditions.

### M4.2
Perform limited adaptation on training captures, using validation captures for selection. Add no-signal handling and a validation-tuned rejection rule.

**Pass criterion.** Report held-out session results at final evaluation; report rejection coverage, false rejections and false acceptance on selected unfamiliar signals. Low confidence is a heuristic, not proof of general open-set detection.

### LLM harness context
The harness exposes capture metadata and domain-shift diagnostics so the LLM can reason about mismatch causes and suggest adaptation strategies.

| Tool | Purpose |
|------|---------|
| `capture.evaluate` | Run model on labeled captures; report per-session/source metrics with acquisition conditions |
| `capture.compare_domains` | Synthetic vs. capture validation report |
| `rejection.configure` | Set confidence threshold for no-signal/rejection rule |
| `rejection.evaluate` | Report rejection coverage, false rejections, false acceptance on unfamiliar signals |

---

## M5 — Diagnostics and Profiling (W10/W11)

### Goal
Diagnose before optimizing.

### M5.1 (W10)
Diagnose injected RF failures: SNR leakage, swapped IQ, clipping, inconsistent scaling, invalid power normalization or gradient failures. Naive subtraction across the phase wrap boundary is a useful defect; wrapped phase itself is not automatically wrong.

**Artifact.** Symptom, hypothesis, isolating experiment, correction and post-fix result.

**Pass criterion.** Evidence identifies the cause rather than merely correlating a histogram with it. Select the deployment candidate using validation metrics and Pi resource measurements, not the locked test.

### M5.2 (W11)
Profile training input wait, computation and memory; separately profile receiver DSP, queuing and inference. Test mixed precision only if justified by a measured T4 bottleneck.

**Artifact.** Stage timings and optional FP32/mixed-precision comparison with accuracy.

**Pass criterion.** Include warm-up and appropriate GPU synchronization. Explain neutral or negative optimization results. GPU utilization alone does not establish whether a workload is compute- or memory-bound.

### LLM harness context
**High-value harness milestone.** The LLM becomes a diagnostic partner — the harness feeds it symptoms (gradient stats, timing breakdowns, resource usage), and the LLM helps hypothesize causes. The student must design the isolating experiment.

| Tool | Purpose |
|------|---------|
| `diagnostics.inject_fault` | Inject known RF failures (SNR leakage, swapped IQ, clipping, etc.) for diagnosis drill |
| `diagnostics.gradient_health` | Report gradient norms, NaN/Inf counts, per-layer statistics |
| `profiling.training` | Stage timings: input wait, computation, memory; GPU synchronization included |
| `profiling.receiver` | Stage timings: DSP, queuing, inference separately |
| `profiling.mixed_precision` | Optional FP32 vs. mixed-precision comparison with accuracy delta |

---

## M6 — Pi Deployment and Integration (W6–W13)

### Goal
Deliver a bounded, observable receiver.

### M6.1 (W6/W7/W12)
Use the early exported baseline and replay client to integrate live pyrtlsdr acquisition, stateful DSP and ONNX Runtime CPU. By W12 produce classes, confidence/rejection and timestamps continuously.

**Artifact.** Model, preprocessing/class contract, runnable receiver and logs.

**Pass criterion.** A ten-minute sustained test has bounded memory and backlog. Record actual acquisition rate, processed rate, decision cadence, drops and coverage. The GUI is outside the critical path and receives decimated display data.

### M6.2 (Optional W11)
Compare supported INT8 inference against the working FP32 model on the actual Pi. Use representative training data for calibration; evaluate per-class/per-SNR accuracy and latency.

**Pass criterion.** Record model size, end-to-end timing and accuracy changes. Neither quantization speedup nor FP16 CPU benefit is presumed. ONNX-to-TFLite and Edge TPU are separate optional branches with additional compatibility and hardware requirements, not the core pipeline.

### M6.3 (W12)
Complete integration, including exception handling, input validation, queue limits and a documented restart procedure.

**Pass criterion.** Replay and live processing share the same input contract. Disconnections and missing samples produce explicit status rather than stale predictions.

### M6.4 (W13)
Measure robustness and end-to-end p50/p95/p99 latency, including acquisition/window accumulation, DSP, queueing and inference. Record timestamp definitions, sample count, RAM and thermal/throttling conditions.

**Pass criterion.** For processed sample rate f_s and hop H, compare service capacity against f_s/H windows/s. Declare any intentional coverage reduction. Use repeatable in-band impairment tests; distinguish receiver overload from in-band interference. Commercial Wi-Fi/LTE is not an assumed compatible test source.

### LLM harness context
The harness bridges Colab training and Pi deployment. The LLM can monitor the live receiver through the same tool interface used during training, enabling end-to-end reasoning about the system.

| Tool | Purpose |
|------|---------|
| `receiver.deploy` | Push ONNX model + preprocessing contract to Pi |
| `receiver.status` | Acquisition rate, processed rate, decision cadence, drops, coverage, memory, thermal |
| `receiver.classify` | Run inference on a window; return class, confidence, timestamp |
| `receiver.sustained_test` | Run 10-minute bounded test; report backlog, memory trend, coverage |
| `receiver.latency_profile` | End-to-end p50/p95/p99 including acquisition, DSP, queueing, inference |

---

## M7 — Progressive Capstone (W1–W14)

### Goal
Defend a reproducible live modulation classifier.

### M7.1
W1: introduce objective; W4: freeze classes and label protocol; W6: Pi replay; W12: integrated live receiver; W13: correct using development data, freeze model and run locked evaluation; W14: demonstrate and defend.

**Artifact.** Repository with README, environment/run records, data provenance and splits, training code/checkpoint, ONNX model, receiver, replay sample, metrics and a concise engineering report. Avoid duplicating artifacts already produced.

**Evaluation criteria.** Assess independent labels and split integrity; model-versus-baseline results; per-class/per-SNR performance where SNR is known; capture-domain gaps; rejection behavior; export parity; throughput, latency and coverage; failure analysis; and reproduction from the submitted instructions. Do not invent exact SNR labels for uncalibrated live captures.

**Pass criterion.** The frozen system classifies the declared live signal set and reproduces a fixed replay evaluation. Students explain representation, parameter cost, training budget and deployment choices. Report limitations honestly; the final week is an assessment of an already integrated system.

### LLM harness context
The harness is part of the defense. The student demonstrates the complete LLM-assisted cycle: configure → train → diagnose → deploy → monitor → report. The LLM can reproduce any experiment through the harness, but the student defends every decision. The functional MCP server (or equivalent) demonstrating the complete AI-assisted workflow is an additional deliverable alongside the original capstone artifacts.

---

## Cross-Cutting Harness Requirements

### Determinism
Every harness-initiated run must enforce the three-step deterministic checklist: environment variables before CUDA init, frozen splits and seeded DataLoader, and short verification run reproducibility.

### Budget enforcement
The harness must validate and enforce: 7200s cumulative training on one T4, 250K parameters, batch size 256, 20 epochs. Log actual hardware and elapsed time.

### IQ convention
All data flowing through the harness uses `X.shape == (N, 2, 128)`. Per-window joint-power normalization only. Never normalize I and Q independently.

### Structured reports
Every harness operation produces LLM-consumable output (JSON or structured Markdown) so the LLM can reason about results, compare experiments, and suggest next steps without the student manually formatting data.

### Separation of concerns
The harness enables the LLM to *operate* the tools. The student must *understand* every result and *defend* every decision. The harness is infrastructure; the science is the student's responsibility.
