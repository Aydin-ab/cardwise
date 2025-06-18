.PHONY: all install update test lint type tox pre-commit-setup commit reset dev dockerhub-push flutter backend ingestion

# 🧪 ========== DEFAULT ==========
all: install pre-commit-setup test

# 📦 ========== DEPENDENCIES ==========
install:
	@echo "📦 Installing dependencies..."
	pip install poetry
	poetry install

update:
	@echo "🔄 Updating dependencies..."
	pip install --upgrade poetry
	poetry update
	poetry install --only-root
	@echo "✅ Dependencies updated!"

reset:
	@echo "🔥 Resetting everything..."
	rm -rf poetry.lock .venv
	poetry env remove --all || true
	@echo "✅ Environment reset complete!"
	$(MAKE) all

# ✅ ========== TESTING & QUALITY ==========
test:
	@echo "🧪 Running tests..."
	poetry run pytest --cov=src --cov-report=term-missing

lint:
	@echo "🧹 Running linter..."
	poetry run ruff check .
	poetry run ruff format .

type:
	@echo "🔍 Running type checks..."
	poetry run pyright

tox:
	@echo "🔬 Running multi-version tests with Tox..."
	poetry run tox -p
	@echo "✅ Tox complete!"

# 🔐 ========== GIT & PRE-COMMIT ==========
pre-commit-setup:
	@echo "🔐 Setting up pre-commit hooks..."
	poetry run pre-commit autoupdate
	poetry run pre-commit install

commit:
	@echo "📤 Committing with pre-commit checks..."
	- poetry run pre-commit run --all-files
	git add .
	@if [ -z "$(m)" ]; then \
		read -p "Commit message: " msg; \
	else \
		msg="$(m)"; \
	fi; \
	git commit -m "$$msg"; \
	git push

# 🐳 ========== DOCKER ==========
DOCKERHUB_USERNAME := aydinabiar
TAG := latest
PLATFORM_AMD64 ?= false  # Set to true to add --platform=linux/amd64

dockerhub-push:
	@echo "🐳 Building Docker image..."
	@if [ "$(PLATFORM_AMD64)" = "true" ]; then \
		echo "🔧 Using platform linux/amd64"; \
		docker build --platform=linux/amd64 -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) .; \
	else \
		docker build -f $(DOCKERFILE) -t $(IMAGE_NAME):$(TAG) .; \
	fi
	@echo "🏷️  Tagging image as $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)..."
	docker tag $(IMAGE_NAME):$(TAG) $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)
	@echo "📤 Pushing image to Docker Hub..."
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)
	@echo "✅ Pushed $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG) successfully!"

dev:
	@echo "🧰 Starting dev containers and attaching to CLI..."
	docker compose up -d --build
	docker compose exec cli bash

# 📱 ========== FLUTTER ==========
flutter:
	@echo "🚀 Launching Flutter app..."
	cd frontend/mobile_app && flutter run -d emulator-5554

# 🐍 ========== BACKEND ==========
PORT ?= 10000
backend:
	@echo "🚀 Starting FastAPI backend on http://localhost:$(PORT) ..."
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port $(PORT) --reload

# 🐍 ========== Ingestion ==========
ingestion:
	@echo "🚀 Running ingestion script"
	poetry run python ingestion/main.py