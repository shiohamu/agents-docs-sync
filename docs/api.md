# API ドキュメント

自動生成日時: 2025-11-25 15:31:46

---

## docgen/collectors/collector_utils.py

### ConfigReader

**型**: `class`

**シグネチャ**:
```
class ConfigReader:
```

**説明**:

Common utilities for reading various configuration files.

*定義場所: docgen/collectors/collector_utils.py:10*

---

### read_json_file

**型**: `method`

**シグネチャ**:
```
def read_json_file(file_path: Path) -> dict[str, Any] | None:
```

**説明**:

Read and parse JSON file.

*定義場所: docgen/collectors/collector_utils.py:14*

---

### read_package_json

**型**: `method`

**シグネチャ**:
```
def read_package_json(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read package.json file.

*定義場所: docgen/collectors/collector_utils.py:25*

---

### read_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def read_pyproject_toml(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read pyproject.toml file.

*定義場所: docgen/collectors/collector_utils.py:30*

---

### read_makefile

**型**: `method`

**シグネチャ**:
```
def read_makefile(project_root: Path) -> str | None:
```

**説明**:

Read Makefile content.

*定義場所: docgen/collectors/collector_utils.py:45*

---

### extract_scripts_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_scripts_from_package_json(package_data: dict[str, Any]) -> list[str]:
```

**説明**:

Extract scripts from package.json.

*定義場所: docgen/collectors/collector_utils.py:55*

---

### extract_dependencies_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_dependencies_from_package_json(package_data: dict[str, Any]) -> dict[str, list[str]]:
```

**説明**:

Extract dependencies from package.json.

*定義場所: docgen/collectors/collector_utils.py:61*

---

### parse_makefile_targets

**型**: `method`

**シグネチャ**:
```
def parse_makefile_targets(content: str) -> list[str]:
```

**説明**:

Parse Makefile targets.

*定義場所: docgen/collectors/collector_utils.py:78*

---

### detect_language_from_config

**型**: `method`

**シグネチャ**:
```
def detect_language_from_config(project_root: Path) -> str | None:
```

**説明**:

Detect programming language from configuration files.

*定義場所: docgen/collectors/collector_utils.py:90*

---


## docgen/collectors/project_info_collector.py

### ProjectInfoCollector

**型**: `class`

**シグネチャ**:
```
class ProjectInfoCollector:
```

**説明**:

プロジェクト情報収集クラス

*定義場所: docgen/collectors/project_info_collector.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    package_managers: 言語ごとのパッケージマネージャ辞書

*定義場所: docgen/collectors/project_info_collector.py:18*

---

### collect_all

**型**: `method`

**シグネチャ**:
```
def collect_all(self) -> ProjectInfo:
```

**説明**:

すべてのプロジェクト情報を収集

Returns:
    プロジェクト情報の辞書

*定義場所: docgen/collectors/project_info_collector.py:29*

---

### collect_build_commands

**型**: `method`

**シグネチャ**:
```
def collect_build_commands(self) -> list[str]:
```

**説明**:

ビルドコマンドを収集

Returns:
    ビルドコマンドのリスト

*定義場所: docgen/collectors/project_info_collector.py:46*

---

### collect_test_commands

**型**: `method`

**シグネチャ**:
```
def collect_test_commands(self) -> list[str]:
```

**説明**:

テストコマンドを収集

Returns:
    テストコマンドのリスト

*定義場所: docgen/collectors/project_info_collector.py:127*

---

### collect_dependencies

**型**: `method`

**シグネチャ**:
```
def collect_dependencies(self) -> dict[str, list[str]]:
```

**説明**:

依存関係を収集

Returns:
    依存関係の辞書（言語ごと）

*定義場所: docgen/collectors/project_info_collector.py:222*

---

### collect_coding_standards

**型**: `method`

**シグネチャ**:
```
def collect_coding_standards(self) -> dict[str, Any]:
```

**説明**:

コーディング規約を収集

Returns:
    コーディング規約の辞書

*定義場所: docgen/collectors/project_info_collector.py:307*

---

### collect_ci_cd_info

**型**: `method`

**シグネチャ**:
```
def collect_ci_cd_info(self) -> dict[str, Any]:
```

**説明**:

CI/CD情報を収集

Returns:
    CI/CD情報の辞書

*定義場所: docgen/collectors/project_info_collector.py:372*

---

### collect_project_structure

**型**: `method`

**シグネチャ**:
```
def collect_project_structure(self) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を収集

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/project_info_collector.py:392*

---

### collect_project_description

**型**: `method`

**シグネチャ**:
```
def collect_project_description(self) -> str | None:
```

**説明**:

プロジェクトの説明を収集

Returns:
    プロジェクトの説明文（見つからない場合はNone）

*定義場所: docgen/collectors/project_info_collector.py:429*

---


## docgen/config_manager.py

### ConfigManager

**型**: `class`

**シグネチャ**:
```
class ConfigManager:
```

**説明**:

設定ファイルの管理クラス

*定義場所: docgen/config_manager.py:42*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, docgen_dir: Path, config_path: Path | None, package_config_sample: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    docgen_dir: .docgenディレクトリパス
    config_path: 設定ファイルのパス（Noneの場合はデフォルト）
    package_config_sample: パッケージ内のサンプル設定ファイルパス

*定義場所: docgen/config_manager.py:45*

---

### get_config

**型**: `method`

**シグネチャ**:
```
def get_config(self) -> dict[str, Any]:
```

**説明**:

現在の設定を取得

*定義場所: docgen/config_manager.py:147*

---

### update_config

**型**: `method`

**シグネチャ**:
```
def update_config(self, updates: dict[str, Any]) -> None:
```

**説明**:

設定を動的に更新

Args:
    updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）

*定義場所: docgen/config_manager.py:179*

---


## docgen/detectors/base_detector.py

### BaseDetector

**型**: `class`

**シグネチャ**:
```
class BaseDetector:
```

**説明**:

言語検出のベースクラス

*定義場所: docgen/detectors/base_detector.py:11*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/detectors/base_detector.py:14*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

言語が使用されているか検出

Returns:
    検出された場合True

*定義場所: docgen/detectors/base_detector.py:24*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

検出された言語名を返す

Returns:
    言語名（例: 'python', 'javascript'）

*定義場所: docgen/detectors/base_detector.py:34*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名（例: 'pip', 'npm', 'yarn'）またはNone

*定義場所: docgen/detectors/base_detector.py:44*

---


## docgen/detectors/detector_patterns.py

### DetectorPatterns

**型**: `class`

**シグネチャ**:
```
class DetectorPatterns:
```

**説明**:

Common file detection patterns used by language detectors.

*定義場所: docgen/detectors/detector_patterns.py:6*

---

### get_package_files

**型**: `method`

**シグネチャ**:
```
def get_package_files(cls, language: str) -> list[str]:
```

**説明**:

Get package manager files for a language.

*定義場所: docgen/detectors/detector_patterns.py:136*

---

### get_source_extensions

**型**: `method`

**シグネチャ**:
```
def get_source_extensions(cls, language: str) -> list[str]:
```

**説明**:

Get source file extensions for a language.

*定義場所: docgen/detectors/detector_patterns.py:141*

---

### detect_by_package_files

**型**: `method`

**シグネチャ**:
```
def detect_by_package_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for package manager files.

*定義場所: docgen/detectors/detector_patterns.py:146*

---

### detect_by_source_files

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files.

*定義場所: docgen/detectors/detector_patterns.py:152*

---

### is_excluded_path

**型**: `method`

**シグネチャ**:
```
def is_excluded_path(cls, path: Path, project_root: Path) -> bool:
```

**説明**:

Check if a path should be excluded from detection.

*定義場所: docgen/detectors/detector_patterns.py:164*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(cls, language: str, file_exists_func) -> str | None:
```

**説明**:

Detect package manager for a language using file existence checks.

Args:
    language: Language name
    file_exists_func: Function that takes file patterns (str or tuple) and returns bool

Returns:
    Package manager name or None

*定義場所: docgen/detectors/detector_patterns.py:174*

---


## docgen/detectors/generic_detector.py

### GenericDetector

**型**: `class`

**シグネチャ**:
```
class GenericDetector:
```

**説明**:

汎用言語検出クラス

*定義場所: docgen/detectors/generic_detector.py:9*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

サポートされている汎用言語が使用されているか検出

Returns:
    サポート言語が検出された場合True

*定義場所: docgen/detectors/generic_detector.py:32*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

検出された言語名を返す
複数検出された場合は最初に見つかったものを返す

Returns:
    言語名

*定義場所: docgen/detectors/generic_detector.py:44*

---

### get_all_detected_languages

**型**: `method`

**シグネチャ**:
```
def get_all_detected_languages(self) -> list:
```

**説明**:

検出されたすべての言語を返す

Returns:
    検出された言語のリスト

*定義場所: docgen/detectors/generic_detector.py:57*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

汎用言語プロジェクトで使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名またはNone

*定義場所: docgen/detectors/generic_detector.py:70*

---


## docgen/detectors/go_detector.py

### GoDetector

**型**: `class`

**シグネチャ**:
```
class GoDetector:
```

**説明**:

Goプロジェクト検出クラス

*定義場所: docgen/detectors/go_detector.py:9*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

Goプロジェクトかどうかを検出

Returns:
    Goプロジェクトの場合True

*定義場所: docgen/detectors/go_detector.py:12*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

言語名を返す

*定義場所: docgen/detectors/go_detector.py:31*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

Goプロジェクトで使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名またはNone

*定義場所: docgen/detectors/go_detector.py:35*

---


## docgen/detectors/javascript_detector.py

### JavaScriptDetector

**型**: `class`

**シグネチャ**:
```
class JavaScriptDetector:
```

**説明**:

JavaScript/TypeScriptプロジェクト検出クラス

*定義場所: docgen/detectors/javascript_detector.py:9*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

JavaScript/TypeScriptプロジェクトかどうかを検出

Returns:
    JavaScript/TypeScriptプロジェクトの場合True

*定義場所: docgen/detectors/javascript_detector.py:12*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

言語名を返す

*定義場所: docgen/detectors/javascript_detector.py:45*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

JavaScript/TypeScriptプロジェクトで使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名またはNone

*定義場所: docgen/detectors/javascript_detector.py:59*

---


## docgen/detectors/python_detector.py

### PythonDetector

**型**: `class`

**シグネチャ**:
```
class PythonDetector:
```

**説明**:

Pythonプロジェクト検出クラス

*定義場所: docgen/detectors/python_detector.py:9*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

Pythonプロジェクトかどうかを検出

Returns:
    Pythonプロジェクトの場合True

*定義場所: docgen/detectors/python_detector.py:12*

---

### get_language

**型**: `method`

**シグネチャ**:
```
def get_language(self) -> str:
```

**説明**:

言語名を返す

*定義場所: docgen/detectors/python_detector.py:29*

---

### detect_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_package_manager(self) -> str | None:
```

**説明**:

Pythonプロジェクトで使用されているパッケージマネージャを検出

Returns:
    パッケージマネージャ名またはNone

*定義場所: docgen/detectors/python_detector.py:33*

---


## docgen/docgen.py

### DocGen

**型**: `class`

**シグネチャ**:
```
class DocGen:
```

**説明**:

ドキュメント自動生成メインクラス

*定義場所: docgen/docgen.py:28*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path | None, config_path: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ（Noneの場合は現在の作業ディレクトリ）
    config_path: 設定ファイルのパス（Noneの場合はデフォルト）

*定義場所: docgen/docgen.py:31*

---

### detect_languages

**型**: `method`

**シグネチャ**:
```
def detect_languages(self, use_parallel: bool) -> list[str]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語のリスト

*定義場所: docgen/docgen.py:65*

---

### update_config

**型**: `method`

**シグネチャ**:
```
def update_config(self, updates: dict[str, Any]) -> None:
```

**説明**:

設定を動的に更新

Args:
    updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）

*定義場所: docgen/docgen.py:79*

---

### generate_documents

**型**: `method`

**シグネチャ**:
```
def generate_documents(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/docgen.py:89*

---

### CommandLineInterface

**型**: `class`

**シグネチャ**:
```
class CommandLineInterface:
```

**説明**:

コマンドラインインターフェースクラス

*定義場所: docgen/docgen.py:108*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

*説明なし*

*定義場所: docgen/docgen.py:111*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self) -> int:
```

**説明**:

メイン実行メソッド

*定義場所: docgen/docgen.py:114*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メインエントリーポイント

*定義場所: docgen/docgen.py:279*

---


## docgen/document_generator.py

### DocumentGenerator

**型**: `class`

**シグネチャ**:
```
class DocumentGenerator:
```

**説明**:

ドキュメント生成クラス

*定義場所: docgen/document_generator.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, detected_languages: list[str], config: dict[str, Any], detected_package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    detected_languages: 検出された言語リスト
    config: 設定辞書
    detected_package_managers: 検出されたパッケージマネージャ辞書

*定義場所: docgen/document_generator.py:17*

---

### generate_documents

**型**: `method`

**シグネチャ**:
```
def generate_documents(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/document_generator.py:38*

---


## docgen/generator_factory.py

### GeneratorFactory

**型**: `class`

**シグネチャ**:
```
class GeneratorFactory:
```

**説明**:

ジェネレーターのファクトリークラス

*定義場所: docgen/generator_factory.py:12*

---

### create_generator

**型**: `method`

**シグネチャ**:
```
def create_generator(cls, generator_type: str, project_root: Path, detected_languages: list[str], config: dict[str, Any], detected_package_managers: dict[str, str] | None) -> BaseGenerator:
```

**説明**:

指定されたタイプのジェネレーターを作成

*定義場所: docgen/generator_factory.py:23*

---

### get_available_generators

**型**: `method`

**シグネチャ**:
```
def get_available_generators(cls) -> list[str]:
```

**説明**:

利用可能なジェネレーターのリストを取得

*定義場所: docgen/generator_factory.py:49*

---


## docgen/generators/agents_generator.py

### AgentsGenerator

**型**: `class`

**シグネチャ**:
```
class AgentsGenerator:
```

**説明**:

AGENTS.md生成クラス（OpenAI仕様準拠）

*定義場所: docgen/generators/agents_generator.py:27*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書

*定義場所: docgen/generators/agents_generator.py:30*

---

### agents_path

**型**: `method`

**シグネチャ**:
```
def agents_path(self):
```

*説明なし*

*定義場所: docgen/generators/agents_generator.py:49*

---


## docgen/generators/api_generator.py

### APIGenerator

**型**: `class`

**シグネチャ**:
```
class APIGenerator:
```

**説明**:

APIドキュメント生成クラス

*定義場所: docgen/generators/api_generator.py:25*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書

*定義場所: docgen/generators/api_generator.py:28*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self) -> bool:
```

**説明**:

APIドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/generators/api_generator.py:65*

---


## docgen/generators/base_generator.py

### BaseGenerator

**型**: `class`

**シグネチャ**:
```
class BaseGenerator:
```

**説明**:

ベースジェネレータークラス（AGENTS.mdとREADME.mdの共通部分）

*定義場所: docgen/generators/base_generator.py:17*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト
    config: 設定辞書
    package_managers: 検出されたパッケージマネージャの辞書

*定義場所: docgen/generators/base_generator.py:20*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self) -> bool:
```

**説明**:

ドキュメントを生成

Returns:
    成功したかどうか

*定義場所: docgen/generators/base_generator.py:176*

---


## docgen/generators/commit_message_generator.py

### CommitMessageGenerator

**型**: `class`

**シグネチャ**:
```
class CommitMessageGenerator:
```

**説明**:

コミットメッセージ生成クラス

*定義場所: docgen/generators/commit_message_generator.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, config: dict[str, Any]):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    config: 設定辞書

*定義場所: docgen/generators/commit_message_generator.py:18*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self) -> str | None:
```

