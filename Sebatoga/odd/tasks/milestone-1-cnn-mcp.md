# Milestone 1 — Configurable CNN MCP training

## Objective

Deliver a standalone MCP server that lets an LLM configure, train, monitor,
stop, and inspect reports for a CNN over the external IQ capture database.

## Product decision

Use binary FM-signal detection (`fm` versus reproducible synthetic `noise`).
The supplied SigMF captures are unlabeled 98 MHz FM recordings, so pretending
they contain modulation classes would produce invalid supervision. The server
must keep the external dataset path configurable and must record this label
construction and provenance in every report.

## Authorized scope

- Work only on branch `feature/Sebatoga`, based on `develop`.
- Never commit or copy the external database into the repository.
- Use the database at `/home/sebato/Escritorio/clase_0310/DataBase-IQ-FM-88MHz-108MHz`
  as the default documented input, while allowing another path through config.
- Push only `feature/Sebatoga` to the GitHub remote after local verification.
- Do not modify `main` or `develop`.

## Tasks

- [x] M1-01: Implement SigMF loading, deterministic windowing, normalization,
  synthetic negative generation, and capture-aware dataset metadata.
- [x] M1-02: Implement configurable CNN construction and background training
  service with progress, cancellation, system metrics, checkpoints, and JSON
  reports.
- [x] M1-03: Expose configuration, training, monitoring, cancellation, system
  metrics, and report retrieval through an MCP stdio server.
- [x] M1-04: Add focused tests and usage documentation, then validate with a
  dependency-aware smoke test and repository post-task gate.

## Acceptance criteria

- An MCP client can configure architecture and hyperparameters, start one run,
  query live status/system metrics, stop it, and retrieve a structured report.
- Reports identify dataset path, capture IDs, label strategy, configuration,
  epoch history, final metrics, timing, device, and stop/failure reason.
- Architecture input is validated against the course limits (maximum 250,000
  parameters, batch size 256, and 20 epochs by default).
- Training work never blocks MCP request handling and stop requests are
  observed between batches/epochs.
- Tests cover configuration validation, SigMF decoding/window shape, model
  construction, cancellation, and report serialization.

## Checks

- Focused Python test command from `Sebatoga/`: `python3 -m pytest -q`
- MCP harness scenario: start the stdio server and exercise the exposed tools;
  record `N/A` only if the MCP dependency is unavailable in the environment.
- Post-task environment check from `AGENTS.md`.

## Route and progress

- M1-01 route: delegated direct writer (implementation spans multiple files).
- M1-02 route: delegated direct writer (implementation spans multiple files).
- M1-03 route: delegated direct writer (implementation spans multiple files).
- M1-04 route: delegated direct writer with focused verification.
- Work-unit commit evidence will be recorded after each completed task.

## Verification evidence

- From `Sebatoga/`, `python3 -m compileall -q mcp_server tests`: passed.
- From `Sebatoga/`, `python3 -m pytest -q`: unavailable because `pytest` is
  not installed.
- Fallback `python3 -m unittest discover -v`: passed, 7 tests with 4
  dependency-aware skips because NumPy and PyTorch are not installed.
- From `Sebatoga/`, `python3 -m mcp_server.server`: returned the documented exit code 2 and
  actionable MCP installation message because the MCP SDK is not installed.
- The real SigMF metadata correction is now covered by a focused fixture using
  `global.core:datatype`, `captures[].core:sample_start`, and
  `captures[].core:frequency`; the external database was not copied into the
  repository.
- Runtime dependencies were installed in the ignored `Sebatoga/.venv/` using
  CPU-only PyTorch. The external database remained outside the repository.

## Current verification evidence

- `python3 -c "import numpy, matplotlib, scipy; print('Core packages OK')"`:
  unavailable because NumPy is not installed.
- The focused fixture covers the real SigMF keys and asserts the model input
  shape `(N, 2, L)`; the external database was not copied into the repository.
- For the real-data smoke test, set `SYNTROPY_DATASET_PATH` to the external
  database, configure a bounded `max_windows`, and exercise the MCP workflow;
  record the command output and final report only after that execution.
- From `Sebatoga/`, `.venv/bin/python -m pytest -q`: passed, 7 tests.
- From `Sebatoga/`, `.venv/bin/python -m compileall -q mcp_server tests`: passed.
- From `Sebatoga/`, `.venv/bin/python -c "import numpy, matplotlib, scipy; print('Core packages OK')"`:
  passed.
- Direct real-data training completed on CPU with `max_windows=512`, 3 epochs,
  batch size 64, and 778 model parameters. The report was saved to
  `/tmp/syntropy-training-report.json` with `stop_reason: completed`; train
  accuracy was `0.990228`, validation accuracy `1.0`, and test accuracy `1.0`.
- Live MCP stdio harness completed with 10 tools discovered, configured the
  external dataset, trained one epoch with 64 windows, retrieved the final
  report, and saved it to `/tmp/syntropy-mcp-training-report.json`.
- The MCP harness report recorded `stop_reason: completed`, CPU execution,
  778 parameters, and capture provenance including 98 MHz frequency.

## Current next step

The SigMF key-format blocker is resolved locally on `feature/Sebatoga`, and
bounded real-data training plus the live MCP harness have completed. The
changes and evidence still need a work-unit commit and remote publication.
