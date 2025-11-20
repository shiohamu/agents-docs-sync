# ステップ13: AGENTS.md生成のテストと検証

## 目的

各機能が正常に動作することを確認し、テストを作成します。

## 作業内容

### 1. ローカルでの動作確認

#### 1.1 基本的な動作確認

```bash
# プロジェクトルートで実行
python3 docgen/docgen.py
```

生成された`AGENTS.md`を確認し、以下の点をチェック：

- [ ] すべてのセクションが含まれているか
- [ ] API/ローカルLLMの両パターンが正しく表示されているか（`llm_mode: 'both'`の場合）
- [ ] プロジェクト情報が正しく収集されているか
- [ ] コーディング規約が正しく表示されているか
- [ ] ビルド/テストコマンドが正しく表示されているか

#### 1.2 生成されたAGENTS.mdの確認項目

以下のセクションが含まれていることを確認：

1. **プロジェクト概要**
   - プロジェクトの説明
   - 使用技術のリスト

2. **開発環境のセットアップ**
   - 前提条件
   - 依存関係のインストール手順
   - LLM環境のセットアップ（API/ローカルLLM）

3. **ビルドおよびテスト手順**
   - ビルドコマンド
   - テスト実行コマンド（API/ローカルLLM両パターン）

4. **コーディング規約**
   - フォーマッター
   - リンター
   - スタイルガイド

5. **プルリクエストの手順**
   - ブランチ作成
   - コミット
   - テスト実行
   - PR作成

### 2. 設定の変更テスト

#### 2.1 `llm_mode`の変更テスト

`docgen/config.yaml`の`agents.llm_mode`を変更してテスト：

**テスト1: `llm_mode: 'api'`**

```yaml
agents:
  llm_mode: 'api'
```

- [ ] APIのみのセクションが表示されるか
- [ ] ローカルLLMのセクションが表示されないか

**テスト2: `llm_mode: 'local'`**

```yaml
agents:
  llm_mode: 'local'
```

- [ ] ローカルLLMのみのセクションが表示されるか
- [ ] APIのセクションが表示されないか

**テスト3: `llm_mode: 'both'`**

```yaml
agents:
  llm_mode: 'both'
```

- [ ] 両方のセクションが表示されるか

#### 2.2 APIプロバイダーの変更テスト

```yaml
agents:
  api:
    provider: 'anthropic'
    api_key_env: 'ANTHROPIC_API_KEY'
```

- [ ] Anthropicの説明が正しく表示されるか

#### 2.3 ローカルLLMプロバイダーの変更テスト

```yaml
agents:
  local:
    provider: 'lmstudio'
    model: 'mistral'
    base_url: 'http://localhost:1234'
```

- [ ] LM Studioの説明が正しく表示されるか

#### 2.4 カスタム指示の追加テスト

```yaml
agents:
  custom_instructions: |
    - すべての関数にはdocstringを記述すること
    - テストカバレッジは80%以上を維持すること
    - コミット前にlintとformatを実行すること
```

- [ ] カスタム指示セクションが表示されるか
- [ ] 内容が正しく表示されるか

### 3. エッジケースのテスト

#### 3.1 プロジェクト情報が存在しない場合

- [ ] ビルドコマンドが存在しない場合のメッセージが表示されるか
- [ ] テストコマンドが存在しない場合のメッセージが表示されるか
- [ ] コーディング規約が検出されない場合のメッセージが表示されるか

#### 3.2 設定ファイルに`agents`セクションがない場合

- [ ] デフォルト設定で正常に動作するか
- [ ] エラーが発生しないか

### 4. テストファイルの作成（オプション）

`docgen/generators/test_agents_generator.py`を作成して、ユニットテストを追加：