**説明**:

コミットメッセージを生成

Returns:
    生成されたコミットメッセージ（エラー時はNone）

*定義場所: docgen/generators/commit_message_generator.py:31*

---


## docgen/generators/parsers/base_parser.py

### BaseParser

**型**: `class`

**シグネチャ**:
```
class BaseParser:
```

**説明**:

コード解析のベースクラス

*定義場所: docgen/generators/parsers/base_parser.py:20*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/generators/parsers/base_parser.py:23*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

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

*定義場所: docgen/generators/parsers/base_parser.py:33*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートするファイル拡張子を返す

Returns:
    拡張子のリスト（例: ['.py', '.pyw']）

*定義場所: docgen/generators/parsers/base_parser.py:52*

---

### get_parser_type

**型**: `method`

**シグネチャ**:
```
def get_parser_type(self) -> str:
```

**説明**:

パーサーの種類を返す（キャッシュキーの生成に使用）

Returns:
    パーサーの種類（例: 'python', 'javascript'）

*定義場所: docgen/generators/parsers/base_parser.py:61*

---

### parse_project

**型**: `method`

**シグネチャ**:
```
def parse_project(self, exclude_dirs: list[str] | None, use_parallel: bool, max_workers: int | None, use_cache: bool, cache_manager: Optional['CacheManager']) -> list[APIInfo]:
```

**説明**:

プロジェクト全体を解析

Args:
    exclude_dirs: 除外するディレクトリ（例: ['.git', 'node_modules']）
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）
    max_workers: 並列処理の最大ワーカー数（Noneの場合は自動）
    use_cache: キャッシュを使用するかどうか（デフォルト: True）
    cache_manager: キャッシュマネージャー（Noneの場合はキャッシュを使用しない）

Returns:
    全API情報のリスト

*定義場所: docgen/generators/parsers/base_parser.py:79*

---


## docgen/generators/parsers/generic_parser.py

### GenericParser

**型**: `class`

**シグネチャ**:
```
class GenericParser:
```

**説明**:

汎用コード解析クラス

*定義場所: docgen/generators/parsers/generic_parser.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, language: str):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 言語名（'rust', 'java', 'c', 'cpp', 'go', 'ruby', 'php'など）

*定義場所: docgen/generators/parsers/generic_parser.py:31*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

汎用ファイルを解析

Args:
    file_path: 解析するファイルのパス

Returns:
    API情報のリスト

*定義場所: docgen/generators/parsers/generic_parser.py:42*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

Returns:
    言語に応じた拡張子のリスト

*定義場所: docgen/generators/parsers/generic_parser.py:157*

---


## docgen/generators/parsers/js_parser.py

### JSParser

**型**: `class`

**シグネチャ**:
```
class JSParser:
```

**説明**:

JavaScript/TypeScriptコード解析クラス

*定義場所: docgen/generators/parsers/js_parser.py:13*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

JavaScript/TypeScriptファイルを解析

Args:
    file_path: 解析するファイルのパス

Returns:
    API情報のリスト

*定義場所: docgen/generators/parsers/js_parser.py:31*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/js_parser.py:224*

---


## docgen/generators/parsers/parser_patterns.py

### ParserPatterns

**型**: `class`

**シグネチャ**:
```
class ParserPatterns:
```

**説明**:

Common patterns and utilities for code parsing.

*定義場所: docgen/generators/parsers/parser_patterns.py:9*

---

### extract_docstring

**型**: `method`

**シグネチャ**:
```
def extract_docstring(cls, content: str, language: str, start_pos: int) -> str | None:
```

**説明**:

Extract docstring/comment from content starting at a position.

Args:
    content: Source code content
    language: Programming language
    start_pos: Position to start searching from

Returns:
    Extracted docstring or None

*定義場所: docgen/generators/parsers/parser_patterns.py:53*

---

### find_functions_and_classes

**型**: `method`

**シグネチャ**:
```
def find_functions_and_classes(cls, content: str, language: str) -> list[tuple[str, str, int]]:
```

**説明**:

Find all functions and classes in content.

Args:
    content: Source code content
    language: Programming language

Returns:
    List of (name, type, position) tuples

*定義場所: docgen/generators/parsers/parser_patterns.py:74*

---

### create_api_info

**型**: `method`

**シグネチャ**:
```
def create_api_info(cls, name: str, entity_type: str, file_path: Path, project_root: Path, line_number: int | None, signature: str | None, docstring: str | None) -> APIInfo:
```

**説明**:

Create APIInfo object with common fields.

Args:
    name: Function/class name
    entity_type: Type ('function', 'class', etc.)
    file_path: Source file path
    project_root: Project root path
    line_number: Line number (optional)
    signature: Function signature (optional)
    docstring: Documentation string (optional)

Returns:
    APIInfo object

*定義場所: docgen/generators/parsers/parser_patterns.py:98*

---

### clean_docstring

**型**: `method`

**シグネチャ**:
```
def clean_docstring(cls, docstring: str, language: str) -> str:
```

**説明**:

Clean and normalize docstring content.

Args:
    docstring: Raw docstring
    language: Programming language

Returns:
    Cleaned docstring

*定義場所: docgen/generators/parsers/parser_patterns.py:135*

---


## docgen/generators/parsers/python_parser.py

### PythonParser

**型**: `class`

**シグネチャ**:
```
class PythonParser:
```

**説明**:

Pythonコード解析クラス

*定義場所: docgen/generators/parsers/python_parser.py:30*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

Pythonファイルを解析

Args:
    file_path: 解析するPythonファイルのパス

Returns:
    API情報のリスト

*定義場所: docgen/generators/parsers/python_parser.py:33*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/python_parser.py:62*

---

### PythonASTVisitor

**型**: `class`

**シグネチャ**:
```
class PythonASTVisitor:
```

**説明**:

Python AST訪問クラス

*定義場所: docgen/generators/parsers/python_parser.py:69*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, file_path: Path, project_root: Path):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:72*

---

### visit_ClassDef

**型**: `method`

**シグネチャ**:
```
def visit_ClassDef(self, node: ast.ClassDef):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:78*

---

### visit_FunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_FunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:101*

---

### visit_AsyncFunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_AsyncFunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:104*

---


## docgen/generators/readme_generator.py

### ReadmeGenerator

**型**: `class`

**シグネチャ**:
```
class ReadmeGenerator:
```

**説明**:

README generation class

*定義場所: docgen/generators/readme_generator.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any], package_managers: dict[str, str] | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    languages: List of detected languages
    config: Configuration dictionary
    package_managers: Dictionary of detected package managers

*定義場所: docgen/generators/readme_generator.py:23*

---

### readme_path

**型**: `method`

**シグネチャ**:
```
def readme_path(self):
```

*説明なし*

*定義場所: docgen/generators/readme_generator.py:43*

---


## docgen/language_detector.py

### LanguageDetector

**型**: `class`

**シグネチャ**:
```
class LanguageDetector:
```

**説明**:

言語検出クラス

*定義場所: docgen/language_detector.py:17*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス

*定義場所: docgen/language_detector.py:20*

---

### detect_languages

**型**: `method`

**シグネチャ**:
```
def detect_languages(self, use_parallel: bool) -> list[str]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語のリスト

*定義場所: docgen/language_detector.py:31*

---

### get_detected_languages

**型**: `method`

**シグネチャ**:
```
def get_detected_languages(self) -> list[str]:
```

**説明**:

検出された言語を取得

*定義場所: docgen/language_detector.py:103*

---

### get_detected_package_managers

**型**: `method`

**シグネチャ**:
```
def get_detected_package_managers(self) -> dict[str, str]:
```

**説明**:

検出されたパッケージマネージャを取得

*定義場所: docgen/language_detector.py:107*

---


## docgen/models/agents.py

### LLMConfig

**型**: `class`

**シグネチャ**:
```
class LLMConfig:
```

**説明**:

LLM設定モデル

*定義場所: docgen/models/agents.py:8*

---

### ProjectOverview

**型**: `class`

**シグネチャ**:
```
class ProjectOverview:
```

**説明**:

Project overview model.

*定義場所: docgen/models/agents.py:26*

---

### LLMSetup

**型**: `class`

**シグネチャ**:
```
class LLMSetup:
```

**説明**:

LLM setup model.

*定義場所: docgen/models/agents.py:34*

---

### SetupInstructions

**型**: `class`

**シグネチャ**:
```
class SetupInstructions:
```

**説明**:

Setup instructions model.

*定義場所: docgen/models/agents.py:41*

---

### BuildTestInstructions

**型**: `class`

**シグネチャ**:
```
class BuildTestInstructions:
```

**説明**:

Build and test instructions model.

*定義場所: docgen/models/agents.py:49*

---

### CodingStandards

**型**: `class`

**シグネチャ**:
```
class CodingStandards:
```

**説明**:

Coding standards model.

*定義場所: docgen/models/agents.py:57*

---

### PRGuidelines

**型**: `class`

**シグネチャ**:
```
class PRGuidelines:
```

**説明**:

PR guidelines model.

*定義場所: docgen/models/agents.py:64*

---

### AgentsConfig

**型**: `class`

**シグネチャ**:
```
class AgentsConfig:
```

**説明**:

Configuration model for agents documentation.

*定義場所: docgen/models/agents.py:72*

---

### AgentsGenerationConfig

**型**: `class`

**シグネチャ**:
```
class AgentsGenerationConfig:
```

**説明**:

Agents generation configuration model.

*定義場所: docgen/models/agents.py:85*

---

### AgentsConfigSection

**型**: `class`

**シグネチャ**:
```
class AgentsConfigSection:
```

**説明**:

Agents configuration section model.

*定義場所: docgen/models/agents.py:93*

---

### AgentsDocument

**型**: `class`

**シグネチャ**:
```
class AgentsDocument:
```

**説明**:

AGENTS.mdドキュメントの構造化データモデル

*定義場所: docgen/models/agents.py:106*

---


## docgen/models/api.py

### APIParameter

**型**: `class`

**シグネチャ**:
```
class APIParameter:
```

**説明**:

APIパラメータモデル

*定義場所: docgen/models/api.py:8*

---

### APIInfo

**型**: `class`

**シグネチャ**:
```
class APIInfo:
```

**説明**:

API情報モデル

*定義場所: docgen/models/api.py:18*

---


## docgen/models/cache.py

### CacheEntry

**型**: `class`

**シグネチャ**:
```
class CacheEntry:
```

**説明**:

キャッシュエントリーモデル

*定義場所: docgen/models/cache.py:10*

---

### CacheMetadata

**型**: `class`

**シグネチャ**:
```
class CacheMetadata:
```

**説明**:

キャッシュメタデータモデル

*定義場所: docgen/models/cache.py:19*

---


## docgen/models/config.py

### LanguagesConfig

**型**: `class`

**シグネチャ**:
```
class LanguagesConfig:
```

**説明**:

Languages configuration model.

*定義場所: docgen/models/config.py:10*

---

### OutputConfig

**型**: `class`

**シグネチャ**:
```
class OutputConfig:
```

**説明**:

Output configuration model.

*定義場所: docgen/models/config.py:17*

---

### GenerationConfig

**型**: `class`

**シグネチャ**:
```
class GenerationConfig:
```

**説明**:

Generation configuration model.

*定義場所: docgen/models/config.py:25*

---

### ExcludeConfig

**型**: `class`

**シグネチャ**:
```
class ExcludeConfig:
```

**説明**:

Exclude configuration model.

*定義場所: docgen/models/config.py:34*

---

### CacheConfig

**型**: `class`

**シグネチャ**:
```
class CacheConfig:
```

**説明**:

Cache configuration model.

*定義場所: docgen/models/config.py:41*

---

### DebugConfig

**型**: `class`

**シグネチャ**:
```
class DebugConfig:
```

**説明**:

Debug configuration model.

*定義場所: docgen/models/config.py:47*

---

### DocgenConfig

**型**: `class`

**シグネチャ**:
```
class DocgenConfig:
```

**説明**:

Main configuration model for docgen.

*定義場所: docgen/models/config.py:53*

---


## docgen/models/llm.py

### LLMConfig

**型**: `class`

**シグネチャ**:
```
class LLMConfig:
```

**説明**:

LLM設定モデル

*定義場所: docgen/models/llm.py:6*

---

### LLMClientConfig

**型**: `class`

**シグネチャ**:
```
class LLMClientConfig:
```

**説明**:

LLMクライアント設定モデル

*定義場所: docgen/models/llm.py:24*

---


## docgen/models/project.py

### ProjectInfo

**型**: `class`

**シグネチャ**:
```
class ProjectInfo:
```

**説明**:

Project information model.

*定義場所: docgen/models/project.py:8*

---


## docgen/models/readme.py

### Dependencies

**型**: `class`

**シグネチャ**:
```
class Dependencies:
```

**説明**:

Dependencies model.

*定義場所: docgen/models/readme.py:6*

---

### ReadmeSetupInstructions

**型**: `class`

**シグネチャ**:
```
class ReadmeSetupInstructions:
```

**説明**:

Setup instructions for README.

*定義場所: docgen/models/readme.py:14*

---

### ReadmeConfig

**型**: `class`

**シグネチャ**:
```
class ReadmeConfig:
```

**説明**:

Configuration model for README documentation.

*定義場所: docgen/models/readme.py:21*

---

### ReadmeDocument

**型**: `class`

**シグネチャ**:
```
class ReadmeDocument:
```

**説明**:

READMEドキュメントの構造化データモデル

*定義場所: docgen/models/readme.py:37*

---


## docgen/utils/cache.py

### CacheManager

**型**: `class`

**シグネチャ**:
```
class CacheManager:
```

**説明**:

キャッシュ管理クラス

*定義場所: docgen/utils/cache.py:20*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, cache_dir: Path | None, enabled: bool):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    cache_dir: キャッシュディレクトリ（Noneの場合は`docgen/.cache/`）
    enabled: キャッシュを有効にするかどうか

*定義場所: docgen/utils/cache.py:23*

---

### get_file_hash

**型**: `method`

**シグネチャ**:
```
def get_file_hash(self, file_path: Path) -> str:
```

**説明**:

ファイルのハッシュを計算

Args:
    file_path: ファイルパス

Returns:
    ファイルのSHA256ハッシュ（16進数文字列）

*定義場所: docgen/utils/cache.py:78*

---

### get_cache_key

**型**: `method`

**シグネチャ**:
```
def get_cache_key(self, file_path: Path, parser_type: str) -> str:
```

**説明**:

キャッシュキーを生成

Args:
    file_path: ファイルパス（相対パスまたは絶対パス）
    parser_type: パーサーの種類（例: 'python', 'javascript'）

Returns:
    キャッシュキー

*定義場所: docgen/utils/cache.py:99*

---

### get_cached_result

**型**: `method`

**シグネチャ**:
```
def get_cached_result(self, file_path: Path, parser_type: str) -> list[APIInfo] | None:
```

**説明**:

キャッシュから結果を取得

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類

Returns:
    キャッシュされた結果（存在する場合）、またはNone

*定義場所: docgen/utils/cache.py:124*

---

### set_cached_result

**型**: `method`

**シグネチャ**:
```
def set_cached_result(self, file_path: Path, parser_type: str, result: list[APIInfo]) -> None:
```

**説明**:

結果をキャッシュに保存

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類
    result: 解析結果

