"""
言語検出のベースクラス
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseDetector(ABC):
    """言語検出のベースクラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root

    @abstractmethod
    def detect(self) -> bool:
        """
        言語が使用されているか検出

        Returns:
            検出された場合True
        """
        pass

    @abstractmethod
    def get_language(self) -> str:
        """
        検出された言語名を返す

        Returns:
            言語名（例: 'python', 'javascript'）
        """
        pass

    def _file_exists(self, *paths) -> bool:
        """
        ファイルの存在を確認

        Args:
            *paths: 確認するファイルパス（相対パス）

        Returns:
            いずれかのファイルが存在する場合True
        """
        for path in paths:
            if (self.project_root / path).exists():
                return True
        return False

    def _has_files_with_ext(self, *extensions) -> bool:
        """
        指定された拡張子のファイルが存在するか確認

        Args:
            *extensions: 拡張子（例: '.py', '.js'）

        Returns:
            該当ファイルが存在する場合True
        """
        # プロジェクトルートを正規化（絶対パスに変換）
        project_root_resolved = self.project_root.resolve()

        for ext in extensions:
            try:
                for file_path in self.project_root.rglob(f"*{ext}"):
                    try:
                        # パスの正規化（シンボリックリンクを解決）
                        file_path_resolved = file_path.resolve()

                        # プロジェクトルート外へのアクセスを防止
                        try:
                            file_path_resolved.relative_to(project_root_resolved)
                        except ValueError:
                            # プロジェクトルート外のファイルはスキップ
                            continue

                        # シンボリックリンクをスキップ（オプション）
                        if file_path.is_symlink():
                            continue

                        # 有効なファイルが見つかった
                        return True
                    except (OSError, PermissionError):
                        # ファイルアクセスエラーは無視して続行
                        continue
            except (OSError, PermissionError):
                # ディレクトリアクセスエラーは無視して続行
                continue
        return False
