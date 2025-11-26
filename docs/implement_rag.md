# 実装計画 — `agents-docs-sync` に RAG 機能を追加してコンテキスト強化型ドキュメント生成を実現する

本ドキュメントは `shiohamu/agents-docs-sync` プロジェクトに RAG（Retrieval-Augmented Generation）機能を追加するための実装計画です。このプロジェクトは既に以下の基盤を持っています：

- **既存のLLMクライアント**: OpenAI、Anthropic、ローカルLLM（Ollama、LM Studio）対応済み（`docgen/utils/llm_client.py`）
- **プロンプト管理**: YAMLベースのプロンプトローダー（`docgen/utils/prompt_loader.py`）
- **ドキュメント生成**: agents、README、commit messageの生成機能（`docgen/generators/`）
- **設定管理**: 柔軟な設定システム（`docgen/config.yaml`）

RAG機能を追加することで、コードベース全体から関連情報を抽出し、より正確で根拠のあるドキュメントを生成します。実装は **段階的かつオプトイン型** で進め、既存機能を壊さないことを最優先します。

---

# 目次

1. 概要と方針
2. 主要ディレクトリ / ファイル設計
3. フェーズ1 — 最小実装（ローカルで動く RAG を追加）
4. フェーズ2 — 生成 → 検証 → ドラフト出力の自動化（安全重視）
5. フェーズ3 — 運用改善（差分再埋め込み、再ランク、CI の選択）
6. テスト / CI / pre-commit の追加
7. プロンプトテンプレート（AGENTS.md / README）
8. リスクと安全対策
9. 実行コマンド集 & チェックリスト

---

# 1. 概要と方針

* **目的**：ローカルで RAG を行い、その結果を根拠付きでローカルLLMに渡して `AGENTS.md` と `README.md` のドラフトを生成できるようにする。生成は **オプトイン（`--use-rag`）**。自動コミットは行わず、ドラフトを PR（または手動確認）で扱う運用とする。
* **前提**：ローカルに LLM を立てて HTTP で呼べる（例：Ollama / text-generation-webui など）か、呼び出しラッパーを用意する。
* **最小依存**：`sentence-transformers`, `hnswlib`（または `faiss-cpu`）と `requests`。

---

# 2. 主要ディレクトリ / ファイル設計（追加／変更）

## 新規追加ファイル

```
docgen/
  rag/                          # RAG機能モジュール（新規ディレクトリ）
    __init__.py                 # RAGモジュール初期化
    chunker.py                  # コードベースのチャンク化（言語別パーサー対応）
    embedder.py                 # テキスト埋め込み生成（sentence-transformers使用）
    indexer.py                  # ベクトルインデックス管理（hnswlib/faiss）
    retriever.py                # 類似度検索・チャンク取得
    validator.py                # 生成ドキュメントの検証（出典チェック、幻覚検出）
  index/                        # ベクトルインデックスストレージ（.gitignore対象）
    meta.json                   # インデックスメタデータ（チャンクハッシュ等）
    hnswlib.idx                 # HNSWインデックスファイル
```

## 既存ファイルの変更

```
docgen/
  docgen.py                     # --use-rag フラグ追加、RAGモード分岐
  config.yaml.sample           # RAG設定セクション追加
  generators/
    base_generator.py          # RAGコンテキスト統合メソッド追加
    agents_generator.py        # RAG対応プロンプト生成
    readme_generator.py        # RAG対応プロンプト生成
  utils/
    llm_client.py              # 既存（変更不要、そのまま活用）
    prompt_loader.py           # 既存（変更不要、そのまま活用）
  prompts/
    agents_prompts.yaml        # RAG用プロンプトテンプレート追加
    readme_prompts.yaml        # RAG用プロンプトテンプレート追加
.gitignore                     # docgen/index/ 追加
requirements-docgen.txt        # sentence-transformers, hnswlib 追加
```

## 設計原則

