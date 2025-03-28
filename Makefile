.PHONY: reset all install update test pre-commit-setup commit tox

# Default values (modifiable via arguments, e.g., `make install PYTHON_VERSION=3.11 ENV_NAME=myenv`)
PYTHON_VERSION ?= 3.10
ENV_NAME ?= cardwise
PYTHON_VERSIONS_TOX = 3.8 3.9 3.10 3.11 3.12 3.13

# 🔥 Default: Install or update dependencies, setup pre-commit, and run tests
all: install pre-commit-setup test

# 🚀 Install Poetry Environment (if not already installed)
install:
	pip install poetry  # Ensure Poetry is installed
	poetry install # Install dependencies using lock file (or create one if missing)

install-dev: 
	pip install poetry  # Ensure Poetry is installed
	poetry install --all-groups # Install dependencies using lock file (or create one if missing)

# 🔄 Update dependencies (Poetry) without wiping everything
update:
	@echo "🔄 Updating dependencies..."
	pip install --upgrade poetry  # Upgrade Poetry
	poetry update  # Update dependencies and lock file
	@echo "✅ Dependencies updated!"

# ✅ Run Tests (Supports -html flag for Coverage Report)
test:
	@echo "🔬 Running tests..."
	poetry run pytest --cov=src --cov-report=term-missing; \

# ⚡ Install & Update Pre-commit Hooks
pre-commit-setup:
	poetry run pre-commit autoupdate
	poetry run pre-commit install

# 🏗️ Commit & Push with Pre-commit Check
commit:
	- poetry run pre-commit run --all-files
	git add .
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		read -p "Commit message: " msg; \
	else \
		msg="$(word 2,$(MAKECMDGOALS))"; \
	fi; \
	git commit -m "$$msg"; \
	git push

## Allow passing commit message as a positional argument
%::
	@:


# 🔄 Reset Everything: Remove all generated files, delete Conda environment, and reinstall from scratch
reset:
	@echo "🔥 Resetting everything..."
	rm -rf poetry.lock .venv
	# Enter the current Poetry environment
	poetry shell
	# Remove the current environment
	poetry env remove $(which python)
	@echo "🔥 Removing Poetry environment..."
	poetry env remove --all
	@echo "✅ Environment fully wiped! Reinstalling everything..."
	$(MAKE) all  # Reinstall everything (install, pre-commit-setup, test)
