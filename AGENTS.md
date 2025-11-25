# AGENTS ドキュメント

自動生成日時: 2025-11-25 11:33:28

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

**agents-docs-sync** は、GitHub Actions を利用した CI/CD パイプラインであり、リポジトリへのコミットが行われるたびに以下の処理を自動実行します。

- **テスト実行**  
  - Python 用テスト: `uv run pytest`（カバレッジ付き）と `uv run pytest tests/ -v --tb=short`。  
  - Node.js テスト: `npm test` を併用し、フロントエンドやその他スクリプトの動作確認も行います。

- **ドキュメント生成**  
  - Python スクリプト `docgen/docgen.py`（ビルドコマンド：`uv run python3 docgen/docgen.py`）を実行し、最新の API ドキュメントや使用例を自動で作成します。

- **AGENTS.md の更新**  
  - 上記生成物に基づき `AGENTS.md` を差分コミット。これによりドキュメントとコードベースが常に同期した状態になります。

### 主な依存関係

| ランタイム | パッケージ |
|------------|-----------|
| Python 3.10+ | `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` |

### コーディング規約

- **リンター**: `ruff`
  - 静的解析とコード整形を自動化し、品質の一貫性を保ちます。

### 実行コマンドまとめ
```bash
# ビルド（ドキュメント生成）
uv run python3 docgen/docgen.py

# Python テスト
uv run pytest
uv run pytest tests/ -v --tb=short

# Node.js テスト
npm test
```

### 期待される成果物
- 最新のテストレポート（カバレッジ含む）
- 自動生成されたドキュメントファイル群
- `AGENTS.md` の内容が最新状態に保たれる

このパイプラインは、コミット単位で CI を走らせることで開発フローを高速化しつつ、一貫した品質と文書整合性を保証します。

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
### 前提条件

- Python 3.12以上

### 依存関係のインストール

#### Python依存関係

```bash
uv sync
```

### LLM環境のセットアップ

#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`
   - ベースURL: http://localhost:11434

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください
<!-- MANUAL_END:setup -->

---

## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順

```bash
uv run python3 docgen/docgen.py
```

### テスト実行

#### APIを使用する場合

```bash
uv run pytest
npm test
uv run pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
uv run pytest
npm test
uv run pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。
<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   uv run pytest
   npm test
   uv run pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:other -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   uv run pytest
   npm test
   uv run pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->

---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 11:33:28*
