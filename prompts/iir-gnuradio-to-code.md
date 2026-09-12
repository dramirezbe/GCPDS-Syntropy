# Prompt: GNU Radio → Code (IIR Filter)

## Context

Topic: IIR filter applied to IQ dummy signal
Goal: Create a GNU Radio flowgraph that implements an IIR filter on IQ data

## Prompt

```
Create a Python script that uses GNU Radio to implement an IIR low-pass filter on a synthetic IQ signal.

Requirements:
1. Generate a synthetic IQ signal as a GNU Radio complex vector source
2. Apply a recursive IIR filter (single_pole_iir_filter or fft_filter)
3. Output the filtered signal
4. Include a simple test that verifies the filter works

The script should:
- Use gnuradio blocks: vector_source_c, single_pole_iir_filter_ff, vector_sink_c
- Be runnable with: python3 script.py
- Print signal statistics before and after filtering
- Verify that the output shape matches the input shape

Example structure:

#!/usr/bin/env python3
import numpy as np
from gnuradio import gr
from gnuradio import blocks

class IIRFilterFlowgraph(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        # Generate synthetic IQ data
        N, L = 5, 1000
        SEED = 42
        rng = np.random.default_rng(SEED)
        I = rng.standard_normal((N, L)).astype(np.float32)
        Q = rng.standard_normal((N, L)).astype(np.float32)
        iq_signal = I + 1j * Q

        # Flatten for GNU Radio
        iq_flat = iq_signal.flatten().tolist()

        # Create flowgraph
        self.source = blocks.vector_source_c(iq_flat)
        self.iir = blocks.single_pole_iir_filter_ff(0.1, 1)
        self.sink = blocks.vector_sink_c()

        # Connect
        self.connect(self.source, self.iir, self.sink)

if __name__ == '__main__':
    fg = IIRFilterFlowgraph()
    fg.run()
    output = np.array(fg.sink.data())
    print(f'Input shape: {fg.source.length()}')
    print(f'Output shape: {len(output)}')
```

Adapt this example to work with your specific IIR filter requirements.
```

## Expected Output

1. Python script using GNU Radio blocks
2. Synthetic IQ signal generation
3. IIR filter application
4. Output verification
