"""
言語検出モジュール
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .detectors.generic_detector import GenericDetector
from .detectors.go_detector import GoDetector
from .detectors.javascript_detector import JavaScriptDetector
from .detectors.python_detector import PythonDetector
from .utils.logger import get_logger

logger = get_logger("language_detector")


class LanguageDetector:
    """言語検出クラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトルートパス
        """
        self.project_root = project_root
        self.detected_languages = []
        self.detected_package_managers = {}

    def detect_languages(self, use_parallel: bool = True) -> list[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        detectors = [
            PythonDetector(self.project_root),
            JavaScriptDetector(self.project_root),
            GoDetector(self.project_root),
            GenericDetector(self.project_root),
        ]

        detected = []

        if use_parallel:
            # 並列処理で検出
            with ThreadPoolExecutor(max_workers=len(detectors)) as executor:
                future_to_detector = {
                    executor.submit(detector.detect): detector for detector in detectors
                }

                for future in as_completed(future_to_detector):
                    detector = future_to_detector[future]
                    try:
                        if future.result():
                            lang = detector.get_language()
                            if lang not in detected:
                                detected.append(lang)
                                logger.info(f"✓ 検出: {lang}")
                    except Exception as e:
                        logger.warning(
                            f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}"
                        )
        else:
            # 逐次処理で検出
            for detector in detectors:
                try:
                    if detector.detect():
                        lang = detector.get_language()
                        if lang not in detected:
                            detected.append(lang)
                            logger.info(f"✓ 検出: {lang}")
                except Exception as e:
                    logger.warning(
                        f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}"
                    )

        self.detected_languages = detected

        # パッケージマネージャの検出
        package_managers = {}
        for detector in detectors:
            try:
                if detector.detect():
                    lang = detector.get_language()
                    pm = detector.detect_package_manager()
                    if pm:
                        package_managers[lang] = pm
                        logger.info(f"✓ パッケージマネージャ検出: {lang} -> {pm}")
            except Exception as e:
                logger.warning(
                    f"パッケージマネージャ検出中にエラーが発生しました ({detector.__class__.__name__}): {e}"
                )

        self.detected_package_managers = package_managers
        return detected

    def get_detected_languages(self) -> list[str]:
        """検出された言語を取得"""
        return self.detected_languages

    def get_detected_package_managers(self) -> dict[str, str]:
        """検出されたパッケージマネージャを取得"""
        return self.detected_package_managers
