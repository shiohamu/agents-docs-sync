"""
Pythonコード解析モジュール
docstringを抽出してAPI情報を生成
"""

import ast
from pathlib import Path
import sys
from typing import Any

from .base_parser import BaseParser

# Python 3.9+ では ast.unparse が利用可能
if sys.version_info >= (3, 9):
    _ast_unparse = ast.unparse
else:
    # Python 3.8以下では簡易的な実装を使用
    def _ast_unparse(node):
        """簡易的なASTノードの文字列化"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Str):  # Python 3.7以前
            return repr(node.s)
        else:
            return str(node)


class PythonParser(BaseParser):
    """Pythonコード解析クラス"""

    def parse_file(self, file_path: Path) -> list[dict[str, Any]]:
        """
        Pythonファイルを解析

        Args:
            file_path: 解析するPythonファイルのパス

        Returns:
            API情報のリスト
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            visitor = PythonASTVisitor(file_path, self.project_root)
            visitor.visit(tree)

            return visitor.apis
        except SyntaxError:
            # 構文エラーは無視
            return []
        except Exception as e:
            # base_parserのloggerを使用
            from .base_parser import logger

            logger.warning(f"{file_path} の解析エラー: {e}")
            return []

    def get_supported_extensions(self) -> list[str]:
        """サポートする拡張子を返す"""
        return [".py", ".pyw"]


class PythonASTVisitor(ast.NodeVisitor):
    """Python AST訪問クラス"""

    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.apis = []
        self.class_stack = []

    def visit_ClassDef(self, node: ast.ClassDef):
        # プライベートクラス（_で始まる）はスキップ（オプション）
        if node.name.startswith("_") and not node.name.startswith("__"):
            return

        signature = self._get_class_signature(node)
        docstring = ast.get_docstring(node) or ""

        self.apis.append(
            {
                "name": node.name,
                "type": "class",
                "signature": signature,
                "docstring": docstring,
                "line": node.lineno,
                "file": str(self.file_path.relative_to(self.project_root)),
            }
        )

        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self._visit_function(node, "function")

    def visit_AsyncFunctionDef(self, node):
        self._visit_function(node, "function")

    def _visit_function(self, node, base_type: str):
        # プライベート関数（_で始まる）はスキップ（オプション）
        if node.name.startswith("_") and not node.name.startswith("__"):
            return

        api_type = "method" if self.class_stack else base_type
        signature = self._get_function_signature(node)
        docstring = ast.get_docstring(node) or ""

        # パラメータと戻り値の型を取得
        parameters = []
        for arg in node.args.args:
            param_str = arg.arg
            if arg.annotation:
                param_str += f": {_ast_unparse(arg.annotation)}"
            parameters.append(param_str)

        return_type = ""
        if node.returns:
            return_type = _ast_unparse(node.returns)

        self.apis.append(
            {
                "name": node.name,
                "type": api_type,
                "signature": signature,
                "docstring": docstring,
                "parameters": parameters,
                "return_type": return_type,
                "line": node.lineno,
                "file": str(self.file_path.relative_to(self.project_root)),
            }
        )

    def _get_function_signature(self, node) -> str:
        """
        関数のシグネチャを文字列として取得

        Args:
            node: AST関数ノード (FunctionDef or AsyncFunctionDef)

        Returns:
            シグネチャ文字列
        """
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {_ast_unparse(arg.annotation)}"
            args.append(arg_str)

        def_type = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        signature = f"{def_type} {node.name}({', '.join(args)})"
        if node.returns:
            signature += f" -> {_ast_unparse(node.returns)}"
        signature += ":"

        return signature

    def _get_class_signature(self, node: ast.ClassDef) -> str:
        """
        クラスのシグネチャを文字列として取得

        Args:
            node: ASTクラスノード

        Returns:
            シグネチャ文字列
        """
        return f"class {node.name}:"
