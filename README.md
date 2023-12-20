[![License: GNU Affero General Public License v3.0](https://img.shields.io/static/v1?label=license&message=GNU%20AFFERO&color=blue)](https://github.com/lukin0110/poetry-copier/blob/main/LICENSE) ![CI](https://github.com/lukin0110/poetry-copier/actions/workflows/test.yml/badge.svg?branch=main) [![GitHub Repo stars](https://img.shields.io/github/stars/lukin0110/poetry-copier)
](https://github.com/lukin0110/poetry-copier/stargazers)

> [!IMPORTANT]
>
> This is undergoing significant development and may change frequently. It's not considered stable yet.

# Poetry Copier

A [copier](https://copier.readthedocs.io/en/stable/) template for scaffolding Python packages and apps (FastAPI and Gradio) using [Poetry](https://python-poetry.org/) as package 
manager and [DevContainers](https://containers.dev/) as reproducible development environment.

This template is a loose port of the [Radix Poetry Cookiecutter](https://github.com/radix-ai/poetry-cookiecutter) and comes with the same [LICENSE](LICENSE).

## 💻 Demo

Check out the following demos for examples of scaffolded projects using this template:

- FastAPI App with GitHub Actions: [poetry-copier-fastapi-demo](https://github.com/lukin0110/poetry-copier-fastapi-demo)
- Python Package with GitHub Actions: [poetry-copier-package-demo](https://github.com/lukin0110/poetry-copier-package-demo)

## 🎉 Features

- 🐳 Reproducible [Docker](https://www.docker.com/) based development environments with [Docker Compose](https://docs.docker.com/compose/), [VSCode Dev Containers](https://code.visualstudio.com/docs/remote/containers) and [GitHub Codespaces](https://github.com/features/codespaces)
- 🐍 Scaffold a Python package or a [FastAPI](https://fastapi.tiangolo.com/) app with [Pydantic V2](https://docs.pydantic.dev/2.5/) or a [Gradio](https://www.gradio.app/) app to demo Machine Learning models
- 📦 Dependency management with [Poetry](https://python-poetry.org/)
- 🏃 Task running with [Poe the Poet](https://poethepoet.natn.io/index.html)
- ✍️ Code formatting with [Ruff](https://docs.astral.sh/ruff/)
- ✅ Code linting with [Pre-commit](https://pre-commit.com/), [Mypy](), and [Ruff](https://docs.astral.sh/ruff/)
- 🧪 Test coverage with [Coverage.py](https://coverage.readthedocs.io/en/7.3.2/) and [Pytest](https://docs.pytest.org/en/7.4.x/)
- ♻️ Continuous integration with [GitHub Actions](https://docs.github.com/en/actions) or [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- 🧰 Dependency updates with [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) (only with GitHub Actions)
- 🚧 Interactive scaffolding and updates with [Copier](https://copier.readthedocs.io/en/stable/)

## 🚀 Using

1. Install the latest [copier](https://copier.readthedocs.io/en/stable/#installation) in your [Python environment](https://github.com/pyenv/pyenv) _(please use python>=3.8)_:
    ```bash
    pip install "copier>=9.1.0"
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
More information on how to update a project and resolve conflicts can be found in the [Copier documentation](https://copier.readthedocs.io/en/stable/updating/).   

## 💭 Rationale
This template aims to provide [dev/prod parity](https://12factor.net/dev-prod-parity) by using [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) and reuse the various 
stages to *develop locally*, *run CI/CD tasks* and *publish a package/deploy an application*. Docker is key in 
achieving this objective. It aims to establish and utilize consistent, reproducible environments, significantly 
reducing the effort required to initiate a project upon checkout. The template is designed so that you can choose how 
you want to develop locally, either using Docker or Poetry directly (without Docker).

---

👷🏼 **Troubleshooting**: [docs/troubleshooting.md](https://github.com/lukin0110/poetry-copier/blob/main/docs/troubleshooting.md)

🎨 **Technical design**: [docs/design.md](https://github.com/lukin0110/poetry-copier/blob/main/docs/design.md)

🛠️ [Open an issue](https://github.com/lukin0110/poetry-copier/issues/new) if you have any questions or suggestions
