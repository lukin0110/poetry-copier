# Development

> **Note**: this document is a work in progress.

## Usage

Scaffold locally:
```bash
copier copy ../poetry-copier .
```

## Troubleshoot `Permission denied (publickey).` in the DevContainer on OSX

1. Add all private keys to the ssh-agent: `ssh-add -A`
2. Reboot Docker Desktop
3. Reopen VSCode

`SSH Keys` should be shared now with the `DevContainer` 😎

### Other useful commands

1. Restart the ssh-agent: `eval "$(ssh-agent -s)"`
2. View ssh keys: `ssh-add -l`

### Problem description
On OSX, `SSH Keys` are not always automatically shared between the host and the `DevContainer`. They are lazily added to 
the *SSH Agent*. When they're not added to the *SSH Agent*, you'll get the following error when trying to execute 
`git pull`, `git push` or `git clone` commands in the `DevContainer`:
```bash
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Related issue on `vscode-remote-release`: [Automatically add SSH keys to ssh-agent](https://github.com/microsoft/vscode-remote-release/issues/4024)

## Development without Docker

The template aims to strike a balance between Docker-based and non-Docker-based development. To utilize Poetry without Docker, follow these steps:

1. Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Activate pyenv: 
```bash 
pyenv shell 3.11.6
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

## Useful reads

- [Speeding up Ubuntu Docker builds with podman](https://www.declarativesystems.com/2020/02/27/speeding-up-ubuntu-docker-builds-with-podman.html)
- [Opening VS Code with URLs](https://github.com/Microsoft/vscode-docs/blob/main/docs/editor/command-line.md#opening-vs-code-with-urls)
- [Visual Studio Code Remote Development](https://github.com/microsoft/vscode-remote-release)
- [Running Docker Compose in Codespaces](https://notes.alexkehayias.com/running-docker-compose-in-codespaces/): not applied at this moment