1. **既存コードの尊重**: 既存のLLMクライアント、プロンプトローダーをそのまま活用
2. **オプトイン**: RAG機能はフラグ制御でオフにできる
3. **段階的移行**: まずは読み取り専用のインデックス構築から開始

---

# 3. フェーズ1 — 最小実装（RAGインデックス構築と基本検索）

目的：既存のdocgenシステムに影響を与えず、RAGインデックスを構築し、基本的な検索機能を実装する。

## 作業項目

### 1. RAGモジュールの基礎実装

**1.1 `docgen/rag/__init__.py`**
```python
# RAGモジュールのエクスポート
from .chunker import CodeChunker
from .embedder import Embedder
from .indexer import VectorIndexer
from .retriever import DocumentRetriever
```

**1.2 `docgen/rag/chunker.py`**
- コードベース全体をチャンク化（既存の`collectors`モジュールを活用）
- Pythonファイル: 関数/クラス単位でチャンク
- Markdownファイル: ヘッダ単位でチャンク
- 設定ファイル（YAML/TOML）: セクション単位でチャンク
- メタデータ: `{"file": Path, "type": str, "name": str, "text": str, "start_line": int, "end_line": int, "hash": str}`

**1.3 `docgen/rag/embedder.py`**
- `sentence-transformers` を使用してテキスト埋め込み生成
- デフォルトモデル: `all-MiniLM-L6-v2` （軽量・高速）
- モデルは設定ファイルで変更可能

**1.4 `docgen/rag/indexer.py`**
- `hnswlib` を使用したベクトルインデックス構築・保存・読み込み
- 差分更新対応（`meta.json` でチャンクハッシュ管理）
- インデックスの永続化（`docgen/index/`）

**1.5 `docgen/rag/retriever.py`**
- クエリからtop-k類似チャンク取得
- スコアでフィルタリング（閾値以下を除外）
- 結果のランキング

### 2. 設定ファイルへのRAGセクション追加

**`docgen/config.yaml.sample` にRAG設定を追加**
```yaml
# RAG設定（実験的機能）
rag:
  # RAG機能を有効化
  enabled: false

  # 埋め込みモデル設定
  embedding:
    model: 'all-MiniLM-L6-v2'
    device: 'cpu'  # 'cpu' or 'cuda'

  # インデックス設定
  index:
    type: 'hnswlib'  # 'hnswlib' or 'faiss'
    ef_construction: 200
    M: 16

  # 検索設定
  retrieval:
    top_k: 6
    score_threshold: 0.3

  # チャンク設定
  chunking:
    max_chunk_size: 512
    overlap: 50
```

### 3. CLIコマンド追加

**`docgen/docgen.py` の変更箇所**
```python
# RAG関連のサブコマンド追加
parser.add_argument('--build-index', action='store_true',
                   help='RAGインデックスをビルド')
parser.add_argument('--use-rag', action='store_true',
                   help='RAGを使用してドキュメント生成')
```

### 4. 追加依存パッケージ

**`requirements-docgen.txt` に追加**
```text
# RAG dependencies
sentence-transformers>=2.2.0
hnswlib>=0.7.0
torch>=2.0.0
```

## 確認コマンド

```bash
# 依存関係インストール
uv sync
pip install sentence-transformers hnswlib

# インデックス構築（初回）
uv run python -m docgen.docgen --build-index

# インデックス確認
ls -la docgen/index/
# 出力例: meta.json, hnswlib.idx

# インデックスからの検索テスト（対話的）
uv run python -m docgen.rag.retriever --query "LLM client initialization"
```

---

# 4. フェーズ2 — ドキュメント生成へのRAG統合

目的：RAGで取得したコンテキストを既存のドキュメント生成パイプラインに統合し、より正確なドキュメントを生成する。

## 作業項目

### 1. ジェネレータへのRAGサポート追加

