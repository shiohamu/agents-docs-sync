# AGENTS ドキュメント

自動生成日時: 2025-11-21 14:50:50

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

`agents-docs-sync` は GitHub に push された変更をトリガーとして実行される CI/CD パイプラインです。主な機能は以下の通りです。

- **ドキュメント自動生成**  
  Python スクリプト `docgen/docgen.py` を使用し、YAML 設定から Markdown ドキュメントを作成します。
- **テスト実行とカバレッジ報告**  
  Pytest ベースの単体・統合テストが自動で走り、コード品質を保証します。

### 技術スタック
| コンポーネント | バージョン要件 |
|-----------------|---------------|
| Python          | 3.11+         |
| Shell           | Bash (POSIX)  |

#### 主な依存ライブラリ
- `pyyaml>=6.0.3`
- `pytest>=7.4.0`
- `pytest-cov>=4.1.0`
- `pytest-mock>=3.11.1`

### ビルド & テストコマンド

| タスク | コマンド |
|--------|----------|
| ドキュメント生成 | `uv run python3 docgen/docgen.py` |
| 単体テスト   | `uv run pytest` <br> `uv run python3 -m pytest test` <br> `uv run pytest tests/ -v --tb=short` |

### コーディング規約
- **リンター**：`ruff`

これらを組み合わせることで、リポジトリ内の変更が即座に最新ドキュメントへ反映され、品質保証も同時に行われます。

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

*このドキュメントは自動生成されています。最終更新: 2025-11-21 14:50:50*
