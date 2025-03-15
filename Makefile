.PHONY: reset all install update test pre-commit-setup commit tox

# Default values (modifiable via arguments, e.g., `make install PYTHON_VERSION=3.11 ENV_NAME=myenv`)
PYTHON_VERSION ?= 3.10
ENV_NAME ?= cardwise
PYTHON_VERSIONS_TOX = 3.8 3.9 3.10 3.11 3.12 3.13

# 🔥 Default: Install or update dependencies, setup pre-commit, and run tests
all: install pre-commit-setup test

# 🚀 Install Conda Environment & Poetry Dependencies (if not already installed)
install:
	@if conda env list | grep -qw "$(ENV_NAME)"; then \
		echo "✅ Conda environment '$(ENV_NAME)' exists."; \
	else \
		echo "🚀 Creating Conda environment '$(ENV_NAME)' with Python $(PYTHON_VERSION)..."; \
		conda create -y -n $(ENV_NAME) python=$(PYTHON_VERSION); \
		echo "⚠️ Run 'conda activate $(ENV_NAME)' before continuing."; \
	fi
	pip install poetry  # Ensure Poetry is installed
	@if ! poetry install; then \
		echo "🔄 Detected changes in pyproject.toml, regenerating lock file..."; \
		poetry lock --no-update; \
		poetry install; \
	fi

# 🔄 Update dependencies (Poetry + Conda) without wiping everything
update:
	@echo "🔄 Updating dependencies..."
	pip install --upgrade poetry  # Upgrade Poetry
	poetry update  # Update dependencies and lock file
	poetry install  # Ensure all dependencies are installed
	@echo "✅ Dependencies updated!"

# ✅ Run Tests (Supports -html flag for Coverage Report)
test:
	@echo "🔬 Running tests..."
	poetry run pytest --cov=src --cov-report=term-missing; \

# ⚡ Install & Update Pre-commit Hooks
pre-commit-setup:
	poetry run pre-commit install
	poetry run pre-commit autoupdate

# 🏗️ Commit & Push with Pre-commit Check
commit:
	poetry run pre-commit run --all-files
	git add .
	git commit -m "$(shell read -p 'Commit message: ' msg; echo $$msg)"
	git push

# 🔄 Reset Everything: Remove all generated files, delete Conda environment, and reinstall from scratch
reset:
	@echo "🔥 Resetting everything..."
	@if conda env list | grep -qw "$(ENV_NAME)"; then \
		echo "🗑️ Deleting Conda environment '$(ENV_NAME)'..."; \
		conda env remove -y -n $(ENV_NAME); \
	else \
		echo "⚠️ Conda environment '$(ENV_NAME)' does not exist, skipping removal."; \
	fi
	rm -rf poetry.lock .venv
	@echo "✅ Environment fully wiped! Reinstalling everything..."
	$(MAKE) all  # Reinstall everything (install, pre-commit-setup, test)