**1.1 `docgen/generators/base_generator.py` の拡張**
```python
class BaseGenerator:
    def _get_rag_context(self, query: str, top_k: int = 6) -> str:
        """
        RAGコンテキストを取得してフォーマット

        Args:
            query: 検索クエリ
            top_k: 取得するチャンク数

        Returns:
            フォーマット済みのコンテキスト文字列
        """
        if not self.config.get('rag', {}).get('enabled', False):
            return ""

        from docgen.rag.retriever import DocumentRetriever
        retriever = DocumentRetriever(self.config)
        chunks = retriever.retrieve(query, top_k=top_k)

        # コンテキストのフォーマット
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[{i}] {chunk['file']}:{chunk['start_line']}-{chunk['end_line']}\n"
                f"{chunk['text']}\n"
            )
        return "\n".join(context_parts)
```

**1.2 `docgen/generators/agents_generator.py` の修正**
```python
def generate_agents_doc(self) -> str:
    """AGENTS.mdを生成"""
    # RAGコンテキスト取得
    rag_context = self._get_rag_context(
        "agent definitions and configuration"
    )

    # プロンプト読み込み（既存のPromptLoaderを使用）
    from docgen.utils.prompt_loader import PromptLoader

    system_prompt = PromptLoader.load_system_prompt(
        'agents_prompts.yaml',
        'generate_with_rag' if rag_context else 'generate'
    )

    user_prompt = PromptLoader.load_prompt(
        'agents_prompts.yaml',
        'full_with_rag',
        rag_context=rag_context,
        project_info=self._collect_project_info()
    )

    # LLMで生成（既存のLLMクライアントを使用）
    return self.llm_client.generate(system_prompt, user_prompt)
```

### 2. プロンプトファイルへのRAGテンプレート追加

**2.1 `docgen/prompts/agents_prompts.yaml` に追加**
```yaml
system_prompts:
  # 既存のプロンプト...

  generate_with_rag: |
    あなたはドキュメント生成アシスタントです。
    以下のソースコードスニペットを**のみ**使用してAGENTS.mdを生成してください。

    重要な制約：
    - 提供されたコンテキスト内の情報のみを使用すること
    - すべての記述に出典を付けること（[file:line]形式）
    - コンテキストに情報がない場合は「情報不足」と明記すること

prompts:
  # 既存のプロンプト...

  full_with_rag: |
    # コンテキスト情報
    {rag_context}

    # プロジェクト情報
    {project_info}

    上記のコンテキストを使用して、以下の構成でAGENTS.mdを生成してください：

    1. プロジェクト概要
    2. セットアップ手順
    3. ビルド・テスト手順
    4. コーディング規約
    5. PRガイドライン

    各セクションで情報を記載する際は、必ず出典を [file:line] 形式で付けてください。
```

**2.2 `docgen/prompts/readme_prompts.yaml` に追加**
```yaml
system_prompts:
  generate_with_rag: |
    あなたはREADMEドキュメント生成アシスタントです。
    提供されたコードスニペットのみを使用してREADME.mdを生成してください。

    制約：
    - 正確なファイルパスとコマンドを記載すること
    - すべての情報に出典 [file:line] を付けること
    - 推測や想像を含めないこと

prompts:
  full_with_rag: |
    # コンテキスト
    {rag_context}

    上記を基にREADME.mdを生成してください。
    セクション: Quickstart, Installation, Usage, Development, Links
```

### 3. ドキュメント検証機能の実装

**3.1 `docgen/rag/validator.py`**
```python
class DocumentValidator:
    """生成ドキュメントの検証"""

    def validate_citations(self, doc: str, project_root: Path) -> list[str]:
        """出典の存在確認"""
        errors = []
        # [file:line] パターンを抽出
        citations = re.findall(r'\[([^:]+):(\d+)\]', doc)

        for file_path, line_num in citations:
            full_path = project_root / file_path
            if not full_path.exists():
                errors.append(f"Referenced file not found: {file_path}")
            # 行番号の妥当性チェック等

        return errors

    def detect_hallucinations(self, doc: str, known_facts: list[str]) -> list[str]:
        """幻覚（誤情報）の検出"""
        # 簡易実装：既知の事実と矛盾する記述を検出
        warnings = []
        # ...
        return warnings
```

