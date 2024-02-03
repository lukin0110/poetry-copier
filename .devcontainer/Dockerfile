# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Create and activate a virtual environment.
RUN python -m venv /opt/testing-env
ENV PATH /opt/testing-env/bin:$PATH
ENV VIRTUAL_ENV /opt/testing-env

# Install python dependencies for testing.
COPY testing/pyproject.toml . 
RUN pip install poetry==1.7.1 && poetry install --no-root

# Mark the workspace as safe for git
RUN git config --system --add safe.directory '*'
