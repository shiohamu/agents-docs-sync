"""
プロジェクトスキャナー
"""

from pathlib import Path

from .detectors.docker_detector import DockerDetector
from .detectors.generic_detector import GenericDetector
from .detectors.python_detector import PythonDetector
from .models import ArchitectureManifest


class ProjectScanner:
    """プロジェクトをスキャンしてアーキテクチャを抽出"""

    def __init__(self, project_root: Path, exclude_directories: list[str] | None = None):
        self.project_root = project_root
        self.detectors = [
            PythonDetector(exclude_directories=exclude_directories),
            GenericDetector(exclude_directories=exclude_directories),
            DockerDetector(),
        ]

    def scan(self) -> ArchitectureManifest:
        """プロジェクトをスキャン"""
        services = []
        for detector in self.detectors:
            detected = detector.detect(self.project_root)
            services.extend(detected)

        return ArchitectureManifest(project_name=self.project_root.name, services=services)
