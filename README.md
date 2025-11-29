# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
**技術スタック**

- **言語**：Python 3.x（メインロジック）＋Bash／シェルスクリプト（CI・デプロイ補助）
- **ビルドツール**：Poetry（`pyproject.toml`で定義、エントリポイント `agents-docs-sync`, `agents_docs_sync`)
- **構成管理**：pydantic / dataclasses で読み込む `AgentsConfig` モデル (`docgen/models/agents.py:72`)  
- **ファイル操作**：Python 標準ライブラリ（pathlib, shutil）＋MD5/SHA256 チェックサム

---

### アーキテクチャ概要

```
┌─────────────────────┐
│  CLI (entry point)   │  ← agents-docs-sync → docgen.docgen:main()
├─────────────────────┤
│  config loader       │  load AgentsConfig from YAML/JSON
├─────────────────────┤
│  sync engine         │  compare source & target, copy/update files
├─────────────────────┤
│  docs generator      │  parse agent code → Markdown via Jinja templates
└─────────────────────┘
```

1. **CLI**  
   - `--help`で使い方を表示（RELEASE.md の「動作確認」セクション参照）。  
   - オプション: `-c/--config`, `-d/--dry-run`, `-v/--verbose`.

2. **構成管理** (`AgentsConfig`)  
   ```python
   class AgentsConfig(BaseModel):
       source_dir: Path          # 生成元コードのディレクトリ
       target_dir: Path          # ドキュメント出力先
       exclude_patterns: List[str] = []
       template_path: Optional[Path]
   ```

3. **同期エンジン**  
   - タイムスタンプとチェックサムで差分検知。  
   - 変更があれば `shutil.copy2`、削除されていれば対象ファイルを消去。  
   - dry‑run モードでは何が行われるかだけログに出力。

4. **ドキュメント生成**  
   - ソースコードの docstring を抽出し、Jinja テンプレートで Markdown へ変換。  
   - `docgen/docgen.py` 内に `generate_docs()` が実装されており、複数アジェントを一括処理。

---

### 主な機能

| 機能 | 内容 |
|------|------|
| **自動生成** | アクション・エージェントのコードから Markdown を自動作成。 |
| **同期管理** | ソースとターゲットディレクトリを常に一致させ、差分だけを反映。 |
| **dry‑run** | 変更予定ファイル一覧のみ表示し、本番実行前に確認可能。 |
| **カスタムテンプレート** | `template_path` を指定して独自フォーマットへ拡張可。 |
| **ロギング・通知** | 色付きログと verbosity レベルで進捗を分かりやすく表示。 |
| **CI/デプロイ統合** | シェルスクリプトから `agents-docs-sync` を呼び出し、GitHub Actions などに組み込み容易。 |

---

### 利用シナリオ

1. **開発フローの一部として**  
   - エージェントコードを更新したら CI が自動でドキュメント生成・同期を行い、最新状態を Wiki や Docs サイトへプッシュ。

2. **社内イントラネット用**  
   - 複数プロジェクトのエージェント仕様書を一元管理し、変更点だけを差分更新。  

3. **オープンソースリポジトリ**  
   - `agents-docs-sync` を pre‑commit フックとして設定し、ドキュメント漏れを防止。

---

### まとめ

- シンプルな CLI と構成ファイルで「エージェントのコード ↔ ドキュメント」を自動同期。  
- Python の標準ライブラリ＋pydantic を活用して堅牢に設計され、Poetry によるパッケージ化が容易です。  
- 既存ドキュメントを保守しつつ、新規エージェント追加時の手間を大幅削減できるツールとして実装されています。





## 使用技術

- Shell
- Python

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 11:35:08*