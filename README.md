# Yojip

Join multiple audio outputs into synchronized PipeWire combined sinks ("parties").

## Commands

```
yojip outputs              List available audio outputs
yojip party                Create a combined sink with all outputs (and set it as default)
yojip party create         Same as above
yojip party delete         Destroy the combined sink
```

## Requirements

- PipeWire (with `pipewire-pulse` for `pactl`)
- Python 3.10+

## Installation

```bash
pip install yojip
```

Or run from source:

```bash
python -m yojip outputs
```
