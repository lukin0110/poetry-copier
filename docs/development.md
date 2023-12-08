# Development

Note: this document is a work in progress.

## Usage

Scaffold locally:
```bash
copier copy ../poetry-copier .
```

## Integrations

### Codecov

1. Signup on [Codecov](https://about.codecov.io/sign-up/)
2. Setup repo 
3. Add `CODECOV_TOKEN` to [GitHub Secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) with the value from Codecov
4. Copy badge from Codecov to README.md
5. Add following to `.github/workflows/test.yml`:

```yaml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: reports/coverage.xml
        env:
          CODECOV_TOKEN: {% raw %}${{ secrets.CODECOV_TOKEN }}{% endraw %}
```

## Useful reads

- [Speeding up Ubuntu Docker builds with podman](https://www.declarativesystems.com/2020/02/27/speeding-up-ubuntu-docker-builds-with-podman.html)
- [Opening VS Code with URLs](https://github.com/Microsoft/vscode-docs/blob/main/docs/editor/command-line.md#opening-vs-code-with-urls)
- [Visual Studio Code Remote Development](https://github.com/microsoft/vscode-remote-release)
