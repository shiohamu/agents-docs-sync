"""Common utilities for collecting project information."""

import json
from pathlib import Path
from typing import Any

from ..utils.file_utils import safe_read_file


class ConfigReader:
    """Common utilities for reading various configuration files."""

    @staticmethod
    def read_json_file(file_path: Path) -> dict[str, Any] | None:
        """Read and parse JSON file."""
        content = safe_read_file(file_path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def read_package_json(project_root: Path) -> dict[str, Any] | None:
        """Read package.json file."""
        return ConfigReader.read_json_file(project_root / "package.json")

    @staticmethod
    def read_pyproject_toml(project_root: Path) -> dict[str, Any] | None:
        """Read pyproject.toml file."""
        try:
            import tomllib
        except ImportError:
            return None

        file_path = project_root / "pyproject.toml"
        try:
            with open(file_path, "rb") as f:
                return tomllib.load(f)
        except (OSError, ValueError):
            return None

    @staticmethod
    def read_makefile(project_root: Path) -> str | None:
        """Read Makefile content."""
        makefile_paths = ["Makefile", "makefile"]
        for makefile in makefile_paths:
            content = safe_read_file(project_root / makefile)
            if content:
                return content
        return None

    @staticmethod
    def extract_scripts_from_package_json(package_data: dict[str, Any]) -> list[str]:
        """Extract scripts from package.json."""
        scripts = package_data.get("scripts", {})
        return list(scripts.keys())

    @staticmethod
    def extract_dependencies_from_package_json(
        package_data: dict[str, Any],
    ) -> dict[str, list[str]]:
        """Extract dependencies from package.json."""
        deps = {}

        # Regular dependencies
        if "dependencies" in package_data:
            deps["npm"] = list(package_data["dependencies"].keys())

        # Dev dependencies
        if "devDependencies" in package_data:
            deps.setdefault("npm-dev", []).extend(package_data["devDependencies"].keys())

        return deps

    @staticmethod
    def parse_makefile_targets(content: str) -> list[str]:
        """Parse Makefile targets."""
        targets = []
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("\t") and not line.startswith("#") and ":" in line:
                target = line.split(":")[0].strip()
                if target and not target.startswith("."):
                    targets.append(target)
        return targets

    @staticmethod
    def detect_language_from_config(project_root: Path) -> str | None:
        """Detect programming language from configuration files."""
        # Python
        if (project_root / "pyproject.toml").exists() or (project_root / "setup.py").exists():
            return "python"

        # JavaScript/TypeScript
        package_json = ConfigReader.read_package_json(project_root)
        if package_json:
            return "javascript"  # Could be refined to detect TypeScript

        # Go
        if (project_root / "go.mod").exists():
            return "go"

        # Rust
        if (project_root / "Cargo.toml").exists():
            return "rust"

        return None
