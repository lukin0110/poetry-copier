"""Test utilities."""

import json
import os
import tomllib
from pathlib import Path
from pprint import pprint
from typing import Any

import yaml
from deepdiff import DeepDiff


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


def assert_yaml(path: Path) -> dict[str, Any]:
    """Check if the given path is a valid yaml file."""
    try:
        with path.open("r") as fh:
            return yaml.full_load(fh)
    except yaml.YAMLError as e:
        raise AssertionError(f"Could not load: {path}") from e


def assert_devcontainer(path: Path) -> None:
    """Check if the given path is a valid devcontainer definition."""
    try:
        with path.open("r") as fh:
            data = json.load(fh)
            expected = {
                "name": "mcfly",
                "dockerComposeFile": "../docker-compose.yml",
                "service": "devcontainer",
                "runServices": ["devcontainer"],
                "shutdownAction": "stopCompose",
                "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/mcfly/,type=bind,consistency=delegated",
                "workspaceFolder": "/workspaces/mcfly/",
                "remoteUser": "root",
                "overrideCommand": True,
                "initializeCommand": "touch ${localWorkspaceFolder}/.env",
                "mounts": ["type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock,consistency=consistent"],
                "customizations": {
                    "vscode": {
                        "extensions": [
                            "charliermarsh.ruff",
                            "eamodio.gitlens",
                            "github.copilot",
                            "GitHub.vscode-github-actions",
                            "GitHub.vscode-pull-request-github",
                            "ms-azuretools.vscode-docker",
                            "ms-python.mypy-type-checker",
                            "ms-python.python",
                            "ryanluker.vscode-coverage-gutters",
                            "tamasfe.even-better-toml",
                            "visualstudioexptteam.vscodeintellicode",
                        ],
                        "settings": {
                            "coverage-gutters.coverageFileNames": ["reports/coverage.xml"],
                            "editor.codeActionsOnSave": {
                                "source.fixAll": "explicit",
                                "source.organizeImports": "explicit",
                            },
                            "editor.formatOnSave": True,
                            "editor.rulers": [100],
                            "editor.tabSize": 4,
                            "dev.containers.copyGitConfig": True,
                            "github.copilot.chat.edits.enabled": True,
                            "files.autoSave": "onFocusChange",
                            "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
                            "[toml]": {"editor.formatOnSave": False},
                            "mypy-type-checker.importStrategy": "fromEnvironment",
                            "mypy-type-checker.preferDaemon": True,
                            "python.defaultInterpreterPath": "/opt/mcfly-env/bin/python",
                            "python.terminal.activateEnvironment": False,
                            "python.testing.pytestEnabled": True,
                            "ruff.importStrategy": "fromEnvironment",
                            "ruff.logLevel": "warning",
                            "terminal.integrated.defaultProfile.linux": "zsh",
                            "terminal.integrated.profiles.linux": {"zsh": {"path": "/usr/bin/zsh"}},
                            "workbench.editor.wrapTabs": True,
                        },
                    },
                },
            }
            diff = DeepDiff(expected, data)
            pprint(diff)  # noqa: T203
            assert not diff
    except json.JSONDecodeError as e:
        raise AssertionError(f"Could not load: {path}") from e
