# 🧩 Contributing to Cardwise

Welcome, and thank you for considering contributing to **Cardwise**!  
We appreciate all contributions — from bug reports and suggestions to code, tests, and documentation.

---

## ⚙️ Getting Started

1. **Clone the repository**:

```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
```

2. **Install dependencies, set up pre-commit, and run tests**:

```bash
   make
```

This will install a Poetry virtual environment, setup pre-commit hooks, and verify the codebase is working.

---

## 🔨 Improving the App

### ➕ Adding a New Bank Parser

If you'd like to support a new bank, follow these steps:

1. Add a parser in `ingestion/parsers/{new_bank}.py`
2. Write tests in `tests/ingestion/test_{new_bank}.py`
3. Upload the corresponding HTML file to the GCS bucket at:
   `{bucket_name}/data/bank_htmls/{new_bank}.html`

Use the `normalize_string()` utility to derive the correct filename from the bank name:

```py3
# cardwise/domain/utils.py

def normalize_string(s: str) -> str:
    s_ = "".join([c.lower() for c in s if c.isalnum() or c == " "])
    return s_.strip().replace(" ", "_")
```

Examples:

* "Bank of America" → `bank_of_america`
* "Chase" → `chase`
* "Capital One" → `capital_one`

> This lets us dynamically match parsers and HTML files without hardcoding logic.

---

### 📌 TODO: Automate Offer Retrieval

We would love to **automate fetching HTML offers** from banks.
Attempts using Selenium and Puppeteer have failed due to strict security from the banks. API access is also not available (need an expensive business license).

If you have ideas for overcoming this, [open a discussion](https://github.com/aydin-ab/cardwise/discussions) or submit a proposal!

---

## 🧪 Running Tests

We use:
* [`pytest`](https://docs.pytest.org/) for test execution
* [`pytest-cov`](https://pytest-cov.readthedocs.io/) for code coverage

Run tests:

```bash
make test
```

✅ Write meaningful tests for all features and bug fixes.

---

## 🧹 Linting & Formatting

We use [`ruff`](https://docs.astral.sh/ruff/) for:
* Code linting
* Auto-formatting (like Black)
* Import sorting (like isort)
* Basic security checks (like Bandit)

Run all formatting checks:

```bash
make lint
```

---

## 🧠 Type Checking

We use [`pyright`](https://github.com/microsoft/pyright) in `strict` mode.

Run type checks:

```bash
make type
```

---

## 🧪 Tox for Multi-Python Support

We test against Python 3.10–3.13 using [`tox`](https://tox.readthedocs.io/).

To run:

```bash
make tox
```

> ✅ Note: The full suite runs only on 3.10 by default for speed.
> 🛠️ Make sure required versions are installed via `pyenv`.

---

## ✅ Commit Messages

We follow [**Conventional Commits**](https://www.conventionalcommits.org/):

* `feat`: new feature
* `fix`: bug fix
* `docs`: docs only
* `test`: add or update tests
* `chore`: cleanup/config updates
* `build`: dependency or build changes
* `ci`: GitHub Actions or CI pipeline changes
* `perf`: performance improvements
* `refactor`: code cleanup with no behavior change
* `style`: whitespace, formatting, etc.
* `revert`: revert previous commit

For breaking changes:

```bash
feat!: change signature of OfferParser interface
```

Or add `BREAKING CHANGE:` in the commit body.

---

## 🔄 Pre-commit Hooks

We use [**pre-commit**](https://pre-commit.com/) to catch issues before you commit.

Install hooks:

```bash
make pre-commit-setup
```

Hooks run automatically on `git commit`.

---

## 🚀 Making a Pull Request

1. **Fork** the repo

2. **Create a branch**:

```bash
   git checkout -b feat/add-citi-parser
```

3. **Make your changes**

4. **Run tests & linters**

5. **Open a pull request**

I’ll review it as soon as possible!

---

Thanks for helping make **Cardwise** better 💜
Feel free to [open issues](https://github.com/aydin-ab/cardwise/issues) or [start discussions](https://github.com/aydin-ab/cardwise/discussions) if you have ideas or questions.