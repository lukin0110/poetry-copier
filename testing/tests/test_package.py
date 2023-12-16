"""Test Python package generation."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import copier

from .utils import assert_devcontainer, assert_paths, assert_toml

logger = logging.getLogger(__name__)


def test_github_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "github",
        "repository_url": "https://github.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.debug("GitHub package: %s", tmpdir)
        copier.run_copy("../template", tmpdir, data=answers_, quiet=True, cleanup_on_error=True)
        expected = expected_paths | {
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
