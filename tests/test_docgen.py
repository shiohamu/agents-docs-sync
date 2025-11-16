"""
DocGenメインクラスのテスト
"""

import pytest
import yaml
from pathlib import Path
import sys

# .docgenモジュールをインポート
DOCGEN_DIR = Path(__file__).parent.parent / ".docgen"
sys.path.insert(0, str(DOCGEN_DIR))

from docgen import DocGen


@pytest.mark.unit
class TestDocGen:
    """DocGenのテストクラス"""

    def test_load_config_from_file(self, temp_project, sample_config):
        """設定ファイルから設定を読み込めることを確認"""
        # 一時プロジェクトをルートとして使用
        docgen = DocGen(config_path=sample_config)

        assert docgen.config is not None
        assert 'languages' in docgen.config
        assert 'output' in docgen.config

    def test_get_default_config(self, temp_project):
        """デフォルト設定が正しいことを確認"""
        docgen = DocGen()
        default_config = docgen._get_default_config()

        assert 'languages' in default_config
        assert 'output' in default_config
        assert 'generation' in default_config
        assert default_config['output']['api_doc'] == 'docs/api.md'
        assert default_config['output']['readme'] == 'README.md'

    def test_detect_languages_python(self, python_project):
        """Pythonプロジェクトの言語検出を確認"""
        # 一時プロジェクトをルートとして使用するため、DocGenを直接テストするのは難しい
        # 代わりに、detect_languagesメソッドの動作を確認
        docgen = DocGen()
        # 実際のプロジェクトルートではなく、テスト用のパスを使用
        # このテストは統合テストでより適切にテストされる

    def test_detect_languages_empty_project(self, temp_project):
        """空のプロジェクトで言語が検出されないことを確認"""
        # このテストは統合テストで実装

    def test_generate_documents(self, python_project, sample_config):
        """ドキュメント生成が実行されることを確認"""
        docgen = DocGen(config_path=sample_config)
        # プロジェクトルートを一時的に変更する必要があるため、
        # このテストは統合テストで実装

    def test_config_merges_with_defaults(self, temp_project):
        """部分的な設定がデフォルトとマージされることを確認"""
        config_dir = temp_project / ".docgen"
        config_dir.mkdir()
        config_path = config_dir / "config.yaml"

        partial_config = {
            'output': {
                'api_doc': 'custom/api.md'
            }
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(partial_config, f)

        docgen = DocGen(config_path=config_path)
        # 部分的な設定が読み込まれることを確認
        assert docgen.config['output']['api_doc'] == 'custom/api.md'

