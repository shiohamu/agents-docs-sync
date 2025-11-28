"""
手動セクション管理 Mixin

既存のドキュメントから手動で記述されたセクションを抽出し、
自動生成されたコンテンツとマージする機能を提供します。
"""

from docgen.utils.markdown_utils import MANUAL_END_PREFIX, MANUAL_START_PREFIX


class ManualSectionMixin:
    """手動セクション管理機能を提供する Mixin"""

    def _extract_manual_sections(self, content: str) -> dict[str, str]:
        """
        既存のコンテンツから手動セクションを抽出

        Args:
            content: 既存のドキュメントコンテンツ

        Returns:
            セクションIDとコンテンツの辞書
        """
        manual_sections = {}
        lines = content.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if MANUAL_START_PREFIX in line:
                # セクションIDを抽出 (例: <!-- MANUAL_START: section_id -->)
                try:
                    section_id = (
                        line.split(MANUAL_START_PREFIX)[1]
                        .split("-->")[0]
                        .strip()
                        .replace(":", "")
                        .strip()
                    )
                    current_section = section_id
                    current_content = []
                except IndexError:
                    pass
            elif MANUAL_END_PREFIX in line:
                if current_section:
                    manual_sections[current_section] = "\n".join(current_content).strip()
                    current_section = None
                    current_content = []
            elif current_section:
                current_content.append(line)

        return manual_sections

    def _merge_manual_sections(
        self, generated_content: str, manual_sections: dict[str, str]
    ) -> str:
        """
        生成されたコンテンツに手動セクションをマージ

        Args:
            generated_content: 自動生成されたコンテンツ
            manual_sections: 抽出された手動セクションの辞書

        Returns:
            マージされたコンテンツ
        """
        if not manual_sections:
            return generated_content

        merged_lines = []
        lines = generated_content.split("\n")

        # マーカーが見つかったかどうかを追跡
        found_sections = set()

        for line in lines:
            merged_lines.append(line)

            if MANUAL_START_PREFIX in line:
                try:
                    section_id = (
                        line.split(MANUAL_START_PREFIX)[1]
                        .split("-->")[0]
                        .strip()
                        .replace(":", "")
                        .strip()
                    )
                    if section_id in manual_sections:
                        # 手動コンテンツを挿入
                        merged_lines.append(manual_sections[section_id])
                        found_sections.add(section_id)
                except IndexError:
                    pass

        return "\n".join(merged_lines)