*定義場所: docgen/utils/cache.py:164*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(self) -> None:
```

**説明**:

キャッシュをクリア

*定義場所: docgen/utils/cache.py:194*

---

### invalidate_file

**型**: `method`

**シグネチャ**:
```
def invalidate_file(self, file_path: Path, parser_type: str | None) -> None:
```

**説明**:

特定のファイルのキャッシュを無効化

Args:
    file_path: ファイルパス
    parser_type: パーサーの種類（Noneの場合はすべてのパーサータイプ）

*定義場所: docgen/utils/cache.py:201*

---

### save

**型**: `method`

**シグネチャ**:
```
def save(self) -> None:
```

**説明**:

キャッシュを保存（明示的に保存する場合）

*定義場所: docgen/utils/cache.py:237*

---

### get_cache_stats

**型**: `method`

**シグネチャ**:
```
def get_cache_stats(self) -> dict[str, Any]:
```

**説明**:

キャッシュの統計情報を取得

Returns:
    統計情報の辞書

*定義場所: docgen/utils/cache.py:241*

---


## docgen/utils/config_utils.py

### get_nested_config

**型**: `function`

**シグネチャ**:
```
def get_nested_config(config: dict[str, Any]) -> Any:
```

**説明**:

ネストされた設定値を安全に取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    設定値。存在しない場合はdefault

Examples:
    >>> config = {"a": {"b": {"c": "value"}}}
    >>> get_nested_config(config, "a", "b", "c")
    'value'
    >>> get_nested_config(config, "a", "x", "y", default="default")
    'default'

*定義場所: docgen/utils/config_utils.py:8*

---

### get_config_bool

**型**: `function`

**シグネチャ**:
```
def get_config_bool(config: dict[str, Any]) -> bool:
```

**説明**:

設定値をブール値として取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    ブール値

*定義場所: docgen/utils/config_utils.py:36*

---

### get_config_list

**型**: `function`

**シグネチャ**:
```
def get_config_list(config: dict[str, Any]) -> list:
```

**説明**:

設定値をリストとして取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    リスト

*定義場所: docgen/utils/config_utils.py:56*

---

### get_config_str

**型**: `function`

**シグネチャ**:
```
def get_config_str(config: dict[str, Any]) -> str:
```

**説明**:

設定値を文字列として取得

Args:
    config: 設定辞書
    *keys: 取得するキーのパス
    default: デフォルト値

Returns:
    文字列

*定義場所: docgen/utils/config_utils.py:81*

---


## docgen/utils/error.py

### DocGenError

**型**: `class`

**シグネチャ**:
```
class DocGenError:
```

**説明**:

DocGenの基本例外クラス

*定義場所: docgen/utils/error.py:13*

---

### ConfigError

**型**: `class`

**シグネチャ**:
```
class ConfigError:
```

**説明**:

設定関連のエラー

*定義場所: docgen/utils/error.py:19*

---

### LanguageDetectionError

**型**: `class`

**シグネチャ**:
```
class LanguageDetectionError:
```

**説明**:

言語検出関連のエラー

*定義場所: docgen/utils/error.py:25*

---

### DocumentGenerationError

**型**: `class`

**シグネチャ**:
```
class DocumentGenerationError:
```

**説明**:

ドキュメント生成関連のエラー

*定義場所: docgen/utils/error.py:31*

---

### handle_error

**型**: `function`

**シグネチャ**:
```
def handle_error(error: Exception, context: str, raise_exception: bool) -> None:
```

**説明**:

エラーを統一的に処理

Args:
    error: 発生した例外
    context: エラーのコンテキスト情報
    raise_exception: DocGenErrorを発生させるかどうか

*定義場所: docgen/utils/error.py:37*

---


## docgen/utils/exceptions.py

### ErrorMessages

**型**: `class`

**シグネチャ**:
```
class ErrorMessages:
```

**説明**:

共通エラーメッセージ定数

*定義場所: docgen/utils/exceptions.py:9*

---

### DocGenError

**型**: `class`

**シグネチャ**:
```
class DocGenError:
```

**説明**:

ドキュメント生成システムの基本例外クラス

*定義場所: docgen/utils/exceptions.py:24*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, details: str | None, error_code: str | None, context: dict[str, Any] | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:27*

---

### __str__

**型**: `method`

**シグネチャ**:
```
def __str__(self) -> str:
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:39*

---

### ConfigError

**型**: `class`

**シグネチャ**:
```
class ConfigError:
```

**説明**:

設定関連のエラー

*定義場所: docgen/utils/exceptions.py:49*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, config_path: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:52*

---

### LLMError

**型**: `class`

**シグネチャ**:
```
class LLMError:
```

**説明**:

LLM関連のエラー

*定義場所: docgen/utils/exceptions.py:64*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, provider: str | None, model: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:67*

---

### ParseError

**型**: `class`

**シグネチャ**:
```
class ParseError:
```

**説明**:

解析関連のエラー

*定義場所: docgen/utils/exceptions.py:81*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, file_path: str | None, language: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:84*

---

### CacheError

**型**: `class`

**シグネチャ**:
```
class CacheError:
```

**説明**:

キャッシュ関連のエラー

*定義場所: docgen/utils/exceptions.py:100*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, cache_key: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:103*

---

### FileOperationError

**型**: `class`

**シグネチャ**:
```
class FileOperationError:
```

**説明**:

ファイル操作関連のエラー

*定義場所: docgen/utils/exceptions.py:115*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, file_path: str | None, operation: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:118*

---


## docgen/utils/file_utils.py

### safe_read_file

**型**: `function`

**シグネチャ**:
```
def safe_read_file(file_path: Path, encoding: str) -> str | None:
```

**説明**:

ファイルを安全に読み込む

Args:
    file_path: 読み込むファイルのパス
    encoding: 文字エンコーディング

Returns:
    ファイルの内容。読み込み失敗時はNone

*定義場所: docgen/utils/file_utils.py:20*

---

### save_yaml_file

**型**: `function`

**シグネチャ**:
```
def save_yaml_file(file_path: Path, data: dict[str, Any]) -> bool:
```

**説明**:

YAMLファイルを保存

Args:
    file_path: 保存先ファイルパス
    data: 保存するデータ

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:39*

---

### safe_write_file

**型**: `function`

**シグネチャ**:
```
def safe_write_file(file_path: Path, content: str, encoding: str) -> bool:
```

**説明**:

ファイルを安全に書き込む

Args:
    file_path: 書き込むファイルのパス
    content: 書き込む内容
    encoding: 文字エンコーディング

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:61*

---

### safe_read_json

**型**: `function`

**シグネチャ**:
```
def safe_read_json(file_path: Path) -> Any | None:
```

**説明**:

JSONファイルを安全に読み込む

Args:
    file_path: JSONファイルのパス

Returns:
    パースされたJSONデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:81*

---

### load_toml_file

**型**: `function`

**シグネチャ**:
```
def load_toml_file(file_path: Path) -> dict[str, Any] | None:
```

**説明**:

TOMLファイルを読み込む

Args:
    file_path: 読み込むTOMLファイルのパス

Returns:
    読み込んだ辞書。読み込み失敗時はNone

*定義場所: docgen/utils/file_utils.py:100*

---

### find_files_with_extensions

**型**: `function`

**シグネチャ**:
```
def find_files_with_extensions(root_dir: Path, extensions: list[str]) -> list[Path]:
```

**説明**:

指定された拡張子のファイルを検索

Args:
    root_dir: 検索するルートディレクトリ
    extensions: 拡張子のリスト（例: ['.py', '.js']）

Returns:
    見つかったファイルのリスト

*定義場所: docgen/utils/file_utils.py:121*

---

### safe_read_yaml

**型**: `function`

**シグネチャ**:
```
def safe_read_yaml(file_path: Path) -> Any | None:
```

**説明**:

YAMLファイルを安全に読み込む

Args:
    file_path: YAMLファイルのパス

Returns:
    パースされたYAMLデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:138*

---

### safe_read_toml

**型**: `function`

**シグネチャ**:
```
def safe_read_toml(file_path: Path) -> Any | None:
```

**説明**:

TOMLファイルを安全に読み込む

Args:
    file_path: TOMLファイルのパス

Returns:
    パースされたTOMLデータ。失敗時はNone

*定義場所: docgen/utils/file_utils.py:159*

---


## docgen/utils/llm_client.py

### BaseLLMClient

**型**: `class`

**シグネチャ**:
```
class BaseLLMClient:
```

**説明**:

LLMクライアントの抽象基底クラス

*定義場所: docgen/utils/llm_client.py:18*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | LLMConfig):
```

**説明**:

初期化

Args:
    config: LLM設定辞書またはLLMConfigオブジェクト

*定義場所: docgen/utils/llm_client.py:21*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

テキストを生成

Args:
    prompt: プロンプト
    system_prompt: システムプロンプト（オプション）
    **kwargs: その他のパラメータ

Returns:
    生成されたテキスト（エラー時はNone）

*定義場所: docgen/utils/llm_client.py:38*

---

### create_outlines_model

**型**: `method`

**シグネチャ**:
```
def create_outlines_model(self):
```

**説明**:

Outlinesモデルを作成

Returns:
    Outlinesモデルインスタンス（Outlinesが利用できない場合はNone）

*定義場所: docgen/utils/llm_client.py:52*

---

### OpenAIClient

**型**: `class`

**シグネチャ**:
```
class OpenAIClient:
```

**説明**:

OpenAI APIクライアント

*定義場所: docgen/utils/llm_client.py:115*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm_client.py:118*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

OpenAI APIを使用してテキストを生成

*定義場所: docgen/utils/llm_client.py:140*

---

### AnthropicClient

**型**: `class`

**シグネチャ**:
```
class AnthropicClient:
```

**説明**:

Anthropic APIクライアント

*定義場所: docgen/utils/llm_client.py:169*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm_client.py:172*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

Anthropic APIを使用してテキストを生成

*定義場所: docgen/utils/llm_client.py:193*

---

### LocalLLMClient

**型**: `class`

**シグネチャ**:
```
class LocalLLMClient:
```

**説明**:

ローカルLLMクライアント（Ollama、LM Studio対応）

*定義場所: docgen/utils/llm_client.py:229*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm_client.py:232*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

ローカルLLMを使用してテキストを生成

*定義場所: docgen/utils/llm_client.py:258*

---

### LLMClientFactory

**型**: `class`

**シグネチャ**:
```
class LLMClientFactory:
```

**説明**:

LLMクライアントのファクトリークラス

*定義場所: docgen/utils/llm_client.py:352*

---

### create_client

**型**: `method`

**シグネチャ**:
```
def create_client(config: dict[str, Any] | LLMClientConfig, mode: str) -> BaseLLMClient | None:
```

**説明**:

LLMクライアントを作成

Args:
    config: LLM設定辞書またはLLMClientConfigオブジェクト
    mode: 'api' または 'local'

Returns:
    LLMクライアントインスタンス（エラー時はNone）

*定義場所: docgen/utils/llm_client.py:356*

---

### create_client_with_fallback

**型**: `method`

**シグネチャ**:
```
def create_client_with_fallback(config: dict[str, Any], preferred_mode: str) -> BaseLLMClient | None:
```

**説明**:

LLMクライアントを作成（フォールバック付き）

Args:
    config: LLM設定辞書
    preferred_mode: 優先するモード（'api' または 'local'）

Returns:
    LLMクライアントインスタンス（エラー時はNone）

*定義場所: docgen/utils/llm_client.py:415*

---


## docgen/utils/llm_client_utils.py

### LLMClientInitializer

**型**: `class`

**シグネチャ**:
```
class LLMClientInitializer:
```

**説明**:

Common initialization patterns for LLM clients.

*定義場所: docgen/utils/llm_client_utils.py:20*

---

### setup_provider_config

**型**: `method`

**シグネチャ**:
```
def setup_provider_config(config: dict[str, Any], provider: str) -> dict[str, Any]:
```

**説明**:

Set up provider-specific configuration.

Args:
    config: Configuration dictionary
    provider: Provider name ('openai', 'anthropic', etc.)

Returns:
    Updated configuration dictionary

*定義場所: docgen/utils/llm_client_utils.py:24*

---

### get_api_key

**型**: `method`

**シグネチャ**:
```
def get_api_key(config, env_var: str, default_env: str) -> str:
```

**説明**:

Get API key from config or environment.

Args:
    config: LLMConfig object
    env_var: Environment variable name from config
    default_env: Default environment variable name

Returns:
    API key string

*定義場所: docgen/utils/llm_client_utils.py:41*

---

### initialize_client_with_fallback

**型**: `method`

**シグネチャ**:
```
def initialize_client_with_fallback(client_class, config: dict[str, Any], import_name: str, package_name: str, error_prefix: str):
```

**説明**:

Initialize LLM client with common error handling.

Args:
    client_class: Client class to instantiate
    config: Configuration dictionary
    import_name: Module name to import
    package_name: Package name for error messages
    error_prefix: Prefix for error messages

Returns:
    Initialized client instance

Raises:
    ImportError: If required package is not installed
    ConfigError: If initialization fails

*定義場所: docgen/utils/llm_client_utils.py:58*

---

### handle_api_response

**型**: `method`

**シグネチャ**:
```
def handle_api_response(response, response_processor):
```

**説明**:

Handle API response with common error checking.

Args:
    response: API response object
    response_processor: Optional function to process response content

Returns:
    Processed response content or None

*定義場所: docgen/utils/llm_client_utils.py:95*

---

### create_retry_wrapper

**型**: `method`

**シグネチャ**:
```
def create_retry_wrapper(max_retries: int, retry_delay: float):
```

**説明**:

Create a retry wrapper function.

Args:
    max_retries: Maximum number of retries
    retry_delay: Delay between retries

Returns:
    Retry wrapper function

*定義場所: docgen/utils/llm_client_utils.py:140*

---


## docgen/utils/logger.py

### setup_logger

**型**: `function`

**シグネチャ**:
```
def setup_logger(name: str, level: str | None, log_file: Path | None) -> logging.Logger:
```

**説明**:

ロガーを設定して返す

Args:
    name: ロガー名
    level: ログレベル（'DEBUG', 'INFO', 'WARNING', 'ERROR'）
            Noneの場合は環境変数DOCGEN_LOG_LEVELから取得、それもなければ'INFO'
    log_file: ログファイルのパス（Noneの場合は標準出力のみ）

Returns:
    設定済みのロガー

*定義場所: docgen/utils/logger.py:11*

---

### get_logger

**型**: `function`

**シグネチャ**:
```
def get_logger(name: str | None) -> logging.Logger:
```

**説明**:

ロガーを取得する（既に設定されている場合はそれを返す）

Args:
    name: ロガー名（Noneの場合は'docgen'）

Returns:
    ロガー

*定義場所: docgen/utils/logger.py:62*

---


## docgen/utils/markdown_utils.py

### get_current_timestamp

**型**: `function`

**シグネチャ**:
```
def get_current_timestamp() -> str:
```

**説明**:

Get current timestamp in standard format.

*定義場所: docgen/utils/markdown_utils.py:31*

---

### extract_project_description

**型**: `function`

**シグネチャ**:
```
def extract_project_description(project_root: Path, project_info_description: str | None, exclude_readme_path: Path | None) -> str:
```

**説明**:

Extract project description from README.md or project info.

Args:
    project_root: Project root directory
    project_info_description: Description from project info (fallback)
    exclude_readme_path: README path to exclude (to prevent circular reference)

Returns:
    Project description text

*定義場所: docgen/utils/markdown_utils.py:38*

---

### format_commands_with_package_manager

**型**: `function`

**シグネチャ**:
```
def format_commands_with_package_manager(commands: list[str], package_managers: dict[str, str], language: str, max_commands: int) -> list[str]:
```

**説明**:

Format build/test commands with package manager awareness.

Args:
    commands: List of commands to format
    package_managers: Dict of language -> package manager
    language: Programming language
    max_commands: Maximum number of commands to display

Returns:
    Formatted command lines

*定義場所: docgen/utils/markdown_utils.py:79*

---

### MarkdownSectionBuilder

**型**: `class`

**シグネチャ**:
```
class MarkdownSectionBuilder:
```

**説明**:

Utility class for building markdown sections.

*定義場所: docgen/utils/markdown_utils.py:114*

---

### build_section

**型**: `method`

**シグネチャ**:
```
def build_section(header: str, content_lines: list[str]) -> list[str]:
```

**説明**:

Build a markdown section with header and content.

Args:
    header: Section header (without ##)
    content_lines: Content lines

Returns:
    Formatted markdown lines

*定義場所: docgen/utils/markdown_utils.py:118*

---

### build_code_block

**型**: `method`

**シグネチャ**:
```
def build_code_block(commands: list[str], language: str) -> list[str]:
```

**説明**:

Build a code block with commands.

Args:
    commands: List of commands
    language: Code block language

Returns:
    Formatted code block lines

*定義場所: docgen/utils/markdown_utils.py:135*

---

### clean_llm_output_advanced

**型**: `function`

**シグネチャ**:
```
def clean_llm_output_advanced(text: str) -> str:
```

**説明**:

Advanced LLM output cleaning with thinking process removal and code block handling.

Args:
    text: LLM generated text to clean

Returns:
    Cleaned text with thinking processes removed

*定義場所: docgen/utils/markdown_utils.py:155*

---


## docgen/utils/outlines_utils.py

### should_use_outlines

**型**: `function`

**シグネチャ**:
```
def should_use_outlines(config: dict[str, Any]) -> bool:
```

**説明**:

Outlinesを使用するかどうかを判定

Args:
    config: 設定辞書

Returns:
    Outlinesを使用するかどうか

*定義場所: docgen/utils/outlines_utils.py:19*

---

### create_outlines_model

**型**: `function`

**シグネチャ**:
```
def create_outlines_model(client, provider: str):
```

**説明**:

Outlinesモデルを作成

Args:
    client: LLMクライアント
    provider: プロバイダー名 ('openai', 'anthropic', 'local')

Returns:
    Outlinesモデルインスタンス（作成できない場合はNone）

*定義場所: docgen/utils/outlines_utils.py:33*

---

### get_llm_client_with_fallback

**型**: `function`

**シグネチャ**:
```
def get_llm_client_with_fallback(config: dict[str, Any], agents_config: dict[str, Any]):
```

**説明**:

LLMクライアントを取得（フォールバック付き）

Args:
    config: メイン設定
    agents_config: AGENTS設定

Returns:
    LLMクライアントインスタンス

*定義場所: docgen/utils/outlines_utils.py:69*

---

### clean_llm_output

**型**: `function`

**シグネチャ**:
```
def clean_llm_output(text: str) -> str:
```

**説明**:

LLMの出力から思考過程や試行錯誤の痕跡を削除

Args:
    text: LLMで生成されたテキスト

Returns:
    クリーンアップされたテキスト

*定義場所: docgen/utils/outlines_utils.py:88*

---

### validate_output

**型**: `function`

**シグネチャ**:
```
def validate_output(text: str) -> bool:
```

**説明**:

LLMの出力を検証して、不適切な内容が含まれていないかチェック

Args:
    text: 検証するテキスト

Returns:
    検証に合格したかどうか

*定義場所: docgen/utils/outlines_utils.py:293*

---


## docgen/utils/project_utils.py

### get_project_structure

**型**: `function`

**シグネチャ**:
```
def get_project_structure(project_root: Path, max_depth: int, max_items: int) -> list[str]:
```

**説明**:

プロジェクト構造を取得（重要なディレクトリとファイルのみ）

Args:
    project_root: プロジェクトルート
    max_depth: 最大深さ
    max_items: 最大項目数

Returns:
    構造の行リスト

*定義場所: docgen/utils/project_utils.py:8*

---


## docgen/utils/uv_utils.py

### detect_uv_usage

**型**: `function`

**シグネチャ**:
```
def detect_uv_usage(project_root: Path) -> bool:
```

**説明**:

プロジェクトがuvを使用しているかを検出

Args:
    project_root: プロジェクトのルートディレクトリ

Returns:
    uvを使用している場合True

*定義場所: docgen/utils/uv_utils.py:8*

---

### wrap_command_with_uv

**型**: `function`

**シグネチャ**:
```
def wrap_command_with_uv(command: str) -> str:
```

**説明**:

uvを使用する場合のコマンドをuv runでラップ

Args:
    command: 元のコマンド

Returns:
    uv runでラップされたコマンド

*定義場所: docgen/utils/uv_utils.py:50*

---


## scripts/generate_requirements.py

### generate_requirements_file

**型**: `function`

**シグネチャ**:
```
def generate_requirements_file(extras: list[str], output_file: Path, include_base: bool) -> None:
```

**説明**:

pyproject.tomlからrequirementsファイルを生成

Args:
    extras: オプショナル依存関係のリスト（例: ['docgen', 'test']）
    output_file: 出力ファイルのパス
    include_base: 基本依存関係を含めるかどうか

*定義場所: scripts/generate_requirements.py:12*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メイン処理

*定義場所: scripts/generate_requirements.py:74*

---


## tests/conftest.py

### temp_project

**型**: `function`

**シグネチャ**:
```
def temp_project():
```

**説明**:

Create a temporary project directory with basic structure.

*定義場所: tests/conftest.py:11*

---

### sample_config

**型**: `function`

**シグネチャ**:
```
def sample_config():
```

**説明**:

Return a sample configuration dictionary.

*定義場所: tests/conftest.py:44*

---

### mock_llm_client

**型**: `function`

**シグネチャ**:
```
def mock_llm_client(mocker):
```

**説明**:

Mock LLMクライアント

*定義場所: tests/conftest.py:66*

---


## tests/test_cli.py

### TestCommandLineInterface

**型**: `class`

**シグネチャ**:
```
class TestCommandLineInterface:
```

**説明**:

CommandLineInterfaceクラスのテスト

*定義場所: tests/test_cli.py:10*

---

### test_init

**型**: `method`

**シグネチャ**:
```
def test_init(self):
```

**説明**:

初期化テスト

*定義場所: tests/test_cli.py:13*

---

### test_run_detect_only

**型**: `method`

**シグネチャ**:
```
def test_run_detect_only(self, mock_docgen_class, tmp_path):
```

**説明**:

言語検出のみ実行テスト

*定義場所: tests/test_cli.py:19*

---


## tests/test_config_manager.py

### TestConfigManager

**型**: `class`

**シグネチャ**:
```
class TestConfigManager:
```

**説明**:

ConfigManagerクラスのテスト

*定義場所: tests/test_config_manager.py:15*

---

### test_config_manager_initialization_with_config_path

**型**: `method`

**シグネチャ**:
```
def test_config_manager_initialization_with_config_path(self, temp_project):
```

**説明**:

設定ファイルパス指定での初期化テスト

*定義場所: tests/test_config_manager.py:18*

---

### test_config_manager_initialization_default_config_path

**型**: `method`

**シグネチャ**:
```
def test_config_manager_initialization_default_config_path(self, temp_project):
```

**説明**:

デフォルト設定ファイルパスでの初期化テスト

*定義場所: tests/test_config_manager.py:30*

---

### test_load_config_existing_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_existing_file(self, mock_safe_read_yaml, temp_project):
```

