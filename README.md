# agents-docs-sync

> **A CI pipeline tool that runs tests, generates documentation and automatically updates `AGENTS.md` on every commit.**

---

## 1️⃣ プロジェクト名と概要  

**agents‑docs‑sync** は、Python とシェルスクリプトで構成された小規模なユーティリティです。  
コミットごとに次の処理を自動化します。

| 処理 | 内容 |
|------|-------|
| **テスト実行** | `pytest`（Python） + `npm test`（Node.js）で単体・統合テストを走らせます。 |
| **ドキュメント生成** | `docgen/docgen.py` を呼び出し、YAML から Markdown ドキュメントへ変換します。 |
| **AGENTS.md 更新** | 自動的に最新のエージェント情報を反映したマークダウンファイルを書き込みます。 |

---

## 2️⃣ セットアップ手順・インストール方法  

### Prerequisites  
- `uv`（Python パッケージ管理ツール）: <https://github.com/astral-sh/uv>  
- Node.js (v18+): <https://nodejs.org/>  
- Git

```bash
# 1. クローン
git clone https://github.com/<your-org>/agents-docs-sync.git
cd agents‑docs‑sync

# 2. Python 環境を作成して依存関係インストール
uv sync   # uv が未導入の場合は pipx install uv を実行してください。

# 3. Node.js のパッケージもインストール（必要に応じて）
npm ci

```

> **Tip**  
> `uv` は Poetry と同等の機能を持つ軽量ツールです。`pyproject.toml` に依存関係が記述されているので、単一コマンドで環境構築できます。

---

## 3️⃣ 使用方法・使用例  

### ドキュメント生成（手動）  
```bash
uv run python3 docgen/docgen.py
```
実行後は `docs/` ディレクトリに Markdown ファイルが作成され、同時に `AGENTS.md` が更新されます。

> **NOTE**  
> スクリプトは YAML 配下のエージェント定義を読み取り、対応するマークダウンへ変換します。YAML のフォーマット変更は自動で反映されます。

### テスト実行（手動）  

```bash
# Python 用テスト
uv run pytest

# Node.js 用テスト
npm test

# 詳細出力付き
uv run pytest tests/ -v --tb=short
```

---

## 4️⃣ コマンドの例  

| タスク | 実行コマンド |
|--------|--------------|
| **ドキュメント生成** | `uv run python3 docgen/docgen.py` |
| **Python テスト実行** | `uv run pytest`<br>`uv run pytest tests/ -v --tb=short` |
| **Node.js テスト実行** | `npm test` |

> すべてのコマンドはプロジェクトルートから呼び出してください。

---

## 5️⃣ 技術スタック  

- **言語**
  - Python (3.11+)
  - Shell
- **パッケージ管理 / ビルドツール**  
  - `uv`（Python）  
  - npm（Node.js）
- **テストフレームワーク**  
  - Pytest (`pytest`, `pytest-cov`, `pytest-mock`)  
  - Jest/その他 Node テスティングライブラリ
- **Lint / コーディング規約**
  - Ruff (Python Linter)
- **ドキュメント生成**
  - Python スクリプト（`docgen/docgen.py`）と PyYAML

---

## 6️⃣ その他の情報  

<!-- MANUAL_START:LICENSE -->
### ライセンス  
本プロジェクトは MIT License の下で公開されています。詳細については `LICENSE` ファイルをご覧ください。
<!-- MANUAL_END:LICENSE -->

<!-- MANUAL_START:CREDITS -->
### クレジット
- Python 社の PyYAML、pytest エコシステムに感謝します  
- Node.js 開発者コミュニティへも敬意を表します
<!-- MANUAL_END:CREDITS -->

> **フォローアップ**  
> CI/CD 環境（GitHub Actions, GitLab CI 等）でこのリポジトリの `main` ブランチにプッシュするたびに自動実行されるよう設定すると、ドキュメントとテストを常に最新状態に保てます。  
> 具体的なワークフローファイルはプロジェクトルートの `.github/workflows/ci.yml` に記載しています。

---