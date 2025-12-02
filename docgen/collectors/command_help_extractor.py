"""
Command help text extractor utility
Extracts help text and descriptions from Python CLI entry points
"""

import importlib
from pathlib import Path
import sys
from typing import Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


class CommandHelpExtractor:
    """Extract help text from Python CLI entry points"""

    @staticmethod
    def extract_from_entry_point(entry_point: str, project_root: Path | None = None) -> str:
        """
        Extract description from a Python entry point

        Args:
            entry_point: Entry point string in format "module.path:function"
            project_root: Project root directory to add to sys.path

        Returns:
            Description string, or empty string if extraction fails
        """
        try:
            # Parse entry point format: "module.path:function"
            if ":" not in entry_point:
                logger.debug(f"Invalid entry point format: {entry_point}")
                return ""

            module_path, _ = entry_point.split(":", 1)

            # Add project root to sys.path if provided
            original_path = sys.path.copy()
            if project_root:
                sys.path.insert(0, str(project_root))

            try:
                # Import the module
                module = importlib.import_module(module_path)

                # Try to find argparse parser in the module
                description = CommandHelpExtractor._extract_argparse_description(module)

                return description

            finally:
                # Restore original sys.path
                sys.path = original_path

        except Exception as e:
            logger.debug(f"Failed to extract description from {entry_point}: {e}")
            return ""

    @staticmethod
    def _extract_argparse_description(module: Any) -> str:
        """
        Extract description from argparse parser in a module

        Args:
            module: Imported module to search for argparse parser

        Returns:
            Parser description or empty string
        """
        try:
            # Look for common patterns in the module
            # 1. Check if module has a CommandLineInterface class with a run method
            if hasattr(module, "CommandLineInterface"):
                cli_class = module.CommandLineInterface
                if hasattr(cli_class, "run"):
                    # Try to extract from the run method source
                    import inspect

                    source = inspect.getsource(cli_class.run)

                    # Look for argparse.ArgumentParser(description="...")
                    import re

                    match = re.search(
                        r'argparse\.ArgumentParser\s*\([^)]*description\s*=\s*["\']([^"\']+)["\']',
                        source,
                    )
                    if match:
                        return match.group(1)

            # 2. Check for main() function
            if hasattr(module, "main"):
                import inspect

                source = inspect.getsource(module.main)

                import re

                match = re.search(
                    r'argparse\.ArgumentParser\s*\([^)]*description\s*=\s*["\']([^"\']+)["\']',
                    source,
                )
                if match:
                    return match.group(1)

            return ""

        except Exception as e:
            logger.debug(f"Failed to extract argparse description: {e}")
            return ""

    @staticmethod
    def extract_options_from_entry_point(
        entry_point: str, project_root: Path | None = None
    ) -> list[dict[str, str]]:
        """
        Extract command options from a Python entry point

        Args:
            entry_point: Entry point string in format "module.path:function"
            project_root: Project root directory to add to sys.path

        Returns:
            List of option dicts with 'name' and 'help' keys
        """
        try:
            # Parse entry point format: "module.path:function"
            if ":" not in entry_point:
                logger.debug(f"Invalid entry point format: {entry_point}")
                return []

            module_path, _ = entry_point.split(":", 1)

            # Add project root to sys.path if provided
            original_path = sys.path.copy()
            if project_root:
                sys.path.insert(0, str(project_root))

            try:
                # Import the module
                module = importlib.import_module(module_path)

                # Try to find argparse options in the module
                options = CommandHelpExtractor._extract_argparse_options(module)

                return options

            finally:
                # Restore original sys.path
                sys.path = original_path

        except Exception as e:
            logger.debug(f"Failed to extract options from {entry_point}: {e}")
            return []

    @staticmethod
    def _extract_argparse_options(module: Any) -> list[dict[str, str]]:
        """
        Extract options from argparse parser in a module

        Args:
            module: Imported module to search for argparse parser

        Returns:
            List of option dicts with 'name' and 'help' keys
        """
        try:
            options = []

            # Look for common patterns in the module
            # 1. Check if module has a CommandLineInterface class with a run method
            if hasattr(module, "CommandLineInterface"):
                cli_class = module.CommandLineInterface
                if hasattr(cli_class, "run"):
                    # Try to extract from the run method source
                    import inspect

                    source = inspect.getsource(cli_class.run)

                    # Look for parser.add_argument(...) calls
                    import re

                    # Pattern to match: parser.add_argument("--option", ..., help="description", ...)
                    # or parser.add_argument("option", ..., help="description", ...)
                    pattern = r'parser\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                    matches = re.findall(pattern, source)

                    for option_name, help_text in matches:
                        # Skip version action as it's auto-handled
                        if "version" in option_name:
                            continue
                        options.append({"name": option_name, "help": help_text})

            # 2. Check for main() function
            if not options and hasattr(module, "main"):
                import inspect

                source = inspect.getsource(module.main)

                import re

                pattern = r'parser\.add_argument\(\s*["\']([^"\']+)["\'][^)]*help\s*=\s*["\']([^"\']+)["\']'
                matches = re.findall(pattern, source)

                for option_name, help_text in matches:
                    if "version" in option_name:
                        continue
                    options.append({"name": option_name, "help": help_text})

            return options

        except Exception as e:
            logger.debug(f"Failed to extract argparse options: {e}")
            return []
