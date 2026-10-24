# Realtime DSP-to-CNN pipeline

## Objective

Add a complete bounded realtime pipeline to the CNN MCP server:

```text
IQ source -> DSP -> ring buffer -> windowing -> CNN inference -> predictions
```

The classifier operates on raw/baseband IQ using the existing binary `fm=1`
and synthetic `noise=0` model contract.

## Authorized scope

- Work only on branch `feature/Sebatoga` and under `Sebatoga/`.
- Reuse the existing `(N, 2, L)` `float32` CNN input contract.
- Keep the external SigMF database outside the repository.
- Do not modify `main` or `develop`.

## Tasks

- [x] RCP-01: Implement DSP processing, bounded thread-safe ring buffers, and
  SigMF replay/injection sources.
- [x] RCP-02: Implement CNN checkpoint loading, realtime windowing, inference,
  prediction history, cancellation, and pipeline metrics.
- [x] RCP-03: Expose pipeline configuration, start/stop, injection, status,
  metrics, and prediction retrieval through MCP.
- [x] RCP-04: Add focused tests, end-to-end injection verification, update
  documentation, and publish a work-unit commit.
- [x] RCP-05: Add a dependency-free terminal dashboard for live pipeline
  status, metrics, buffers, and predictions with clean shutdown.
- [x] RCP-06: Provide safe initial parameters and a one-line dashboard startup
  path, including an explicit checkpoint fallback when none is supplied.

## Decisions

- DSP input remains raw/baseband complex IQ; no FM demodulation is added.
- The first source modes are deterministic SigMF replay and MCP IQ injection.
- Buffers are bounded and instrumented; `block` is the safe default policy and
  `drop_oldest` is available for realtime operation.
- The existing binary CNN is reused; no future modulation classes are added.
- Pipeline execution is one singleton service, consistent with the current MCP
  server architecture.
- The visualization is a local terminal dashboard using the Python standard
  library; it does not introduce a web UI or mandatory runtime dependency.
- The zero-argument CLI uses injection mode, a bounded fixture, and documented
  defaults; a trained checkpoint is preferred and a temporary bootstrap model
  is used only when no checkpoint is supplied or found.

## Checks

- Focused tests: `.venv/bin/python -m pytest -q` from `Sebatoga/`.
- Compile check: `.venv/bin/python -m compileall -q mcp_server tests`.
- End-to-end harness: configure a checkpoint, inject deterministic IQ, start
  the pipeline, retrieve predictions and metrics, then stop it.
- Post-task environment check from `AGENTS.md`.

## Route and progress

- RCP-01 route: delegated direct writer; implementation spans multiple files.
- RCP-02 route: delegated direct writer; inference and orchestration are
  coupled across multiple files.
- RCP-03 route: delegated direct writer; MCP surface and tests change together.
- RCP-04 route: delegated direct writer with focused verification.
- Delivery strategy: `ask-on-risk`; current work is expected to remain under
  the advisory 400-authored-line work-unit heuristic.

## Acceptance criteria

- A bounded IQ stream can flow through DSP, buffering, windowing, and CNN
  inference without blocking MCP request handling.
- Cancellation wakes blocked stages and produces a terminal pipeline status.
- Status and metrics expose throughput, latency, buffer depth, drops, and the
  latest prediction timestamp.
- Predictions include class, confidence, probabilities, and sample position.
- Replay and injection paths are deterministic and covered by tests.
- The dashboard can monitor injection or SigMF replay and always restores the
  terminal after stop, quit, or keyboard interruption.

## Verification evidence

- `.venv/bin/python -m pytest -q`: passed (11 tests).
- `.venv/bin/python -m compileall -q mcp_server tests`: passed.
- End-to-end injection harness: passed with a temporary `build_cnn` checkpoint;
  predictions, terminal status, metrics, and cancellation were observed.
- ANSI fallback harness: passed with a temporary compatible checkpoint and the
  deterministic injection fixture; one window was inferred and cleanup ended
  the pipeline in `cancelled` status.
- `.venv/bin/python -c "import numpy, matplotlib, scipy; print('Core packages OK')"`:
  passed.
- Local work-unit commit: `57d5b93` (`feat(m1): add realtime IQ CNN pipeline`).
- RCP-06 tests and checks: `.venv/bin/python -m pytest -q` passed (21 tests),
  and `.venv/bin/python -m compileall -q mcp_server tests` passed.
- Zero-argument harness: `.venv/bin/python -m mcp_server.tui` ran from
  `Sebatoga/`, rendered one injected 1024-sample window using a temporary
  `bootstrap (random, untrained)` checkpoint, exited with code 0, and left no
  dashboard process running.
