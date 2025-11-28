"""
LLM生成 Mixin

LLMを使用したドキュメント生成、Outlines統合、
およびハイブリッド生成機能を提供します。
"""

from typing import Any

from docgen.models.project import ProjectInfo
from docgen.utils.llm import LLMClientFactory


class LLMMixin:
    """LLM生成機能を提供する Mixin"""

    def _generate_with_llm(self, project_info: ProjectInfo) -> str:
        """
        LLMを使用してドキュメントを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列（エラー時はテンプレート生成にフォールバック）
        """
        try:
            return self._generate_with_outlines(project_info)

        except Exception as e:
            self.logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _should_use_outlines(self) -> bool:
        """
        Outlinesを使用するかどうかを判定

        Returns:
            Outlinesを使用するかどうか
        """
        from ..utils.outlines_utils import should_use_outlines

        return should_use_outlines(self.agents_config)

    def _get_llm_client_with_fallback(self) -> Any:
        """
        LLMクライアントを取得（フォールバック付き）

        Returns:
            LLMクライアント（取得できない場合はNone）
        """
        llm_mode = self.agents_config.get("llm_mode", "api")
        preferred_mode = "api" if llm_mode in "api" else "local"

        return LLMClientFactory.create_client_with_fallback(
            self.agents_config, preferred_mode=preferred_mode
        )

    def _generate_with_outlines(self, project_info: ProjectInfo) -> str:
        """
        Outlinesを使用して構造化されたドキュメントを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        try:
            # LLMクライアントを取得
            client = self._get_llm_client_with_fallback()

            if not client:
                self.logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # Outlinesモデルを作成
            outlines_model = self._create_outlines_model(client)

            if outlines_model is None:
                # Outlinesがサポートされていない場合、テンプレート生成にフォールバック
                self.logger.info(
                    "Outlinesがサポートされていないため、テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # RAGコンテキストを取得
            rag_context = ""
            if self.config.get("rag", {}).get("enabled", False):
                # ドキュメント全体生成のためのクエリ
                query = f"full documentation context for {self.project_root.name}"
                rag_context = self._get_rag_context(query)

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info, rag_context=rag_context)

            # 構造化出力モデルで生成
            self.logger.info("Outlinesを使用して構造化されたドキュメントを生成中...")
            structured_data = outlines_model(prompt, self._get_structured_model())

            # 構造化データをマークダウンに変換
            markdown = self._convert_structured_data_to_markdown(structured_data, project_info)

            return markdown

        except Exception as e:
            self.logger.error(
                f"Outlines生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _create_outlines_model(self, client):
        """
        Outlinesモデルを作成

        Args:
            client: LLMクライアント

        Returns:
            Outlinesモデル
        """
        from ..utils.outlines_utils import create_outlines_model

        return create_outlines_model(client)

    def _generate_hybrid(self, project_info: ProjectInfo) -> str:
        """
        テンプレートとLLMを組み合わせて生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # まずテンプレートを生成
        template_content = self._generate_template(project_info)

        try:
            # プロジェクト概要セクションのみLLMで改善
            existing_overview = self._get_project_overview_section(template_content)
            improved_overview = self._generate_overview_with_llm(project_info, existing_overview)

            if improved_overview and improved_overview != existing_overview:
                return self._replace_overview_section(template_content, improved_overview)
            else:
                return template_content

        except Exception as e:
            self.logger.warning(
                f"ハイブリッド生成中にエラーが発生しました: {e}。テンプレートのみを使用します。",
                exc_info=True,
            )
            return template_content

    def _generate_overview_with_llm(
        self, project_info: ProjectInfo, existing_overview: str
    ) -> str | None:
        """
        LLMを使用してプロジェクト概要を生成

        Args:
            project_info: プロジェクト情報
            existing_overview: 既存の概要

        Returns:
            改善された概要（生成失敗時はNone）
        """
        try:
            # LLMクライアントを取得
            client = self._get_llm_client_with_fallback()

            if not client:
                self.logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレートのみを使用します。"
                )
                return None

            self.logger.info("LLMを使用してプロジェクト概要セクションを改善中...")

            # RAGコンテキストを取得
            rag_context = ""
            if self.config.get("rag", {}).get("enabled", False):
                query = f"project overview architecture summary for {self.project_root.name}"
                rag_context = self._get_rag_context(query)

            # プロンプト作成
            prompt = f"""
以下のプロジェクト情報と既存の概要を元に、より詳細で魅力的なプロジェクト概要（マークダウン形式）を生成してください。
技術的な詳細、アーキテクチャ、主要な機能を強調してください。

# プロジェクト情報
名前: {self.project_root.name}
説明: {project_info.description}
言語: {", ".join(self.languages)}

# RAGコンテキスト (参考情報)
{rag_context}

# 既存の概要
{existing_overview}

# 指示
- 日本語で記述してください。
- "## プロジェクト概要" などの見出しは含めず、内容のみを返してください。
- 簡潔かつ具体的に記述してください。
"""
            # 生成
            response = client.generate(prompt)
            return self._clean_llm_output(response)

        except Exception as e:
            self.logger.warning(f"概要生成中にエラーが発生しました: {e}")
            return None

    def _format_project_info_for_prompt(self, project_info: ProjectInfo) -> str:
        """
        プロジェクト情報をプロンプト用に整形

        Args:
            project_info: プロジェクト情報

        Returns:
            整形された文字列
        """
        info_parts = []
        info_parts.append(f"Project Name: {self.project_root.name}")
        info_parts.append(f"Description: {project_info.description}")
        info_parts.append(f"Languages: {', '.join(self.languages)}")

        if self.package_managers:
            pms = [f"{lang}: {pm}" for lang, pm in self.package_managers.items()]
            info_parts.append(f"Package Managers: {', '.join(pms)}")

        if project_info.dependencies:
            deps = []
            if "python" in project_info.dependencies:
                deps.extend(project_info.dependencies["python"])
            if "nodejs" in project_info.dependencies:
                deps.extend(project_info.dependencies["nodejs"])
            if deps:
                info_parts.append(f"Dependencies: {', '.join(deps[:20])}...")  # Limit to 20

        return "\n".join(info_parts)
