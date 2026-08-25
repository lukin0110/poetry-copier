# Development

> **Note**: this document is a work in progress.

## Usage

Scaffold locally:
```bash
copier copy --vcs-ref HEAD ../uv-copier .
```

## Run tests
```
cd testing
uv run -m pytest
```

## Scaffold a project and check it

Generate a project from the *working tree* (uncommitted changes included) and run its lint and
test suites, the local equivalent of the `generate_package` and `generate_fastapi` jobs in
`.github/workflows/test.yml`:

```bash
.claude/hooks/scaffold-check.sh package fastapi
```

Generated projects are cached in `~/.cache/uv-copier-hooks/<checkout-key>/scaffold/<variant>/`
(keyed per checkout, so git worktrees don't share state), which keeps their `.venv`, `.git`,
`uv.lock` and tool caches warm between runs. Reset with:

```bash
rm -rf ~/.cache/uv-copier-hooks
```

Note: a manual run covering fewer than the default variants (`package fastapi`) does not count
as "checked" — the `Stop` hook will still verify the pending change.

## Claude Code hooks

Two hooks are configured in [.claude/settings.json](../.claude/settings.json), sharing helpers
from `.claude/hooks/lib.sh`:

| Hook | Script | What it does |
| --- | --- | --- |
| `PostToolUse` | `.claude/hooks/test-template.sh` | Runs the `testing/` pytest suite after an edit to `template/` or `copier.yml`, and flags the change for the `Stop` hook. |
| `Stop` | `.claude/hooks/scaffold-check.sh` | Scaffolds the `package` and `fastapi` variants (concurrently) and runs `poe lint` and `poe test` on each, once per turn. Triggered by the flag or by a change in the fingerprint of `template/` + `copier.yml` since the last successful check — so template changes made via shell commands are caught too. |

Both exit with status `2` on failure so the report is fed back to Claude.

## Useful reads

- [Speeding up Ubuntu Docker builds with podman](https://www.declarativesystems.com/2020/02/27/speeding-up-ubuntu-docker-builds-with-podman.html)
- [Opening VS Code with URLs](https://github.com/Microsoft/vscode-docs/blob/main/docs/editor/command-line.md#opening-vs-code-with-urls)
- [Visual Studio Code Remote Development](https://github.com/microsoft/vscode-remote-release)
- [Running Docker Compose in Codespaces](https://notes.alexkehayias.com/running-docker-compose-in-codespaces/): not applied at this moment

## Development without Docker

The template aims to strike a balance between Docker-based and non-Docker-based development. To utilize uv without Docker, follow these steps:

1. Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Activate pyenv: 
```bash 
pyenv shell 3.14.3
```
3. Install uv: 
```bash 
pip install uv
uv sync
```
3. Install pre-commit:
```bash
pre-commit clean # In case of erratic behaviour of the environment
pre-commit install --install-hooks
```
