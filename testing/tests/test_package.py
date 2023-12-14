"""Test Python package generation."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import copier
import pytest

from .utils import assert_devcontainer, assert_paths, assert_toml

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
        "use_app": False,
        "use_fastapi": False,
        "use_gradio": False,
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
        }
        assert_paths(tmpdir, expected)
        assert_devcontainer(Path(tmpdir) / ".devcontainer/devcontainer.json")
        assert_toml(Path(tmpdir) / "pyproject.toml")


def test_gitlab_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "gitlab",
        "repository_url": "https://gitlab.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.debug("GitLab package: %s", tmpdir)
        copier.run_copy("../template", tmpdir, data=answers_, cleanup_on_error=True)
        expected = expected_paths | {".gitlab-ci.yml"}
        assert_paths(tmpdir, expected)
        assert_devcontainer(Path(tmpdir) / ".devcontainer/devcontainer.json")
        assert_toml(Path(tmpdir) / "pyproject.toml")