### 4. CLIでの実行

**`docgen/docgen.py` のメイン処理**
```python
def main():
    # ...
    if args.use_rag:
        # RAGモードでのドキュメント生成
        config['rag']['enabled'] = True

    docgen = DocGen(config_path=args.config)
    success = docgen.generate_documents()

    if args.use_rag:
        # 生成後の検証
        from docgen.rag.validator import DocumentValidator
        validator = DocumentValidator()
        errors = validator.validate_citations(
            Path('AGENTS.md').read_text(),
            docgen.project_root
        )
        if errors:
            logger.warning(f"Validation errors: {errors}")
```

## 確認コマンド

```bash
# RAG有効化でドキュメント生成
uv run python -m docgen.docgen --use-rag

# 生成結果の確認
cat AGENTS.md | grep "\[.*:.*\]"  # 出典チェック

# 検証の実行
uv run python -m docgen.rag.validator AGENTS.md
```

---

# 5. フェーズ3 — 運用改善（差分更新、再ランキング、パフォーマンス最適化）

目的：効率化と精度向上。大規模化対応。

## 作業項目（段階的）

### 1. 差分インデックス更新

**実装内容**
- `meta.json` にチャンクごとのハッシュ（SHA256）を保存
- 変更のあるチャンクのみ再埋め込みしてインデックスに反映
- hnswlibは削除が困難なので、頻繁な削除が必要なら定期的に再構築
- 増分追加は可能なので、新規ファイルは都度追加

**実装箇所**
```python
# docgen/rag/indexer.py
class VectorIndexer:
    def incremental_update(self, new_chunks: list, existing_meta: dict):
        """差分更新"""
        # 既存チャンクのハッシュと比較
        # 変更されたチャンクのみ再埋め込み
        # インデックスに追加
        pass
```

### 2. 再ランキング（精度向上）

**実装内容**
- 軽量cross-encoder（`sentence-transformers`のcross-encoder）を導入
- retrieverのtop-Kを多めに取得（例：top-20）
- cross-encoderでrerank → 上位Nをコンテキストとして使用

**実装箇所**
```python
# docgen/rag/retriever.py
from sentence_transformers import CrossEncoder

class DocumentRetriever:
    def retrieve_with_rerank(self, query: str, top_k: int = 6, rerank_k: int = 20):
        """再ランキング付き検索"""
        # 初期検索（多めに取得）
        candidates = self._retrieve(query, top_k=rerank_k)

        # cross-encoderで再スコアリング
        reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        scores = reranker.predict([
            [query, chunk['text']] for chunk in candidates
        ])

        # スコア順にソートして上位k件
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [chunk for chunk, _ in ranked[:top_k]]
```

### 3. キャッシュ戦略

**実装内容**
- 埋め込み結果のキャッシュ（既存の`docgen/utils/cache.py`を活用）
- LLM生成結果のキャッシュ（同一クエリの再利用）

```python
# docgen/rag/embedder.py
from docgen.utils.cache import cache_manager

class Embedder:
    @cache_manager.cache('embeddings')
    def embed_text(self, text: str) -> np.ndarray:
        """テキスト埋め込み（キャッシュ付き）"""
        return self.model.encode(text)
```

### 4. CI/CD統合戦略

**オプション1: CI では RAG を実行しない（推奨）**
- CI では既存のテンプレートベース生成のみ実行
- RAG生成はローカル開発者またはself-hosted runnerでのみ実行
- 理由：重い処理、大きなモデルファイル、計算リソース

**オプション2: 軽量RAGをCIで実行**
- 小さな埋め込みモデル（50MB以下）を使用
- インデックスをキャッシュ
- 変更ファイルのみを対象に部分的なRAG実行

