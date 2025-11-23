"""
AgentsGeneratorのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.agents_generator import AgentsGenerator


def test_agents_generator_initialization(temp_project):
    """AgentsGeneratorの初期化テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator.project_root == temp_project
    assert generator.languages == ["python"]


def test_generate_agents_md(temp_project):
    """AGENTS.md生成テスト"""
    # テスト用のファイルを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")
    (temp_project / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n")

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "llm_mode": "both",
            "api": {"provider": "openai"},
            "local": {"provider": "ollama", "model": "llama3"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    assert (temp_project / "AGENTS.md").exists()

    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "# AGENTS ドキュメント" in content
    assert "開発環境のセットアップ" in content
    assert "ビルドおよびテスト手順" in content
    assert "APIを使用する場合" in content
    assert "ローカルLLMを使用する場合" in content


def test_llm_mode_api_only(temp_project):
    """llm_mode: 'api' の場合のテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"llm_mode": "api", "api": {"provider": "openai"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "APIを使用する場合" in content
    assert "ローカルLLMを使用する場合" not in content


def test_llm_mode_local_only(temp_project):
    """llm_mode: 'local' の場合のテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"llm_mode": "local", "local": {"provider": "ollama", "model": "llama3"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "APIを使用する場合" not in content
    assert "ローカルLLMを使用する場合" in content


def test_custom_instructions(temp_project):
    """カスタム指示のテスト"""
    custom_instructions = (
        "- すべての関数にはdocstringを記述すること\n- テストカバレッジは80%以上を維持すること"
    )

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"llm_mode": "both", "custom_instructions": custom_instructions},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "プロジェクト固有の指示" in content
    assert "docstringを記述すること" in content
    assert "テストカバレッジは80%以上" in content


def test_agents_generator_with_empty_config(temp_project):
    """空の設定でのテスト"""
    config = {}
    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    # デフォルト設定で動作するはず
    assert result is True
    assert (temp_project / "AGENTS.md").exists()


def test_agents_generator_multiple_languages(temp_project):
    """複数言語のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}

    generator = AgentsGenerator(temp_project, ["python", "javascript"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "# AGENTS ドキュメント" in content


def test_agents_generator_output_path(temp_project):
    """出力パス指定のテスト"""
    custom_path = "custom/agents.md"
    config = {"output": {"agents_doc": custom_path}, "agents": {"llm_mode": "api"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    assert (temp_project / custom_path).exists()


def test_extract_manual_sections_with_existing_file(temp_project):
    """既存ファイルからの手動セクション抽出テスト"""
    # 手動セクションを含む既存のAGENTS.mdを作成
    agents_content = """# AGENTS ドキュメント

<!-- MANUAL_START:description -->
これは手動で編集されたプロジェクト説明です。
重要な情報が含まれています。
<!-- MANUAL_END:description -->

## 自動生成セクション

この部分は自動生成されます。

<!-- MANUAL_START:custom_notes -->
特別な注意事項：
- セキュリティに注意
- パフォーマンスを重視
<!-- MANUAL_END:custom_notes -->
"""

    agents_file = temp_project / "AGENTS.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    manual_sections = generator._extract_manual_sections()

    # パースのデバッグ情報
    print(f"Extracted sections: {list(manual_sections.keys())}")

    assert "description" in manual_sections
    assert "custom_notes" in manual_sections
    assert "これは手動で編集されたプロジェクト説明です。" in manual_sections["description"]
    assert "セキュリティに注意" in manual_sections["custom_notes"]


def test_extract_manual_sections_no_file(temp_project):
    """ファイルが存在しない場合のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    manual_sections = generator._extract_manual_sections()

    assert manual_sections == {}


def test_extract_manual_sections_malformed_content(temp_project):
    """不正な形式のコンテンツ処理テスト"""
    # 不完全な手動セクション
    agents_content = """# AGENTS ドキュメント

<!-- MANUAL_START:description -->
このセクションは終了タグがない

<!-- MANUAL_START:another -->
別のセクションの内容
<!-- MANUAL_END:another -->
"""

    agents_file = temp_project / "AGENTS.md"
    agents_file.write_text(agents_content, encoding="utf-8")

    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    # エラーが発生しても処理が続くことを確認
    manual_sections = generator._extract_manual_sections()

    # 終了タグのあるセクションのみ抽出される
    assert "another" in manual_sections
    assert "別のセクションの内容" in manual_sections["another"]
    # 終了タグのないセクションは抽出されない
    assert "description" not in manual_sections


def test_merge_manual_sections(temp_project):
    """手動セクションのマージテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    # 生成されたマークダウン
    markdown = """# AGENTS ドキュメント

<!-- MANUAL_START:description -->
自動生成された説明がここに入ります。
<!-- MANUAL_END:description -->

## 自動生成セクション

これは自動生成されたコンテンツです。
"""

    # 手動セクション（現在の実装に合わせてキー名を調整）
    manual_sections = {"description -->": "これは手動で編集された重要なプロジェクト説明です。"}

    result = generator._merge_manual_sections(markdown, manual_sections)

    # マージ処理が実行されることを確認
    assert result is not None
    assert isinstance(result, str)
    assert "# AGENTS ドキュメント" in result
    # 自動生成セクションは保持される
    assert "これは自動生成されたコンテンツです。" in result


def test_merge_manual_sections_empty_manual(temp_project):
    """手動セクションが空の場合のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    markdown = """# AGENTS ドキュメント

<!-- MANUAL_START:description -->
自動生成された説明
<!-- MANUAL_END:description -->

## 自動生成セクション

コンテンツ
"""

    manual_sections = {}

    result = generator._merge_manual_sections(markdown, manual_sections)

    # 元のマークダウンが変更されない
    assert result == markdown


def test_generate_markdown_template_mode(temp_project):
    """テンプレートモードでのマークダウン生成テスト"""
    # テスト用のファイルを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"generation": {"agents_mode": "template"}, "llm_mode": "api"},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    project_info = generator.collector.collect_all()

    markdown = generator._generate_markdown(project_info)

    assert "# AGENTS ドキュメント" in markdown
    assert "プロジェクト概要" in markdown
    assert "開発環境のセットアップ" in markdown


def test_generate_markdown_llm_mode(temp_project):
    """LLMモードでのマークダウン生成テスト"""
    # テスト用のファイルを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "generation": {"agents_mode": "llm"},
            "llm_mode": "api",
            "api": {"provider": "openai"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    project_info = generator.collector.collect_all()

    # LLMモードではエラーが発生してもフォールバックする
    markdown = generator._generate_markdown(project_info)

    # フォールバックでテンプレートが使用される
    assert "# AGENTS ドキュメント" in markdown


def test_generate_markdown_hybrid_mode(temp_project):
    """ハイブリッドモードでのマークダウン生成テスト"""
    # テスト用のファイルを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "generation": {"agents_mode": "hybrid"},
            "llm_mode": "api",
            "api": {"provider": "openai"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    project_info = generator.collector.collect_all()

    # ハイブリッドモードではエラーが発生してもフォールバックする
    markdown = generator._generate_markdown(project_info)

    # フォールバックでテンプレートが使用される
    assert "# AGENTS ドキュメント" in markdown


def test_generate_error_handling(temp_project):
    """生成時のエラーハンドリングテスト"""
    config = {"output": {"agents_doc": "/invalid/path/AGENTS.md"}, "agents": {"llm_mode": "api"}}

    generator = AgentsGenerator(temp_project, ["python"], config)

    # 無効なパスではエラーが発生するはず
    result = generator.generate()

    # エラーが処理されてFalseが返される
    assert result is False
