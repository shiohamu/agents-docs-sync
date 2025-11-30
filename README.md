# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
**agents-docs-sync は、プロジェクト内のエージェント設定を自動的に解析し、整形された Markdown ドキュメント（`AGENTS.md` など）へ同期する CLI ツールです。**

### 主な機能
- **構成ファイルからデータ抽出**  
  `docgen/models/agents.py` に定義されている Pydantic モデル (`ProjectOverview`, `AgentsConfigSection`, `AgentsGenerationConfig`) を用いて、YAML／JSON 等の設定を正確にパースします。  
- **ドキュメント自動生成**  
  抽出した構造化データから Markdown を生成し、既存ドキュメントと差分がある場合のみ更新することで無駄な書き換えを防ぎます。  
- **CLI インターフェース**  
  `agents-docs-sync --help` により使用方法・オプション一覧を即座に確認でき、スクリプトや CI パイプラインから簡単呼び出し可能です（例：`.github/workflows/docs.yml`）。  
- **シンプルな統合**  
  `pyproject.toml` の `[project.scripts]` に登録されているエントリポイント (`docgen.docgen:main`) を利用することで、Python 環境を持つ任意のマシンで即座に実行できます。  

### アーキテクチャ
```
┌───────────────────────┐
│  CLI (agents-docs-sync) │   ← pyproject.toml entry point  
├─────────────┬───────────┤
│ parser      │ generator │   ← docgen/docgen.py 内で実装  
│             └───────────┘   
│                                                    
│   data models  (Pydantic) – docgen/models/agents.py    
│                                                    
└───────────────────────┘
```
- **Parser**：設定ファイルを読み込み、`AgentsConfigSection`, `AgentsGenerationConfig` 等のモデルへ変換。  
- **Generator**：各モデルから Markdown テンプレート（Jinja2 など）に埋め込んでドキュメント生成。差分検出は `git diff --name-only` を利用し、必要なファイルのみを書き込みます。

### 開発・運用
- **テスト**：pytest + coverage によりモデルと生成ロジックを網羅的に検証。  
- **CI/CD 連携**：GitHub Actions の `agents-docs-sync` スクリプトで自動同期が可能です（設定ファイル変更時のみ実行）。  

### 使用例
```bash
# インストール後の基本コマンド
$ agents-docs-sync --config path/to/agents.yaml

# ドキュメント確認用ヘルプ表示
$ agents-docs-sync --help
```

**まとめ**  
`agents-docs-sync` は、エージェント関連設定をコードベースとドキュメントの両方で一貫性を保つために設計された軽量ツールです。Python の標準的なパッケージング・スクリプト機能と Pydantic モデルによる型安全さが組み合わされ、プロジェクト全体のドキュメント品質向上へ直接寄与します。





## 使用技術

- Python
- Shell

## 依存関係

- **Python**: `pyproject.toml` または `requirements.txt` を参照

## セットアップ


## 前提条件

- Python 3.12以上



## インストール


### Python

```bash
# uvを使用する場合
uv sync
```




## LLM環境のセットアップ

### APIを使用する場合

1. **APIキーの取得と設定**

   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください




## ビルドおよびテスト

### ビルド

```bash
uv sync
```
```bash
uv build
```
```bash
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest tests/ -v --tb=short
```
```bash
npm test
```
```bash
go test ./...
```





---

*このREADME.mdは自動生成されています。最終更新: 2025-11-30 15:47:14*