.PHONY: all requirements prod dev conda_env generate_conda update_conda create_conda clean

# Default behavior: clean first, then generate everything
all: clean requirements conda_env

# Ensure pip-tools is installed before running pip-compile
requirements: prod dev

prod:
	@pip show pip-tools > /dev/null || pip install pip-tools
	pip-compile --output-file=requirements.txt

dev:
	@pip show pip-tools > /dev/null || pip install pip-tools
	pip-compile --extra dev --output-file=requirements-dev.txt

conda_env: generate_conda check_conda

generate_conda:
	python generate_conda_env.py

check_conda:
	@if conda info --envs | grep -q "^cardwise "; then \
		echo "✅ Conda environment 'cardwise' exists. Updating..."; \
		$(MAKE) update_conda; \
	else \
		echo "🚀 Conda environment not found. Creating it..."; \
		$(MAKE) create_conda; \
	fi

update_conda:
	@echo "🔄 Updating Conda environment 'cardwise'..."
	conda env update --file conda_env.yaml --prune
	@echo "✅ Conda environment updated!"

create_conda:
	@echo "🚀 Creating Conda environment 'cardwise'..."
	conda env create --file conda_env.yaml
	@echo "✅ Conda environment created!"
	@echo "⚠️ Run 'conda activate cardwise' to use it."

clean:
	rm -f requirements.txt requirements-dev.txt conda_env.yaml

test:
	pytest --cov=src --cov-report=term-missing

coverage-html:
	pytest --cov=src --cov-report=html && open htmlcov/index.html


# Install pre-commit hooks (if not installed already)
pre-commit-install:
	pre-commit install

# Update pre-commit hooks when `.pre-commit-config.yaml` changes
pre-commit-update:
	pre-commit autoupdate
	pre-commit install

# Run all pre-commit hooks manually
pre-commit-run:
	pre-commit run --all-files


# Commit and push changes with a message
commit:
	git add .
	git commit -m "$(m)"
	git push

