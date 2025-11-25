# AGENTS ドキュメント

自動生成日時: 2025-11-25 09:55:00

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
`agents-docs-sync` は、Python と Shell スクリプトで構成された GitHub Actions ベースの CI/CD パイプラインです。

主な機能は以下の通り：

1. **コミットごとに自動実行**：Push あるいは Pull Request が発生するとワークフローが起動します。
2. **テスト実行**：
   - Python 用テスト: `uv run pytest`（カバレッジ・モックも併用）
   - JavaScript/Node.js テスト（プロジェクトに含まれる場合）: `npm test`
3. **ドキュメント生成**：Python スクリプト `docgen/docgen.py` を実行し、最新の API ドキュメントを作成します。
4. **AGENTS.md の自動更新**：生成した情報から `AGENTS.md` を差分コミットして PR に反映させます。

### 技術スタック
- **言語・実装**: Python 3.x, Shell スクリプト
- **ビルド/テストツール**: `uv`（Python パッケージ管理） + `pytest`, `npm`
- **依存ライブラリ (Python)**:
```text
pyyaml>=6.0.3
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
```
- **コード品質**: `ruff` を利用した静的リンティング
- **CI/CD 実装**: GitHub Actions（`.github/workflows/ci.yml` など）

### 使用方法

・フックの有効化
```bash
user@hogehoge: ~$ agents_docs_sync hooks enable  # git hookで自動テスト、AGENTS.md、README.md更新
```

・フックの無効化
```bash
user@hogehoge: ~$ agents_docs_sync hooks disable  # git hook無効化
```

・ヘルプ
```bash
user@hogehoge: ~$ agents_docs_sync --help

usage: agents_docs_sync [-h] [--version] [--config CONFIG] [--detect-only] [--no-api-doc] [--no-readme] {commit-msg,hooks} ...

汎用ドキュメント自動生成システム

positional arguments:
  {commit-msg,hooks}  実行するコマンド
    commit-msg        コミットメッセージ生成
    hooks             Git hooksの管理

options:
  -h, --help          show this help message and exit
  --version           show program's version number and exit
  --config CONFIG     設定ファイルのパス
  --detect-only       言語検出のみ実行
  --no-api-doc        APIドキュメントを生成しない
  --no-readme         READMEを更新しない
```

### 利点
* コミットごとに自動で検証・文書化が行われるため、ドキュメント不整合を防止。
* 変更箇所だけを即座に反映でき、手作業による更新の手間が大幅削減されます。

これらの機能は開発フロー全体で品質と一貫性を維持するために設計されています。
<!-- MANUAL_END:description -->
---

## 開発環境のセットアップ

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

   - LM Studioをインストール: https://lmstudio.ai/
   - モデルをダウンロードして起動
   - ベースURL: http://localhost:11434

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
npm test
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
   npm test
   uv run pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 09:55:00*
