"""Test Python package generation."""

import logging
from tempfile import TemporaryDirectory

import copier
import pytest

from tests.utils import assert_paths

logger = logging.getLogger(__name__)


@pytest.fixture()
def answers() -> dict[str, str | bool]:
    """Provide answers to generate a python package."""
    return {
        "ci": "github",
        "description": "A package used in tests to test a scaffolded python package",
        "name": "McFly",
        "package_type": "package",
        "repository_url": "https://github.com/lukin0110/mcfly/",
        "use_makefile": False,
        "use_private_package_repository": False,
        "python_version": "3.11.6",
        "package_slug": "mcfly",
        "use_app": False,
        "use_fastapi": False,
        "use_gradio": False,
        "use_push_ecr": False,
    }


def test_generation(answers: dict[str, str | bool]) -> None:
    """Should generate all the required files."""
    with TemporaryDirectory() as tmpdir:
        copier.run_copy("../template", tmpdir, data=answers, overwrite=True)
        assert_paths(
            tmpdir,
            {
                ".devcontainer/devcontainer.json",
                ".github/workflows/push_to_ghcr.yml",
                ".github/workflows/test.yml",
                ".github/dependabot.yml",
                "docs/README.md",
                "src/mcfly/__init__.py",
                "src/mcfly/py.typed",
                "tests/mcfly/__init__.py",
                "tests/mcfly/test_foo.py",
                "tests/__init__.py",
                "tests/conftest.py",
                ".copier-answers.yml",
                ".dockerignore",
                ".gitignore",
                ".pre-commit-config.yaml",
                ".python-version",
                "docker-compose.yml",
                "Dockerfile",
                "pyproject.toml",
                "README.md",
            },
        )
