# Yojip

Speaker-syncing tool using PipeWire combined sinks ("parties").

## Project structure

```
yojip/              # Python package (PEP 621 layout)
├── __init__.py     # __version__
├── __main__.py     # argparse CLI + PipeWire subprocess calls
├── AGENTS.md
├── pyproject.toml  # setuptools build config
├── README.md
├── LICENSE
└── .gitignore
```

## CLI

Entry point: `yojip` (registered in `pyproject.toml`), also `python -m yojip`.
Uses `argparse`. No external Python dependencies.

Commands:
- `yojip outputs` — list audio sinks by parsing `pw-dump` JSON
- `yojip party create/add/remove/list/destroy` — manage combined sinks

## PipeWire integration

All interaction via `subprocess` calls to PipeWire CLI tools:
- `pw-dump` — enumerate objects (sinks, nodes)
- `pw-cli` — create/destroy/adapter nodes (combined sinks, loopbacks)

## Development

```bash
python -m build                  # build sdist + wheel
python -m twine upload dist/*    # publish to PyPI
```

Run locally: `python -m yojip outputs`

Repository: https://github.com/Shanwis/Yojip
License: MIT

## Notes

- No external Python dependencies (stdlib only).
- PipeWire system tools must be installed.
- Python 3.10+.
- Party = combined sink (multiple audio outputs in sync).
