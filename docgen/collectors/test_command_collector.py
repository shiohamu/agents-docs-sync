"""
Test command collector module
Collects test commands from various configuration files.
"""

from pathlib import Path

from ..utils.file_utils import safe_read_file, safe_read_json
from ..utils.logger import setup_logger
from .collector_utils import BuildCommandCollector


class TestCommandCollector:
    """Test command collector class"""

    SCRIPTS_DIR = "scripts"
    RUN_TESTS_SCRIPT = "run_tests.sh"
    MAKEFILE_NAMES = ["Makefile", "makefile"]
    PYTEST_INI = "pytest.ini"
    PACKAGE_JSON = "package.json"

    def __init__(self, project_root: Path, package_managers: dict[str, str] | None = None):
        """
        Initialize

        Args:
            project_root: Project root directory
            package_managers: Dictionary of detected package managers
        """
        self.project_root = project_root
        self.package_managers = package_managers or {}
        self.logger = setup_logger(__name__)
        self.build_collector = BuildCommandCollector(project_root, package_managers)

    def collect_test_commands(self) -> list[str]:
        """
        Collect test commands

        Returns:
            List of test commands
        """
        commands = []

        # Collect from scripts/run_tests.sh
        test_script = self.project_root / self.SCRIPTS_DIR / self.RUN_TESTS_SCRIPT
        content = safe_read_file(test_script)
        if content:
            for line in content.split("\n"):
                if "pytest" in line or "test" in line.lower():
                    # Extract command line
                    command = line.strip()
                    if command:
                        command = self.build_collector._add_uv_run_if_needed(command)
                    commands.append(command)

        # Collect from Makefile
        makefile = self.project_root / self.MAKEFILE_NAMES[0]
        if makefile.exists():
            content = makefile.read_text(encoding="utf-8")
            # Extract command line for test target
            in_test_target = False
            for line in content.split("\n"):
                if line.strip() == "test:":
                    in_test_target = True
                elif line.strip().endswith(":") and in_test_target:
                    break  # Next target
                elif in_test_target and line.startswith("\t") and line.strip():
                    command = line.lstrip("\t")
                    if command and not command.startswith("@"):
                        command = self.build_collector._add_uv_run_if_needed(command)
                        commands.append(command)

        # For Python projects
        if "python" in self.package_managers:
            pm = self.package_managers["python"]
            if pm == "uv":
                commands.append("uv run pytest tests/ -v --tb=short")
            elif pm == "poetry":
                commands.append("poetry run pytest tests/ -v --tb=short")
            else:  # pip
                commands.append("pytest tests/ -v --tb=short")
        # Collect from pytest.ini (if package manager is not specified)
        elif (self.project_root / self.PYTEST_INI).exists():
            command = "pytest tests/ -v --tb=short"
            command = self.build_collector._add_uv_run_if_needed(command)
            commands.append(command)

        # Collect from package.json
        package_data = safe_read_json(self.project_root / self.PACKAGE_JSON)
        if package_data and "scripts" in package_data and "test" in package_data["scripts"]:
            pm = self.package_managers.get("javascript", "npm")
            if pm == "pnpm":
                commands.append("pnpm test")
            elif pm == "yarn":
                commands.append("yarn test")
            else:  # npm
                commands.append("npm test")

        # For Go projects
        if "go" in self.package_managers:
            pm = self.package_managers["go"]
            if pm == "go":
                commands.append("go test ./...")

        # Deduplicate preserving order
        seen = set()
        unique_commands = []
        for c in commands:
            if c not in seen:
                unique_commands.append(c)
                seen.add(c)
        return unique_commands
