"""
汎用プロジェクト検出器
"""

from pathlib import Path

from docgen.detectors.detector_patterns import DetectorPatterns

from ..models import Service


class GenericDetector:
    """様々なプログラミング言語のプロジェクトを検出"""

    def __init__(self, exclude_directories: list[str] | None = None):
        self.exclude_dirs = set(exclude_directories) if exclude_directories else set()
        # DetectorPatternsからデフォルトの除外ディレクトリも取得
        self.exclude_dirs.update(DetectorPatterns.EXCLUDE_DIRS)

    def detect(self, project_root: Path) -> list[Service]:
        """プロジェクトをスキャンしてサービスを検出"""
        services = []

        # 言語ごとのパッケージマネージャーファイルをチェック
        for lang, files in DetectorPatterns.PACKAGE_FILES.items():
            # Pythonは専用のDetectorがあるので、ここではスキップするか
            # あるいは共通の仕組みとして統合するか。現状はPython以外をターゲットにする。
            if lang == "python":
                continue

            for file_pattern in files:
                # glob形式をサポート（*.csproj など）
                found = False
                if "*" in file_pattern:
                    if list(project_root.glob(file_pattern)):
                        found = True
                elif (project_root / file_pattern).exists():
                    found = True

                if found:
                    services.append(
                        Service(
                            name=project_root.name,
                            type=lang,
                            description=f"{lang.capitalize()} project detected by {file_pattern}",
                            metadata={"entry_file": file_pattern},
                            dependencies=[],
                        )
                    )
                    # 1つの言語に対して1つのファイルが見つかれば十分
                    break

        # パッケージマネージャーファイルが見つからない場合、ソースファイルの存在を確認
        if not services:
            for lang, exts in DetectorPatterns.SOURCE_EXTENSIONS.items():
                if lang == "python":
                    continue

                # パフォーマンスのため、トップレベルまたは1段階下のディレクトリのみをチェック（archgenの用途的に）
                # 全走査は重いので DetectorPatterns.detect_by_source_files_with_exclusions を使う
                if DetectorPatterns.detect_by_source_files_with_exclusions(project_root, lang):
                    services.append(
                        Service(
                            name=project_root.name,
                            type=lang,
                            description=f"{lang.capitalize()} project detected by source files",
                            metadata={},
                            dependencies=[],
                        )
                    )

        return services
