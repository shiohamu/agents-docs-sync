# AGENTS ドキュメント

自動生成日時: 2025-11-22 18:10:21

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

`agents-docs-sync` はソースに変更がコミットされるたびに、以下の一連作業を自動で実行するパイプラインです。

1. **テスト実行**  
   - Python の単体テストは `uv run pytest`（標準）と詳細レポート用に `-v --tb=short` を併せて走らせます。  
   - Node.js 側のユニットテストも同時に起動し、フロントエンド側の整合性を確保します。

2. **ドキュメント生成**  
   - `docgen/docgen.py`（Python）を実行 (`uv run python3 docgen/docgen.py`) して最新の Sphinx/Markdown ドキュメントを作成し、変更内容が反映されるように保守します。

3. **AGENTS.md の自動更新**  
   - 上記ドキュメント生成結果から `agents` ディレクトリ内情報を抽出し、マークダウンファイルへ差分を書き込みます。  

### 主要技術
- Python（バージョンはプロジェクトルートで管理）  
- Shell スクリプトによるビルド・テストワークフロー統合

### 依存関係 (Python)
| ライブラリ | バージョン |
|------------|-----------|
| `pyyaml`   | ≥6.0.3     |
| `pytest`   | ≥7.4.0     |
| `pytest-cov` | ≥4.1.0  |
| `pytest-mock` | ≥3.11.1 |

### ビルド・テストコマンド
- **ビルド**: `uv run python3 docgen/docgen.py`
- **Python テスト**: `uv run pytest`, `uv run pytest tests/ -v --tb=short`
- **Node.js テスト**: `npm test`

### コーディング規約
プロジェクト全体は `ruff` をリンターとして使用し、コード品質と一貫性を保っています。

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

*このドキュメントは自動生成されています。最終更新: 2025-11-22 18:10:21*
