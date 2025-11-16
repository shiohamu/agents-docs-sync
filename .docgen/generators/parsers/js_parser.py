"""
JavaScript/TypeScriptコード解析モジュール
JSDocコメントを抽出してAPI情報を生成
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from .base_parser import BaseParser


class JSParser(BaseParser):
    """JavaScript/TypeScriptコード解析クラス"""

    # JSDocコメントのパターン
    JSDOC_PATTERN = re.compile(
        r'/\*\*\s*\n(.*?)\*/\s*\n\s*(?:export\s+)?(?:async\s+)?(?:function|class|const|let|var)\s+(\w+)',
        re.DOTALL | re.MULTILINE
    )

    # 関数定義のパターン
    FUNCTION_PATTERN = re.compile(
        r'(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>|(\w+)\s*:\s*(?:async\s+)?\([^)]*\)\s*=>)',
        re.MULTILINE
    )

    # クラス定義のパターン
    CLASS_PATTERN = re.compile(
        r'(?:export\s+)?class\s+(\w+)',
        re.MULTILINE
    )

    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        JavaScript/TypeScriptファイルを解析

        Args:
            file_path: 解析するファイルのパス

        Returns:
            API情報のリスト
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            apis = []

            # JSDoc付きの関数/クラスを抽出
            for match in self.JSDOC_PATTERN.finditer(content):
                docstring = match.group(1).strip()
                name = match.group(2)

                # 行番号を取得
                line_num = content[:match.start()].count('\n') + 1

                # 関数かクラスかを判定
                api_type = 'function'
                if 'class' in match.group(0):
                    api_type = 'class'

                # シグネチャを抽出
                signature = self._extract_signature(content, match.end(), name, api_type)

                apis.append({
                    'name': name,
                    'type': api_type,
                    'signature': signature,
                    'docstring': self._clean_jsdoc(docstring),
                    'line': line_num,
                    'file': str(file_path.relative_to(self.project_root))
                })

            # JSDocなしの関数/クラスも抽出（簡易版）
            for match in self.FUNCTION_PATTERN.finditer(content):
                name = match.group(1) or match.group(2) or match.group(3)
                if name and not any(api['name'] == name for api in apis):
                    line_num = content[:match.start()].count('\n') + 1
                    signature = self._extract_signature(content, match.end(), name, 'function')
                    apis.append({
                        'name': name,
                        'type': 'function',
                        'signature': signature,
                        'docstring': '',
                        'line': line_num,
                        'file': str(file_path.relative_to(self.project_root))
                    })

            for match in self.CLASS_PATTERN.finditer(content):
                name = match.group(1)
                if name and not any(api['name'] == name for api in apis):
                    line_num = content[:match.start()].count('\n') + 1
                    signature = f"class {name}"
                    apis.append({
                        'name': name,
                        'type': 'class',
                        'signature': signature,
                        'docstring': '',
                        'line': line_num,
                        'file': str(file_path.relative_to(self.project_root))
                    })

            return apis
        except Exception as e:
            print(f"警告: {file_path} の解析エラー: {e}")
            return []

    def _extract_signature(self, content: str, start_pos: int, name: str, api_type: str) -> str:
        """
        シグネチャを抽出

        Args:
            content: ファイル内容
            start_pos: 開始位置
            name: 関数/クラス名
            api_type: 'function' または 'class'

        Returns:
            シグネチャ文字列
        """
        # 簡易的なシグネチャ抽出
        if api_type == 'class':
            return f"class {name}"

        # 関数のシグネチャを抽出（簡易版）
        lines = content[start_pos:start_pos + 10].split('\n')
        if lines:
            first_line = lines[0].strip()
            if '(' in first_line:
                end_pos = first_line.find(')') + 1
                if end_pos > 0:
                    # 関数名を含むシグネチャを構築
                    sig = first_line[:end_pos]
                    # 関数名が含まれていない場合は追加
                    if name not in sig:
                        # パラメータ部分を抽出
                        param_start = sig.find('(')
                        if param_start >= 0:
                            return f"function {name}{sig[param_start:]}"
                    return sig

        return f"function {name}(...)"

    def _clean_jsdoc(self, docstring: str) -> str:
        """
        JSDocコメントをクリーンアップ

        Args:
            docstring: 生のJSDoc文字列

        Returns:
            クリーンアップされた文字列
        """
        # * を削除
        lines = [line.strip().lstrip('*').strip() for line in docstring.split('\n')]
        return '\n'.join(lines).strip()

    def get_supported_extensions(self) -> List[str]:
        """サポートする拡張子を返す"""
        return ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']

