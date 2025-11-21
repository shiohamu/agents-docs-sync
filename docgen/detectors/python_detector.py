"""
Pythonプロジェクト検出モジュール
"""

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
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "Pipfile.lock",
            "poetry.lock",
            "environment.yml",
            "conda-environment.yml",
            "uv.lock",
        ):
            return True

        # .pyファイルの存在確認
        if self._has_files_with_ext(".py"):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        return "python"

    def detect_package_manager(self) -> str | None:
        """
        Pythonプロジェクトで使用されているパッケージマネージャを検出

        Returns:
            パッケージマネージャ名またはNone
        """
        # uv.lockが存在する場合（優先度最高）
        if self._file_exists("uv.lock"):
            return "uv"

        # poetry.lockが存在する場合
        if self._file_exists("poetry.lock"):
            return "poetry"

        # pyproject.tomlが存在し、[tool.poetry]セクションがある場合
        if self._file_exists("pyproject.toml"):
            try:
                import tomllib

                with open(self.project_root / "pyproject.toml", "rb") as f:
                    data = tomllib.load(f)
                    if "tool" in data and "poetry" in data["tool"]:
                        return "poetry"
            except ImportError:
                # tomllibが利用できない場合（Python 3.10以前）
                pass
            except Exception:
                pass

        # environment.ymlまたはconda-environment.ymlが存在する場合
        if self._file_exists("environment.yml", "conda-environment.yml"):
            return "conda"

        # requirements.txtが存在する場合（デフォルト）
        if self._file_exists("requirements.txt"):
            return "pip"

        # setup.pyが存在する場合
        if self._file_exists("setup.py"):
            return "pip"

        return None
