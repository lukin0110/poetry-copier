"""Test Gradio App generation."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import copier
import pytest

from .utils import assert_paths, assert_toml

logger = logging.getLogger(__name__)


@pytest.fixture()
def answers() -> dict[str, str | bool]:
    """Provide answers to generate a python package."""
    return {
        "description": "A package used in tests to test a scaffolded python package",
        "name": "McFly",
        "package_type": "package",
        "use_makefile": False,
        "use_private_package_repository": False,
        "python_version": "3.11.6",
        "package_slug": "mcfly",
        "use_app": True,
        "use_fastapi": False,
        "use_gradio": True,
        "use_push_ecr": False,
    }


def test_github_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "github",
        "repository_url": "https://github.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.debug("GitHub package: %s", tmpdir)
        copier.run_copy("../template", tmpdir, data=answers_, cleanup_on_error=True)
        expected = expected_paths | {
            ".github/workflows/push_to_ghcr.yml",
            ".github/workflows/test.yml",
            ".github/dependabot.yml",
            "src/mcfly/app.py",
        }
        assert_paths(tmpdir, expected)
        toml = assert_toml(Path(tmpdir) / "pyproject.toml")
        assert toml["tool"]["poe"]["tasks"]["serve"] == {
            "help": "Serve Gradio App",
            "cmd": "gradio src/mcfly/app.py",
            "use_exec": True,
            "args": [
                {
                    "help": "Bind socket to this host (default: 0.0.0.0)",
                    "name": "host",
                    "options": ["--host"],
                    "default": "0.0.0.0",  # noqa: S104
                },
                {
                    "help": "Bind socket to this port (default: 8000)",
                    "name": "port",
                    "options": ["--port"],
                    "default": "8000",
                },
                {"help": "Enable development mode", "type": "boolean", "name": "dev", "options": ["--dev"]},
            ],
        }
