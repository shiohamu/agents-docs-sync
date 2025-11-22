# AGENTS ドキュメント

自動生成日時: 2025-11-22 18:49:05

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
このリポジトリは、コミットが行われるたびに自動で以下の処理を実行するパイプラインです。

1. **テスト実行**
   - Python テスト：`uv run pytest`（カバレッジ付き）
   - JavaScript テスト：`npm test`
   - 詳細表示と短いトレースバックでの再確認: `uv run pytest tests/ -v --tb=short`

2. **ドキュメント生成**
   ビルドコマンドは `uv run python3 docgen/docgen.py`。
   これにより、YAML 定義から自動的に Markdown ドキュメントが作成されます（依存ライブラリ：`pyyaml>=6.0.3`）。

3. **AGENTS.md の更新**
   - 自動生成されたドキュメントを元に AGENTS.md 内の該当セクションを書き換え、常に最新状態を保持します。

### 主要な技術・ツール

- **言語**: Python, Shell
- **依存関係**
  - `pyyaml>=6.0.3`
  - `pytest>=7.4.0`
  - `pytest-cov>=4.1.0`
  - `pytest-mock>=3.11.1`
- **ビルド**: `uv run python3 docgen/docgen.py`
- **テスト**: 上記の pytest と npm test
- **コーディング規約**: Ruff リンター

### 使用方法

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

*このドキュメントは自動生成されています。最終更新: 2025-11-22 18:49:05*
