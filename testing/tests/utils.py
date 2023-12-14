"""Test utilities."""

import json
import os
import tomllib
from pathlib import Path
from typing import Any


def assert_paths(directory: str, paths: set[str]) -> None:
    """Check if the given set of paths exist in the specified directory.

    Parameters
    ----------
    directory : str
        The directory in which to check for the paths.
    paths : set[str]
        A set of relative file paths to check for in the directory.

    Raises
    ------
    AssertionError
        If any of the paths in the set are not found in the directory.
    """
    tree = set()
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(Path(root) / file, directory)
            tree.add(relative_path)

    if tree != paths:
        diff1, diff2 = paths - tree, tree - paths
        msg = [f"Asserted but not in tree: {diff1}."] if diff1 else []
        msg += [f"In tree but not asserted: {diff2}."] if diff2 else []
        raise AssertionError(" ".join(msg))


def assert_toml(path: Path) -> dict[str, Any]:
    """Check if the given path is a valid toml file."""
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except tomllib.TOMLDecodeError as e:
        raise AssertionError(f"Could not load: {path}") from e


def assert_devcontainer(path: Path) -> None:
    """Check if the given path is a valid devcontainer definition."""
    try:
        with path.open("r") as fh:
            data = json.load(fh)
            assert data == {
                "name": "mcfly",
                "dockerComposeFile": "../docker-compose.yml",
                "service": "devcontainer",
                "runServices": ["devcontainer"],
                "shutdownAction": "stopCompose",
                "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/mcfly/,type=bind,consistency=cached",
                "workspaceFolder": "/workspaces/mcfly/",
                "remoteUser": "root",
                "overrideCommand": True,
                "initializeCommand": "touch .env",
                "customizations": {
                    "vscode": {
                        "extensions": [
                            "charliermarsh.ruff",
                            "eamodio.gitlens",
                            "ms-python.mypy-type-checker",
                            "ms-python.python",
                            "ryanluker.vscode-coverage-gutters",
                            "tamasfe.even-better-toml",
                            "visualstudioexptteam.vscodeintellicode",
                        ],
                        "settings": {
                            "coverage-gutters.coverageFileNames": ["reports/coverage.xml"],
                            "editor.codeActionsOnSave": {"source.fixAll": True, "source.organizeImports": True},
                            "editor.formatOnSave": True,
                            "editor.rulers": [100],
                            "editor.tabSize": 4,
                            "files.autoSave": "onFocusChange",
                            "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
                            "[toml]": {"editor.formatOnSave": False},
                            "mypy-type-checker.importStrategy": "fromEnvironment",
                            "python.defaultInterpreterPath": "/opt/mcfly-env/bin/python",
                            "python.terminal.activateEnvironment": False,
                            "python.testing.pytestEnabled": True,
                            "ruff.importStrategy": "fromEnvironment",
                            "ruff.logLevel": "warn",
                            "terminal.integrated.defaultProfile.linux": "zsh",
                            "terminal.integrated.profiles.linux": {"zsh": {"path": "/usr/bin/zsh"}},
                        },
                    },
                    "codespaces": {"openFiles": ["README.md"]},
                },
            }
    except json.JSONDecodeError as e:
        raise AssertionError(f"Could not load: {path}") from e
