# AGENTS ドキュメント

自動生成日時: 2025-11-27 14:12:13

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


このプロジェクトは、ソースコードにコミットが入るたびに以下のタスクを自動で実行する CI/CD パイプラインです。  
* **テスト**（Python/Node.js/Golang） → 失敗したらビルド停止  
* **ドキュメント生成** (`docgen/docgen.py`) → 最新情報を反映し、`AGENTS.md` を更新  
* **コード品質チェック** (Ruff)  

### 主な構成
| 要素 | 内容 |
|------|------|
| 言語 | Python（メイン）＋Shell スクリプトで補完 |
| 依存関係 | `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` (Python) |
| ビルドツール | **uv**（パッケージ管理・実行） |

### 実行フロー
```bash
# 依存関係の同期とビルド
$ uv sync          # requirements の解決
$ uv build         # バイナリ/パッケージ作成

# ドキュメント生成スクリプトを実行し、AGENTS.md を更新
$ uv run python3 docgen/docgen.py

# テストの走査（Python, Node.js, Go それぞれ）
$ uv run pytest tests/ -v --tb=short      # Python 用
$ npm test                                 # JavaScript 用
$ go test ./...                            # Golang 用
```

### コーディング規約・Lint
* **Ruff** を使用して静的解析とフォーマットを自動で行います。  
  ```bash
  $ ruff check . --fix   # 問題点の検出＆修正候補提示
  ```

### 利用シナリオ（AI エージェント向け）
1. **コミット** → GitHub Actions がトリガー。
2. 上記ビルド・テストスクリプトが走り、すべて合格したら `AGENTS.md` を最新化。  
3. 失敗時は該当ステップで停止し、通知を送る（例: Slack, Teams）。  

このパイプラインにより、ドキュメントとコードの整合性が保たれ、エージェント開発者は常に最新状態の `AGENTS.md` を参照できます。
**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->

<!-- MANUAL_END:setup -->
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

<!-- MANUAL_END:other -->



### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```





---

## プルリクエストの手順

<!-- MANUAL_START:pr -->

<!-- MANUAL_END:pr -->
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



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 14:12:13*