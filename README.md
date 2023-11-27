# Poetry Copier: a copier template

A [copier](https://copier.readthedocs.io/en/stable/) template for scaffolding Python packages and/or FastAPI apps using 
[Poetry](https://python-poetry.org/) as package manager.

This template is a loose port of the [Radix Poetry Cookiecutter](https://github.com/radix-ai/poetry-cookiecutter) template and comes with the same [LICENSE](LICENSE).

## Using

1. Install the latest [copier](https://copier.readthedocs.io/en/stable/#installation) in your [Python environment](https://github.com/pyenv/pyenv) _(please use python>=3.8)_:
    ```bash
    $ pip install "copier>=9.0.1"
    ```
2. Create a new repository and clone it locally.
3. Run copier in your cloned directory:
    ```bash
    $ copier copy --vcs-ref main git@github.com:lukin0110/poetry-copier.git .
    ```

## Rationale
This template aims to provide [dev/prod parity](https://12factor.net/dev-prod-parity) by using [Docker multi-stage build](https://docs.docker.com/build/building/multi-stage/) and reuse the
various stages to *develop locally*, *run CI/CD tasks* and *deploy the application*. Docker is key in achieving this objective. It aims to establish and utilize consistent, reproducible environments, significantly reducing the effort required to initiate a project upon checkout.

_Note: it does not use [DevContainers](https://containers.dev/) (yet). I'm tackling complexity per complexity_ 😎.
