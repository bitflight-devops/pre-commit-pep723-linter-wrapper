# Copilot Instructions for PEP 723 Loader

## Project Overview

**PEP 723 Loader** auto-installs [PEP 723](https://peps.python.org/pep-0723/) inline script dependencies before running linters (mypy, ruff, basedpyright). Small Python 3.10+ project (~500 LOC) using uv for builds/deps, monorepo in `packages/pep723_loader/`.

**CRITICAL**: Install `uv` first: `pip install uv`

## Build and Validation Commands

### Initial Setup (ALWAYS run first)

```bash
uv sync  # ~60-90s first run, <5s after. Installs all deps into .venv/
```

### Testing

```bash
uv run pytest                      # All tests with coverage (~10-15s), requires ≥70%
uv run pytest --no-cov             # Faster iteration
uv run pytest path/to/test.py      # Single file
uv run pytest path/to/test.py::TestClass::test_method  # Single test
```

Expected: 39 tests pass, ~91% coverage.

### Linting, Formatting, Type Checking

```bash
uv run ruff check --fix .          # Auto-fix issues (~2-3s)
uv run ruff format .                # Format code (~1-2s)
uv run mypy packages/               # Type check (~5-8s)
uv run basedpyright packages/       # Alternative type checker (~10-15s)
uv run prek run --all-files         # All hooks (~30-60s first, ~10-20s after) - uses prek for faster execution
```

### Building

```bash
uv build  # Creates wheel + sdist in dist/ (~5-10s)
```

### Full Pre-Push Validation

```bash
uv sync && uv run ruff check --fix . && uv run ruff format . && \
uv run mypy packages/ && uv run basedpyright packages/ && uv run pytest
```

## Project Layout & Architecture

```
packages/pep723_loader/
├── cli.py               # Typer CLI entry, wraps commands, installs deps, propagates exit codes
├── pep723_checker.py    # Core: discovers .py files, runs `uv export --script`, aggregates deps
├── dependencies.py      # Reserved (empty)
├── version.py           # Git tag-based version via hatch-vcs
└── tests/
    ├── unit/            # Mock subprocess calls, use fixtures in fixtures/
    └── e2e/             # Real command execution tests
```

**Key Flow**: CLI → extract Python files from args → `Pep723Checker` runs `uv export --script` → install via `uv pip install` → execute wrapped command → propagate exit code.

**Config Files**:

- `pyproject.toml`: Tool configs (ruff: 120 char lines, Google docstrings; mypy: strict; pytest: ≥70% cov)
- `.pre-commit-config.yaml`: Hooks use `uv run --no-sync` with pep723-loader (dogfooding)
- `.gitignore`: Excludes `.venv/`, `dist/`, `__pycache__/`, cache dirs

## CI/CD Workflows

**auto-publish.yml** (on push to `main`): Bumps version → builds → publishes to PyPI via OIDC → creates GitHub release. Uses `astral-sh/setup-uv@v7`, requires `pypi` environment.

**zizmor.yml** (on push/PR): Scans workflows for security issues.

## Common Pitfalls

1. **`uv: command not found`**: Install with `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Shallow clone warnings**: Harmless - from setuptools-scm in CI environments
3. **Import errors**: Run `uv sync` first
4. **Pre-commit/prek fails**: Ensure `uv sync` ran; hooks use `--no-sync` for speed
5. **Coverage <70%**: Add tests; use `pytest --cov-report=html` for details
6. **Type errors in git.py**: Ignore - it's gitpython, not our code

## Code Conventions

- Python 3.10+ (use `|` for unions, not `Union`)
- Full type hints (mypy strict mode)
- Google-style docstrings, 120 char lines
- Path objects over strings
- f-strings over `.format()` or `%`
- Tests follow AAA pattern (Arrange, Act, Assert)

## When to Search Beyond This

These instructions are validated. Only search if:

- Command fails unexpectedly
- Adding new dependency/tool
- Instructions incomplete for your scenario

**Default validation**: `uv sync && uv run pytest`
