# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PEP 723 Loader is a CLI wrapper that auto-installs inline script dependencies before executing linters/tools. It parses PEP 723 metadata blocks from Python scripts and uses `uv` to install dependencies, enabling tools like mypy, ruff, or basedpyright to lint scripts with inline dependencies without manual environment setup.

## Commands

```bash
# Run tests with coverage
uv run pytest

# Run single test file
uv run pytest packages/pep723_loader/tests/unit/test_cli.py

# Run single test
uv run pytest packages/pep723_loader/tests/unit/test_cli.py::TestFixtureFiles::test_with_deps_uv_shebang

# Linting and formatting
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run mypy packages/
uv run basedpyright packages/

# Run pre-commit hooks
uv run pre-commit run --all-files

# Build package
uv build
```

## Architecture

### Package Structure

```
packages/pep723_loader/
├── cli.py           # Typer CLI entry point, wraps commands with dependency installation
├── pep723_checker.py # Core logic: discovers .py files, extracts PEP 723 deps via `uv export --script`
├── dependencies.py   # Reserved for future dependency management
└── tests/
    ├── unit/         # Unit tests with pytest-mock
    └── e2e/          # End-to-end CLI tests
```

### Key Flow

1. CLI receives command + arguments (e.g., `pep723-loader mypy --strict script.py`)
2. `Pep723Checker` extracts Python file paths from arguments
3. For each file, runs `uv export --script` to get PEP 723 requirements
4. Aggregates requirements and pipes to `uv pip install -r -`
5. Executes the wrapped command with original arguments
6. Propagates the command's exit code

### PEP 723 Inline Metadata Format

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///
```

### Pre-commit Integration

The tool integrates with pre-commit via local hooks in `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: mypy
      entry: uv run --with pep723-loader pep723-loader mypy
      language: system
      types: [python]
```

## Code Conventions

- Python 3.10+ with full type hints
- Google-style docstrings (enforced by ruff)
- Tests follow AAA pattern with pytest-mock
- Line length: 120 characters
- Ruff for linting/formatting, mypy + basedpyright for type checking
