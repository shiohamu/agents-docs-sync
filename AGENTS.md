# AGENTS ドキュメント


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->

自動生成日時: 2025-11-26 06:25:33

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要


プロジェクト `agents-docs-sync` は、コミットごとに自動でテストを実行し、最新のドキュメントを生成して **AGENTS.md** を更新する CI パイプラインです。  
主な機能は以下の通りです。

- **Python とシェルスクリプトによる構成**：`docgen/docgen.py` が Python で書かれ、ビルド・テストをまとめた Bash スクリプトも同梱しています。
- **依存関係管理**  
  - `uv sync`: 必要なパッケージ（pyyaml, pytest 系統など）をインストールします。  
  - パッケージはすべて最新版で互換性が保証されています (`>=` バージョン指定)。
- **ビルドプロセス**  
  ```bash
  uv sync          # 依存関係の同期
  uv build         # ビルド（必要に応じたコンパイルやバイナリ生成）
  uv run python3 docgen/docgen.py   # ドキュメントを生成し AGENTS.md を更新
  ```
- **テスト実行**  
  - Python: `uv run pytest tests/ -v --tb=short`（カバレッジ付き）  
  - JavaScript/TypeScript: `npm test`  
  - Go (外部モジュールが含まれる場合): `go test ./...`
- **コード品質**  
  - Linter：`ruff` を使用し PEP8 / 型ヒントのチェックを行います。CI 側で自動実行され、コミット前に修正するよう促します。

### ワークフロー

1. コード変更 → Git Push  
2. CI がトリガーされる  
3. `uv sync` で依存関係が再確認・インストール  
4. テスト実行（失敗するとビルドは中断）  
5. 成功時に `docgen.py` を走らせて最新の API ドキュメントを生成し、**AGENTS.md** の該当セクションが自動更新される。  

### 使い方

```bash
# 開発環境セットアップ（uv がインストール済み）
uv sync          # Python パッケージを取得
npm install      # JavaScript/TypeScript 用パッケージ
go mod download   # Go モジュールのダウンロード

# ローカルでビルド・テスト実行
uv build
uv run python3 docgen/docgen.py
uv run pytest tests/
npm test
go test ./...

# コード整形と静的解析（手動）
ruff check . --fix   # 形式を修正する場合
```

### 注意点

- **AGENTS.md** は自動生成されるため、マニュアルで編集したい箇所は `<!-- MANUAL_START -->` … `<!-- MANUAL_END -->` のような手動セクションに限定してください。  
- CI では最新の依存関係を使用するので、ローカル環境と同一バージョンになることが推奨されます（`.uv.lock` が管理します）。  

この仕組みにより、ドキュメントは常にコードベースと同期し、AI エージェントや開発者が最新情報を即座に参照できるようになっています。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 06:25:33*