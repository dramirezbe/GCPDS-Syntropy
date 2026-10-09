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

- Focused Python test command: `python3 -m pytest -q`
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

- `python3 -m compileall -q mcp_server tests`: passed.
- `python3 -m unittest discover -v`: passed with 3 dependency-aware skips
  because NumPy and PyTorch are not installed in the current environment.
- `python3 -m mcp_server.server`: returned the documented exit code 2 and
  actionable MCP installation message because the MCP SDK is not installed.
- Full training and live MCP client harness remain pending until optional
  dependencies are available.

## Final verification evidence

- Work-unit commit: `b0ba2d7` (`feat(m1): expose configurable CNN training over MCP`).
- `python3 -m unittest discover -v`: passed, 6 tests with 3 expected skips.
- `python3 -m compileall -q mcp_server tests`: passed.
- `python3 -m mcp_server.server`: correctly returned exit code 2 with an
  actionable MCP installation message.
- `python3 -c "import numpy, matplotlib, scipy; print('Core packages OK')"`:
  unavailable because the environment lacks NumPy.
- Live training and a real MCP client harness are pending dependency setup;
  they were not represented as passing checks.

## Current next step

Feature implementation is complete for this branch. `feature/Sebatoga` is
published on `origin`; merge/PR approval remains with the user.
