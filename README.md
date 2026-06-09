# Yojip

Join multiple audio outputs into synchronized PipeWire combined sinks ("parties").

## Usage

```text
yojip outputs              List available audio outputs
yojip party create NAME    Create a combined sink
yojip party add NAME OUT   Add output to a party
yojip party remove NAME OUT
yojip party list
yojip party destroy NAME
```

## Installation

```bash
pip install yojip
```

Requires PipeWire (typically pre-installed on modern Linux audio systems).
