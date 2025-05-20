.PHONY: reset all install update test pre-commit-setup commit tox


# 🔥 Default: Install or update dependencies, setup pre-commit, and run tests
all: install pre-commit-setup test

# 🚀 Install Poetry Environment (if not already installed)
install:
	pip install poetry  # Ensure Poetry is installed
	poetry install # Install dependencies using lock file (or create one if missing)

# 🔄 Update dependencies (Poetry) without wiping everything
update:
	@echo "🔄 Updating dependencies..."
	pip install --upgrade poetry  # Upgrade Poetry
	poetry update  # Update dependencies and lock file + reinstall
	poetry install --only-root  # Reinstall root
	@echo "✅ Dependencies updated!"

# ✅ Run Tests (Supports -html flag for Coverage Report)
test:
	@echo "🔬 Running tests..."
	poetry run pytest --cov=src --cov-report=term-missing; \

lint:
	poetry run ruff check .
	poetry run ruff format . 

type:
	poetry run pyright 

# Add command that runs tox to test multiple Python versions
tox:
	@echo "🔬 Running tests with Tox..."
	poetry run tox -p
	@echo "✅ Tox tests completed!"

# ⚡ Install & Update Pre-commit Hooks
pre-commit-setup:
	poetry run pre-commit autoupdate
	poetry run pre-commit install

# 🏗️ Commit & Push with Pre-commit Check
commit:
	- poetry run pre-commit run --all-files
	git add .
	@if [ -z "$(m)" ]; then \
		read -p "Commit message: " msg; \
	else \
		msg="$(m)"; \
	fi; \
	git commit -m "$$msg"; \
	git push


# 🔄 Reset Everything: Remove all generated files, delete Conda environment, and reinstall from scratch
reset:
	@echo "🔥 Resetting everything..."
	rm -rf poetry.lock .venv
	# Remove the current environment
	poetry env remove $(which python)
	@echo "🔥 Removing Poetry environment..."
	poetry env remove --all
	@echo "✅ Environment fully wiped! Reinstalling everything..."
	$(MAKE) all
