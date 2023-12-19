# Technical design

Overview of design decisions and architecture of the template.

## 🦺 All git directories marked as safe within the DevContainer

When Linux users run Git commands in a Docker container within a mounted directory, they may encounter the following 
warning: `detected dubious ownership in repository`. This issue can be resolved by marking the repository as safe. This action is performed in the `Dockerfile` in the *dev* stage. All git directories are marked as safe by the following command:

```bash
git config --system --add safe.directory '*'
```

Reasons:
- Adding this to the [Dockerfile](../template/Dockerfile.jinja) will provide a centralized solution to the issue.
- Using `--system` will add the config to `/etc/gitconfig`. In case `--global` is used it will be added to `~/.gitconfig`. However, this approach will cause VSCode to fail in sharing Git config and credentials from the host system with the `DevContainer`.

## 🐳 Docker support within the DevContainer

The [docker cli](https://docs.docker.com/engine/reference/commandline/cli/) has been installed in the DevContainer to 
allow running docker commands in the DevContainer and interact with docker on the host system. The 
*docker-outside-of-docker* concept is used instead of *docker-in-docker*. This means that the docker engine is not 
running inside the DevContainer but the host docker engine is used instead. 

This is achieved by:
- Mounting the docker socket from the host system into the DevContainer.
- Installing the docker cli in the DevContainer

### 1. Mounting the docker socket in .devcontainer/devcontainer.json
```json
{
  "mounts": [
    "type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock,consistency=consistent"
  ]
}
```

### 2. Installing the docker cli in the DevContainer

The image of the *DevContainer* is defined in the root [Dockerfile](../template/Dockerfile.jinja) of the template as 
*dev* target. The installation of the docker cli is based on the [installation script of docker](https://get.docker.com/).

Dockerfile snippet:
```dockerfile
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL "https://download.docker.com/linux/debian/gpg" | gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    apt_repo="deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" && \
    echo "$apt_repo" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get --yes --no-install-recommends install docker-ce-cli docker-compose-plugin
```

> [!IMPORTANT]
>
> The [features](https://containers.dev/features) section of DevContainers is not used. Mainly to stay explicitly in control of what is installed 
> in the DevContainer. Possible useful features are: 
> [docker-outside-of-docker](https://github.com/devcontainers/features/tree/main/src/docker-outside-of-docker) and 
> [docker-in-docker](https://github.com/devcontainers/features/tree/main/src/docker-in-docker).
