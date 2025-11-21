# AGENTS ドキュメント

自動生成日時: 2025-11-21 17:02:25

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
このリポジトリは **agents-docs-sync** パイプラインを実装しており、コミットごとに品質保証とドキュメントの自動更新を行います。

- **主なフロー**
  - `pytest` を使ってユニットテストを実行し、エージェントコードが期待通りに機能することを検証します。
  - `docgen/docgen.py` により最新の Markdown ドキュメントを生成します。
  - 自動でトップレベルの **AGENTS.md** を再構築し、全てのエージェントファイルとそのドキュメンテーション文字列が反映されるようにします。

- **技術スタック**
  - Python 3（≥3.10）  
    * `pyyaml >=6.0.3` – YAML 設定をパース。  
    * `pytest >=7.4.0`, `pytest-cov >=4.1.0`, `pytest-mock >=3.11.1` – テスト・カバレッジツール。
  - Shell スクリプトでパイプラインの各ステップをオーケストレーション。

- **ビルド & テストコマンド**
  ```bash
  # ドキュメント生成（ビルド）
  uv run python3 docgen/docgen.py

  # テスト実行（複数エイリアスあり）
  uv run pytest
  uv run python3 -m pytest test
  uv run pytest tests/ -v --tb=short
  ```

- **コーディング規約**
  コードは `ruff` によって linting が実施され、PEP‑8 の遵守と一般的なバグ検出が保証されています。

このセットアップにより、コミットごとにクリーンで完全ドキュメント化されたエージェント集合のスナップショットを生成しつつ、CI パイプラインは軽量かつ再現性高く保たれます。
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

*このドキュメントは自動生成されています。最終更新: 2025-11-21 17:02:25*
