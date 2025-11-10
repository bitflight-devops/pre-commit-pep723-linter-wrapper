
"""PEP 723 wrapper for linting Python scripts

This script ensures that 'uv' is available locally, and uses it to install the dependencies for the script into the current environment.

This is useful for using mypy, ruff, pyright, basedpright, pylint, flake8, bandit, etc. without having to have a vnv with the script dependencies or tools installed..

Architecture:
    - Follows SOLID principles with abstract interfaces
    - Dependency injection for flexibility and testability
    - Generic and project-agnostic design
    - Parses all build parameters from CMake arguments (no hardcoded fields)

SOLID Principles Applied:
    S: Single Responsibility - Each class has one clear purpose
    O: Open/Closed - Extensible via interfaces without modification
    L: Liskov Substitution - Implementations are interchangeable
    I: Interface Segregation - Specific interfaces for each concern
    D: Dependency Inversion - Depends on abstractions, not concretions
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


