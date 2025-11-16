"""
Pythonコード解析モジュール
docstringを抽出してAPI情報を生成
"""

import ast
import inspect
import sys
from pathlib import Path
from typing import List, Dict, Any
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

    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Pythonファイルを解析

        Args:
            file_path: 解析するPythonファイルのパス

        Returns:
            API情報のリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            apis = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    api_info = self._parse_function(node, file_path)
                    if api_info:
                        apis.append(api_info)
                elif isinstance(node, ast.ClassDef):
                    api_info = self._parse_class(node, file_path)
                    if api_info:
                        apis.append(api_info)

            return apis
        except SyntaxError:
            # 構文エラーは無視
            return []
        except Exception as e:
            print(f"警告: {file_path} の解析エラー: {e}")
            return []

    def _parse_function(self, node: ast.FunctionDef, file_path: Path) -> Dict[str, Any]:
        """
        関数ノードを解析

        Args:
            node: AST関数ノード
            file_path: ファイルパス

        Returns:
            API情報の辞書
        """
        # プライベート関数（_で始まる）はスキップ（オプション）
        if node.name.startswith('_') and not node.name.startswith('__'):
            return None

        signature = self._get_function_signature(node)
        docstring = ast.get_docstring(node) or ""

        return {
            'name': node.name,
            'type': 'function',
            'signature': signature,
            'docstring': docstring,
            'line': node.lineno,
            'file': str(file_path.relative_to(self.project_root))
        }

    def _parse_class(self, node: ast.ClassDef, file_path: Path) -> Dict[str, Any]:
        """
        クラスノードを解析

        Args:
            node: ASTクラスノード
            file_path: ファイルパス

        Returns:
            API情報の辞書
        """
        # プライベートクラス（_で始まる）はスキップ（オプション）
        if node.name.startswith('_') and not node.name.startswith('__'):
            return None

        signature = self._get_class_signature(node)
        docstring = ast.get_docstring(node) or ""

        return {
            'name': node.name,
            'type': 'class',
            'signature': signature,
            'docstring': docstring,
            'line': node.lineno,
            'file': str(file_path.relative_to(self.project_root))
        }

    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """
        関数のシグネチャを文字列として取得

        Args:
            node: AST関数ノード

        Returns:
            シグネチャ文字列
        """
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {_ast_unparse(arg.annotation)}"
            args.append(arg_str)

        signature = f"def {node.name}({', '.join(args)})"
        if node.returns:
            signature += f" -> {_ast_unparse(node.returns)}"

        return signature

    def _get_class_signature(self, node: ast.ClassDef) -> str:
        """
        クラスのシグネチャを文字列として取得

        Args:
            node: ASTクラスノード

        Returns:
            シグネチャ文字列
        """
        bases = []
        for base in node.bases:
            bases.append(_ast_unparse(base))

        signature = f"class {node.name}"
        if bases:
            signature += f"({', '.join(bases)})"

        return signature

    def get_supported_extensions(self) -> List[str]:
        """サポートする拡張子を返す"""
        return ['.py', '.pyw']