**説明**:

既存の設定ファイル読み込みテスト

*定義場所: tests/test_config_manager.py:40*

---

### test_load_config_nonexistent_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_nonexistent_file(self, mock_safe_read_yaml, temp_project):
```

**説明**:

存在しない設定ファイルのテスト

*定義場所: tests/test_config_manager.py:92*

---

### test_create_default_config_with_sample

**型**: `method`

**シグネチャ**:
```
def test_create_default_config_with_sample(self, mock_safe_read_yaml, temp_project):
```

**説明**:

サンプル設定ファイルからのデフォルト設定作成テスト

*定義場所: tests/test_config_manager.py:113*

---

### test_create_default_config_without_sample

**型**: `method`

**シグネチャ**:
```
def test_create_default_config_without_sample(self, mock_safe_read_yaml, temp_project):
```

**説明**:

サンプル設定ファイルなしの場合のデフォルト設定作成テスト

*定義場所: tests/test_config_manager.py:137*

---

### test_copy_sample_config_success

**型**: `method`

**シグネチャ**:
```
def test_copy_sample_config_success(self, temp_project):
```

**説明**:

サンプル設定ファイルのコピー成功テスト

*定義場所: tests/test_config_manager.py:158*

---

### test_copy_sample_config_failure

**型**: `method`

**シグネチャ**:
```
def test_copy_sample_config_failure(self, temp_project):
```

**説明**:

サンプル設定ファイルのコピー失敗テスト

*定義場所: tests/test_config_manager.py:178*

---

### test_get_default_config

**型**: `method`

**シグネチャ**:
```
def test_get_default_config(self, temp_project):
```

**説明**:

デフォルト設定の取得テスト

*定義場所: tests/test_config_manager.py:197*

---

### test_get_config

**型**: `method`

**シグネチャ**:
```
def test_get_config(self, temp_project):
```

**説明**:

設定取得テスト

*定義場所: tests/test_config_manager.py:214*

---

### test_update_config_simple

**型**: `method`

**シグネチャ**:
```
def test_update_config_simple(self, temp_project):
```

**説明**:

シンプルな設定更新テスト

*定義場所: tests/test_config_manager.py:257*

---

### test_update_config_nested

**型**: `method`

**シグネチャ**:
```
def test_update_config_nested(self, temp_project):
```

**説明**:

ネストされた設定更新テスト

*定義場所: tests/test_config_manager.py:287*

---


## tests/test_detectors/test_generic_detector.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root, relative_path, content):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:8*

---

### TestGenericDetector

**型**: `class`

**シグネチャ**:
```
class TestGenericDetector:
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:18*

---

### test_detect_rust

**型**: `method`

