"""Pydantic models for configuration validation."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProjectOverview(BaseModel):
    """Project overview model."""

    name: str
    languages: list[str]
    dependencies: list[str] | None = None


class LLMSetup(BaseModel):
    """LLM setup model."""

    api_setup: str | None = None
    local_setup: str | None = None


class SetupInstructions(BaseModel):
    """Setup instructions model."""

    prerequisites: list[str] | None = None
    installation_commands: list[str] | None = None
    llm_setup: LLMSetup | None = None


class BuildTestInstructions(BaseModel):
    """Build and test instructions model."""

    build_commands: list[str] | None = None
    test_commands: list[str] | None = None
    test_execution_notes: str | None = None


class CodingStandards(BaseModel):
    """Coding standards model."""

    standards: list[str] | None = None
    notes: str | None = None


class PRGuidelines(BaseModel):
    """PR guidelines model."""

    branch_creation: str | None = None
    commit_guidelines: str | None = None
    pr_creation: str | None = None


class AgentsConfig(BaseModel):
    """Configuration model for agents documentation."""

    title: str = Field(description="ドキュメントのタイトル")
    description: str = Field(description="プロジェクトの説明")
    project_overview: ProjectOverview
    setup_instructions: SetupInstructions
    build_test_instructions: BuildTestInstructions
    coding_standards: CodingStandards | None = None
    pr_guidelines: PRGuidelines | None = None
    auto_generated_note: str | None = Field(default=None, description="自動生成に関する注意書き")


class Dependencies(BaseModel):
    """Dependencies model."""

    python: list[str] | None = None
    nodejs: list[str] | None = None
    other: list[str] | None = None


class ReadmeSetupInstructions(BaseModel):
    """Setup instructions for README."""

    prerequisites: list[str] | None = None
    installation_steps: list[str] | None = None


class ReadmeConfig(BaseModel):
    """Configuration model for README documentation."""

    title: str = Field(description="プロジェクトタイトル")
    description: str = Field(description="プロジェクトの説明")
    technologies: list[str] = Field(description="使用技術のリスト")
    dependencies: Dependencies | None = Field(description="言語ごとの依存関係")
    setup_instructions: ReadmeSetupInstructions | None = None
    project_structure: list[str] | None = Field(default=None, description="プロジェクト構造の説明")
    build_commands: list[str] | None = Field(default=None, description="ビルドコマンド")
    test_commands: list[str] | None = Field(default=None, description="テストコマンド")
    manual_sections: dict[str, str] | None = Field(
        default=None, description="手動で記述されたセクション"
    )


class LanguagesConfig(BaseModel):
    """Languages configuration model."""

    auto_detect: bool = True
    preferred: list[str] = Field(default_factory=list)


class OutputConfig(BaseModel):
    """Output configuration model."""

    api_doc: str = "docs/api.md"
    readme: str = "README.md"
    agents_doc: str = "AGENTS.md"


class GenerationConfig(BaseModel):
    """Generation configuration model."""

    update_readme: bool = True
    generate_api_doc: bool = True
    generate_agents_doc: bool = True
    preserve_manual_sections: bool = True


class AgentsGenerationConfig(BaseModel):
    """Agents generation configuration model."""

    agents_mode: str = "template"
    readme_mode: str = "template"
    enable_commit_message: bool = True


class LLMConfig(BaseModel):
    """LLM設定モデル"""

    provider: str | None = Field(
        default=None, description="LLMプロバイダー (openai, anthropic, ollama, local)"
    )
    model: str | None = Field(default=None, description="モデル名")
    api_key: str | None = Field(default=None, description="APIキー")
    api_key_env: str | None = Field(default=None, description="APIキー環境変数名")
    base_url: str | None = Field(default=None, description="ベースURL")
    endpoint: str | None = Field(default=None, description="エンドポイントURL")
    timeout: int = Field(default=30, description="タイムアウト秒数")
    max_retries: int = Field(default=3, description="最大リトライ回数")
    retry_delay: float = Field(default=1.0, description="リトライ遅延秒数")
    temperature: float | None = Field(default=None, description="温度パラメータ")
    max_tokens: int | None = Field(default=None, description="最大トークン数")


class AgentsConfigSection(BaseModel):
    """Agents configuration section model."""

    llm_mode: str = "both"
    generation: AgentsGenerationConfig = Field(default_factory=AgentsGenerationConfig)
    api: LLMConfig | None = Field(default=None, description="API LLM設定")
    local: LLMConfig | None = Field(default=None, description="ローカルLLM設定")
    coding_standards: dict[str, Any] | None = Field(
        default=None, description="コーディング規約設定"
    )
    custom_instructions: str | None = Field(default=None, description="プロジェクト固有の指示")


class ExcludeConfig(BaseModel):
    """Exclude configuration model."""

    directories: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)


class CacheConfig(BaseModel):
    """Cache configuration model."""

    enabled: bool = True


class DebugConfig(BaseModel):
    """Debug configuration model."""

    enabled: bool = False


class DocgenConfig(BaseModel):
    """Main configuration model for docgen."""

    languages: LanguagesConfig = Field(default_factory=LanguagesConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    agents: AgentsConfigSection = Field(default_factory=AgentsConfigSection)
    exclude: ExcludeConfig = Field(default_factory=ExcludeConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    debug: DebugConfig = Field(default_factory=DebugConfig)


class ProjectInfo(BaseModel):
    """Project information model."""

    description: str | None = None
    build_commands: list[str] = Field(default_factory=list)
    test_commands: list[str] = Field(default_factory=list)
    dependencies: dict[str, list[str]] = Field(default_factory=dict)
    coding_standards: dict[str, Any] | None = None
    ci_cd_info: dict[str, Any] | None = None
    project_structure: dict[str, Any] | None = None


class AgentsDocument(BaseModel):
    """AGENTS.mdドキュメントの構造化データモデル"""

    title: str = Field(description="ドキュメントのタイトル")
    description: str = Field(description="プロジェクトの説明")
    project_overview: ProjectOverview
    setup_instructions: SetupInstructions
    build_test_instructions: BuildTestInstructions
    coding_standards: CodingStandards | None = None
    pr_guidelines: PRGuidelines | None = None
    auto_generated_note: str = Field(description="自動生成に関する注意書き")


class ReadmeDocument(BaseModel):
    """READMEドキュメントの構造化データモデル"""

    title: str = Field(description="プロジェクトタイトル")
    description: str = Field(description="プロジェクトの説明")
    technologies: list[str] = Field(description="使用技術のリスト")
    dependencies: Dependencies | None = Field(description="言語ごとの依存関係")
    setup_instructions: ReadmeSetupInstructions | None = None
    project_structure: list[str] | None = Field(default=None, description="プロジェクト構造の説明")
    build_commands: list[str] | None = Field(default=None, description="ビルドコマンド")
    test_commands: list[str] | None = Field(default=None, description="テストコマンド")
    manual_sections: dict[str, str] | None = Field(
        default=None, description="手動で記述されたセクション"
    )


class APIParameter(BaseModel):
    """APIパラメータモデル"""

    name: str = Field(description="パラメータ名")
    type: str = Field(description="パラメータの型")
    description: str | None = Field(default=None, description="パラメータの説明")
    default: Any = Field(default=None, description="デフォルト値")
    required: bool = Field(default=True, description="必須かどうか")


class APIInfo(BaseModel):
    """API情報モデル"""

    name: str = Field(description="関数/メソッド/クラスの名前")
    type: str = Field(description="種類 (function, method, class, etc.)")
    file_path: str = Field(description="ファイルパス")
    line_number: int | None = Field(default=None, description="行番号")
    signature: str | None = Field(default=None, description="シグネチャ")
    docstring: str | None = Field(default=None, description="ドキュメント文字列")
    parameters: list[APIParameter] | None = Field(default=None, description="パラメータ情報")
    return_type: str | None = Field(default=None, description="戻り値の型")
    decorators: list[str] | None = Field(default=None, description="デコレータ")
    visibility: str | None = Field(default=None, description="可視性 (public, private, protected)")
    language: str = Field(description="プログラミング言語")


class LLMClientConfig(BaseModel):
    """LLMクライアント設定モデル"""

    openai: LLMConfig | None = Field(default=None, description="OpenAI設定")
    anthropic: LLMConfig | None = Field(default=None, description="Anthropic設定")
    ollama: LLMConfig | None = Field(default=None, description="Ollama設定")
    local: LLMConfig | None = Field(default=None, description="ローカルLLM設定")
    default_provider: str = Field(default="openai", description="デフォルトプロバイダー")


class CacheEntry(BaseModel):
    """キャッシュエントリーモデル"""

    data: list[APIInfo] = Field(description="キャッシュされたAPI情報")
    timestamp: datetime = Field(description="キャッシュ作成時刻")
    file_hash: str = Field(description="ファイルハッシュ")
    parser_type: str = Field(description="パーサーの種類")


class CacheMetadata(BaseModel):
    """キャッシュメタデータモデル"""

    version: str = Field(default="1.0", description="キャッシュバージョン")
    created_at: datetime = Field(description="キャッシュ作成時刻")
    last_updated: datetime = Field(description="最終更新時刻")
    total_entries: int = Field(default=0, description="総エントリー数")
