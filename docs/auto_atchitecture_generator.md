# 実装手順

## 前提準備

1. リポジトリをローカルにクローンする。

   ```bash
   git clone https://github.com/shiohamu/agents-docs-sync
   cd agents-docs-sync
   ```
2. 開発用ブランチを作成する。

   ```bash
   git checkout -b feat/architecture-generation
   ```
3. 必要パッケージを追加（仮想環境推奨）。`requirements-docgen.txt` を新規作成または既存に追記：

   ```
   diagrams
   pydantic
   pyyaml
   jinja2
   pydot
   ```

   インストール：

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-docgen.txt
   ```

## 1. Pydantic モデル追加

1. `docgen/models/arch.py` を作成。`ArchitectureManifest` と `Service` の型を定義する。
2. モデルは JSON/YAML の入出力に対応させる（`BaseModel` を継承）。

## 2. リポジトリ走査パーサ実装

1. `docgen/parsers/arch_parser.py` を作成。以下の機能を実装する：

   * リポジトリルートを受け取り `ArchitectureManifest` を返す関数 `scan_repo_for_arch(root: Path)` を用意。
   * `docker-compose.yml` 検出とパース（サービス名・ports・depends_on を抽出）。
   * `Dockerfile` の `EXPOSE` 抽出。
   * `k8s` マニフェスト（`Service`/`Deployment`）の検出。
   * `package.json` / `requirements.txt` 等のヒューリスティクス（フレームワークや言語判定）をオプション実装。
2. 出力を `ArchitectureManifest` インスタンスで返す。

## 3. Diagrams ジェネレータ実装

1. `docgen/generators/arch_generator.py` を作成。以下を実装：

   * `generate_diagram(manifest: ArchitectureManifest, outdir: Path, format: str="png") -> Path` 関数。
   * `map_type_to_cls` で manifest の `type` を `diagrams` のクラス名にマップするロジック。
   * `jinja2` テンプレートまたは直接 `diagrams` API を使い、`Cluster` とノード・エッジを生成。
   * 生成後、出力ファイルパスを返す（例 `outdir/architecture.png`）。
2. エラー時は例外を投げる設計にする。

## 4. CLI / docgen 統合

1. 既存の `docgen` CLI 起点（`docgen/docgen.py` 等）にフラグ/コマンド `generate-arch` を追加：

   * フロー：`scan_repo_for_arch()` → YAML/JSON を `docs/arch_manifest.yml` に書き出し → `generate_diagram(...)` を実行 → `docs/architecture.{png,svg}` を出力。
2. 既存の `tools/gen_agents_md.py` 等と同様のログ出力・エラーハンドリングを行う。

## 5. 出力/マニフェストの保存ルール

1. 生成マニフェストを `docs/arch_manifest.yml` に保存する。
2. 生成図を `docs/architecture.png`（および `docs/architecture.svg` をオプション）として保存する。
3. CI の自動コミットを行う場合は生成物用ブランチまたは PR 作成フローを採る（直接コミットはループに注意）。

## 6. テスト

1. `tests/test_arch_parser.py` を追加：

   * サンプル `docker-compose.yml` / `Dockerfile` / k8s YAML を用意して `scan_repo_for_arch` の出力を検証する。
2. `tests/test_arch_generator.py` を追加：

   * 簡易 manifest を生成し、`generate_diagram` を実行して出力ファイルが存在することを検証する。
3. CI で `pytest` を実行する（`python -m pytest tests`）。

## 7. CI ワークフロー追加

1. 新規ワークフロー `/.github/workflows/generate-architecture.yml` を追加（Push/PR トリガー）。主要ステップ：

   * `actions/checkout`
   * Python セットアップ
   * 依存インストール (`pip install -r requirements-docgen.txt`)
   * `python -c "from docgen.parsers.arch_parser import scan_repo_for_arch; m=scan_repo_for_arch(Path('.')); open('docs/arch_manifest.yml','w').write(m.json())"`
   * `python -c "from docgen.generators.arch_generator import generate_diagram; ..."`
   * `actions/upload-artifact` で `docs/architecture.*` を保存
2. 自動コミット方式を採るなら別ジョブで `git config`→commit→push を行う（ループ防止のため `paths-ignore` またはコミットユーザ判定を実装）。

## 8. ドキュメント追記

1. `README.md` の `docgen` セクションに新機能の使い方（ローカル実行コマンド、CI の有効化方法、manifest の編集方法）を追記する。
2. `docs/arch_manifest_schema.md` を作成して manifest スキーマを明確化する。

## 9. サンプル/PoC を追加

1. `examples/arch_poc/` を作成し、サンプル `docker-compose.yml`, `Dockerfile`, 期待される `arch_manifest.yml` を置く。
2. `examples/README.md` に「実行手順」を記載：

   ```bash
   python -m docgen.cli generate-arch
   ls docs/architecture.*
   ```

## 10. コード品質・レビュー準備

1. Lint/フォーマット：`flake8` / `black` を実行してコード整形する。
2. ユニットテストを追加してカバレッジを確認する。
3. 変更をコミットして PR を作成する。

   ```bash
   git add .
   git commit -m "feat: add architecture generation (parser + generator + CI)"
   git push origin feat/architecture-generation
   ```
4. PR の説明テンプレートに「変更点」「実行手順」「CI の動作確認方法」「既知の制約」を記載する。

## 11. ロールアウト

1. PR マージ後、CI が正常に生成物を作ることを確認する（アーティファクト／PR コメント）。
2. 必要なら生成図をドキュメントに埋め込む（`docs/` 内の README に画像リンクを追加）。
3. 運用ルールをチームに共有（manifest の手動編集ルール、生成頻度、PR ワークフロー）。

## 12. 拡張計画（今後のタスク）

1. AST ベースの言語解析（Python/JS/Java 等）の追加。
2. OpenAPI / Tracing（OTel）データからの依存検出統合。
3. カスタムアイコン対応（`docs/icons/` に収め `Custom` で利用）。
4. 大規模グラフ向けに DOT 生成モードと `sfdp` 等レイアウトエンジンの導入。

---

以上の手順に従って実装・テスト・CI 組込みを行ってください。
