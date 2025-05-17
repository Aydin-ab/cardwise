# Contributing to Cardwise

Welcome, and thank you for considering contributing to **Cardwise**!  
We appreciate all kinds of contributions — from bug reports and suggestions to code and documentation improvements.

---

## 🛠️ Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
    ```
    
2. **Run make** to install dependencies on a poetry virtual env, install pre-commit, and run the tests:
   ```bash
   make
   ```

Or you can do it manually:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
    ```

2. **Install dependencies** with [Poetry](https://python-poetry.org/docs/#installation):

   ```bash
   poetry install
   ```

3. **Run the app (optional)**:

    You can test the app with:
    ```bash
    poetry run search_offers -h
    ```

    You can run a dev docker container via Docker:

   ```bash
   docker compose up dev
   ```

   You also have a `.devcontainer/` snippet folder if you prefer using dev containers

   Remember to populate `htmls/` with your own data if you want to use the default parameters of `search_offers`

---

## 🧪 Running Tests

We use [pytest](https://docs.pytest.org/en/stable/getting-started.html) for testing and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/readme.html) for coverage reports.

Run tests locally:
Using make:
```bash
make test
```
Or using Poetry:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Or using Docker:

```bash
docker compose up test
```

Or using Tox (Python 3.10 only):
```bash
poetry run tox -e py310
```

Code coverage is collected via pytest-cov. Please write meaningful tests for new features and bug fixes.


---

## ✅ **Linting & Formatting with Ruff**

We use [Ruff](https://docs.astral.sh/ruff/installation/) for:

* **Linting**
* **Code formatting** (~Black)
* **Import sorting** (~isort)
* **Security checks** (~Bandit rules)

Run checks with make:

```bash
make lint
```

Run checks manually:

```bash
poetry run ruff check .       # lint
poetry run ruff format .      # auto-format
```

Or via Tox:

```bash
poetry run tox -e lint
```

---

## 🔍 **Static Type Checking with Pyright**

We use [Pyright](https://github.com/microsoft/pyright) with `strict` mode enabled to catch type issues early.

Run type checking with make:
```bash
make type
```

Or Run type checking manually:

```bash
poetry run pyright
```

Or via Tox:

```bash
poetry run tox -e type
```

---

## 🧪 **Multi-Python Compatibility with Tox**

To ensure compatibility across Python 3.9–3.13, we use [Tox](https://tox.readthedocs.io/) to verify our code builds against multiple Python versions.

Run tox with make:
```bash
make tox
```

Or run tox manually:

```bash
poetry run tox                  # run all environments
poetry run tox -p               # run in parallel
poetry run tox -e py310         # run tests with Python 3.10
```

> Note: Full test suite runs only on Python 3.10 to save time.
> Note: Tox is configured to use `pyenv` for Python versions. Ensure you have the required versions installed.

---

## 📝 Commit Messages

Please use [Conventional Commits](https://www.conventionalcommits.org/) with one of the following types:

* `feat`: new feature
* `fix`: bug fix
* `docs`: documentation change
* `test`: adding or updating tests
* `chore`: maintenance tasks (e.g. formatting, configs)
* `build`: changes that affect the build system or external dependencies
* `ci`: changes to CI configuration files and scripts
* `perf`: performance improvements
* `refactor`: code changes that neither fix a bug nor add a feature
* `style`: formatting, missing semi-colons, etc; no code change
* `revert`: revert a previous commit
* `BREAKING CHANGE`: a commit that introduces breaking changes (place this at the end of the commit message body)
    * (or) `!`: a commit that introduces breaking changes (place this at the end of the commit message header)

---

#### 🔄 **Pre-commit Hooks**

Cardwise supports [**pre-commit**](https://pre-commit.com/) to catch linting and formatting issues before you commit.

To install the hook:

```bash
make pre-commit-setup
```

Or run it manually:

```bash
poetry run pre-commit autoupdate
poetry run pre-commit install
```

Then it runs automatically on each commit. You can also run it manually:

```bash
poetry run pre-commit run --all-files
```

---


## 🚀 Making a PR

1. Fork the repo
2. Create a feature branch:

   ```bash
   git checkout -b feat/my-new-feature
   ```
3. Make your changes
4. Run tests and format your code
5. Open a pull request!

---

Thanks for helping make Cardwise better 💜
