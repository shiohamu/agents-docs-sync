# AGENTS ドキュメント

自動生成日時: 2025-11-25 17:52:03

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
`agents-docs-sync` は、ソースコードに変更が加えられるたびに自動的にテストを実行し、最新のドキュメントと `AGENTS.md` を生成・更新するCI/CDパイプラインです。  
主な特徴は以下の通りです。

- **言語**: Python（ビルド／テスト）＋シェルスクリプト（環境構築や補助処理）
- **自動化フロー**
  1. コミット時に GitHub Actions が起動  
     → `uv` を使って仮想環境をセットアップ
  2. Python テスト (`pytest`) とコードカバレッジ測定（`pytest-cov`）実行  
     → エラーがあればビルド失敗で通知
  3. ドキュメント生成スクリプト `docgen/docgen.py` を実行し、YAML/Markdown ファイルを更新  
     → 依存関係や使用例を自動的に反映
  4. 更新された `AGENTS.md` がコミットされることでドキュメントが常に最新状態になる

- **主要コマンド**
  - ビルド: `uv run python3 docgen/docgen.py`
  - テスト:  
    ```bash
    uv run pytest          # 全テスト実行（デフォルト）
    npm test               # Node.js 環境での追加チェック
    uv run pytest tests/ -v --tb=short   # 詳細出力付き
    ```
- **依存ライブラリ**
  ```yaml
  pyyaml>=6.0.3
  pytest>=7.4.0
  pytest-cov>=4.1.0
  pytest-mock>=3.11.1
  ```

- **コーディング規約**  
  - 静的解析とリンティングは `ruff` を使用。`.pyproject.toml` に設定を記述し、CI 上で自動チェックされます。

> ⚡️ *開発者向けヒント*  
> ビルドやテストが失敗した場合は、ログに表示されたエラー箇所から修正を行い、再度コミットしてください。`AGENTS.md` は手作業で編集する必要はありません。

このパイプラインにより、コードベースとドキュメントの同期性を保ちながら開発サイクルを高速化できます。
<!-- MANUAL_END:description -->

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
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

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください

<!-- MANUAL_END:setup -->

---

## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順


ビルド手順は設定されていません。


### テスト実行


テストコマンドは設定されていません。

<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->



### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```




<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:other -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   
   # テストコマンドを実行
   
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 17:52:03*


---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 17:52:35*
