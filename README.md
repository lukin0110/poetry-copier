# Poetry Copier

A [copier](https://copier.readthedocs.io/en/stable/) template for scaffolding Python packages and/or FastAPI apps using 
[Poetry](https://python-poetry.org/) as package manager.

This template is a loose port of the [Radix Poetry Cookiecutter](https://github.com/radix-ai/poetry-cookiecutter) and comes with the same [LICENSE](LICENSE).

## 🎉 Features

- 🐳 Reproducible development environments with [Docker](https://www.docker.com/)
- 📦 Dependency management with [Poetry](https://python-poetry.org/)
- 🏃 Task running with [Poe the Poet](https://poethepoet.natn.io/index.html)
- ✍️ Code formatting with [Ruff](https://docs.astral.sh/ruff/)
- ✅ Code linting with [Pre-commit](https://pre-commit.com/), [Mypy](), and [Ruff](https://docs.astral.sh/ruff/)
- 🧪 Test coverage with [Coverage.py](https://coverage.readthedocs.io/en/7.3.2/) and [Pytest](https://docs.pytest.org/en/7.4.x/)
- ♻️ Continuous integration with [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- ⚡️ Optionally include [FastAPI](https://fastapi.tiangolo.com/) with [Pydantic V2](https://docs.pydantic.dev/2.5/)
- 🚧 Interactive scaffolding and updates with [Copier](https://copier.readthedocs.io/en/stable/)

## Using

1. Install the latest [copier](https://copier.readthedocs.io/en/stable/#installation) in your [Python environment](https://github.com/pyenv/pyenv) _(please use python>=3.8)_:
    ```bash
    pip install "copier>=9.0.1"
    ```
2. Create a new repository and clone it locally.
3. Run copier in your cloned directory:
    ```bash
    copier copy --vcs-ref=HEAD git@github.com:lukin0110/poetry-copier.git .
    ```
   
### Updating a project

```bash
copier update --vcs-ref=HEAD --defaults
```

## Rationale
This template aims to provide [dev/prod parity](https://12factor.net/dev-prod-parity) by using [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) and reuse the various 
stages to *develop locally*, *run CI/CD tasks* and *publish a package/deploy an application*. Docker is key in 
achieving this objective. It aims to establish and utilize consistent, reproducible environments, significantly 
reducing the effort required to initiate a project upon checkout. The template is designed so that you can choose how 
you want to develop locally, either using Docker or Poetry directly (without Docker).

_Note: it does not use [DevContainers](https://containers.dev/) (yet). I'm tackling complexity per complexity_ 😎.