**シグネチャ**:
```
def test_detect_rust(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:19*

---

### test_detect_java

**型**: `method`

**シグネチャ**:
```
def test_detect_java(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:25*

---

### test_detect_ruby

**型**: `method`

**シグネチャ**:
```
def test_detect_ruby(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:31*

---

### test_detect_cpp

**型**: `method`

**シグネチャ**:
```
def test_detect_cpp(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:37*

---

### test_detect_without_supported_language

**型**: `method`

**シグネチャ**:
```
def test_detect_without_supported_language(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:43*

---

### test_detect_package_manager_none

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_none(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:48*

---

### test_get_all_detected_languages

**型**: `method`

**シグネチャ**:
```
def test_get_all_detected_languages(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:52*

---

### test_get_language_returns_first_detected

**型**: `method`

**シグネチャ**:
```
def test_get_language_returns_first_detected(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:60*

---

### test_detect_with_header_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_header_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:66*

---

### test_detect_case_insensitive_extensions

**型**: `method`

**シグネチャ**:
```
def test_detect_case_insensitive_extensions(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_generic_detector.py:72*

---


## tests/test_detectors/test_go_detector.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root, relative_path, content):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:8*

---

### TestGoDetector

**型**: `class`

**シグネチャ**:
```
class TestGoDetector:
```

**説明**:

GoDetectorクラスのテスト

*定義場所: tests/test_detectors/test_go_detector.py:18*

---

### test_detect_with_go_mod

**型**: `method`

**シグネチャ**:
```
def test_detect_with_go_mod(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:21*

---

### test_detect_with_go_sum

**型**: `method`

**シグネチャ**:
```
def test_detect_with_go_sum(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:27*

---

### test_detect_with_gopkg_toml

**型**: `method`

**シグネチャ**:
```
def test_detect_with_gopkg_toml(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:32*

---

### test_detect_with_gopkg_lock

**型**: `method`

**シグネチャ**:
```
def test_detect_with_gopkg_lock(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:37*

---

### test_detect_with_glide_yaml

**型**: `method`

**シグネチャ**:
```
def test_detect_with_glide_yaml(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:42*

---

### test_detect_with_glide_lock

**型**: `method`

**シグネチャ**:
```
def test_detect_with_glide_lock(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:47*

---

### test_detect_package_manager_go_modules

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_go_modules(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:52*

---

### test_detect_package_manager_dep

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_dep(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:57*

---

### test_detect_package_manager_glide

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_glide(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:62*

---

### test_detect_package_manager_none

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_none(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:67*

---

### test_detect_with_go_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_go_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:71*

---

### test_detect_without_go_files

**型**: `method`

**シグネチャ**:
```
def test_detect_without_go_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:80*

---

### test_get_language

**型**: `method`

**シグネチャ**:
```
def test_get_language(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_go_detector.py:84*

---


## tests/test_detectors/test_javascript_detector.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root, relative_path, content):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:8*

---

### TestJavaScriptDetector

**型**: `class`

**シグネチャ**:
```
class TestJavaScriptDetector:
```

**説明**:

JavaScriptDetectorクラスのテスト

*定義場所: tests/test_detectors/test_javascript_detector.py:18*

---

### test_detect_with_package_json

**型**: `method`

**シグネチャ**:
```
def test_detect_with_package_json(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:21*

---

### test_detect_with_js_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_js_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:26*

---

### test_detect_with_ts_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_ts_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:32*

---

### test_detect_with_tsconfig_json

**型**: `method`

**シグネチャ**:
```
def test_detect_with_tsconfig_json(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:38*

---

### test_detect_without_javascript

**型**: `method`

**シグネチャ**:
```
def test_detect_without_javascript(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:44*

---

### test_get_language_javascript

**型**: `method`

**シグネチャ**:
```
def test_get_language_javascript(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:48*

---

### test_detect_package_manager_pnpm

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_pnpm(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:53*

---

### test_detect_package_manager_yarn

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_yarn(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:58*

---

### test_detect_package_manager_npm_lock

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_npm_lock(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:63*

---

### test_detect_package_manager_npm_package_json

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_npm_package_json(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:68*

---

### test_detect_package_manager_none

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_none(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:73*

---

### test_get_language_typescript_with_tsconfig

**型**: `method`

**シグネチャ**:
```
def test_get_language_typescript_with_tsconfig(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:77*

---

### test_get_language_typescript_with_ts_files

**型**: `method`

**シグネチャ**:
```
def test_get_language_typescript_with_ts_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:83*

---

### test_get_language_typescript_with_tsx_files

**型**: `method`

**シグネチャ**:
```
def test_get_language_typescript_with_tsx_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_javascript_detector.py:88*

---


## tests/test_detectors/test_python_detector.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root, relative_path, content):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:10*

---

### TestPythonDetector

**型**: `class`

**シグネチャ**:
```
class TestPythonDetector:
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:20*

---

### test_detect_with_requirements_txt

**型**: `method`

**シグネチャ**:
```
def test_detect_with_requirements_txt(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:21*

---

### test_detect_with_setup_py

**型**: `method`

**シグネチャ**:
```
def test_detect_with_setup_py(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:27*

---

### test_detect_with_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def test_detect_with_pyproject_toml(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:32*

---

### test_detect_with_py_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_py_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:37*

---

### test_detect_without_python

**型**: `method`

**シグネチャ**:
```
def test_detect_without_python(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:42*

---

### test_get_language

**型**: `method`

**シグネチャ**:
```
def test_get_language(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:46*

---

### test_detect_package_manager_uv

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_uv(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:50*

---

### test_detect_package_manager_poetry

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_poetry(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:55*

---

### test_detect_package_manager_poetry_pyproject

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_poetry_pyproject(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:60*

---

### test_detect_package_manager_conda

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_conda(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:65*

---

### test_detect_package_manager_pip_requirements

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_pip_requirements(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:70*

---

### test_detect_package_manager_pip_setup_py

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_pip_setup_py(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:75*

---

### test_detect_package_manager_none

**型**: `method`

**シグネチャ**:
```
def test_detect_package_manager_none(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:80*

---

### test_detect_with_nested_python_files

**型**: `method`

**シグネチャ**:
```
def test_detect_with_nested_python_files(self, temp_project):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:84*

---

### test_detect_ignores_symlinks

**型**: `method`

**シグネチャ**:
```
def test_detect_ignores_symlinks(self, temp_project, monkeypatch):
```

*説明なし*

*定義場所: tests/test_detectors/test_python_detector.py:89*

---


## tests/test_docgen.py

### TestDocGen

**型**: `class`

**シグネチャ**:
```
class TestDocGen:
```

**説明**:

DocGenクラスのテスト

*定義場所: tests/test_docgen.py:18*

---

### test_initialization_default

**型**: `method`

**シグネチャ**:
```
def test_initialization_default(self, temp_project):
```

**説明**:

デフォルト設定での初期化テスト

*定義場所: tests/test_docgen.py:21*

---

### test_load_config_missing_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_missing_file(self, temp_project):
```

**説明**:

設定ファイルが存在しない場合のテスト

*定義場所: tests/test_docgen.py:31*

---

### test_update_config

**型**: `method`

**シグネチャ**:
```
def test_update_config(self, temp_project):
```

**説明**:

設定更新テスト

*定義場所: tests/test_docgen.py:41*

---

### test_detect_languages_parallel

**型**: `method`

**シグネチャ**:
```
def test_detect_languages_parallel(self, mock_generic, mock_go, mock_js, mock_python, temp_project):
```

**説明**:

並列言語検出テスト

*定義場所: tests/test_docgen.py:56*

---

### test_detect_languages_sequential

**型**: `method`

**シグネチャ**:
```
def test_detect_languages_sequential(self, mock_generic, mock_go, mock_js, mock_python, temp_project):
```

**説明**:

逐次言語検出テスト

*定義場所: tests/test_docgen.py:85*

---

### test_generate_documents_success

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_success(self, mock_language_detector, mock_agents, mock_readme, mock_api, temp_project):
```

**説明**:

ドキュメント生成成功テスト

*定義場所: tests/test_docgen.py:113*

---

### test_generate_documents_partial_failure

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_partial_failure(self, mock_agents, mock_readme, mock_api, temp_project):
```

**説明**:

ドキュメント生成一部失敗テスト

*定義場所: tests/test_docgen.py:136*

---

### test_generate_documents_no_languages

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project):
```

**説明**:

言語が検出されない場合のテスト

*定義場所: tests/test_docgen.py:152*

---

### test_main_commit_msg_command

**型**: `method`

**シグネチャ**:
```
def test_main_commit_msg_command(self, mock_generator, temp_project, capsys):
```

**説明**:

commit-msgコマンドのテスト

*定義場所: tests/test_docgen.py:163*

---

### test_main_detect_only

**型**: `method`

**シグネチャ**:
```
def test_main_detect_only(self, temp_project, caplog):
```

**説明**:

detect-onlyオプションのテスト

*定義場所: tests/test_docgen.py:180*

---


## tests/test_document_generator.py

### TestDocumentGenerator

**型**: `class`

**シグネチャ**:
```
class TestDocumentGenerator:
```

**説明**:

DocumentGeneratorクラスのテスト

*定義場所: tests/test_document_generator.py:18*

---

### test_document_generator_initialization

**型**: `method`

**シグネチャ**:
```
def test_document_generator_initialization(self, temp_project):
```

**説明**:

DocumentGeneratorの初期化テスト

*定義場所: tests/test_document_generator.py:21*

---

### test_generate_documents_no_languages

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project, caplog):
```

**説明**:

言語がない場合のテスト

*定義場所: tests/test_document_generator.py:31*

---

### test_generate_documents_success

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_success(self, mock_factory, temp_project, caplog):
```

**説明**:

ドキュメント生成成功テスト

*定義場所: tests/test_document_generator.py:42*

---

### test_generate_documents_partial_failure

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_partial_failure(self, mock_factory, temp_project, caplog):
```

**説明**:

部分的な失敗テスト

*定義場所: tests/test_document_generator.py:67*

---

### test_generate_documents_exception

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_exception(self, mock_factory, temp_project, caplog):
```

**説明**:

例外処理テスト

*定義場所: tests/test_document_generator.py:90*

---

### test_generate_documents_disabled_generators

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_disabled_generators(self, mock_factory, temp_project):
```

**説明**:

ジェネレーターが無効な場合のテスト

*定義場所: tests/test_document_generator.py:104*

---

### test_generate_documents_only_api

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_only_api(self, mock_factory, temp_project, caplog):
```

**説明**:

APIドキュメントのみ生成テスト

*定義場所: tests/test_document_generator.py:121*

---


## tests/test_edge_cases.py

### TestEdgeCases

**型**: `class`

**シグネチャ**:
```
class TestEdgeCases:
```

**説明**:

エッジケースのテスト

*定義場所: tests/test_edge_cases.py:25*

---

### test_empty_project_root

**型**: `method`

**シグネチャ**:
```
def test_empty_project_root(self):
```

**説明**:

空のプロジェクトルートでのテスト

*定義場所: tests/test_edge_cases.py:28*

---

### test_nonexistent_project_root

**型**: `method`

**シグネチャ**:
```
def test_nonexistent_project_root(self):
```

**説明**:

存在しないプロジェクトルートでのテスト

*定義場所: tests/test_edge_cases.py:33*

---

### test_python_parser_with_malformed_ast

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_malformed_ast(self, temp_project):
```

**説明**:

不正なASTを持つPythonファイルの解析テスト

*定義場所: tests/test_edge_cases.py:40*

---

### test_python_parser_with_unicode_content

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_unicode_content(self, temp_project):
```

**説明**:

Unicode文字を含むPythonファイルの解析テスト

*定義場所: tests/test_edge_cases.py:55*

---

### test_python_parser_with_very_long_docstring

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_very_long_docstring(self, temp_project):
```

**説明**:

非常に長いdocstringの解析テスト

*定義場所: tests/test_edge_cases.py:75*

---

### test_agents_generator_with_invalid_config

**型**: `method`

**シグネチャ**:
```
def test_agents_generator_with_invalid_config(self, temp_project):
```

**説明**:

無効な設定でのAgentsGeneratorテスト

*定義場所: tests/test_edge_cases.py:93*

---

### test_api_generator_with_empty_languages

**型**: `method`

**シグネチャ**:
```
def test_api_generator_with_empty_languages(self, temp_project):
```

**説明**:

空の言語リストでのAPIGeneratorテスト

*定義場所: tests/test_edge_cases.py:107*

---

### test_readme_generator_with_readonly_filesystem

**型**: `method`

**シグネチャ**:
```
def test_readme_generator_with_readonly_filesystem(self, temp_project, monkeypatch):
```

**説明**:

読み取り専用ファイルシステムでのReadmeGeneratorテスト

*定義場所: tests/test_edge_cases.py:118*

---

### test_docgen_with_circular_imports

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_circular_imports(self, temp_project):
```

**説明**:

循環インポートのあるプロジェクトのテスト

*定義場所: tests/test_edge_cases.py:134*

---

### test_docgen_with_very_deep_directory_structure

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_very_deep_directory_structure(self, temp_project):
```

**説明**:

非常に深いディレクトリ構造のテスト

*定義場所: tests/test_edge_cases.py:157*

---

### test_docgen_with_special_characters_in_paths

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_special_characters_in_paths(self, temp_project):
```

**説明**:

パスに特殊文字を含む場合のテスト

*定義場所: tests/test_edge_cases.py:178*

---

### test_docgen_with_symlink_loops

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_symlink_loops(self, temp_project):
```

**説明**:

シンボリックリンクのループがある場合のテスト

*定義場所: tests/test_edge_cases.py:196*

---

### test_python_parser_with_binary_file_extension

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_binary_file_extension(self, temp_project):
```

**説明**:

.pycファイルなどのバイナリ拡張子のテスト

*定義場所: tests/test_edge_cases.py:218*

---

### test_agents_generator_with_very_long_custom_instructions

**型**: `method`

**シグネチャ**:
```
def test_agents_generator_with_very_long_custom_instructions(self, temp_project):
```

**説明**:

非常に長いカスタム指示のテスト

*定義場所: tests/test_edge_cases.py:230*

---

### test_api_generator_with_mixed_file_types

**型**: `method`

**シグネチャ**:
```
def test_api_generator_with_mixed_file_types(self, temp_project):
```

**説明**:

混在したファイルタイプのテスト

*定義場所: tests/test_edge_cases.py:245*

---

### test_llm_client_factory_with_invalid_config

**型**: `method`

**シグネチャ**:
```
def test_llm_client_factory_with_invalid_config(self):
```

**説明**:

無効なLLM設定でのテスト

*定義場所: tests/test_edge_cases.py:271*

---

### test_llm_client_factory_fallback

**型**: `method`

**シグネチャ**:
```
def test_llm_client_factory_fallback(self):
```

**説明**:

LLMクライアントのフォールバックテスト

*定義場所: tests/test_edge_cases.py:277*

---

### test_agents_generator_with_llm_failure

**型**: `method`

**シグネチャ**:
```
def test_agents_generator_with_llm_failure(self, temp_project):
```

**説明**:

LLM失敗時のAgentsGeneratorテスト

*定義場所: tests/test_edge_cases.py:285*

---

### test_readme_generator_with_llm_failure

**型**: `method`

**シグネチャ**:
```
def test_readme_generator_with_llm_failure(self, temp_project):
```

**説明**:

LLM失敗時のReadmeGeneratorテスト

*定義場所: tests/test_edge_cases.py:296*

---


## tests/test_edges/test_boundaries.py

### test_boundary_language_order_and_all_detected

**型**: `function`

**シグネチャ**:
```
def test_boundary_language_order_and_all_detected(temp_project):
```

*説明なし*

*定義場所: tests/test_edges/test_boundaries.py:15*

---

### test_boundary_with_third_language

**型**: `function`

**シグネチャ**:
```
def test_boundary_with_third_language(temp_project):
```

*説明なし*

*定義場所: tests/test_edges/test_boundaries.py:27*

---


## tests/test_edges/test_symlinks.py

### test_symlink_is_ignored_by_all_detectors

**型**: `function`

**シグネチャ**:
```
def test_symlink_is_ignored_by_all_detectors(temp_project):
```

*説明なし*

*定義場所: tests/test_edges/test_symlinks.py:8*

---


## tests/test_generator_factory.py

### TestGeneratorFactory

**型**: `class`

**シグネチャ**:
```
class TestGeneratorFactory:
```

**説明**:

GeneratorFactoryクラスのテスト

*定義場所: tests/test_generator_factory.py:20*

---

### test_create_generator_api

**型**: `method`

**シグネチャ**:
```
def test_create_generator_api(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generator_factory.py:23*

---

### test_create_generator_readme

**型**: `method`

**シグネチャ**:
```
def test_create_generator_readme(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generator_factory.py:35*

---

### test_create_generator_agents

**型**: `method`

**シグネチャ**:
```
def test_create_generator_agents(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generator_factory.py:49*

---

### test_create_generator_commit_message

**型**: `function`

**シグネチャ**:
```
def test_create_generator_commit_message(temp_project):
```

**説明**:

Unknown generator type for commit_message

*定義場所: tests/test_generator_factory.py:64*

---

### test_create_generator_unknown_type

**型**: `function`

**シグネチャ**:
```
def test_create_generator_unknown_type(temp_project):
```

**説明**:

Unknown generator type test

*定義場所: tests/test_generator_factory.py:72*

---


## tests/test_generators/test_agents_generator.py

### test_agents_generator_initialization

**型**: `function`

**シグネチャ**:
```
def test_agents_generator_initialization(temp_project):
```

**説明**:

AgentsGeneratorの初期化テスト

*定義場所: tests/test_generators/test_agents_generator.py:17*

---

### test_generate_agents_md

**型**: `function`

**シグネチャ**:
```
def test_generate_agents_md(temp_project):
```

**説明**:

AGENTS.md生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:25*

---

### test_llm_mode_api_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_api_only(temp_project):
```

**説明**:

llm_mode: 'api' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:54*

---

### test_llm_mode_local_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_local_only(temp_project):
```

**説明**:

llm_mode: 'local' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:70*

---

### test_custom_instructions

**型**: `function`

**シグネチャ**:
```
def test_custom_instructions(temp_project):
```

**説明**:

カスタム指示のテスト

*定義場所: tests/test_generators/test_agents_generator.py:86*

---

### test_agents_generator_with_empty_config

**型**: `function`

**シグネチャ**:
```
def test_agents_generator_with_empty_config(temp_project):
```

**説明**:

空の設定でのテスト

*定義場所: tests/test_generators/test_agents_generator.py:107*

---

### test_agents_generator_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_agents_generator_multiple_languages(temp_project):
```

**説明**:

複数言語のテスト

*定義場所: tests/test_generators/test_agents_generator.py:118*

---

### test_agents_generator_output_path

**型**: `function`

**シグネチャ**:
```
def test_agents_generator_output_path(temp_project):
```

**説明**:

出力パス指定のテスト

*定義場所: tests/test_generators/test_agents_generator.py:130*

---

### test_extract_manual_sections_with_existing_file

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections_with_existing_file(temp_project):
```

**説明**:

既存ファイルからの手動セクション抽出テスト

*定義場所: tests/test_generators/test_agents_generator.py:142*

---

### test_extract_manual_sections_no_file

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections_no_file(temp_project):
```

**説明**:

ファイルが存在しない場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:180*

---

### test_extract_manual_sections_malformed_content

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections_malformed_content(temp_project):
```

**説明**:

不正な形式のコンテンツ処理テスト

*定義場所: tests/test_generators/test_agents_generator.py:190*

---

### test_merge_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_merge_manual_sections(temp_project):
```

**説明**:

手動セクションのマージテスト

*定義場所: tests/test_generators/test_agents_generator.py:219*

---

### test_merge_manual_sections_empty_manual

**型**: `function`

**シグネチャ**:
```
def test_merge_manual_sections_empty_manual(temp_project):
```

**説明**:

手動セクションが空の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:249*

---

### test_generate_markdown_template_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_template_mode(temp_project):
```

**説明**:

テンプレートモードでのマークダウン生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:273*

---

### test_generate_markdown_llm_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_llm_mode(temp_project):
```

**説明**:

LLMモードでのマークダウン生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:293*

---

### test_generate_markdown_hybrid_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_hybrid_mode(temp_project):
```

**説明**:

ハイブリッドモードでのマークダウン生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:317*

---

### test_generate_error_handling

**型**: `function`

**シグネチャ**:
```
def test_generate_error_handling(temp_project):
```

**説明**:

生成時のエラーハンドリングテスト

*定義場所: tests/test_generators/test_agents_generator.py:341*

---


## tests/test_generators/test_api_generator.py

### TestAPIGenerator

**型**: `class`

**シグネチャ**:
```
class TestAPIGenerator:
```

**説明**:

APIGeneratorクラスのテスト

*定義場所: tests/test_generators/test_api_generator.py:17*

---

### test_api_generator_initialization

**型**: `method`

**シグネチャ**:
```
def test_api_generator_initialization(self, temp_project):
```

**説明**:

APIGeneratorの初期化テスト

*定義場所: tests/test_generators/test_api_generator.py:20*

---

### test_api_generator_initialization_cache_disabled

**型**: `method`

**シグネチャ**:
```
def test_api_generator_initialization_cache_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時の初期化テスト

*定義場所: tests/test_generators/test_api_generator.py:30*

---

### test_generate_api_doc_python

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_python(self, temp_project):
```

**説明**:

PythonファイルのAPIドキュメント生成テスト

*定義場所: tests/test_generators/test_api_generator.py:37*

---

### test_generate_api_doc_javascript

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_javascript(self, temp_project):
```

**説明**:

JavaScriptファイルのAPIドキュメント生成テスト

*定義場所: tests/test_generators/test_api_generator.py:84*

---

### test_generate_api_doc_multiple_languages

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_multiple_languages(self, temp_project):
```

**説明**:

複数言語のAPIドキュメント生成テスト

*定義場所: tests/test_generators/test_api_generator.py:127*

---

### test_generate_api_doc_empty_project

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_empty_project(self, temp_project):
```

**説明**:

空のプロジェクトでのAPIドキュメント生成テスト

*定義場所: tests/test_generators/test_api_generator.py:159*

---

### test_generate_api_doc_output_directory_creation

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_output_directory_creation(self, temp_project):
```

**説明**:

出力ディレクトリが存在しない場合のテスト

*定義場所: tests/test_generators/test_api_generator.py:174*

---

### test_generate_api_doc_with_cache

**型**: `method`

**シグネチャ**:
```
def test_generate_api_doc_with_cache(self, temp_project):
```

**説明**:

キャッシュ有効時のテスト

*定義場所: tests/test_generators/test_api_generator.py:184*

---


## tests/test_generators/test_commit_message_generator.py

### TestCommitMessageGenerator

**型**: `class`

**シグネチャ**:
```
class TestCommitMessageGenerator:
```

**説明**:

CommitMessageGeneratorクラスのテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:18*

---

### test_commit_message_generator_initialization

**型**: `method`

**シグネチャ**:
```
def test_commit_message_generator_initialization(self, temp_project):
```

**説明**:

CommitMessageGeneratorの初期化テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:21*

---

### test_generate_no_staged_changes

**型**: `method`

**シグネチャ**:
```
def test_generate_no_staged_changes(self, temp_project):
```

**説明**:

ステージングされた変更がない場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:31*

---

### test_generate_with_llm

**型**: `method`

**シグネチャ**:
```
def test_generate_with_llm(self, mock_llm_factory, temp_project):
```

**説明**:

LLMを使用したコミットメッセージ生成テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:43*

---

### test_generate_llm_client_creation_failure

**型**: `method`

**シグネチャ**:
```
def test_generate_llm_client_creation_failure(self, mock_llm_factory, temp_project):
```

**説明**:

LLMクライアント作成失敗時のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:74*

---

### test_generate_llm_returns_empty

**型**: `method`

**シグネチャ**:
```
def test_generate_llm_returns_empty(self, mock_llm_factory, temp_project):
```

**説明**:

LLMが空文字列を返す場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:87*

---

### test_generate_llm_returns_multiline

**型**: `method`

**シグネチャ**:
```
def test_generate_llm_returns_multiline(self, mock_llm_factory, temp_project):
```

**説明**:

LLMが複数行を返す場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:103*

---

### test_get_staged_changes_success

**型**: `method`

**シグネチャ**:
```
def test_get_staged_changes_success(self, temp_project):
```

**説明**:

ステージングされた変更の取得成功テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:120*

---

### test_get_staged_changes_stat_failure

**型**: `method`

**シグネチャ**:
```
def test_get_staged_changes_stat_failure(self, temp_project):
```

**説明**:

git diff --cached --statが失敗した場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:140*

---

### test_get_staged_changes_no_git_repo

**型**: `method`

**シグネチャ**:
```
def test_get_staged_changes_no_git_repo(self, temp_project):
```

**説明**:

Gitリポジトリがない場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:153*

---

### test_get_staged_changes_diff_failure

**型**: `method`

**シグネチャ**:
```
def test_get_staged_changes_diff_failure(self, temp_project):
```

**説明**:

詳細diff取得失敗時のテスト（statのみ返す）

*定義場所: tests/test_generators/test_commit_message_generator.py:162*

---

### test_get_staged_changes_long_diff_truncated

**型**: `method`

**シグネチャ**:
```
def test_get_staged_changes_long_diff_truncated(self, temp_project):
```

**説明**:

長いdiffが切り詰められるテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:178*

---

### test_create_prompt

**型**: `method`

**シグネチャ**:
```
def test_create_prompt(self, temp_project):
```

**説明**:

プロンプト作成テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:199*

---

### test_create_prompt_with_custom_changes

**型**: `method`

**シグネチャ**:
```
def test_create_prompt_with_custom_changes(self, temp_project):
```

**説明**:

カスタム変更内容でのプロンプト作成テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:211*

---

### test_generate_exception_handling

**型**: `method`

**シグネチャ**:
```
def test_generate_exception_handling(self, temp_project):
```

**説明**:

例外処理のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:231*

---


## tests/test_generators/test_readme_generator.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root, relative_path, content):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:16*

---

### TestReadmeGenerator

**型**: `class`

**シグネチャ**:
```
class TestReadmeGenerator:
```

**説明**:

ReadmeGeneratorクラスのテスト

*定義場所: tests/test_generators/test_readme_generator.py:26*

---

### test_readme_generator_initialization

**型**: `method`

**シグネチャ**:
```
def test_readme_generator_initialization(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:29*

---

### test_generate_readme_without_llm

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_without_llm(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:37*

---

### test_generate_readme_empty_project

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_empty_project(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:66*

---

### test_generate_readme_multiple_languages

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_multiple_languages(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:81*

---

### test_generate_readme_with_project_info_error

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_with_project_info_error(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:99*

---

### test_extract_manual_sections

**型**: `method`

**シグネチャ**:
```
def test_extract_manual_sections(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:112*

---

### test_extract_manual_sections_empty

**型**: `method`

**シグネチャ**:
```
def test_extract_manual_sections_empty(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:134*

---

### test_generate_readme_custom_output_path

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_custom_output_path(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:148*

---

### test_generate_readme_preserve_manual_sections

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_preserve_manual_sections(self, temp_project):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:160*

---

### test_generate_readme_with_llm

**型**: `method`

**シグネチャ**:
```
def test_generate_readme_with_llm(self, temp_project, monkeypatch):
```

*説明なし*

*定義場所: tests/test_generators/test_readme_generator.py:187*

---


## tests/test_integration.py

### TestIntegration

**型**: `class`

**シグネチャ**:
```
class TestIntegration:
```

**説明**:

統合テストクラス

*定義場所: tests/test_integration.py:18*

---

### test_full_pipeline_python_project

**型**: `method`

**シグネチャ**:
```
def test_full_pipeline_python_project(self, temp_project, caplog):
```

**説明**:

Pythonプロジェクトの完全なパイプラインテスト

*定義場所: tests/test_integration.py:21*

---

### test_full_pipeline_javascript_project

**型**: `method`

**シグネチャ**:
```
def test_full_pipeline_javascript_project(self, temp_project):
```

**説明**:

JavaScriptプロジェクトの完全なパイプラインテスト

*定義場所: tests/test_integration.py:98*

---

### test_detect_only_mode

**型**: `method`

**シグネチャ**:
```
def test_detect_only_mode(self, temp_project, caplog):
```

**説明**:

言語検出のみモードのテスト

*定義場所: tests/test_integration.py:157*

---

### test_config_file_handling

**型**: `method`

**シグネチャ**:
```
def test_config_file_handling(self, temp_project):
```

**説明**:

設定ファイルハンドリングのテスト

*定義場所: tests/test_integration.py:181*

---

### test_error_handling

**型**: `method`

**シグネチャ**:
```
def test_error_handling(self, temp_project):
```

**説明**:

エラーハンドリングのテスト

*定義場所: tests/test_integration.py:206*

---


## tests/test_language_detector.py

### TestLanguageDetector

**型**: `class`

**シグネチャ**:
```
class TestLanguageDetector:
```

**説明**:

LanguageDetectorクラスのテスト

*定義場所: tests/test_language_detector.py:8*

---

### test_init

**型**: `method`

**シグネチャ**:
```
def test_init(self, tmp_path):
```

**説明**:

初期化テスト

*定義場所: tests/test_language_detector.py:11*

---

### test_detect_languages_python

**型**: `method`

**シグネチャ**:
```
def test_detect_languages_python(self, tmp_path):
```

**説明**:

Python言語検出テスト

*定義場所: tests/test_language_detector.py:18*

---

### test_get_detected_package_managers

**型**: `method`

**シグネチャ**:
```
def test_get_detected_package_managers(self, tmp_path):
```

**説明**:

パッケージマネージャ取得テスト

*定義場所: tests/test_language_detector.py:29*

---


## tests/test_parsers/test_generic_parser.py

### TestGenericParser

**型**: `class`

**シグネチャ**:
```
class TestGenericParser:
```

**説明**:

GenericParserクラスのテスト

*定義場所: tests/test_parsers/test_generic_parser.py:17*

---

### test_parse_file_rust

**型**: `method`

**シグネチャ**:
```
def test_parse_file_rust(self, temp_project):
```

**説明**:

Rustファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:20*

---

### test_parse_file_java

**型**: `method`

**シグネチャ**:
```
def test_parse_file_java(self, temp_project):
```

**説明**:

Javaファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:52*

---

### test_parse_file_go

**型**: `method`

**シグネチャ**:
```
def test_parse_file_go(self, temp_project):
```

**説明**:

Goファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:90*

---

### test_parse_file_ruby

**型**: `method`

**シグネチャ**:
```
def test_parse_file_ruby(self, temp_project):
```

**説明**:

Rubyファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:121*

---

### test_parse_file_php

**型**: `method`

**シグネチャ**:
```
def test_parse_file_php(self, temp_project):
```

**説明**:

PHPファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:150*

---

### test_parse_file_c

**型**: `method`

**シグネチャ**:
```
def test_parse_file_c(self, temp_project):
```

**説明**:

Cファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:188*

---

### test_parse_file_cpp

**型**: `method`

**シグネチャ**:
```
def test_parse_file_cpp(self, temp_project):
```

**説明**:

C++ファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:221*

---

### test_parse_file_unsupported_language

**型**: `method`

**シグネチャ**:
```
def test_parse_file_unsupported_language(self, temp_project):
```

**説明**:

サポートされていない言語のテスト

*定義場所: tests/test_parsers/test_generic_parser.py:252*

---

### test_parse_file_empty

**型**: `method`

**シグネチャ**:
```
def test_parse_file_empty(self, temp_project):
```

**説明**:

空のファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:267*

---

### test_parse_file_no_comments

**型**: `method`

**シグネチャ**:
```
def test_parse_file_no_comments(self, temp_project):
```

**説明**:

コメントなしのファイルの解析テスト

*定義場所: tests/test_parsers/test_generic_parser.py:277*

---

### test_parser_initialization

**型**: `method`

**シグネチャ**:
```
def test_parser_initialization(self, temp_project):
```

**説明**:

パーサーの初期化テスト

*定義場所: tests/test_parsers/test_generic_parser.py:294*

---


## tests/test_parsers/test_js_parser.py

### TestJSParser

**型**: `class`

**シグネチャ**:
```
class TestJSParser:
```

**説明**:

JSParserクラスのテスト

*定義場所: tests/test_parsers/test_js_parser.py:17*

---

### test_parse_file_with_jsdoc_function

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_jsdoc_function(self, temp_project):
```

**説明**:

JSDoc付き関数の解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:20*

---

### test_parse_file_with_class

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_class(self, temp_project):
```

**説明**:

クラスの解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:61*

---

### test_parse_file_with_arrow_function

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_arrow_function(self, temp_project):
```

**説明**:

アロー関数の解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:93*

---

### test_parse_file_with_export

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_export(self, temp_project):
```

**説明**:

export付き関数の解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:130*

---

### test_parse_file_no_jsdoc

**型**: `method`

**シグネチャ**:
```
def test_parse_file_no_jsdoc(self, temp_project):
```

**説明**:

JSDocなしの関数の解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:169*

---

### test_parse_file_typescript

**型**: `method`

**シグネチャ**:
```
def test_parse_file_typescript(self, temp_project):
```

**説明**:

TypeScriptファイルの解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:196*

---

### test_parse_file_empty

**型**: `method`

**シグネチャ**:
```
def test_parse_file_empty(self, temp_project):
```

**説明**:

空のファイルの解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:225*

---

### test_parse_file_complex_jsdoc

**型**: `method`

**シグネチャ**:
```
def test_parse_file_complex_jsdoc(self, temp_project):
```

**説明**:

複雑なJSDocの解析テスト

*定義場所: tests/test_parsers/test_js_parser.py:235*

---

### test_parse_file_mixed_content

**型**: `method`

**シグネチャ**:
```
def test_parse_file_mixed_content(self, temp_project):
```

**説明**:

JSDoc付きとJSDocなしが混在するファイルのテスト

*定義場所: tests/test_parsers/test_js_parser.py:268*

---


## tests/test_parsers/test_python_parser.py

### TestPythonParser

**型**: `class`

**シグネチャ**:
```
class TestPythonParser:
```

**説明**:

PythonParserクラスのテスト

*定義場所: tests/test_parsers/test_python_parser.py:17*

---

### test_parse_file_with_function

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_function(self, temp_project):
```

**説明**:

関数定義を含むPythonファイルの解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:20*

---

### test_parse_file_with_class

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_class(self, temp_project):
```

**説明**:

クラス定義を含むPythonファイルの解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:69*

---

### test_parse_file_no_docstring

**型**: `method`

**シグネチャ**:
```
def test_parse_file_no_docstring(self, temp_project):
```

**説明**:

docstringのない関数の解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:115*

---

### test_parse_file_syntax_error

**型**: `method`

**シグネチャ**:
```
def test_parse_file_syntax_error(self, temp_project):
```

**説明**:

構文エラーのあるファイルの解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:138*

---

### test_parse_file_empty

**型**: `method`

**シグネチャ**:
```
def test_parse_file_empty(self, temp_project):
```

**説明**:

空のファイルの解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:152*

---

### test_parse_file_with_async_function

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_async_function(self, temp_project):
```

**説明**:

async関数の解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:162*

---

### test_parse_file_with_complex_types

**型**: `method`

**シグネチャ**:
```
def test_parse_file_with_complex_types(self, temp_project):
```

**説明**:

複雑な型ヒントを含む関数の解析テスト

*定義場所: tests/test_parsers/test_python_parser.py:184*

---


## tests/test_project_info_collector.py

### TestProjectInfoCollector

**型**: `class`

**シグネチャ**:
```
class TestProjectInfoCollector:
```

**説明**:

ProjectInfoCollectorクラスのテスト

*定義場所: tests/test_project_info_collector.py:18*

---

### test_project_info_collector_initialization

**型**: `method`

**シグネチャ**:
```
def test_project_info_collector_initialization(self, temp_project):
```

**説明**:

ProjectInfoCollectorの初期化テスト

*定義場所: tests/test_project_info_collector.py:21*

---

### test_project_info_collector_initialization_with_package_managers

**型**: `method`

**シグネチャ**:
```
def test_project_info_collector_initialization_with_package_managers(self, temp_project):
```

**説明**:

パッケージマネージャ付き初期化テスト

*定義場所: tests/test_project_info_collector.py:27*

---

### test_collect_all

**型**: `method`

**シグネチャ**:
```
def test_collect_all(self, temp_project):
```

**説明**:

全情報収集テスト

*定義場所: tests/test_project_info_collector.py:35*

---

### test_collect_build_commands_from_pipeline_script

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_from_pipeline_script(self, temp_project):
```

**説明**:

パイプラインスクリプトからのビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:79*

---

### test_collect_build_commands_with_package_managers

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_with_package_managers(self, temp_project):
```

**説明**:

パッケージマネージャ考慮のビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:99*

---

### test_collect_build_commands_from_makefile

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_from_makefile(self, temp_project):
```

**説明**:

Makefileからのビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:118*

---

### test_collect_build_commands_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:144*

---

### test_collect_test_commands_from_makefile

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_from_makefile(self, temp_project):
```

**説明**:

Makefileからのテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:164*

---

### test_collect_test_commands_with_package_managers

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_with_package_managers(self, temp_project):
```

**説明**:

パッケージマネージャ考慮のテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:185*

---

### test_collect_build_commands_with_uv_run

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_with_uv_run(self, temp_project):
```

**説明**:

uvプロジェクトでのpythonコマンドにuv runがつくテスト

*定義場所: tests/test_project_info_collector.py:209*

---

### test_collect_test_commands_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:227*

---

### test_collect_dependencies_from_requirements_txt

**型**: `method`

**シグネチャ**:
```
def test_collect_dependencies_from_requirements_txt(self, temp_project):
```

**説明**:

requirements.txtからの依存関係収集テスト

*定義場所: tests/test_project_info_collector.py:245*

---

### test_collect_dependencies_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_dependencies_from_package_json(self, temp_project):
```

**説明**:

package.jsonからの依存関係収集テスト

*定義場所: tests/test_project_info_collector.py:265*

---

### test_collect_coding_standards_from_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def test_collect_coding_standards_from_pyproject_toml(self, temp_project):
```

**説明**:

pyproject.tomlからのコーディング規約収集テスト

*定義場所: tests/test_project_info_collector.py:289*

---

### test_collect_ci_cd_info_github_actions

**型**: `method`

**シグネチャ**:
```
def test_collect_ci_cd_info_github_actions(self, temp_project):
```

**説明**:

GitHub Actions CI/CD情報収集テスト

*定義場所: tests/test_project_info_collector.py:316*

---

### test_collect_project_structure

**型**: `method`

**シグネチャ**:
```
def test_collect_project_structure(self, temp_project):
```

**説明**:

プロジェクト構造収集テスト

*定義場所: tests/test_project_info_collector.py:339*

---

### test_collect_project_description_from_readme

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_readme(self, temp_project):
```

**説明**:

READMEからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:358*

---

### test_collect_project_description_from_setup_py

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_setup_py(self, temp_project):
```

**説明**:

setup.pyからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:377*

---

### test_collect_project_description_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:397*

---


## tests/test_utils/common.py

### write_file

**型**: `function`

**シグネチャ**:
```
def write_file(root: Path, relative_path: str, content: str) -> Path:
```

*説明なし*

*定義場所: tests/test_utils/common.py:4*

---


## tests/test_utils/test_cache.py

### TestCacheManager

**型**: `class`

**シグネチャ**:
```
class TestCacheManager:
```

**説明**:

CacheManagerクラスのテスト

*定義場所: tests/test_utils/test_cache.py:18*

---

### test_cache_manager_initialization_enabled

**型**: `method`

**シグネチャ**:
```
def test_cache_manager_initialization_enabled(self, temp_project):
```

**説明**:

キャッシュ有効時の初期化テスト

*定義場所: tests/test_utils/test_cache.py:21*

---

### test_cache_manager_initialization_disabled

**型**: `method`

**シグネチャ**:
```
def test_cache_manager_initialization_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時の初期化テスト

*定義場所: tests/test_utils/test_cache.py:34*

---

### test_cache_manager_custom_cache_dir

**型**: `method`

**シグネチャ**:
```
def test_cache_manager_custom_cache_dir(self, temp_project):
```

**説明**:

カスタムキャッシュディレクトリのテスト

*定義場所: tests/test_utils/test_cache.py:41*

---

### test_load_cache_existing_file

**型**: `method`

**シグネチャ**:
```
def test_load_cache_existing_file(self, temp_project):
```

**説明**:

既存のキャッシュファイル読み込みテスト

*定義場所: tests/test_utils/test_cache.py:50*

---

### test_load_cache_invalid_json

**型**: `method`

**シグネチャ**:
```
def test_load_cache_invalid_json(self, temp_project):
```

**説明**:

無効なJSONのキャッシュファイル読み込みテスト

*定義場所: tests/test_utils/test_cache.py:67*

---

### test_load_cache_nonexistent_file

**型**: `method`

**シグネチャ**:
```
def test_load_cache_nonexistent_file(self, temp_project):
```

**説明**:

存在しないキャッシュファイルのテスト

*定義場所: tests/test_utils/test_cache.py:81*

---

### test_save_cache

**型**: `method`

**シグネチャ**:
```
def test_save_cache(self, temp_project):
```

**説明**:

キャッシュ保存テスト

*定義場所: tests/test_utils/test_cache.py:88*

---

### test_save_cache_disabled

**型**: `method`

**シグネチャ**:
```
def test_save_cache_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時の保存テスト

*定義場所: tests/test_utils/test_cache.py:106*

---

### test_get_file_hash

**型**: `method`

**シグネチャ**:
```
def test_get_file_hash(self, temp_project):
```

**説明**:

ファイルハッシュの生成テスト

*定義場所: tests/test_utils/test_cache.py:116*

---

### test_get_file_hash_nonexistent_file

**型**: `method`

**シグネチャ**:
```
def test_get_file_hash_nonexistent_file(self, temp_project):
```

**説明**:

存在しないファイルのハッシュ生成テスト

*定義場所: tests/test_utils/test_cache.py:134*

---

### test_get_cached_result

**型**: `method`

**シグネチャ**:
```
def test_get_cached_result(self, temp_project):
```

**説明**:

キャッシュ結果取得テスト

*定義場所: tests/test_utils/test_cache.py:143*

---

### test_get_cached_result_disabled

**型**: `method`

**シグネチャ**:
```
def test_get_cached_result_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時の結果取得テスト

*定義場所: tests/test_utils/test_cache.py:155*

---

### test_set_cached_result

**型**: `method`

**シグネチャ**:
```
def test_set_cached_result(self, temp_project):
```

**説明**:

キャッシュ結果設定テスト

*定義場所: tests/test_utils/test_cache.py:167*

---

### test_set_cached_result_disabled

**型**: `method`

**シグネチャ**:
```
def test_set_cached_result_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時の結果設定テスト

*定義場所: tests/test_utils/test_cache.py:185*

---

### test_clear_cache

**型**: `method`

**シグネチャ**:
```
def test_clear_cache(self, temp_project):
```

**説明**:

キャッシュクリアテスト

*定義場所: tests/test_utils/test_cache.py:201*

---

### test_clear_cache_disabled

**型**: `method`

**シグネチャ**:
```
def test_clear_cache_disabled(self, temp_project):
```

**説明**:

キャッシュ無効時のクリアテスト

*定義場所: tests/test_utils/test_cache.py:216*

---


## tests/test_utils/test_config_utils.py

### TestConfigUtils

**型**: `class`

**シグネチャ**:
```
class TestConfigUtils:
```

**説明**:

ConfigUtils関数のテスト

*定義場所: tests/test_utils/test_config_utils.py:22*

---

### test_get_nested_config_simple

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_simple(self):
```

**説明**:

単純なネストされた設定取得テスト

*定義場所: tests/test_utils/test_config_utils.py:25*

---

### test_get_nested_config_deep

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_deep(self):
```

**説明**:

深いネストされた設定取得テスト

*定義場所: tests/test_utils/test_config_utils.py:32*

---

### test_get_nested_config_default

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_default(self):
```

**説明**:

存在しないキーのデフォルト値テスト

*定義場所: tests/test_utils/test_config_utils.py:39*

---

### test_get_nested_config_none_default

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_none_default(self):
```

**説明**:

デフォルト値なしの存在しないキーテスト

*定義場所: tests/test_utils/test_config_utils.py:46*

---

### test_get_nested_config_non_dict

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_non_dict(self):
```

**説明**:

非辞書値の中間でのテスト

*定義場所: tests/test_utils/test_config_utils.py:53*

---

### test_get_nested_config_empty_keys

**型**: `method`

**シグネチャ**:
```
def test_get_nested_config_empty_keys(self):
```

**説明**:

空のキーシーケンステスト

*定義場所: tests/test_utils/test_config_utils.py:60*

---

### test_get_config_bool_true

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_true(self):
```

**説明**:

ブール値Trueの取得テスト

*定義場所: tests/test_utils/test_config_utils.py:67*

---

### test_get_config_bool_false

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_false(self):
```

**説明**:

ブール値Falseの取得テスト

*定義場所: tests/test_utils/test_config_utils.py:74*

---

### test_get_config_bool_string_true

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_true(self):
```

**説明**:

文字列"true"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:81*

---

### test_get_config_bool_string_false

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_false(self):
```

**説明**:

文字列"false"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:88*

---

### test_get_config_bool_string_yes

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_yes(self):
```

**説明**:

文字列"yes"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:95*

---

### test_get_config_bool_string_no

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_no(self):
```

**説明**:

文字列"no"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:102*

---

### test_get_config_bool_string_one

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_one(self):
```

**説明**:

文字列"1"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:109*

---

### test_get_config_bool_string_zero

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_string_zero(self):
```

**説明**:

文字列"0"のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:116*

---

### test_get_config_bool_invalid_string

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_invalid_string(self):
```

**説明**:

無効な文字列のブール変換テスト

*定義場所: tests/test_utils/test_config_utils.py:123*

---

### test_get_config_bool_default

**型**: `method`

**シグネチャ**:
```
def test_get_config_bool_default(self):
```

**説明**:

デフォルト値付きブール取得テスト

*定義場所: tests/test_utils/test_config_utils.py:130*

---

### test_get_config_list_valid

**型**: `method`

**シグネチャ**:
```
def test_get_config_list_valid(self):
```

**説明**:

有効なリストの取得テスト

*定義場所: tests/test_utils/test_config_utils.py:137*

---

### test_get_config_list_string

**型**: `method`

**シグネチャ**:
```
def test_get_config_list_string(self):
```

**説明**:

文字列からのリスト変換テスト（カンマ区切り）

*定義場所: tests/test_utils/test_config_utils.py:144*

---

### test_get_config_list_invalid

**型**: `method`

**シグネチャ**:
```
def test_get_config_list_invalid(self):
```

**説明**:

無効な値のリスト変換テスト

*定義場所: tests/test_utils/test_config_utils.py:151*

---

### test_get_config_str_valid

**型**: `method`

**シグネチャ**:
```
def test_get_config_str_valid(self):
```

**説明**:

有効な文字列の取得テスト

*定義場所: tests/test_utils/test_config_utils.py:158*

---

### test_get_config_str_non_string

**型**: `method`

**シグネチャ**:
```
def test_get_config_str_non_string(self):
```

**説明**:

非文字列の文字列変換テスト

*定義場所: tests/test_utils/test_config_utils.py:165*

---

### test_get_config_str_none

**型**: `method`

**シグネチャ**:
```
def test_get_config_str_none(self):
```

**説明**:

None値の文字列変換テスト

*定義場所: tests/test_utils/test_config_utils.py:172*

---


## tests/test_utils/test_exceptions.py

### TestExceptions

**型**: `class`

**シグネチャ**:
```
class TestExceptions:
```

**説明**:

例外クラスのテスト

*定義場所: tests/test_utils/test_exceptions.py:24*

---

### test_docgen_error_basic

**型**: `method`

**シグネチャ**:
```
def test_docgen_error_basic(self):
```

**説明**:

DocGenErrorの基本テスト

*定義場所: tests/test_utils/test_exceptions.py:27*

---

### test_docgen_error_with_details

**型**: `method`

**シグネチャ**:
```
def test_docgen_error_with_details(self):
```

**説明**:

詳細付きDocGenErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:35*

---

### test_config_error

**型**: `method`

**シグネチャ**:
```
def test_config_error(self):
```

**説明**:

ConfigErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:43*

---

### test_llm_error

**型**: `method`

**シグネチャ**:
```
def test_llm_error(self):
```

**説明**:

LLMErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:51*

---

### test_parse_error

**型**: `method`

**シグネチャ**:
```
def test_parse_error(self):
```

**説明**:

ParseErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:59*

---

### test_cache_error

**型**: `method`

**シグネチャ**:
```
def test_cache_error(self):
```

**説明**:

CacheErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:67*

---

### test_file_operation_error

**型**: `method`

**シグネチャ**:
```
def test_file_operation_error(self):
```

**説明**:

FileOperationErrorのテスト

*定義場所: tests/test_utils/test_exceptions.py:75*

---

### test_exception_inheritance

**型**: `method`

**シグネチャ**:
```
def test_exception_inheritance(self):
```

**説明**:

例外クラスの継承関係テスト

*定義場所: tests/test_utils/test_exceptions.py:83*

---

### test_exception_without_details

**型**: `method`

**シグネチャ**:
```
def test_exception_without_details(self):
```

**説明**:

詳細なしの例外テスト

*定義場所: tests/test_utils/test_exceptions.py:98*

---

### test_exception_with_empty_details

**型**: `method`

**シグネチャ**:
```
def test_exception_with_empty_details(self):
```

**説明**:

空の詳細付き例外テスト

*定義場所: tests/test_utils/test_exceptions.py:105*

---

### test_exception_chaining

**型**: `method`

**シグネチャ**:
```
def test_exception_chaining(self):
```

**説明**:

例外チェーン機能のテスト

*定義場所: tests/test_utils/test_exceptions.py:112*

---

### test_exception_attributes

**型**: `method`

**シグネチャ**:
```
def test_exception_attributes(self):
```

**説明**:

例外の属性アクセステスト

*定義場所: tests/test_utils/test_exceptions.py:124*

---

### test_exception_repr

**型**: `method`

**シグネチャ**:
```
def test_exception_repr(self):
```

**説明**:

例外のreprテスト

*定義場所: tests/test_utils/test_exceptions.py:134*

---


## tests/test_utils/test_file_utils.py

### TestFileUtils

**型**: `class`

**シグネチャ**:
```
class TestFileUtils:
```

**説明**:

FileUtils関数のテスト

*定義場所: tests/test_utils/test_file_utils.py:28*

---

### test_safe_read_file_existing

**型**: `method`

**シグネチャ**:
```
def test_safe_read_file_existing(self, temp_project):
```

**説明**:

存在するファイルの安全読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:31*

---

### test_safe_read_file_nonexistent

**型**: `method`

**シグネチャ**:
```
def test_safe_read_file_nonexistent(self, temp_project):
```

**説明**:

存在しないファイルの安全読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:40*

---

### test_safe_read_file_encoding_error

**型**: `method`

**シグネチャ**:
```
def test_safe_read_file_encoding_error(self, temp_project):
```

**説明**:

エンコーディングエラーのファイル読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:47*

---

### test_safe_read_file_permission_error

**型**: `method`

**シグネチャ**:
```
def test_safe_read_file_permission_error(self, temp_project):
```

**説明**:

権限エラーのファイル読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:56*

---

### test_safe_write_file_success

**型**: `method`

**シグネチャ**:
```
def test_safe_write_file_success(self, temp_project):
```

**説明**:

ファイルの安全書き込み成功テスト

*定義場所: tests/test_utils/test_file_utils.py:65*

---

### test_safe_write_file_permission_error

**型**: `method`

**シグネチャ**:
```
def test_safe_write_file_permission_error(self, temp_project):
```

**説明**:

権限エラーのファイル書き込みテスト

*定義場所: tests/test_utils/test_file_utils.py:75*

---

### test_safe_read_json_valid

**型**: `method`

**シグネチャ**:
```
def test_safe_read_json_valid(self, temp_project):
```

**説明**:

有効なJSONファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:84*

---

### test_safe_read_json_invalid

**型**: `method`

**シグネチャ**:
```
def test_safe_read_json_invalid(self, temp_project):
```

**説明**:

無効なJSONファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:93*

---

### test_safe_read_json_nonexistent

**型**: `method`

**シグネチャ**:
```
def test_safe_read_json_nonexistent(self, temp_project):
```

**説明**:

存在しないJSONファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:101*

---

### test_safe_read_yaml_valid

**型**: `method`

**シグネチャ**:
```
def test_safe_read_yaml_valid(self, temp_project):
```

**説明**:

有効なYAMLファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:108*

---

### test_safe_read_yaml_no_yaml

**型**: `method`

**シグネチャ**:
```
def test_safe_read_yaml_no_yaml(self):
```

**説明**:

YAMLライブラリなしの場合のテスト

*定義場所: tests/test_utils/test_file_utils.py:124*

---

### test_safe_read_toml_valid

**型**: `method`

**シグネチャ**:
```
def test_safe_read_toml_valid(self, temp_project):
```

**説明**:

有効なTOMLファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:131*

---

### test_safe_read_toml_no_tomllib

**型**: `method`

**シグネチャ**:
```
def test_safe_read_toml_no_tomllib(self):
```

**説明**:

TOMLライブラリなしの場合のテスト

*定義場所: tests/test_utils/test_file_utils.py:144*

---

### test_save_yaml_file_success

**型**: `method`

**シグネチャ**:
```
def test_save_yaml_file_success(self, temp_project):
```

**説明**:

YAMLファイルの保存成功テスト

*定義場所: tests/test_utils/test_file_utils.py:150*

---

### test_save_yaml_file_no_yaml

**型**: `method`

**シグネチャ**:
```
def test_save_yaml_file_no_yaml(self):
```

**説明**:

YAMLライブラリなしの場合の保存テスト

*定義場所: tests/test_utils/test_file_utils.py:159*

---

### test_load_toml_file_valid

**型**: `method`

**シグネチャ**:
```
def test_load_toml_file_valid(self, temp_project):
```

**説明**:

有効なTOMLファイルの読み込みテスト

*定義場所: tests/test_utils/test_file_utils.py:165*

---

### test_load_toml_file_no_tomllib

**型**: `method`

**シグネチャ**:
```
def test_load_toml_file_no_tomllib(self):
```

**説明**:

TOMLライブラリなしの場合のテスト

*定義場所: tests/test_utils/test_file_utils.py:178*

---

### test_find_files_with_extensions

**型**: `method`

**シグネチャ**:
```
def test_find_files_with_extensions(self, temp_project):
```

**説明**:

拡張子によるファイル検索テスト

*定義場所: tests/test_utils/test_file_utils.py:184*

---

### test_find_files_with_extensions_recursive

**型**: `method`

**シグネチャ**:
```
def test_find_files_with_extensions_recursive(self, temp_project):
```

**説明**:

再帰的なファイル検索テスト

*定義場所: tests/test_utils/test_file_utils.py:205*

---


## tests/test_utils/test_llm_client.py

### TestBaseLLMClient

**型**: `class`

**シグネチャ**:
```
class TestBaseLLMClient:
```

**説明**:

BaseLLMClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:27*

---

### test_base_llm_client_initialization

**型**: `method`

**シグネチャ**:
```
def test_base_llm_client_initialization(self):
```

**説明**:

BaseLLMClientの初期化テスト

*定義場所: tests/test_utils/test_llm_client.py:30*

---

### TestOpenAIClient

**型**: `class`

**シグネチャ**:
```
class TestOpenAIClient:
```

**説明**:

OpenAIClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:49*

---

### test_openai_client_initialization_success

**型**: `method`

**シグネチャ**:
```
def test_openai_client_initialization_success(self):
```

**説明**:

OpenAIClientの正常初期化テスト

*定義場所: tests/test_utils/test_llm_client.py:52*

---

### test_openai_client_initialization_config_error

**型**: `method`

**シグネチャ**:
```
def test_openai_client_initialization_config_error(self, mock_openai):
```

**説明**:

OpenAIClientの設定エラーテスト

*定義場所: tests/test_utils/test_llm_client.py:59*

---

### test_openai_client_generate_success

**型**: `method`

**シグネチャ**:
```
def test_openai_client_generate_success(self, mock_openai):
```

**説明**:

OpenAIClientのgenerate成功テスト

*定義場所: tests/test_utils/test_llm_client.py:67*

---

### test_openai_client_generate_error

**型**: `method`

**シグネチャ**:
```
def test_openai_client_generate_error(self, mock_openai):
```

**説明**:

OpenAIClientのgenerateエラーテスト

*定義場所: tests/test_utils/test_llm_client.py:82*

---

### test_ollama_client_error_handling

**型**: `method`

**シグネチャ**:
```
def test_ollama_client_error_handling(self, mock_client_class):
```

**説明**:

Ollamaクライアントのエラーハンドリングテスト

*定義場所: tests/test_utils/test_llm_client.py:94*

---

### TestLocalLLMClient

**型**: `class`

**シグネチャ**:
```
class TestLocalLLMClient:
```

**説明**:

LocalLLMClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:108*

---

### test_local_client_initialization_success

**型**: `method`

**シグネチャ**:
```
def test_local_client_initialization_success(self):
```

**説明**:

LocalLLMClientの正常初期化テスト

*定義場所: tests/test_utils/test_llm_client.py:111*

---

### test_local_client_generate_ollama_success

**型**: `method`

**シグネチャ**:
```
def test_local_client_generate_ollama_success(self, mock_post):
```

**説明**:

LocalLLMClientのOllama generate成功テスト

*定義場所: tests/test_utils/test_llm_client.py:119*

---

### test_local_client_generate_openai_compatible_success

**型**: `method`

**シグネチャ**:
```
def test_local_client_generate_openai_compatible_success(self, mock_client_class):
```

**説明**:

LocalLLMClientのOpenAI互換generate成功テスト

*定義場所: tests/test_utils/test_llm_client.py:132*

---

### test_local_client_generate_error

**型**: `method`

**シグネチャ**:
```
def test_local_client_generate_error(self, mock_client_class):
```

**説明**:

LocalLLMClientのgenerateエラーテスト

*定義場所: tests/test_utils/test_llm_client.py:147*

---

### TestAnthropicClient

**型**: `class`

**シグネチャ**:
```
class TestAnthropicClient:
```

**説明**:

AnthropicClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:159*

---

### test_anthropic_client_initialization_success

**型**: `method`

**シグネチャ**:
```
def test_anthropic_client_initialization_success(self):
```

**説明**:

AnthropicClientの正常初期化テスト

*定義場所: tests/test_utils/test_llm_client.py:162*

---

### test_anthropic_client_initialization_config_error

**型**: `method`

**シグネチャ**:
```
def test_anthropic_client_initialization_config_error(self, mock_anthropic):
```

**説明**:

AnthropicClientの設定エラーテスト

*定義場所: tests/test_utils/test_llm_client.py:169*

---

### test_anthropic_client_generate_success

**型**: `method`

**シグネチャ**:
```
def test_anthropic_client_generate_success(self, mock_anthropic):
```

**説明**:

AnthropicClientのgenerate成功テスト

*定義場所: tests/test_utils/test_llm_client.py:177*

---

### test_anthropic_client_generate_error

**型**: `method`

**シグネチャ**:
```
def test_anthropic_client_generate_error(self, mock_anthropic):
```

**説明**:

AnthropicClientのgenerateエラーテスト

*定義場所: tests/test_utils/test_llm_client.py:192*

---

### TestLLMClientFactory

**型**: `class`

**シグネチャ**:
```
class TestLLMClientFactory:
```

**説明**:

LLMClientFactoryクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:204*

---

### test_create_client_openai

**型**: `method`

**シグネチャ**:
```
def test_create_client_openai(self, mock_openai_client):
```

**説明**:

OpenAIクライアント作成テスト

*定義場所: tests/test_utils/test_llm_client.py:208*

---

### test_create_client_anthropic

**型**: `method`

**シグネチャ**:
```
def test_create_client_anthropic(self, mock_anthropic_client):
```

**説明**:

Anthropicクライアント作成テスト

*定義場所: tests/test_utils/test_llm_client.py:216*

---

### test_create_client_local

**型**: `method`

**シグネチャ**:
```
def test_create_client_local(self, mock_local_client):
```

**説明**:

Localクライアント作成テスト

*定義場所: tests/test_utils/test_llm_client.py:226*

---

### test_create_client_unknown_provider

**型**: `method`

**シグネチャ**:
```
def test_create_client_unknown_provider(self):
```

**説明**:

不明なプロバイダーテスト

*定義場所: tests/test_utils/test_llm_client.py:235*

---

### test_create_client_unknown_mode

**型**: `method`

**シグネチャ**:
```
def test_create_client_unknown_mode(self):
```

**説明**:

不明なモードテスト

*定義場所: tests/test_utils/test_llm_client.py:241*

---

### test_create_client_with_fallback_api_to_local

**型**: `method`

**シグネチャ**:
```
def test_create_client_with_fallback_api_to_local(self, mock_create_client):
```

**説明**:

APIからLocalへのフォールバックテスト

*定義場所: tests/test_utils/test_llm_client.py:248*

---

### test_create_client_with_fallback_local_to_api

**型**: `method`

**シグネチャ**:
```
def test_create_client_with_fallback_local_to_api(self, mock_create_client):
```

**説明**:

LocalからAPIへのフォールバックテスト

*定義場所: tests/test_utils/test_llm_client.py:256*

---


## tests/test_utils/test_logger.py

### TestLogger

**型**: `class`

**シグネチャ**:
```
class TestLogger:
```

**説明**:

Loggerクラスのテスト

*定義場所: tests/test_utils/test_logger.py:22*

---

### test_setup_logger_default

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_default(self):
```

**説明**:

デフォルト設定でのロガーセットアップテスト

*定義場所: tests/test_utils/test_logger.py:25*

---

### test_setup_logger_with_level

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_with_level(self):
```

**説明**:

ログレベル指定でのセットアップテスト

*定義場所: tests/test_utils/test_logger.py:38*

---

### test_setup_logger_with_invalid_level

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_with_invalid_level(self):
```

**説明**:

無効なログレベル指定でのテスト

*定義場所: tests/test_utils/test_logger.py:45*

---

### test_setup_logger_with_env_level

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_with_env_level(self):
```

**説明**:

環境変数からのログレベル取得テスト

*定義場所: tests/test_utils/test_logger.py:53*

---

### test_setup_logger_with_log_file

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_with_log_file(self, temp_project):
```

**説明**:

ログファイル指定でのセットアップテスト

*定義場所: tests/test_utils/test_logger.py:61*

---

### test_setup_logger_idempotent

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_idempotent(self):
```

**説明**:

同じロガー名の再セットアップが冪等であるテスト

*定義場所: tests/test_utils/test_logger.py:74*

---

### test_get_logger_default

**型**: `method`

**シグネチャ**:
```
def test_get_logger_default(self):
```

**説明**:

デフォルト設定でのロガー取得テスト

*定義場所: tests/test_utils/test_logger.py:83*

---

### test_get_logger_with_name

**型**: `method`

**シグネチャ**:
```
def test_get_logger_with_name(self):
```

**説明**:

名前指定でのロガー取得テスト

*定義場所: tests/test_utils/test_logger.py:90*

---

### test_get_logger_idempotent

**型**: `method`

**シグネチャ**:
```
def test_get_logger_idempotent(self):
```

**説明**:

同じ名前のロガーが再取得可能テスト

*定義場所: tests/test_utils/test_logger.py:96*

---

### test_get_logger_auto_setup

**型**: `method`

**シグネチャ**:
```
def test_get_logger_auto_setup(self):
```

**説明**:

ハンドラーがないロガーが自動設定されるテスト

*定義場所: tests/test_utils/test_logger.py:103*

---

### test_setup_logger_formatter

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_formatter(self):
```

**説明**:

フォーマッターの設定テスト

*定義場所: tests/test_utils/test_logger.py:115*

---

### test_setup_logger_file_handler_encoding

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_file_handler_encoding(self, temp_project):
```

**説明**:

ファイルハンドラーのエンコーディングテスト

*定義場所: tests/test_utils/test_logger.py:130*

---

### test_setup_logger_multiple_calls_same_name

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_multiple_calls_same_name(self):
```

**説明**:

同じ名前で複数回setup_loggerを呼ぶテスト

*定義場所: tests/test_utils/test_logger.py:144*

---

### test_setup_logger_console_output

**型**: `method`

**シグネチャ**:
```
def test_setup_logger_console_output(self):
```

**説明**:

コンソール出力のテスト

*定義場所: tests/test_utils/test_logger.py:153*

---


## tests/test_utils/test_outlines_utils.py

### TestOutlinesUtils

**型**: `class`

**シグネチャ**:
```
class TestOutlinesUtils:
```

**説明**:

OutlinesUtils関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:18*

---

### test_should_use_outlines_enabled_in_config

**型**: `method`

**シグネチャ**:
```
def test_should_use_outlines_enabled_in_config(self):
```

**説明**:

設定でOutlinesが有効な場合のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:21*

---

### test_should_use_outlines_disabled_in_config

**型**: `method`

**シグネチャ**:
```
def test_should_use_outlines_disabled_in_config(self):
```

**説明**:

設定でOutlinesが無効な場合のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:29*

---

### test_should_use_outlines_not_in_config

**型**: `method`

**シグネチャ**:
```
def test_should_use_outlines_not_in_config(self):
```

**説明**:

設定にOutlines設定がない場合のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:36*

---

### test_should_use_outlines_not_available

**型**: `method`

**シグネチャ**:
```
def test_should_use_outlines_not_available(self):
```

**説明**:

Outlinesライブラリが利用できない場合のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:43*

---

### test_create_outlines_model_openai

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_openai(self, mock_outlines):
```

**説明**:

OpenAIプロバイダーのOutlinesモデル作成テスト

*定義場所: tests/test_utils/test_outlines_utils.py:52*

---

### test_create_outlines_model_anthropic

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_anthropic(self):
```

**説明**:

AnthropicプロバイダーのOutlinesモデル作成テスト

*定義場所: tests/test_utils/test_outlines_utils.py:66*

---

### test_create_outlines_model_local

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_local(self):
```

**説明**:

LocalプロバイダーのOutlinesモデル作成テスト

*定義場所: tests/test_utils/test_outlines_utils.py:75*

---

### test_create_outlines_model_unknown_provider

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_unknown_provider(self):
```

**説明**:

未知のプロバイダーのテスト

*定義場所: tests/test_utils/test_outlines_utils.py:88*

---

### test_create_outlines_model_outlines_not_available

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_outlines_not_available(self):
```

**説明**:

Outlinesライブラリが利用できない場合のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:96*

---

### test_create_outlines_model_exception_handling

**型**: `method`

**シグネチャ**:
```
def test_create_outlines_model_exception_handling(self, mock_outlines):
```

**説明**:

例外発生時のエラーハンドリングテスト

*定義場所: tests/test_utils/test_outlines_utils.py:105*

---

### test_integration_with_llm_client_factory

**型**: `method`

**シグネチャ**:
```
def test_integration_with_llm_client_factory(self, mock_outlines, temp_project):
```

**説明**:

LLMClientFactoryとの統合テスト

*定義場所: tests/test_utils/test_outlines_utils.py:119*

---