**実装例（GitHub Actions）**
```yaml
# .github/workflows/docgen-rag.yml
name: RAG-Enhanced Documentation

on:
  workflow_dispatch:  # 手動トリガーのみ

jobs:
  generate-docs:
    runs-on: self-hosted  # self-hosted runner推奨
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
          pip install sentence-transformers hnswlib
      - name: Build RAG index
        run: uv run python -m docgen.docgen --build-index
      - name: Generate docs with RAG
        run: uv run python -m docgen.docgen --use-rag
      - name: Validate outputs
        run: uv run python -m docgen.rag.validator AGENTS.md
```

---

# 6. テスト / CI 統合

## 追加テスト

**テストファイルの配置**
```
tests/
  rag/
    test_chunker.py           # チャンク化のテスト
    test_embedder.py          # 埋め込み生成のテスト
    test_indexer.py           # インデックス構築・読み込みのテスト
    test_retriever.py         # 検索機能のテスト
    test_validator.py         # ドキュメント検証のテスト
```

**テスト内容例**

**`tests/rag/test_chunker.py`**
```python
import pytest
from pathlib import Path
from docgen.rag.chunker import CodeChunker

def test_python_file_chunking(tmp_path):
    """Pythonファイルが関数単位でチャンクされること"""
    test_file = tmp_path / "test.py"
    test_file.write_text("""
def foo():
    pass

def bar():
    pass
""")

    chunker = CodeChunker()
    chunks = chunker.chunk_file(test_file)

    assert len(chunks) == 2
    assert chunks[0]['name'] == 'foo'
    assert chunks[1]['name'] == 'bar'

def test_markdown_chunking(tmp_path):
    """Markdownファイルがヘッダ単位でチャンクされること"""
    test_file = tmp_path / "test.md"
    test_file.write_text("""
# Header 1
Content 1

## Header 2
Content 2
""")

    chunker = CodeChunker()
    chunks = chunker.chunk_file(test_file)

    assert len(chunks) >= 2
```

**`tests/rag/test_indexer.py`**
```python
import pytest
import numpy as np
from docgen.rag.indexer import VectorIndexer

def test_index_build_and_load(tmp_path):
    """インデックスの保存→読み込みができること"""
    indexer = VectorIndexer(index_dir=tmp_path)

    # テストデータ
    embeddings = np.random.rand(10, 384).astype('float32')
    metadata = [{'id': i, 'text': f'chunk {i}'} for i in range(10)]

    # インデックス構築
    indexer.build(embeddings, metadata)

    # 保存
    indexer.save()

    # 新しいインスタンスで読み込み
    indexer2 = VectorIndexer(index_dir=tmp_path)
    indexer2.load()

    # 検索テスト
    query_embedding = np.random.rand(384).astype('float32')
    results = indexer2.search(query_embedding, k=3)

    assert len(results) == 3
```

**`tests/rag/test_validator.py`**
```python
import pytest
from pathlib import Path
from docgen.rag.validator import DocumentValidator

def test_citation_validation(tmp_path):
    """出典チェックが動作すること"""
    # テストファイル作成
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo():\n    pass\n")

    # 検証対象ドキュメント
    doc = f"関数fooは [test.py:1] で定義されています。"

    validator = DocumentValidator()
    errors = validator.validate_citations(doc, tmp_path)

    assert len(errors) == 0

def test_invalid_citation(tmp_path):
    """存在しないファイルの出典を検出すること"""
    doc = "この機能は [nonexistent.py:1] で実装されています。"

    validator = DocumentValidator()
    errors = validator.validate_citations(doc, tmp_path)

    assert len(errors) > 0
    assert 'nonexistent.py' in errors[0]
```

## CI設定

