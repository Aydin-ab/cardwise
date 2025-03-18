TODO:
DONE ✅ pip-tools – Locks dependencies (pip-compile) to ensure reproducibility.
DONE ✅ tox – Automates testing across multiple Python versions.
DONE ✅ conda-lock – If using Conda, generates lock files for deterministic environments.

Docs
✅ README.md – Clear instructions for installation, usage, and contributing.
✅ CONTRIBUTING.md – Guidelines for contributing to the project.
✅ CODE_OF_CONDUCT.md – Encourages a respectful and inclusive community.
✅ Docstrings – Improve inline documentation for functions and modules.

📌 If the project grows, consider Sphinx or MkDocs for auto-generated documentation.


Security
DONE ✅ bandit – Static security analysis to catch vulnerabilities in Python code.
DONE ✅ pip-audit – Checks for known vulnerabilities in dependencies.
DONE ✅ Secrets Scanning – Use gitleaks or trufflehog or GitHub's secret scanning to detect leaked credentials.


🚀 5. Performance Profiling
✅ cProfile & py-spy – Analyze bottlenecks in execution time.
✅ pytest-benchmark – Measures performance regressions in tests.

📌 Helps identify slow code and optimize critical paths.

📊 6. Logging & Error Handling
DONE ✅ Structured Logging – Use logging instead of print().
DONE ✅ Sentry – Capture errors in production.



📡 7. Deployment & Packaging
✅ Define a License
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
DONE ✅ GitHub Actions Matrix Testing – Run tests on multiple Python versions.
✅ Automatic Versioning – Use bump2version or semantic-release.
✅ GitHub Action for Releases – Auto-generate release notes.



DOC

For tox make sure to properly install pyenv (see the shell section) and install all pythons you wanna test
https://github.com/pyenv/pyenv?tab=readme-ov-file#installation
Run tox in parallel with `tox -p`



