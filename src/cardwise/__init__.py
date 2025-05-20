from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cardwise")  # Must match name in pyproject.toml
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback during local dev or tests
