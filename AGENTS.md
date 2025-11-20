# AGENTS ドキュメント

自動生成日時: 2025-11-20 10:34:13

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

**agents‑docs-sync** は、Python・JavaScript（TypeScript もサポート）と C の三言語で構築された軽量 CI/CD パイプラインです。
主に以下の機能を提供します。

- **ドキュメント自動生成** – `python3 docgen/docgen.py` を実行して、プロジェクト全体の API ドキュメントや設定ファイルを書き出す。
- **統合テストサポート** – Python 版では `pytest`, JavaScript/TypeScript は Jest（推奨）、C のユニットテストは CMocka 等で実装可能。
  テストの実行例:
  ```bash
  python3 -m pytest test          # Pytest 実行 (カバレッジ付き)
  pytest tests/ -v --tb=short     # 詳細出力と短いトレースバック
  ```
- **依存関係管理** – Python は `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` を必須。
  JavaScript/TypeScript と C のビルド・テストはそれぞれのツールチェーンで管理。

**使用技術**

- Python (3.x)
- JavaScript / TypeScript
- C

<!-- MANUAL_END:description -->

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
uv sync
uv run python3 docgen/docgen.py
```

### テスト実行

#### APIを使用する場合

```bash
uv run pytest
uv run pytest tests/ -v --tb=short
uv run python3 -m pytest test
```

#### ローカルLLMを使用する場合

```bash
uv run pytest
uv run pytest tests/ -v --tb=short
uv run python3 -m pytest test
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
   uv run pytest tests/ -v --tb=short
   uv run python3 -m pytest test
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このドキュメントは自動生成されています。最終更新: 2025-11-20 10:34:13*
