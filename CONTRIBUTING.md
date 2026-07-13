# Contributing

Thanks for helping improve Issue Scout.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Before opening a pull request

```bash
pytest
ruff check .
ruff format --check .
```

Please keep changes focused, include tests for behavior changes, and explain the user-facing impact in the pull request description.

