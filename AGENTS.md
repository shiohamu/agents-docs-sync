# AGENTS ドキュメント


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->

自動生成日時: 2025-11-26 06:34:02

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要


agents-docs-sync は、コミットごとに自動でテストを実行し、ドキュメント（docgen）を生成して `AGENTS.md` を更新する CI/CD パイプラインです。  
Python とシェルベースのツールを組み合わせて構築されており、以下のフローが走ります。

1. **ビルド** – 依存関係は `uv sync` により解決し、`uv build` でパッケージング。  
2. **テスト実行** – Python 用に `pytest`, Node.js の npm test, Go の go test を同時に走らせます。  
3. **ドキュメント生成** – `python3 docgen/docgen.py` が API ドキュメントを作成し、最新情報で `AGENTS.md` を更新します。

### 主要依存関係

- Python: `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`
- コーディング規約は **ruff** を使用し、プロジェクト全体で統一されたスタイルを保ちます。

### 実行手順

```bash
# 依存関係のインストールとビルド
uv sync && uv build

# ドキュメント生成（AGENTS.md の更新も含む）
uv run python3 docgen/docgen.py

# テスト実行 (Python)
uv run pytest tests/ -v --tb=short

# npm test で JavaScript / TypeScript 用テスト
npm test

# Go パッケージの単体テスト
go test ./...
```

### 開発者向けヒント

- **CI/CD**: このリポジトリは GitHub Actions 等に組み込むことで、プッシュ時・PR 時自動化できます。  
- **ドキュメント更新頻度**: `docgen.py` は変更があった際だけ再生成するよう最適化されているため、大規模プロジェクトでも高速です。  
- **エージェントの利用**: AGENTS.md が自動で最新情報に保たれるので、AI エージェントは常に正確なインタフェース仕様を参照できます。

この仕組みにより、コードベースとドキュメントが同期し続けるため、開発者や AI アシスタントの作業効率向上につながります。
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

### ビルド手順


```bash
uv sync
uv build
uv run python3 docgen/docgen.py
```


### テスト実行


```bash
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```


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

<!-- MANUAL_START:pr -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash


   uv run pytest tests/ -v --tb=short

   npm test

   go test ./...


   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:pr -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 06:34:02*