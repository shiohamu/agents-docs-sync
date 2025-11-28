"""
テンプレート処理 Mixin

Jinja2テンプレートのレンダリングやコマンドのフォーマット機能を提供します。
"""

from typing import Any


class TemplateMixin:
    """テンプレート処理機能を提供する Mixin"""

    def _format_commands(self, commands: list[str]) -> str:
        """
        コマンドリストをマークダウンのコードブロックとしてフォーマット

        Args:
            commands: コマンドのリスト

        Returns:
            フォーマットされたマークダウン文字列
        """
        if not commands:
            return ""
        parts = ["```bash"]
        for cmd in commands[:5]:  # 最大5個
            parts.append(cmd)
        if len(commands) > 5:
            parts.append("# ... その他のコマンド")
        parts.append("```")
        return "\n".join(parts)

    def _generate_custom_instructions_section(
        self, custom_instructions: str | dict[str, Any]
    ) -> list[str]:
        """
        カスタム指示セクションを生成

        Args:
            custom_instructions: カスタム指示の内容（文字列または辞書）

        Returns:
            生成された行のリスト
        """
        lines = []
        lines.append("## プロジェクト固有の指示")
        lines.append("")

        if isinstance(custom_instructions, str):
            lines.append(custom_instructions)
        elif isinstance(custom_instructions, dict):
            # dictの場合はキーをセクションとして扱う
            for key, value in custom_instructions.items():
                lines.append(f"### {key}")
                lines.append("")
                lines.append(str(value))
                lines.append("")

        lines.append("")
        return lines

    def _render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """
        Jinja2テンプレートをレンダリング

        Args:
            template_name: テンプレートファイル名
            context: テンプレート変数

        Returns:
            レンダリングされた文字列
        """
        from pathlib import Path

        from jinja2 import Environment, FileSystemLoader

        # テンプレートディレクトリのパスを解決
        # docgen/generators/mixins/template_mixin.py -> docgen/templates
        current_dir = Path(__file__).parent
        template_dir = current_dir.parent.parent / "templates"

        if not template_dir.exists():
            # パッケージとしてインストールされている場合のフォールバック
            import docgen

            template_dir = Path(docgen.__file__).parent / "templates"

        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template(template_name)
        return template.render(context)

    def _format_project_structure(self, structure: dict[str, Any] | None) -> str:
        """
        プロジェクト構造をツリー形式で整形

        Args:
            structure: プロジェクト構造の辞書

        Returns:
            整形された文字列
        """
        if not structure:
            return ""

        def format_node(data, prefix="", is_last=True):
            """ノードを再帰的にツリー形式でフォーマット"""
            lines = []

            if isinstance(data, dict):
                items = list(data.items())
                for i, (key, value) in enumerate(items):
                    is_last_item = i == len(items) - 1
                    connector = "└─ " if is_last_item else "├─ "

                    if value == "file" or value == "directory":
                        lines.append(f"{prefix}{connector}{key}")
                    elif isinstance(value, dict):
                        lines.append(f"{prefix}{connector}{key}")
                        # 再帰的に子要素を処理
                        extension = "   " if is_last_item else "│  "
                        child_lines = format_node(value, prefix + extension, is_last_item)
                        lines.extend(child_lines)
                    else:
                        lines.append(f"{prefix}{connector}{key}")

            return lines

        # プロジェクト名をルートとして表示
        # self.project_root is available via BaseGenerator
        project_name = self.project_root.name
        all_lines = [f"{project_name}/"]
        all_lines.extend(format_node(structure, " ", True))

        return "\n".join(all_lines)
