# AGENTS ドキュメント

自動生成日時: 2025-11-21 09:34:21

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

**agents‑docs-sync** は、Python・JavaScript（TypeScript もサポート）と C の三言語で構築された軽量 CI/CD パイプラインです。
主にコードベースのドキュメントを自動生成し、複数リポジトリ間で同期する機能を提供します。

### 主な特徴
- **多言語対応**：Python, JavaScript/TypeScript, C のソースから統一された Markdown / reStructuredText を作成
- **CI/CD 連携**：GitHub Actions 等のワークフローで簡単に組み込めるよう設計
- **高速ビルド**：`python3 docgen/docgen.py` により、依存関係を最小化した軽量な実行環境

### 主要コンポーネント
| コンポーネント | 概要 |
|-----------------|------|
| `docgen/`        | Python スクリプトでソース解析・ドキュメント生成 |
| `tests/`         | pytest を用いたユニットテスト（Python）と Jest などの JS テスト (省略) |

### 開発環境
- **依存ライブラリ**
  - Python: `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`
- **ビルドコマンド**
  ```bash
  python3 docgen/docgen.py
  ```
- **テスト実行例**
  ```bash
  pytest
  python3 -m pytest test
  pytest tests/ -v --tb=short
  ```

### コーディング規約
- Python は `ruff` を使用したリンティングを推奨
- JavaScript / TypeScript のスタイルは ESLint (設定ファイル未提供)

<!-- MANUAL_END:description -->

---

## 開発環境のセットアップ

### 前提条件

- Python 3.12以上
- Node.js 18以上

### 依存関係のインストール

#### Python依存関係

```bash
pip install -r requirements-docgen.txt
pip install -r requirements-test.txt
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
python3 docgen/docgen.py
```

### テスト実行

#### ローカルLLMを使用する場合

```bash
pytest
python3 -m pytest test
pytest tests/ -v --tb=short
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
   pytest
   python3 -m pytest test
   pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このドキュメントは自動生成されています。最終更新: 2025-11-21 09:34:21*
