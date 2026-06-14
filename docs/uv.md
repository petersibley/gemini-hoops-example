# Python Environment Management with `uv`

Standard tool for Python dependency, environment, and version management on macOS.

## Installation

```bash
brew install uv
```

## Core Commands

### Python Versions
```bash
uv python list
```

### Running Code
```bash
# Run script in uv-managed environment
uv run script.py

# Run command in environment
uv run python -m module
```
