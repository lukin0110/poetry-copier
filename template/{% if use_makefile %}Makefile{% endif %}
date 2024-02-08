# Convenient shortcuts to run some tasks
# Useful if you're not using DevContainers

# Default target when just `make` is executed
default: help

# Show help
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  lint     Run linters"
	@echo "  safety   Run safety"
	@echo "  test     Run tests"
	@echo "  lock     Update poetry lock file"
	@echo "  shell    Open a shell in the dev container"
	@echo ""

# Run lint
.PHONY: lint
lint:
	docker compose run devcontainer poe lint

# Run safety
.PHONY: safety
safety:
	docker compose run devcontainer poe safety

# Run tests
.PHONY: test
test:
	docker compose run devcontainer poe test

# Update poetry lock file
.PHONY: lock
lock:
	docker compose run devcontainer poetry lock --no-update

# Open a docker shell
.PHONY: shell
shell:
	docker compose run devcontainer
