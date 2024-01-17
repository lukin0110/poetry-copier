# ✨ Integrated Development Environments

## Setup PyCharm

Open the repository with PyCharm, and [configure Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote) with the `devcontainer` service.

## Developing

#### Run linters
```bash
docker compose run devcontainer poe lint
```

#### Run tests
```bash
docker compose run devcontainer poe test
```

#### Update poetry lock file
```bash
docker compose run devcontainer poetry lock --no-update
```

Update the docker image with the new lock file:
```bash
docker compose build
```

#### Open a shell in docker
```bash
docker compose run devcontainer
```

### Serve app
```bash
docker compose up app
```
and open [localhost:8001](https://localhost:8001) in your browser.

### Conventient shortcuts with a `Makefile`

If you have chosen to scaffold *convenient shortcuts*, your repository will contain a `Makefile`. Run outside a container:

#### Run linters
```bash
make lint
```

#### Run tests
```bash
make test
```

#### Update poetry lock file
```bash
make lock
```

#### Open a shell in docker
```bash
make shell
```
