"""Pytest configuration."""

import pytest


@pytest.fixture()
def expected_paths(package_slug: str = "mcfly") -> set[str]:
    """Provide a minimal set of required paths."""
    return {
        ".devcontainer/devcontainer.json",
        "docs/README.md",
        f"src/{package_slug}/__init__.py",
        f"src/{package_slug}/py.typed",
        f"tests/{package_slug}/__init__.py",
        f"tests/{package_slug}/test_foo.py",
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
    }
