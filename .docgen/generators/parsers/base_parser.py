"""
パーサーのベースクラス
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional


class BaseParser(ABC):
    """コード解析のベースクラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root

    @abstractmethod
    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        ファイルを解析してAPI情報を抽出

        Args:
            file_path: 解析するファイルのパス

        Returns:
            API情報のリスト。各要素は以下のキーを持つ辞書:
            - name: 関数/クラス名
            - type: 'function' または 'class'
            - signature: シグネチャ
            - docstring: ドキュメント文字列
            - line: 行番号
            - file: ファイルパス（相対パス）
        """
        pass

    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """
        サポートするファイル拡張子を返す

        Returns:
            拡張子のリスト（例: ['.py', '.pyw']）
        """
        pass

    def parse_project(self, exclude_dirs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        プロジェクト全体を解析

        Args:
            exclude_dirs: 除外するディレクトリ（例: ['.git', 'node_modules']）

        Returns:
            全API情報のリスト
        """
        if exclude_dirs is None:
            exclude_dirs = ['.git', '.docgen', '__pycache__', 'node_modules', '.venv', 'venv']

        all_apis = []
        extensions = self.get_supported_extensions()

        for ext in extensions:
            for file_path in self.project_root.rglob(f'*{ext}'):
                # 除外ディレクトリをスキップ
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue

                try:
                    apis = self.parse_file(file_path)
                    for api in apis:
                        api['file'] = str(file_path.relative_to(self.project_root))
                    all_apis.extend(apis)
                except Exception as e:
                    # パースエラーは無視して続行
                    print(f"警告: {file_path} の解析に失敗しました: {e}")
                    continue

        return all_apis

