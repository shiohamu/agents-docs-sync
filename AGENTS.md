# AGENTS ドキュメント

自動生成日時: 2025-11-21 12:40:43

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
`agents-docs-sync` は、GitHub Actions を利用して構築されたマルチ言語（Python・JavaScript・C）向けの CI/CD パイプラインです。  
主な機能は次のとおり：

- **ドキュメント生成**： `uv run python3 docgen/docgen.py` でプロジェクト全体の API ドキュメントを自動生成し、リポジトリ内に配置します。
- **テスト実行**：Python コードは Pytest を用いて単体・統合テストが走り、コードカバレッジも測定されます。  
  - `uv run pytest`
  - `uv run python3 -m pytest test`
  - `uv run pytest tests/ -v --tb=short`
- **静的解析**：`ruff` をリンターとして使用し、一貫したコーディングスタイルと品質を保ちます。

依存関係は以下のパッケージで管理され、必要に応じて `uv` からインストールします：

```text
pyyaml>=6.0.3
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
```

このパイプラインは GitHub Actions のワークフローとして定義され、コミットごとに自動でビルド・テストが走るため、高品質なコードベースを維持しつつ迅速なデプロイメントサイクルを実現します。
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

*このドキュメントは自動生成されています。最終更新: 2025-11-21 12:40:43*
