# AGENTS ドキュメント

自動生成日時: 2025-11-25 15:04:08

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
このプロジェクトは、コミットごとに自動でテスト実行・ドキュメント生成を行い、その結果を `AGENTS.md` に反映させるパイプラインです。
主な構成要素は以下の通りです。

- **言語 & ツール**：Python（3.11+）とシェルスクリプトで実装し、依存関係には `pyyaml>=6.0.3`、`pytest>=7.4.0`、`pytest-cov>=4.1.0`、`pytest-mock>=3.11.1` を使用。Linting は Ruff で統一しています。
- **ビルド**：
  ```bash
  uv run python3 docgen/docgen.py
  ```
  により `docgen/` 内のスクリプトが YAML 定義から Markdown ドキュメントを生成します。
- **テスト実行**：
  - Python テストは `uv run pytest`、詳細オプション付きで `uv run pytest tests/ -v --tb=short`。
  - Node.js の補助スクリプトも存在し、`npm test` により併せて走らせます。
- **AGENTS.md 自動更新**：テストとドキュメント生成が成功した後に、最新の内容を `AGENTS.md` にマージ。これによりコードベースとドキュメントの同期状態が常に保たれます。

このパイプラインは CI/CD で毎回トリガーされるため、コミットごとの品質保証と文書整合性を自動的に確保します。
<!-- MANUAL_END:description -->

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

### LLM環境のセットアップ

#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - LM Studioをインストール: https://lmstudio.ai/
   - モデルをダウンロードして起動
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
   uv run pytest
   npm test
   uv run pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 15:04:08*