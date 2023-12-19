"""Test FastAPI app generation."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import copier

from .utils import assert_paths, assert_toml, assert_yaml

logger = logging.getLogger(__name__)


def test_github_generation(answers: dict[str, str | bool], expected_paths: set[str]) -> None:
    """Should generate all the required files."""
    answers_ = {
        **answers,
        "ci": "github",
        "repository_url": "https://github.com/lukin0110/mcfly/",
        "use_app": True,
        "use_fastapi": True,
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
            "help": "Serve a REST API in production",
            "shell": "    if [ $dev ]\n    then {\n        uvicorn --host $host --port $port --use-colors --reload --factory mcfly.app:create_app\n    } else {\n        uvicorn --host $host --port $port --use-colors --proxy-headers --timeout-graceful-shutdown 10 --timeout-keep-alive 10 --factory mcfly.app:create_app\n    } fi\n    ",
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
        assert_yaml(Path(tmpdir) / ".pre-commit-config.yaml")
        assert_yaml(Path(tmpdir) / "docker-compose.yml")
