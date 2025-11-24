"""Common file detection patterns for language detectors."""

from pathlib import Path


class DetectorPatterns:
    """Common file detection patterns used by language detectors."""

    # Package manager detection patterns: list of (file_patterns, manager_name)
    # file_patterns can be str or tuple of str (all must exist)
    # Order matters - more specific/priority files first
    PACKAGE_MANAGER_PATTERNS = {
        "python": [
            ("uv.lock", "uv"),
            ("poetry.lock", "poetry"),
            # pyproject.toml handled separately due to content check
            ("Pipfile.lock", "pipenv"),
            ("environment.yml", "conda"),
            ("conda-environment.yml", "conda"),
            ("requirements.txt", "pip"),
            ("setup.py", "pip"),
        ],
        "javascript": [
            ("pnpm-lock.yaml", "pnpm"),
            ("yarn.lock", "yarn"),
            ("package-lock.json", "npm"),
            ("bun.lockb", "bun"),
            ("package.json", "npm"),  # fallback
        ],
        "go": [
            ("go.mod", "go"),
            (("Gopkg.toml", "Gopkg.lock"), "dep"),
            (("glide.yaml", "glide.lock"), "glide"),
        ],
    }

    # Package manager files by language
    PACKAGE_FILES = {
        "python": [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "Pipfile.lock",
            "poetry.lock",
            "environment.yml",
            "conda-environment.yml",
            "uv.lock",
        ],
        "javascript": [
            "package.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "package-lock.json",
            "bun.lockb",
        ],
        "typescript": [
            "tsconfig.json",
            "package.json",  # TypeScript projects usually have package.json too
        ],
        "go": [
            "go.mod",
            "go.sum",
            "glide.yaml",
            "glide.lock",
            "Gopkg.toml",
            "Gopkg.lock",
        ],
        "rust": [
            "Cargo.toml",
            "Cargo.lock",
        ],
        "java": [
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
        ],
        "csharp": [
            "*.csproj",
            "*.sln",
        ],
        "cpp": [
            "CMakeLists.txt",
            "Makefile",
            "configure.ac",
            "configure.in",
        ],
    }

    # Source file extensions by language
    SOURCE_EXTENSIONS = {
        "python": [".py", ".pyx", ".pyw"],
        "javascript": [".js", ".jsx", ".mjs", ".cjs"],
        "typescript": [".ts", ".tsx", ".d.ts"],
        "go": [".go"],
        "rust": [".rs"],
        "java": [".java"],
        "csharp": [".cs"],
        "cpp": [".cpp", ".cc", ".cxx", ".c++", ".hpp", ".hxx", ".h"],
        "c": [".c", ".h"],
        "ruby": [".rb"],
        "php": [".php"],
        "swift": [".swift"],
        "kotlin": [".kt"],
        "scala": [".scala"],
        "dart": [".dart"],
    }

    # Common directories to exclude
    EXCLUDE_DIRS = {
        ".venv",
        ".git",
        "__pycache__",
        "node_modules",
        "htmlcov",
        "coverage",
        ".coverage",
        "site-packages",
        "dist",
        "build",
        ".next",
        ".nuxt",
        "target",  # Rust
        "bin",
        "obj",  # .NET
        ".gradle",
        ".idea",
        ".vscode",
        ".DS_Store",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
    }

    @classmethod
    def get_package_files(cls, language: str) -> list[str]:
        """Get package manager files for a language."""
        return cls.PACKAGE_FILES.get(language, [])

    @classmethod
    def get_source_extensions(cls, language: str) -> list[str]:
        """Get source file extensions for a language."""
        return cls.SOURCE_EXTENSIONS.get(language, [])

    @classmethod
    def detect_by_package_files(cls, project_root: Path, language: str) -> bool:
        """Detect language by checking for package manager files."""
        package_files = cls.get_package_files(language)
        return any((project_root / file).exists() for file in package_files)

    @classmethod
    def detect_by_source_files(cls, project_root: Path, language: str) -> bool:
        """Detect language by checking for source files."""
        extensions = cls.get_source_extensions(language)
        for ext in extensions:
            try:
                for _ in project_root.rglob(f"*{ext}"):
                    return True
            except (OSError, PermissionError):
                continue
        return False

    @classmethod
    def is_excluded_path(cls, path: Path, project_root: Path) -> bool:
        """Check if a path should be excluded from detection."""
        try:
            relative_path = path.relative_to(project_root)
            return any(part in cls.EXCLUDE_DIRS for part in relative_path.parts)
        except ValueError:
            # Path is outside project root
            return True

    @classmethod
    def detect_package_manager(cls, language: str, file_exists_func) -> str | None:
        """Detect package manager for a language using file existence checks.

        Args:
            language: Language name
            file_exists_func: Function that takes file patterns (str or tuple) and returns bool

        Returns:
            Package manager name or None
        """
        patterns = cls.PACKAGE_MANAGER_PATTERNS.get(language, [])
        for file_patterns, manager in patterns:
            if isinstance(file_patterns, tuple):
                if file_exists_func(*file_patterns):
                    return manager
            else:
                if file_exists_func(file_patterns):
                    return manager
        return None
