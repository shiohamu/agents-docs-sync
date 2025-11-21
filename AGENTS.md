# AGENTS ドキュメント

自動生成日時: 2025-11-21 12:37:34

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
`agents-docs-sync` は、GitHub Actions を利用して構築されたマルチ言語 CI/CD パイプラインです。  
Python（v3.11+）、JavaScript、および C で書かれたコンポーネントを対象にし、以下の機能を自動化します。

- **ビルド** – `uv run python3 docgen/docgen.py` を実行してプロジェクト用の API ドキュメントとサンプルコードを生成。  
- **テスト** – Python テストは pytest ベースで、カバレッジ (`pytest-cov`) とモック（`pytest-mock`）も併せて使用します。
  ```bash
  uv run pytest
  uv run python3 -m pytest test
  uv run pytest tests/ -v --tb=short
  ```
- **静的解析** – Python コードは Ruff を使って linting・フォーマットチェックを行い、コード品質を保ちます。  
- **依存関係管理** – `pyproject.toml`（uv）で次のパッケージが指定されています:
  - pyyaml >=6.0.3
  - pytest >=7.4.0
  - pytest-cov >=4.1.0
  - pytest-mock >=3.11.1

このセットアップにより、ソースコードとドキュメントの整合性を保ちつつ、複数言語で統一された CI/CD 環境が実現します。
<!-- MANUAL_END:description -->

---

## 開発環境のセットアップ

### 前提条件

- Python 3.12以上
- Node.js 18以上

### 依存関係のインストール

#### Python依存関係

```bash
uv sync
```

#### JavaScript依存関係

```bash
npm install
```

### LLM環境のセットアップ

#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - LM Studioをインストール: https://lmstudio.ai/
   - モデルをダウンロードして起動
   - ベースURL: http://192.168.10.113:1234

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください


---

## ビルドおよびテスト手順

### ビルド手順

```bash
uv run python3 docgen/docgen.py
```

### テスト実行

#### ローカルLLMを使用する場合

```bash
uv run pytest
uv run python3 -m pytest test
uv run pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。



---

## コーディング規約

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
   uv run pytest
   uv run python3 -m pytest test
   uv run pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このドキュメントは自動生成されています。最終更新: 2025-11-21 12:37:34*
