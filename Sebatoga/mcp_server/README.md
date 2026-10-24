# M1 configurable CNN MCP server

This package provides a reusable training core and an MCP stdio server. It
loads SigMF `ci8_le` captures, creates deterministic `(N, 2, L)` `float32`
windows, and trains a bounded configurable CNN in a background thread.

It also exposes a bounded raw-IQ realtime path. `configure_pipeline` selects a
checkpoint and either MCP injection or chunked SigMF replay; the workers then
run DSP, windowing, and CNN inference without FM demodulation. The realtime
tools are `start_realtime_pipeline`, `inject_iq`, `get_pipeline_status`,
`get_pipeline_metrics`, `get_predictions`, and `stop_realtime_pipeline`.
Injection uses JSON-friendly `[[i, q], ...]` pairs. Predictions retain UTC
timestamp, sample position, window length, binary label (`noise=0`, `fm=1`),
confidence, and both class probabilities. Buffers are bounded; `block` is the
default overflow policy and `drop_oldest` is available for live operation.

The loader reads the standard SigMF names `global.core:datatype`,
`captures[].core:sample_start`, and `captures[].core:frequency`. The older
unqualified spellings remain accepted for compatibility with existing local
fixtures.

The intended external input is:
`/home/sebato/Escritorio/clase_0310/DataBase-IQ-FM-88MHz-108MHz`.
The external database is intentionally not part of this repository. Set
`SYNTROPY_DATASET_PATH` or configure another path through the MCP tool.

## Installation

Install the optional runtime dependencies in the environment that launches the
server:

```bash
python3 -m pip install numpy torch mcp psutil
```

## Launch over stdio

From the repository root, enter the dedicated workspace first:

```bash
cd Sebatoga
python3 -m mcp_server.server
```

If the MCP SDK is unavailable, the module remains importable and the launch
command prints an actionable installation message instead of failing during
import.

## One-line realtime dashboard

From `Sebatoga/`, start the safe injection dashboard with:

```bash
python -m mcp_server.tui
```

The command uses injection, a deterministic fixture, a 1024-sample
window/stride/chunk, buffer capacity 8, blocking overflow, and a one-second
refresh. `--no-inject-fixture` disables the initial sample. Checkpoints are
resolved from `SYNTROPY_CHECKPOINT`, then `checkpoints/epoch-001.pt`; when
neither exists, the dashboard creates a temporary random, untrained bootstrap
checkpoint and removes it on exit. The bootstrap is only for exercising the
dashboard. Use `--checkpoint path/to/trained.pt` for useful inference; an
explicit missing path fails clearly.

## Browser dashboard

Start the local web dashboard from `Sebatoga/`:

```bash
.venv/bin/python -m mcp_server.web_server
```

Then open <http://127.0.0.1:8765/>. It uses the same realtime pipeline as the
MCP and terminal dashboards, polls status and metrics every second, and offers
buttons to configure, start, stop, and inject a deterministic IQ fixture. Use
`--checkpoint checkpoints/epoch-003.pt` for a trained model, or let the server
create a temporary bootstrap model for a pipeline demonstration. Stop the
server with `Ctrl-C`.

## MCP workflow

1. Call `get_current_configuration`.
2. Call `configure_dataset` with the external path, window settings, and the
   bounded `max_windows`/`max_captures` limits. The safe default is 2,048
   windows; pass `full_data=true` only when intentionally processing all data.
3. Call `configure_cnn` for channels, kernel size, activation (`relu`, `gelu`,
   `sigmoid`, or `tanh`), and dropout.
4. Call `configure_training` for learning rate, batch size, epochs, optimizer
   (`adam`, `sgd`, or `rmsprop`), checkpoint directory, and device.
5. Call `start_training`. Dataset loading and training run in the background.
6. Poll `get_live_status` and `get_system_metrics`; call `stop_training` when
   cancellation is needed.
7. Call `get_final_report`, then `save_final_report` with a local JSON path.

### Realtime workflow

1. Build or select a checkpoint compatible with the existing `build_cnn` CNN.
2. Call `configure_pipeline` with `checkpoint_path`, `window_length`, and
   either `source="injection"` or `source="sigmf"` plus `sigmf_meta_path`.
3. Start the pipeline, inject I/Q pairs when using injection, and poll status,
   metrics, and predictions.
4. Call `stop_realtime_pipeline`; cancellation wakes blocked bounded buffers.

Reports preserve capture provenance and label construction (`fm=1` from
captures and seeded synthetic Gaussian noise=`0`), plus train, validation, and
test metrics. A missing NumPy, PyTorch, or MCP dependency is reported directly
by the relevant operation.
