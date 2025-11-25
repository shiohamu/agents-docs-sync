# AGENTS ドキュメント

自動生成日時: 2025-11-25 11:06:48

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

**agents-docs-sync** は、Python と Shell スクリプトを組み合わせた GitHub Actions ベースの CI パイプラインです。  
コミットごとに以下の処理が自動で実行されます。

| 処理 | 目的 |
|------|------|
| **テスト実行**（`uv run pytest`, `npm test`） | コード品質を保ち、回帰を防止します。 |
| **ドキュメント生成** (`uv run python3 docgen/docgen.py`) | YAML 定義ファイルから最新の AGENTS.md を作成し、プロジェクト内に反映させます。 |
| **AGENTS.md 自動更新** | コミット時点で正確なドキュメントを保持します。 |

### 主要技術
- **Python (3.11+)**
  - `pyyaml`（≥6.0.3）: YAML の読み込み・書き出しに使用。
  - `pytest`, `pytest-cov`, `pytest-mock`: テスト実行とカバレッジ計測、モック機能を提供。
- **Shell**  
  スクリプトでビルドやテストコマンドの呼び出しを自動化。

### CI/CD 設定
GitHub Actions のワークフローは以下のステップで構成されています。  

1. コードが `main` ブランチへ push または PR が作られたときにトリガー  
2. 依存関係をインストール（`uv pip install -r requirements.txt`）  
3. テスト実行 (`uv run pytest`, `npm test`)  
4. ドキュメント生成 (`uv run python3 docgen/docgen.py`)  
5. 必要に応じて自動コミットしてプッシュ

### コーディング規約
- **リンター**: `ruff` を使用し、コード品質と一貫性を確保します。  

> これらの手順はすべてパイプライン内で実行されるため、人為的なミスやドキュメントの不整合が発生するリスクを最小化しています。

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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 11:06:48*
