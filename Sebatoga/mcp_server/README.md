# M1 configurable CNN MCP server

This package provides a reusable training core and an MCP stdio server. It
loads SigMF `ci8_le` captures, creates deterministic `(N, 2, L)` `float32`
windows, and trains a bounded configurable CNN in a background thread.

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

Reports preserve capture provenance and label construction (`fm=1` from
captures and seeded synthetic Gaussian noise=`0`), plus train, validation, and
test metrics. A missing NumPy, PyTorch, or MCP dependency is reported directly
by the relevant operation.