```python
"""
AgentsGeneratorのテスト
"""

import pytest
from pathlib import Path
import sys

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
sys.path.insert(0, str(DOCGEN_DIR))

from generators.agents_generator import AgentsGenerator


def test_agents_generator_initialization(temp_project):
    """AgentsGeneratorの初期化テスト"""
    config = {
        'output': {'agents_doc': 'AGENTS.md'},
        'agents': {'llm_mode': 'both'}
    }
    generator = AgentsGenerator(temp_project, ['python'], config)
    assert generator.project_root == temp_project
    assert generator.languages == ['python']


def test_generate_agents_md(temp_project):
    """AGENTS.md生成テスト"""
    # テスト用のファイルを作成
    (temp_project / 'requirements.txt').write_text('pytest>=7.0.0\n')
    (temp_project / 'pytest.ini').write_text('[pytest]\ntestpaths = tests\n')

    config = {
        'output': {'agents_doc': 'AGENTS.md'},
        'agents': {
            'llm_mode': 'both',
            'api': {'provider': 'openai'},
            'local': {'provider': 'ollama', 'model': 'llama3'}
        }
    }

    generator = AgentsGenerator(temp_project, ['python'], config)
    result = generator.generate()

    assert result is True
    assert (temp_project / 'AGENTS.md').exists()

    content = (temp_project / 'AGENTS.md').read_text(encoding='utf-8')
    assert '# AGENTS ドキュメント' in content
    assert '開発環境のセットアップ' in content
    assert 'ビルドおよびテスト手順' in content
    assert 'APIを使用する場合' in content
    assert 'ローカルLLMを使用する場合' in content


def test_llm_mode_api_only(temp_project):
    """llm_mode: 'api' の場合のテスト"""
    config = {
        'output': {'agents_doc': 'AGENTS.md'},
        'agents': {
            'llm_mode': 'api',
            'api': {'provider': 'openai'}
        }
    }

    generator = AgentsGenerator(temp_project, ['python'], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / 'AGENTS.md').read_text(encoding='utf-8')
    assert 'APIを使用する場合' in content
    assert 'ローカルLLMを使用する場合' not in content


def test_llm_mode_local_only(temp_project):
    """llm_mode: 'local' の場合のテスト"""
    config = {
        'output': {'agents_doc': 'AGENTS.md'},
        'agents': {
            'llm_mode': 'local',
            'local': {'provider': 'ollama', 'model': 'llama3'}
        }
    }

    generator = AgentsGenerator(temp_project, ['python'], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / 'AGENTS.md').read_text(encoding='utf-8')
    assert 'APIを使用する場合' not in content
    assert 'ローカルLLMを使用する場合' in content


def test_custom_instructions(temp_project):
    """カスタム指示のテスト"""
    custom_instructions = "- すべての関数にはdocstringを記述すること\n- テストカバレッジは80%以上を維持すること"

    config = {
        'output': {'agents_doc': 'AGENTS.md'},
        'agents': {
            'llm_mode': 'both',
            'custom_instructions': custom_instructions
        }
    }

    generator = AgentsGenerator(temp_project, ['python'], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / 'AGENTS.md').read_text(encoding='utf-8')
    assert 'プロジェクト固有の指示' in content
    assert 'docstringを記述すること' in content
    assert 'テストカバレッジは80%以上' in content
```

### 5. 統合テスト

既存のパイプラインスクリプトで動作確認：

```bash
./scripts/run_pipeline.sh
```

- [ ] テストが正常に実行されるか
- [ ] ドキュメント生成が正常に実行されるか
- [ ] AGENTS.mdが正しく生成されるか

## 確認事項

- [ ] ローカルで正常に動作するか
- [ ] 生成されたAGENTS.mdがOpenAI仕様に準拠しているか
- [ ] API/ローカルLLMの両パターンが正しく表示されるか
- [ ] エラーハンドリングが適切に機能するか
- [ ] テストが正常に実行されるか（作成した場合）
- [ ] 設定変更が正しく反映されるか
- [ ] エッジケースが適切に処理されるか

## トラブルシューティング

### AGENTS.mdが生成されない

- `ProjectInfoCollector`が正しくインポートされているか確認
- 設定ファイルの`agents`セクションが正しく記述されているか確認
- エラーメッセージを確認（`traceback.print_exc()`で出力される）

### プロジェクト情報が正しく収集されない

- 対象ファイル（`requirements.txt`、`pytest.ini`など）が存在するか確認
- `ProjectInfoCollector`の各メソッドが正しく実装されているか確認

### テンプレートが正しく表示されない

- マークダウン生成ロジックを確認
- 条件分岐（`llm_mode`など）が正しく動作しているか確認

### 設定変更が反映されない

- 設定ファイルのYAML構文を確認
- インデントが正しいか確認（スペース2つ）
- 設定ファイルを再読み込みしているか確認

## 完了

すべてのステップが完了したら、実装は完了です。生成された`AGENTS.md`を確認し、必要に応じて設定を調整してください。

## 次のステップ

実装が完了したら、以下のことを検討してください：

- [ ] 生成されたAGENTS.mdを実際のLLMで使用して動作確認
- [ ] プロジェクト固有の要件に合わせて設定を調整
- [ ] ドキュメントを更新（必要に応じて）

