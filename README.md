[![License: GNU Affero General Public License v3.0](https://img.shields.io/static/v1?label=license&message=GNU%20AFFERO&color=blue)](https://github.com/lukin0110/uv-copier/blob/main/LICENSE) ![CI](https://github.com/lukin0110/uv-copier/actions/workflows/test.yml/badge.svg?branch=main) [![GitHub Repo stars](https://img.shields.io/github/stars/lukin0110/uv-copier)
](https://github.com/lukin0110/uv-copier/stargazers)

# Uv Copier

A [copier](https://copier.readthedocs.io/en/stable/) template for scaffolding Python packages and apps (FastAPI and Gradio) using [uv](https://docs.astral.sh/uv/) as package 
manager and [Development Containers](https://containers.dev/) as reproducible development environment.

## 💻 Demo

Check out the following demos for examples of scaffolded projects using this template:

- FastAPI App with GitHub Actions: [uv-copier-fastapi-demo](https://github.com/lukin0110/uv-copier-fastapi-demo)
- Python Package with GitHub Actions: [uv-copier-package-demo](https://github.com/lukin0110/uv-copier-package-demo)
- FastAPI App with GitLab CI/CD: [uv-copier-fastapi-demo-gitlab](https://gitlab.com/lukin0110/uv-copier-fastapi-demo-gitlab)
- Python Package GitLab CI/CD: [uv-copier-package-demo-gitlab](https://gitlab.com/lukin0110/uv-copier-package-demo-gitlab)

## 🎉 Features

- 🐳 Reproducible [Docker](https://www.docker.com/) based development environments with [Docker Compose](https://docs.docker.com/compose/) and [Development Containers](https://containers.dev/)
- 🤝 Integrated support for [VSCode](https://code.visualstudio.com/) with [VSCode Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) and [GitHub Codespaces](https://github.com/features/codespaces)
- 🐍 Scaffold a Python package or a [FastAPI](https://fastapi.tiangolo.com/) app with [Pydantic V2](https://docs.pydantic.dev/2.5/), [Streamlit](https://streamlit.io/) app or [Gradio](https://www.gradio.app/) app to demo Machine Learning models
- 📦 Dependency management with [uv](https://docs.astral.sh/uv/)
- 🏃 Task running with [Poe the Poet](https://poethepoet.natn.io/index.html)
- ✍️ Code formatting with [Ruff](https://docs.astral.sh/ruff/)
- ✅ Code linting with [Pre-commit](https://pre-commit.com/), [Ty](https://docs.astral.sh/ty/), and [Ruff](https://docs.astral.sh/ruff/)
- 🧪 Test coverage with [Coverage.py](https://coverage.readthedocs.io/en/7.3.2/) and [Pytest](https://docs.pytest.org/en/7.4.x/)
- ♻️ Continuous integration with [GitHub Actions](https://docs.github.com/en/actions) or [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- 🧰 Dependency updates with [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) (only with GitHub Actions)
- 🚧 Interactive scaffolding and updates with [Copier](https://copier.readthedocs.io/en/stable/)

## 🚀 Using

1. Install the latest [copier](https://copier.readthedocs.io/en/stable/#installation) in your [Python environment](https://github.com/pyenv/pyenv) _(please use python>=3.8)_:
    ```bash
    pip install "copier>=9.12.0"
    ```
2. Create a new repository and clone it locally.
3. Run copier in your cloned directory:
    ```bash
    copier copy --vcs-ref=v1.2.0 git@github.com:lukin0110/uv-copier.git .
    ```

### Updating a project

```bash
copier update --vcs-ref=HEAD --defaults
```
More information on how to update a project and resolve conflicts can be found in the [Copier documentation](https://copier.readthedocs.io/en/stable/updating/).   

## 💭 Rationale
This template aims to provide a minimal, but fully functional, project structure for any python project. Focus on what matters: **coding!**  

Setting up a project can be tedious and requires a lot of "plumbing" to get `CI/CD` right, to get `pyproject.toml` right, to get the `Dockerfile` right, etc.

The use of [Docker](https://www.docker.com/) in conjunction with [Development Containers](https://containers.dev/) are key in this template to provide a smooth development experience. It's possible to develop without a *Development Container* and use [uv](https://docs.astral.sh/uv/) with [virtual environments](https://docs.python.org/3/library/venv.html) straight away, however this template is optimized to provide a working development environment with development containers.

> [!Note]
>
> This template is not a good fit if you don't want to work with *Docker* and/or *Development Containers*.

## 🎯 Goals

- Reduce project setup
- Provide [dev/prod parity](https://12factor.net/dev-prod-parity)
- [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) independent. However, with a strong focus on [VSCode](https://code.visualstudio.com/) since it integrates nicely with *GitHub*, *Development Containers* and *GitHub Copilot*
- Provide a minimal workable setup
- Don't enforce application or package architecture
- Include the *usual suspects* of every project: CI/CD, linting, testing, package manager, development container, etc

---

👷🏼 **Troubleshooting**: [docs/troubleshooting.md](https://github.com/lukin0110/uv-copier/blob/main/docs/troubleshooting.md)

🎨 **Technical design**: [docs/design.md](https://github.com/lukin0110/uv-copier/blob/main/docs/design.md)

🛠️ [Open an issue](https://github.com/lukin0110/uv-copier/issues/new) if you have any questions or suggestions
