"""
マークダウン処理 Mixin

マークダウンの生成、クリーニング、検証機能を提供します。
"""

from docgen.utils.markdown_utils import (
    DESCRIPTION_END,
    DESCRIPTION_START,
    get_current_timestamp,
)


class MarkdownMixin:
    """マークダウン処理機能を提供する Mixin"""

    def _generate_footer(self) -> str:
        """フッターを生成"""
        return f"*この{self._get_document_type()}は自動生成されています。最終更新: {get_current_timestamp()}*"

    def _extract_description_section(self, content: str) -> str:
        """
        Extract description section from content

        Args:
            content: Document content

        Returns:
            Description section text
        """
        lines = content.split("\n")
        description_lines = []
        in_description = False

        for line in lines:
            if DESCRIPTION_START in line:
                in_description = True
                continue
            elif DESCRIPTION_END in line:
                break
            elif in_description:
                description_lines.append(line)

        return "\n".join(description_lines)

    def _clean_llm_output(self, content: str) -> str:
        """
        LLMの出力をクリーニング

        Args:
            content: LLM出力

        Returns:
            クリーニングされたコンテンツ
        """
        # マークダウンコードブロックの削除
        if content.startswith("```markdown"):
            content = content.replace("```markdown", "", 1)
        elif content.startswith("```"):
            content = content.replace("```", "", 1)

        if content.endswith("```"):
            content = content[:-3]

        return content.strip()

    def _validate_output(self, content: str) -> bool:
        """
        生成されたコンテンツを検証

        Args:
            content: 生成されたコンテンツ

        Returns:
            検証に成功した場合True
        """
        if not content:
            return False

        # 最低限の長さチェック
        if len(content) < 50:
            return False

        return True

    def _replace_overview_section(self, content: str, new_overview: str) -> str:
        """
        プロジェクト概要セクションを置き換え

        Args:
            content: 元のコンテンツ
            new_overview: 新しい概要

        Returns:
            置き換え後のコンテンツ
        """
        import re

        from docgen.utils.logger import get_logger

        logger = get_logger("markdown_mixin")

        # デフォルト実装: "## プロジェクト概要" または "## 概要" セクションを置き換え
        # パターン: ヘッダーから次のセクション（## で始まる行）の前まで
        pattern = r"(## (プロジェクト概要|概要)\s*\n)(.*?)(\n## )"
        replacement = r"\1\n" + new_overview + r"\3"

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # デバッグ: 置換が成功したか確認
        if updated_content == content:
            logger.warning(
                "Overview section replacement did not match. Pattern may need adjustment."
            )
        else:
            logger.debug("Overview section successfully replaced.")

        return updated_content

    def _collect_project_description(self) -> str:
        """
        プロジェクト説明を収集

        Returns:
            プロジェクト説明
        """
        from docgen.utils.markdown_utils import extract_project_description

        # self.project_root and self.config are expected to be available from BaseGenerator
        description = self.config.get("description", "")

        # README.mdを除外するかどうかはサブクラスの実装によるが、
        # ここでは汎用的にREADME.mdを除外しない（必要ならサブクラスでオーバーライド）
        # ただし、ReadmeGeneratorではオーバーライドされているはず

        return extract_project_description(self.project_root, description)
