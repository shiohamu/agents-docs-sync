# ステップ10: AGENTS.md生成設定の拡張

## 目的

AGENTS.md生成用の設定セクションを`.docgen/config.yaml`に追加します。

## 作業内容

### 1. `.docgen/config.yaml`を編集

既存の設定に`agents`セクションを追加します：

```yaml
# 既存の設定...

# AGENTS.md生成設定
agents:
  # LLM使用パターン（'api', 'local', 'both'）
  llm_mode: 'both'

  # API使用時の設定
  api:
    provider: 'openai'  # 'openai', 'anthropic', 'custom'
    endpoint: null  # カスタムエンドポイント（オプション）
    api_key_env: 'OPENAI_API_KEY'  # 環境変数名

  # ローカルLLM使用時の設定
  local:
    provider: 'ollama'  # 'ollama', 'lmstudio', 'custom'
    model: 'llama3'  # デフォルトモデル名
    base_url: 'http://localhost:11434'  # デフォルトURL

  # コーディング規約の設定
  coding_standards:
    auto_detect: true
    # 手動で指定する場合（auto_detect: false の場合）
    # style_guide: 'PEP 8'
    # formatter: 'black'
    # linter: 'ruff'

  # プロジェクト固有の指示（オプション）
  custom_instructions: null
  # 例:
  # custom_instructions: |
  #   - すべての関数にはdocstringを記述すること
  #   - テストカバレッジは80%以上を維持すること
```

**注意**: 既存の設定を上書きせず、新しい設定を追加するだけにしてください。

### 2. 設定値の説明

#### `llm_mode`
- `'api'`: APIのみを使用する場合
- `'local'`: ローカルLLMのみを使用する場合
- `'both'`: 両方のパターンを記載する場合（デフォルト）

#### `api.provider`
- `'openai'`: OpenAI APIを使用
- `'anthropic'`: Anthropic APIを使用
- `'custom'`: カスタムAPIエンドポイントを使用

#### `api.endpoint`
- カスタムAPIエンドポイントのURL（`api.provider`が`'custom'`の場合）

#### `api.api_key_env`
- APIキーを格納する環境変数名

#### `local.provider`
- `'ollama'`: Ollamaを使用
- `'lmstudio'`: LM Studioを使用
- `'custom'`: カスタムローカルLLMを使用

#### `local.model`
- 使用するローカルLLMモデル名（例: `'llama3'`, `'mistral'`）

#### `local.base_url`
- ローカルLLMのベースURL（デフォルト: `'http://localhost:11434'`）

#### `coding_standards.auto_detect`
- `true`: プロジェクトから自動検出（推奨）
- `false`: 手動で指定

#### `custom_instructions`
- プロジェクト固有の指示をMarkdown形式で記述

## 確認事項

- [ ] YAMLの構文が正しいか
- [ ] 既存の設定を壊していないか
- [ ] インデントが正しいか（スペース2つ）
- [ ] デフォルト値が適切か
- [ ] コメントが適切に記述されているか

## 次のステップ

このステップが完了したら、[ステップ11: AGENTS.mdテンプレートシステムの実装](./step11-agents-template.md)に進んでください。

