"""
Pythonプロジェクト検出モジュール
"""

from pathlib import Path
from .base_detector import BaseDetector


class PythonDetector(BaseDetector):
    """Pythonプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        Pythonプロジェクトかどうかを検出

        Returns:
            Pythonプロジェクトの場合True
        """
        # requirements.txt, setup.py, pyproject.toml, Pipfile などの存在確認
        if self._file_exists(
            'requirements.txt',
            'setup.py',
            'pyproject.toml',
            'Pipfile',
            'Pipfile.lock',
            'poetry.lock',
            'environment.yml',
            'conda-environment.yml'
        ):
            return True

        # .pyファイルの存在確認
        if self._has_files_with_ext('.py'):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        return 'python'

