# AGENTS ドキュメント

自動生成日時: 2025-11-25 10:36:02

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

**agents-docs-sync** は、GitHub Actions を利用した CI/CD パイプラインであり、コミットごとにテスト実行・ドキュメント生成を自動化し、その結果 `AGENTS.md` も最新の状態へ更新します。  

### 主な処理フロー  
1. **ビルド**：  
   ```bash
   uv run python3 docgen/docgen.py
   ```  
   Python スクリプトがプロジェクト全体から API/クラス情報を抽出し、Markdown ドキュメントへ変換します。  

2. **テスト実行**（Python & Node.js）：  
   - `uv run pytest`  
   - `npm test`  
   - `uv run pytest tests/ -v --tb=short`  
   これにより両言語の単体・統合テストが網羅的に走ります。  

3. **AGENTS.md 更新**：  
   ドキュメント生成後、スクリプトが自動で `AGENTS.md` を再構築し、最新情報を反映します。

### 技術スタック
| 言語 | ツール / ライブラリ |
|------|---------------------|
| Python | uv, pyyaml≥6.0.3, pytest≥7.4.0, pytest-cov≥4.1.0, pytest-mock≥3.11.1 |
| Shell  | Bash（スクリプト実行） |

### コーディング規約
- **Linting**：`ruff`

### 実装ポイント  
* `uv` は高速な依存関係管理と仮想環境構築を提供。  
* カスタムドキュメント生成 (`docgen/docgen.py`) により、手動での Markdown 更新作業が不要に。  

このパイプラインはコミットごとに最新かつ正確な API 仕様・使い方情報を保証し、開発者間の情報共有を円滑化します。

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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 10:36:02*
