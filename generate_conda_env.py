import subprocess
from typing import Any, Dict, List

import toml


def is_available_in_conda(package: str) -> bool:
    """Check if a package is available in Conda."""
    try:
        result = subprocess.run(
            ["conda", "search", package], capture_output=True, text=True, check=False
        )
        return package in result.stdout  # If package name appears in Conda output
    except Exception:
        return False  # Fail-safe: Assume package is not available


# Load dependencies from pyproject.toml
with open("pyproject.toml", "r", encoding="utf-8") as f:
    print("📖 Reading `pyproject.toml`...   ")
    pyproject: Dict[str, Any] = toml.load(f)

dependencies: List[str] = pyproject["project"]["dependencies"]
dev_dependencies: List[str] = pyproject["project"]["optional-dependencies"].get("dev", [])

# Separate Conda vs Pip dependencies
conda_deps: List[str] = ["python=3.10", "pip"]  # Base dependencies
pip_deps: List[str] = []

for dep in dependencies:
    package_name: str = dep.split(" ")[0]  # Remove version constraints (e.g., beautifulsoup4>=4.9)
    if is_available_in_conda(package_name):
        conda_deps.append(package_name)
    else:
        pip_deps.append(dep)

# Add dev dependencies (always go in pip section)
pip_deps.extend(dev_dependencies)

# 🛠️ Fix: Use join() separately to avoid f-string issues
conda_deps_str: str = "\n  - ".join(conda_deps)
pip_deps_str: str = "\n      - ".join(pip_deps) if pip_deps else ""

# Generate Conda YAML content
conda_env: str = f"""
name: cardwise
channels:
  - conda-forge
  - defaults
dependencies:
  - {conda_deps_str}
"""

if pip_deps_str:
    conda_env += f"""
  - pip:
      - {pip_deps_str}
"""

# Write the updated conda_env.yaml
with open("conda_env.yaml", "w", encoding="utf-8") as f:
    f.write(conda_env.strip())

print("✅ `conda_env.yaml` created successfully!")
