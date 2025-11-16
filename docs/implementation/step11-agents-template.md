# ステップ11: AGENTS.mdテンプレートシステムの実装

## 目的

OpenAI仕様に準拠したAGENTS.mdのテンプレートを作成します。

## 作業内容

### 1. `.docgen/templates/`ディレクトリを作成

```bash
mkdir -p .docgen/templates
```

### 2. テンプレートの構造

このテンプレートは、後で`AgentsGenerator`で文字列置換によって使用されます。以下のセクションを含みます：

- プロジェクト概要
- 開発環境のセットアップ（API/ローカルLLM両パターン）
- ビルドおよびテスト手順
- テスト実行（API/ローカルLLM両パターン）
- コーディング規約
- プルリクエストの手順
- プロジェクト固有の指示（オプション）

### 3. テンプレートの参考例

実際のテンプレートは`AgentsGenerator`内で動的に生成されますが、以下のような構造になります：

```markdown
# AGENTS ドキュメント

自動生成日時: {{ generation_date }}

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

{{ project_description }}

**使用技術**: {{ languages }}

---

## 開発環境のセットアップ

### 前提条件

- Python 3.12以上
- Node.js 18以上（該当する場合）

### 依存関係のインストール

#### Python依存関係

```bash
pip install -r requirements.txt
pip install -r requirements-docgen.txt
pip install -r requirements-test.txt
```

#### Node.js依存関係（該当する場合）

```bash
npm install
```

### LLM環境のセットアップ

#### APIを使用する場合

1. **APIキーの取得と設定**
   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**
   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください

---

## ビルドおよびテスト手順

### ビルド手順

```bash
# ビルドコマンドがここに表示されます
```

### テスト実行

#### APIを使用する場合

```bash
pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

---

## コーディング規約

### フォーマッター

- **black** を使用
  ```bash
  black .
  ```

### リンター

- **ruff** を使用
  ```bash
  ruff check .
  ruff format .
  ```

---

## プルリクエストの手順

1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載

---

## プロジェクト固有の指示

（カスタム指示が設定されている場合、ここに表示されます）

---

*このドキュメントは自動生成されています。最終更新: {{ generation_date }}*
```

### 4. 実装上の注意

このテンプレートは参考例です。実際の実装では、`AgentsGenerator`内で動的にマークダウンを生成します。テンプレートファイルとして保存する必要はありませんが、構造の参考として残しておくことができます。

## 確認事項

- [ ] テンプレートの構造がOpenAI仕様に準拠しているか
- [ ] すべてのセクションが含まれているか
- [ ] API/ローカルLLMの両パターンが考慮されているか

## 次のステップ

このステップが完了したら、[ステップ12: AgentsGeneratorの変更](./step12-agents-generator-refactor.md)に進んでください。