**既存のCI（テンプレートベース生成のみ）**
```yaml
# .github/workflows/docgen.yml
name: Generate Documentation

on:
  push:
    branches: [main]
  pull_request:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Generate docs (template-based)
        run: uv run python -m docgen.docgen
      - name: Check for changes
        run: git diff --exit-code AGENTS.md README.md
```

**テスト実行**
```bash
# すべてのテストを実行
uv run pytest tests/ -v

# RAG関連テストのみ
uv run pytest tests/rag/ -v

# カバレッジ付き
uv run pytest tests/ --cov=docgen/rag --cov-report=html
```

---

# 7. プロンプトテンプレート設計原則

## 既存のプロンプトシステム活用

このプロジェクトは既に `docgen/prompts/` に以下のプロンプトファイルを持っています：
- `agents_prompts.yaml`
- `readme_prompts.yaml`
- `commit_message_prompts.yaml`

RAG対応では、これらのファイルに新しいテンプレートを追加します。

## RAG対応プロンプトの構造

### AGENTS.md生成用（`agents_prompts.yaml`への追加例）

```yaml
system_prompts:
  generate_with_rag: |
    あなたはAIコーディングエージェント向けのドキュメント生成アシスタントです。
    **提供されたソースコードスニペットのみ**を使用してAGENTS.mdを生成してください。

    厳格な制約：
    - 提供されたコンテキスト以外の情報を使用しない
    - すべての記述に出典を [ファイルパス:行番号] 形式で付ける
    - コンテキストに情報がない場合は「情報が不足しています」と明記
    - コマンド例は実際のファイルから引用したもののみ使用
    - 推測や一般的な知識に基づく記述は禁止

prompts:
  full_with_rag: |
    # ソースコードコンテキスト
    {rag_context}

    # プロジェクトメタ情報
    - プロジェクト名: {project_name}
    - 主要言語: {languages}
    - ビルドシステム: {build_system}

    上記のコンテキストから以下の情報を抽出してAGENTS.mdを生成：

    ## 必須セクション
    1. **プロジェクト概要** - 目的、主要機能
    2. **開発環境セットアップ** - 前提条件、依存関係インストール、LLM環境
    3. **ビルド・テスト手順** - 具体的なコマンド（出典付き）
    4. **コーディング規約** - 使用ツール（linter, formatter等）
    5. **プルリクエスト手順** - 推奨フロー

    ## 出典形式
    - コード例: ```bash の後に # Source: [file:line]
    - 説明文内: 説明 [file:line]
    - 複数ソース: [file1:line1, file2:line2]
```

### README.md生成用（`readme_prompts.yaml`への追加例）

```yaml
system_prompts:
  generate_with_rag: |
    プロジェクトREADME生成専門アシスタントです。
    提供されたコンテキストのみを使用してREADME.mdを作成します。

    制約:
    - 正確なコマンドとパスのみ記載
    - すべての情報源を [file:line] で明示
    - 手動セクションマーカー <!-- MANUAL_START:xxx --> は保持

prompts:
  full_with_rag: |
    {rag_context}

    上記を基にREADME.mdを生成。
    セクション構成:
    1. Quickstart - 最小限のセットアップ・実行手順
    2. 機能概要 - 主要機能3-5個
    3. Installation - 環境別インストール手順
    4. Usage - 基本的な使い方とコマンド例
    5. Development - 開発者向け情報
    6. Links - AGENTS.md等の関連ドキュメント
```

---

# 8. リスクと安全対策

## 主要リスクと対策

### 1. 幻覚（Hallucination）による誤情報

**リスク**: LLMがコンテキストにない情報を創作する

**対策**:
- システムプロンプトで「コンテキスト外の情報使用禁止」を明記
- すべての記述に出典義務化 `[file:line]` 形式
- `DocumentValidator` で出典の実在確認
- 出典のないステートメントを検出してwarning

**実装**:
```python
# docgen/rag/validator.py
def validate_citations(self, doc: str) -> list[str]:
    """出典のない主張を検出"""
    # センテンス分割
    sentences = re.split(r'[。.]\s*', doc)

    errors = []
    for sent in sentences:
        # 技術的主張を含むが出典がない
        if self._is_technical_claim(sent) and not re.search(r'\[.+:\d+\]', sent):
            errors.append(f"Missing citation: {sent[:50]}...")

    return errors
