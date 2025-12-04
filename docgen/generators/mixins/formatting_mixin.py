"""
Formatting Mixin
Provides common formatting methods for generators
"""


class FormattingMixin:
    """フォーマッティング用のmixin"""

    LANGUAGE_DISPLAY_NAMES = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "ruby": "Ruby",
        "php": "PHP",
        "shell": "Shell",
        "bash": "Bash",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "csharp": "C#",
    }

    def _format_languages(self) -> str:
        """
        言語リストをフォーマット

        Returns:
            フォーマットされた言語リスト
        """
        if not hasattr(self, "languages"):
            return "- Not detected"

        parts = []
        for lang in self.languages:
            display_name = self.LANGUAGE_DISPLAY_NAMES.get(lang, lang.capitalize())
            parts.append(f"- {display_name}")
        return "\n".join(parts) if parts else "- Not detected"

    def _format_commands(self, commands: list[str] | None) -> str:
        """
        コマンドリストをフォーマット

        Args:
            commands: コマンドのリスト

        Returns:
            フォーマットされたコマンド
        """
        if not commands:
            return ""
        return "\n".join([f"```bash\n{cmd}\n```" for cmd in commands])

    def _format_project_structure(self, structure: dict | None) -> str:
        """
        プロジェクト構造をツリー形式でフォーマット

        Args:
            structure: プロジェクト構造の辞書

        Returns:
            フォーマットされたプロジェクト構造
        """
        if not structure:
            return ""

        lines = []
        self._format_structure_tree(structure, lines, prefix="", is_last=True)
        return "\n".join(lines)

    def _format_structure_tree(
        self, structure: dict | list, lines: list[str], prefix: str = "", is_last: bool = True
    ) -> None:
        """
        ツリー形式で構造を再帰的にフォーマット

        Args:
            structure: 構造の辞書またはリスト
            lines: 出力行のリスト
            prefix: 現在のインデントプレフィックス
            is_last: 最後の要素かどうか
        """
        if isinstance(structure, dict):
            items = list(structure.items())
            for idx, (key, value) in enumerate(items):
                is_last_item = idx == len(items) - 1
                connector = "└── " if is_last_item else "├── "

                # Clean up directory names (remove // suffix if present)
                clean_key = key.rstrip("/") if key.endswith("//") else key

                if isinstance(value, dict):
                    # ディレクトリ
                    lines.append(f"{prefix}{connector}{clean_key}/")
                    extension = "    " if is_last_item else "│   "
                    self._format_structure_tree(value, lines, prefix + extension, is_last_item)
                else:
                    # ファイル
                    lines.append(f"{prefix}{connector}{clean_key}")
        elif isinstance(structure, list):
            for idx, item in enumerate(structure):
                is_last_item = idx == len(structure) - 1
                connector = "└── " if is_last_item else "├── "
                # Clean up item names
                clean_item = item.rstrip("/") if item.endswith("//") else item
                lines.append(f"{prefix}{connector}{clean_item}")

    def _format_structure_recursive(
        self, structure: dict, lines: list[str], prefix: str = ""
    ) -> None:
        """
        再帰的にプロジェクト構造をフォーマット (後方互換性のため残す)

        Args:
            structure: 構造の辞書
            lines: 出力行のリスト
            prefix: インデントプレフィックス
        """
        if isinstance(structure, dict):
            for key, value in structure.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}/")
                    self._format_structure_recursive(value, lines, prefix + "  ")
                else:
                    lines.append(f"{prefix}{key}")
        elif isinstance(structure, list):
            for item in structure:
                lines.append(f"{prefix}{item}")
