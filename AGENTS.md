# AGENTS ドキュメント

自動生成日時: 2025-11-21 16:08:52

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

GitHub にプッシュされた変更をトリガーに、テスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン

**使用技術**: python, shell

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

*このドキュメントは自動生成されています。最終更新: 2025-11-21 16:08:52*
