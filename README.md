# pep723-loader

A CLI wrapper that auto-installs [PEP 723](https://peps.python.org/pep-0723/) inline script dependencies before executing linters and other tools.

## The Problem

Python scripts with PEP 723 inline metadata declare their dependencies directly in the file:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31.0",
#   "rich>=13.0.0",
# ]
# ///

import requests
from rich import print
# ...
```

But when you run type checkers or linters on these scripts, they fail because the dependencies aren't installed:

```bash
$ mypy script.py
script.py:8: error: Cannot find implementation or library stub for module named "requests"
script.py:9: error: Cannot find implementation or library stub for module named "rich"
```

## The Solution

`pep723-loader` wraps your linter and automatically installs the inline dependencies first:

```bash
$ pep723-loader mypy script.py
# Dependencies installed, then mypy runs successfully
```

## Installation

```bash
pip install pep723-loader
```

Or with uv:

```bash
uv tool install pep723-loader
```

## Usage

### Command Line

```bash
# Wrap any linter or tool
pep723-loader mypy script.py
pep723-loader basedpyright script.py
pep723-loader ruff check script.py
pep723-loader bandit script.py

# Pass any arguments through to the wrapped command
pep723-loader mypy --strict --warn-unreachable script.py

# Works with directories too
pep723-loader mypy scripts/
```

### Pre-commit Integration

There are two ways to use `pep723-loader` with pre-commit:

#### Simple: If tools are already installed

First, add the tools to your project's dev dependencies:

```bash
uv add --dev pep723-loader mypy
```

Then configure the hook:

```yaml
- repo: local
  hooks:
    - id: mypy
      name: mypy
      entry: pep723-loader mypy
      language: system
      types: [python]
      pass_filenames: true
```

#### Recommended: Self-contained with uv

This approach keeps tools out of your project's dependencies - uv provides them on-demand:

```yaml
- repo: local
  hooks:
    - id: mypy
      name: mypy
      entry: uv run -q --no-sync --with pep723-loader --with mypy pep723-loader mypy
      language: system
      types: [python]
      pass_filenames: true

    - id: basedpyright
      name: basedpyright
      entry: uv run -q --no-sync --with pep723-loader --with basedpyright pep723-loader basedpyright
      language: system
      types: [python]
      pass_filenames: true
```

**What do these flags do?**

| Flag           | Purpose                                                                  |
| -------------- | ------------------------------------------------------------------------ |
| `-q`           | Quiet mode - suppresses uv's output so only linter output is shown       |
| `--no-sync`    | Skip syncing the project's dependencies - faster, we only need the tools |
| `--with <pkg>` | Temporarily add a package for this invocation                            |

The `--with` packages are ephemeral - they're not installed into your project's virtualenv. However, they're cached by uv, so after the first run there's no download overhead.

## How It Works

1. Scans Python files passed as arguments for PEP 723 `# /// script` metadata blocks
2. Extracts dependencies using `uv export --script`
3. Installs dependencies via `uv pip install`
4. Executes the wrapped command with all original arguments
5. Propagates the wrapped command's exit code

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (used for dependency extraction and installation)

## License

Apache License 2.0
