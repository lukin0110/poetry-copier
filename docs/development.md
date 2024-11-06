# Development

> **Note**: this document is a work in progress.

## Usage

Scaffold locally:
```bash
copier copy --vcs-ref HEAD ../poetry-copier .
```

## Useful reads

- [Speeding up Ubuntu Docker builds with podman](https://www.declarativesystems.com/2020/02/27/speeding-up-ubuntu-docker-builds-with-podman.html)
- [Opening VS Code with URLs](https://github.com/Microsoft/vscode-docs/blob/main/docs/editor/command-line.md#opening-vs-code-with-urls)
- [Visual Studio Code Remote Development](https://github.com/microsoft/vscode-remote-release)
- [Running Docker Compose in Codespaces](https://notes.alexkehayias.com/running-docker-compose-in-codespaces/): not applied at this moment

## Development without Docker

The template aims to strike a balance between Docker-based and non-Docker-based development. To utilize Poetry without Docker, follow these steps:

1. Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Activate pyenv: 
```bash 
pyenv shell 3.13.0
```
3. Install Poetry: 
```bash 
pip install poetry
poetry install
```
3. Install pre-commit:
```bash
pre-commit clean # In case of erratic behaviour of the environment
pre-commit install --install-hooks
```