```

### 2. 機密情報の漏洩

**リスク**: 環境変数、APIキー、内部URLの誤記載

**対策**:
- `.env` ファイル、`secrets/` ディレクトリをチャンク化対象から除外
- 生成後に秘密パターンスキャン（正規表現）
- `.gitignore` されているファイルは処理しない

**実装**:
```python
# docgen/rag/chunker.py
EXCLUDED_PATTERNS = [
    r'.*\.env$',
    r'secrets/.*',
    r'.*_SECRET.*',
    r'.*API_KEY.*',
]

def should_process_file(self, file_path: Path) -> bool:
    """機密ファイルをスキップ"""
    str_path = str(file_path)
    return not any(re.match(p, str_path) for p in EXCLUDED_PATTERNS)
```

### 3. パフォーマンス問題

**リスク**: 大規模コードベースでのインデックス構築・検索の遅延

**対策**:
- 差分インデックス更新（変更ファイルのみ処理）
- 埋め込みキャッシュ（`docgen/utils/cache.py` 活用）
- バッチ処理とプログレスバー表示
- 軽量モデル選択（`all-MiniLM-L6-v2`は384次元）

### 4. CI/CD リソース不足

**リスク**: GitHub Actions無料枠での実行時間超過、ストレージ不足

**対策**:
- CI では RAG を実行せず、テンプレートベース生成のみ
- RAG は self-hosted runner または手動トリガーワークフローで実行
- インデックスファイルはリポジトリに含めない（`.gitignore`）

---

# 9. 実行コマンド集 & チェックリスト

## 初期セットアップ

```bash
# プロジェクトのクローン
git clone https://github.com/shiohamu/agents-docs-sync.git
cd agents-docs-sync

# uvとPython環境
pip install uv
uv sync

# RAG依存関係
pip install sentence-transformers hnswlib torch
```

## RAGインデックス管理

```bash
# インデックス構築（初回または全体再構築時）
uv run python -m docgen.docgen --build-index

# インデックスの確認
ls -lh docgen/index/
cat docgen/index/meta.json | jq '.chunk_count'

# インデックスの削除（クリーンビルド前）
rm -rf docgen/index/

# 差分更新（変更ファイルのみ）
uv run python -m docgen.docgen --build-index --incremental
```

## ドキュメント生成

```bash
# 既存のテンプレートベース生成（RAGなし）
uv run python -m docgen.docgen

# RAG有効化での生成
uv run python -m docgen.docgen --use-rag

# 特定のドキュメントのみ生成
uv run python -m docgen.docgen --use-rag --agents-only
uv run python -m docgen.docgen --use-rag --readme-only
```

## 検証とテスト

```bash
# 生成ドキュメントの検証
uv run python -m docgen.rag.validator AGENTS.md
uv run python -m docgen.rag.validator README.md

# RAGモジュールのテスト
uv run pytest tests/rag/ -v

# カバレッジレポート付き
uv run pytest tests/rag/ --cov=docgen/rag --cov-report=term --cov-report=html

# 全テスト実行
uv run pytest tests/ -v --tb=short
```

## 開発ワークフロー

```bash
# 1. 機能追加・変更
git checkout -b feat/add-new-feature
# コード編集...

# 2. インデックス差分更新（変更が大きい場合）
uv run python -m docgen.docgen --build-index --incremental

# 3. RAGでドキュメント生成
uv run python -m docgen.docgen --use-rag

# 4. 検証
uv run python -m docgen.rag.validator AGENTS.md

