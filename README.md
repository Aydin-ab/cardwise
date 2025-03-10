TODO:

Docs
✅ README.md – Clear instructions for installation, usage, and contributing.
✅ CONTRIBUTING.md – Guidelines for contributing to the project.
✅ CODE_OF_CONDUCT.md – Encourages a respectful and inclusive community.
✅ Docstrings – Improve inline documentation for functions and modules.

📌 If the project grows, consider Sphinx or MkDocs for auto-generated documentation.


Security
✅ Secrets Scanning – Use trufflehog or GitHub's secret scanning to detect leaked credentials.

🚀 5. Performance Profiling
✅ cProfile & py-spy – Analyze bottlenecks in execution time.
✅ pytest-benchmark – Measures performance regressions in tests.

📌 Helps identify slow code and optimize critical paths.

📊 6. Logging & Error Handling
✅ Structured Logging – Use logging instead of print().
✅ Sentry – Capture errors in production.
Example :
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

logger.info("App started successfully")


📡 7. Deployment & Packaging
✅ Docker – Create a Dockerfile to package the app.
✅ PyPI Package – If it’s a library, publish it to PyPI.
✅ GitHub Releases – Automate versioning with GitHub Actions & semantic versioning.
example dockerfile:
FROM python:3.10

WORKDIR /app
COPY . /app
RUN pip install -e .

CMD ["python", "-m", "bank_parser.search_offers"]


🛠 8. CI/CD Enhancements
✅ GitHub Actions Matrix Testing – Run tests on multiple Python versions.
✅ Automatic Versioning – Use bump2version or semantic-release.
✅ GitHub Action for Releases – Auto-generate release notes.

Example matrix
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]

    steps:
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run Tests
        run: pytest --cov=src


DOC

For tox make sure to properly install pyenv (see the shell section) and install all pythons you wanna test
https://github.com/pyenv/pyenv?tab=readme-ov-file#installation
Run tox in parallel with `tox -p`
