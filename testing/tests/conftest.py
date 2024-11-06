"""Pytest configuration."""

import pytest


@pytest.fixture()
def answers() -> dict[str, str | bool]:
    """Provide answers to generate a python package."""
    return {
        "description": "A package used in tests to test a scaffolded python package",
        "name": "McFly",
        "package_type": "package",
        "use_pydantic": True,
        "use_makefile": False,
        "use_private_package_repository": False,
        "python_version": "3.13.0",
        "package_slug": "mcfly",
        "use_app": False,
        "use_fastapi": False,
        "use_gradio": False,
        "use_push_ecr": False,
    }


@pytest.fixture()
def expected_paths(package_slug: str = "mcfly") -> set[str]:
    """Provide a minimal set of required paths."""
    return {
        ".devcontainer/devcontainer.json",
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
