# Yojip

Join multiple audio outputs into synchronized PipeWire combined sinks ("parties").

Yojip is a lightweight command-line utility for Linux that lets you play audio through multiple output devices simultaneously using PipeWire. It automatically creates and manages combined sinks, making it easy to stream audio to speakers, headphones, Bluetooth devices, and other outputs at the same time.

## Features
- List available audio outputs
- Create synchronized combined sinks across multiple devices
- Automatically set the combined sink as the default output
- Remove combined sinks when no longer needed
- Simple CLI interface

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

## LICENSE

This project is licensed under the MIT License. See the LICENSE file for details.
