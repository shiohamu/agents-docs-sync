"""コードベースのチャンク化モジュール

コードベースを意味のある単位（関数、クラス、セクション）に分割し、
RAGインデックス用のチャンクを生成します。
"""

import ast
import hashlib
from pathlib import Path
import re
from typing import Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


class CodeChunker:
    """コードベースをチャンク化するクラス"""

    # 機密情報を含む可能性があるパターン
    DEFAULT_EXCLUDE_PATTERNS = [
        r".*\.env$",
        r"secrets/.*",
        r".*_SECRET.*",
        r".*API_KEY.*",
        r".*password.*",
        r".*token.*\.json$",
    ]

    def __init__(self, config: dict[str, Any] | None = None):
        """
        初期化

        Args:
            config: RAG設定（config.yaml の rag セクション）
        """
        self.config = config or {}
        self.max_chunk_size = self.config.get("chunking", {}).get("max_chunk_size", 512)
        self.overlap = self.config.get("chunking", {}).get("overlap", 50)

        # カスタム除外パターン + デフォルトパターン
        custom_patterns = self.config.get("exclude_patterns", [])
        self.exclude_patterns = self.DEFAULT_EXCLUDE_PATTERNS + custom_patterns

    def should_process_file(self, file_path: Path) -> bool:
        """
        ファイルを処理すべきかどうかを判定

        Args:
            file_path: ファイルパス

        Returns:
            処理すべき場合True
        """
        str_path = str(file_path)

        # 除外パターンのチェック
        for pattern in self.exclude_patterns:
            if re.search(pattern, str_path):
                return False

        # バイナリファイルやテストファイルは除外
        excluded_suffixes = {".pyc", ".pyo", ".so", ".dylib", ".whl", ".egg"}
        if file_path.suffix in excluded_suffixes:
            return False

        # 一般的な除外ディレクトリ（.venv, .git, node_modules等）
        excluded_dirs = {
            ".venv",
            "venv",
            ".git",
            ".hg",
            ".svn",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".tox",
            "dist",
            "build",
            ".eggs",
            "*.egg-info",
            ".cache",
            "htmlcov",
            ".coverage",
            ".DS_Store",
        }

        # パスに除外ディレクトリが含まれているかチェック
        path_parts = file_path.parts
        for part in path_parts:
            if part in excluded_dirs or part.startswith("."):
                # ただし、プロジェクトルート直下の設定ファイル（.github等）は許可
                if len(path_parts) == 2 and part.startswith(".") and file_path.is_file():
                    continue
                return False

        # テストファイルを除外
        if file_path.name.lower().startswith("test_") or file_path.name.lower().endswith(
            "_test.py"
        ):
            return False
        if "tests" in path_parts:
            return False

        # 生成されたドキュメントを除外
        if file_path.name in {"API.md", "AGENTS.md"}:
            return False

        return True

    def chunk_file(self, file_path: Path, project_root: Path) -> list[dict[str, Any]]:
        """
        ファイルをチャンク化

        Args:
            file_path: ファイルパス
            project_root: プロジェクトルート

        Returns:
            チャンクのリスト
        """
        if not self.should_process_file(file_path):
            return []

        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError) as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return []

        # ファイルタイプに応じてチャンク化
        if file_path.suffix == ".py":
            return self._chunk_python(content, file_path, project_root)
        elif file_path.suffix == ".md":
            return self._chunk_markdown(content, file_path, project_root)
        elif file_path.suffix in {".yaml", ".yml"}:
            return self._chunk_yaml(content, file_path, project_root)
        elif file_path.suffix == ".toml":
            return self._chunk_toml(content, file_path, project_root)
        else:
            # その他のファイルは全体を1チャンクとする
            return self._chunk_generic(content, file_path, project_root)

    def _chunk_python(
        self, content: str, file_path: Path, project_root: Path
    ) -> list[dict[str, Any]]:
        """Pythonファイルのチャンク化（関数・クラス単位）"""
        chunks = []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")
            return self._chunk_generic(content, file_path, project_root)

        lines = content.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1  # 0-indexed
                end_line = node.end_lineno if node.end_lineno else start_line + 1

                # ノードの内容を抽出
                chunk_text = "\n".join(lines[start_line:end_line])

                chunks.append(
                    {
                        "file": str(file_path.relative_to(project_root)),
                        "type": node.__class__.__name__,
                        "name": node.name,
                        "text": chunk_text,
                        "start_line": start_line + 1,  # 1-indexed for display
                        "end_line": end_line,
                        "hash": self._hash_text(chunk_text),
                    }
                )

        return chunks

    def _chunk_markdown(
        self, content: str, file_path: Path, project_root: Path
    ) -> list[dict[str, Any]]:
        """Markdownファイルのチャンク化（ヘッダ単位）"""
        chunks = []
        lines = content.splitlines()

        current_section = []
        section_start = 0
        header_name = "Introduction"

        for i, line in enumerate(lines):
            # ヘッダ行の検出（# で始まる行）
            if line.startswith("#"):
                # 前のセクションを保存
                if current_section:
                    section_text = "\n".join(current_section)
                    chunks.append(
                        {
                            "file": str(file_path.relative_to(project_root)),
                            "type": "MarkdownSection",
                            "name": header_name,
                            "text": section_text,
                            "start_line": section_start + 1,
                            "end_line": i,
                            "hash": self._hash_text(section_text),
                        }
                    )

                # 新しいセクション開始
                header_name = line.lstrip("#").strip()
                section_start = i
                current_section = [line]
            else:
                current_section.append(line)

        # 最後のセクションを保存
        if current_section:
            section_text = "\n".join(current_section)
            chunks.append(
                {
                    "file": str(file_path.relative_to(project_root)),
                    "type": "MarkdownSection",
                    "name": header_name,
                    "text": section_text,
                    "start_line": section_start + 1,
                    "end_line": len(lines),
                    "hash": self._hash_text(section_text),
                }
            )

        return chunks

    def _chunk_yaml(
        self, content: str, file_path: Path, project_root: Path
    ) -> list[dict[str, Any]]:
        """YAMLファイルのチャンク化（トップレベルキー単位）"""
        chunks = []
        lines = content.splitlines()

        current_section = []
        section_start = 0
        section_name = "preamble"

        for i, line in enumerate(lines):
            # トップレベルキー（インデントなし）の検出
            if line and not line.startswith(" ") and ":" in line:
                # 前のセクションを保存
                if current_section:
                    section_text = "\n".join(current_section)
                    chunks.append(
                        {
                            "file": str(file_path.relative_to(project_root)),
                            "type": "YAMLSection",
                            "name": section_name,
                            "text": section_text,
                            "start_line": section_start + 1,
                            "end_line": i,
                            "hash": self._hash_text(section_text),
                        }
                    )

                # 新しいセクション開始
                section_name = line.split(":")[0].strip()
                section_start = i
                current_section = [line]
            else:
                current_section.append(line)

        # 最後のセクションを保存
        if current_section:
            section_text = "\n".join(current_section)
            chunks.append(
                {
                    "file": str(file_path.relative_to(project_root)),
                    "type": "YAMLSection",
                    "name": section_name,
                    "text": section_text,
                    "start_line": section_start + 1,
                    "end_line": len(lines),
                    "hash": self._hash_text(section_text),
                }
            )

        return chunks

    def _chunk_toml(
        self, content: str, file_path: Path, project_root: Path
    ) -> list[dict[str, Any]]:
        """TOMLファイルのチャンク化（セクション単位）"""
        chunks = []
        lines = content.splitlines()

        current_section = []
        section_start = 0
        section_name = "header"

        for i, line in enumerate(lines):
            # セクションヘッダの検出 ([section])
            if line.strip().startswith("[") and line.strip().endswith("]"):
                # 前のセクションを保存
                if current_section:
                    section_text = "\n".join(current_section)
                    chunks.append(
                        {
                            "file": str(file_path.relative_to(project_root)),
                            "type": "TOMLSection",
                            "name": section_name,
                            "text": section_text,
                            "start_line": section_start + 1,
                            "end_line": i,
                            "hash": self._hash_text(section_text),
                        }
                    )

                # 新しいセクション開始
                section_name = line.strip("[").strip("]")
                section_start = i
                current_section = [line]
            else:
                current_section.append(line)

        # 最後のセクションを保存
        if current_section:
            section_text = "\n".join(current_section)
            chunks.append(
                {
                    "file": str(file_path.relative_to(project_root)),
                    "type": "TOMLSection",
                    "name": section_name,
                    "text": section_text,
                    "start_line": section_start + 1,
                    "end_line": len(lines),
                    "hash": self._hash_text(section_text),
                }
            )

        return chunks

    def _chunk_generic(
        self, content: str, file_path: Path, project_root: Path
    ) -> list[dict[str, Any]]:
        """汎用ファイルのチャンク化（ファイル全体を1チャンク）"""
        return [
            {
                "file": str(file_path.relative_to(project_root)),
                "type": "File",
                "name": file_path.name,
                "text": content,
                "start_line": 1,
                "end_line": len(content.splitlines()),
                "hash": self._hash_text(content),
            }
        ]

    def _hash_text(self, text: str) -> str:
        """テキストのハッシュ値を計算（差分更新用）"""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    def chunk_codebase(self, project_root: Path) -> list[dict[str, Any]]:
        """
        プロジェクト全体をチャンク化

        Args:
            project_root: プロジェクトルート

        Returns:
            すべてのチャンクのリスト
        """
        all_chunks = []

        # プロジェクト内のファイルを走査
        for file_path in project_root.rglob("*"):
            if file_path.is_file():
                chunks = self.chunk_file(file_path, project_root)
                all_chunks.extend(chunks)

        logger.info(f"Created {len(all_chunks)} chunks from codebase")
        return all_chunks
