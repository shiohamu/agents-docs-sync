# AGENTS ドキュメント

自動生成日時: 2025-11-27 21:58:10

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、コミットごとに自動でテスト実行・ドキュメント生成・AGENTS.md の更新を行う CI パイプラインです。  
主なフローは以下の通りです。

1. **依存関係インストール** – `uv sync` で Python 用パッケージ（pyyaml, pytest 系など）と Node.js / Go 環境が揃います。
2. **ビルド・実行** –  
   - `uv build` によりプロジェクトのビルドを完了。  
   - `uv run python3 docgen/docgen.py` を走らせ、現在のコードベースから API/CLI ドキュメントを YAML 形式で生成します。
3. **テスト実行** – Python (`pytest tests/`)・Node.js（npm test）・Go（go test ./…）それぞれの言語環境でユニット／統合テストが走ります。  
4. **AGENTS.md 更新** – 生成されたドキュメントをもとに AGENTS.md を差分反映させ、変更点をコミットします。
5. **コード品質チェック** – `ruff` がスタイル・構文の整合性を確認し、問題があればビルド失敗で修正を促します。

### 主要なポイント
- **多言語サポート**：Python, Node.js, Go のテストと依存管理が一元化されているため、一貫した品質保証が可能です。  
- **自動更新機構**：`docgen.py` は YAML をパースし、AGENTS.md へ必要なセクションを差分で追加/置換しますので、人手によるドキュメント整合性のリスクが低減されます。  
- **簡易実行方法**：ローカル開発者は `uv sync && uv build && uv run python3 docgen/docgen.py` だけでビルドと文書生成を完了でき、CI と同一環境で動作確認が可能です。

このプロジェクトにより、コードベースの変更ごとに最新かつ正確なエージェント仕様を書面化し、開発チーム全体へ即時共有することが実現できます。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 21:58:10*