# 5. 手動レビュー後にコミット
git add AGENTS.md README.md
git commit -m "docs: update documentation with RAG"
git push origin feat/add-new-feature
```

## トラブルシューティング

```bash
# キャッシュクリア
rm -rf docgen/.cache/

# プロンプトキャッシュクリア（開発時）
python -c "from docgen.utils.prompt_loader import PromptLoader; PromptLoader.clear_cache()"

# LLMクライアント接続確認
uv run python -c "from docgen.utils.llm_client import LLMClientFactory; \
  client = LLMClientFactory.create_client({'llm_mode': 'local'}); \
  print('Connected' if client else 'Failed')"

# ログレベル変更（詳細デバッグ）
export LOG_LEVEL=DEBUG
uv run python -m docgen.docgen --use-rag
```

## チェックリスト

### フェーズ1完了確認
- [ ] `docgen/rag/` ディレクトリ作成＋5ファイル実装
- [ ] `docgen/index/` が `.gitignore` に追加
- [ ] `requirements-docgen.txt` に RAG 依存追加
- [ ] `config.yaml.sample` に RAG セクション追加
- [ ] `--build-index` コマンドが動作
- [ ] `docgen/index/meta.json` と `hnswlib.idx` が生成される
- [ ] 検索テストが成功（`retriever --query "test"`）

### フェーズ2完了確認
- [ ] `base_generator.py` に `_get_rag_context()` 追加
- [ ] `agents_generator.py` が RAG コンテキスト使用
- [ ] `readme_generator.py` が RAG コンテキスト使用
- [ ] `agents_prompts.yaml` に RAG テンプレート追加
- [ ] `readme_prompts.yaml` に RAG テンプレート追加
- [ ] `--use-rag` フラグで生成が成功
- [ ] 生成ドキュメントに `[file:line]` 形式の出典が含まれる
- [ ] `DocumentValidator` が出典を検証できる

### フェーズ3完了確認
- [ ] 差分インデックス更新が動作
- [ ] 再ランキング機能が実装され精度向上を確認
- [ ] キャッシュにより2回目以降の生成が高速化
- [ ] self-hosted runner または手動ワークフローでの CI 実行確認
- [ ] テストカバレッジ ≥ 80%

---

# 最後に — 優先度提案（どこから始めるか）

## 推奨実装順序

### ステップ1: 基盤構築（1-2週間）
1. `docgen/rag/` モジュール構造作成
2. `chunker.py` - 既存の `collectors` を参考に実装
3. `embedder.py` - sentence-transformers 統合
4. `indexer.py` - hnswlib による永続化
5. `retriever.py` - 基本検索機能
6. `--build-index` コマンド実装

**検証**: インデックスが構築でき、基本検索が動作すること

### ステップ2: 生成統合（1週間）
1. `base_generator.py` に RAG メソッド追加
2. プロンプトテンプレート更新
3. `--use-rag` フラグ実装
4. `validator.py` - 出典検証

**検証**: RAG 有効化で AGENTS.md と README.md が生成され、出典が含まれること

### ステップ3: 最適化・運用化（継続的）
1. テスト追加（カバレッジ目標 80%）
2. 差分更新実装
3. 再ランキング導入
4. CI/CD ワークフロー調整

## 次のアクション候補

このドキュメントを基に実装を開始する場合、以下の選択肢があります：

1. **フェーズ1のファイル群を生成**
   → `docgen/rag/chunker.py`, `embedder.py`, `indexer.py`, `retriever.py` の初期実装を提供

2. **設定ファイルの更新**
   → `config.yaml.sample` と `.gitignore` に RAG セクションを追加

3. **プロンプトテンプレートの作成**
   → `agents_prompts.yaml`, `readme_prompts.yaml` に RAG 対応テンプレート追加

4. **テストファイルの雛形作成**
   → `tests/rag/` ディレクトリとテストファイル群

**どれから始めますか？** または、**全体のステップバイステップ実装ガイド**を希望されますか？

