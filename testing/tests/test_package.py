"""Test Python package generation."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import copier

from .utils import assert_devcontainer, assert_paths, assert_toml, assert_yaml

logger = logging.getLogger(__name__)


def test_github_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "github",
        "repository_url": "https://github.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.info("GitHub package: %s", tmpdir)
        _path = Path(__file__).parent.parent.parent / "template"
        copier.run_copy(str(_path.absolute()), tmpdir, data=answers_, cleanup_on_error=True)
        expected = expected_paths | {
            ".github/workflows/publish.yml",
            ".github/workflows/test.yml",
            ".github/dependabot.yml",
        }
        assert_paths(tmpdir, expected)
        assert_devcontainer(Path(tmpdir) / ".devcontainer/devcontainer.json", github=True)
        assert_toml(Path(tmpdir) / "pyproject.toml")
        assert_yaml(Path(tmpdir) / ".pre-commit-config.yaml")
        assert_yaml(Path(tmpdir) / "docker-compose.yml")


def test_gitlab_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "gitlab",
        "repository_url": "https://gitlab.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.info("GitLab package: %s", tmpdir)
        _path = Path(__file__).parent.parent.parent / "template"
        copier.run_copy(str(_path.absolute()), tmpdir, data=answers_, cleanup_on_error=True)
        expected = expected_paths | {".gitlab-ci.yml"}
        assert_paths(tmpdir, expected)
        assert_devcontainer(Path(tmpdir) / ".devcontainer/devcontainer.json", gitlab=True)
        assert_toml(Path(tmpdir) / "pyproject.toml")
        assert_yaml(Path(tmpdir) / ".pre-commit-config.yaml")
        assert_yaml(Path(tmpdir) / "docker-compose.yml")


def test_no_ci_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        "ci": "none",
        "repository_url": "https://gitlab.com/lukin0110/mcfly/",
        **answers,
    }
    with TemporaryDirectory() as tmpdir:
        logger.info("No CI package: %s", tmpdir)
        _path = Path(__file__).parent.parent.parent / "template"
        copier.run_copy(str(_path.absolute()), tmpdir, data=answers_, cleanup_on_error=True)
        assert_paths(tmpdir, expected_paths)
        assert_devcontainer(Path(tmpdir) / ".devcontainer/devcontainer.json")
        assert_toml(Path(tmpdir) / "pyproject.toml")
        assert_yaml(Path(tmpdir) / ".pre-commit-config.yaml")
        assert_yaml(Path(tmpdir) / "docker-compose.yml")
