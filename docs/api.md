# API ドキュメント

自動生成日時: 2025-11-26 00:15:45

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

### read_makefile

**型**: `method`

**シグネチャ**:
```
def read_makefile(project_root: Path) -> str | None:
```

**説明**:

Read Makefile content.

*定義場所: docgen/collectors/collector_utils.py:25*

---

### read_package_json

**型**: `method`

**シグネチャ**:
```
def read_package_json(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read package.json file.

*定義場所: docgen/collectors/collector_utils.py:35*

---

### BuildCommandCollector

**型**: `class`

**シグネチャ**:
```
class BuildCommandCollector:
```

**説明**:

ビルドコマンド収集クラス

*定義場所: docgen/collectors/collector_utils.py:40*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None):
```

*説明なし*

*定義場所: docgen/collectors/collector_utils.py:43*

---

### collect_build_commands

**型**: `method`

**シグネチャ**:
```
def collect_build_commands(self) -> list[str]:
```

**説明**:

ビルドコマンドを収集

*定義場所: docgen/collectors/collector_utils.py:54*

---

### read_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def read_pyproject_toml(project_root: Path) -> dict[str, Any] | None:
```

**説明**:

Read pyproject.toml file.

*定義場所: docgen/collectors/collector_utils.py:131*

---

### extract_scripts_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_scripts_from_package_json(package_data: dict[str, Any]) -> list[str]:
```

**説明**:

Extract scripts from package.json.

*定義場所: docgen/collectors/collector_utils.py:146*

---

### extract_dependencies_from_package_json

**型**: `method`

**シグネチャ**:
```
def extract_dependencies_from_package_json(package_data: dict[str, Any]) -> dict[str, list[str]]:
```

**説明**:

Extract dependencies from package.json.

*定義場所: docgen/collectors/collector_utils.py:152*

---

### parse_makefile_targets

**型**: `method`

**シグネチャ**:
```
def parse_makefile_targets(content: str) -> list[str]:
```

**説明**:

Parse Makefile targets.

*定義場所: docgen/collectors/collector_utils.py:169*

---

### detect_language_from_config

**型**: `method`

**シグネチャ**:
```
def detect_language_from_config(project_root: Path) -> str | None:
```

**説明**:

Detect programming language from configuration files.

*定義場所: docgen/collectors/collector_utils.py:181*

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

プロジェクトのビルド/テスト手順、依存関係、コーディング規約などを収集する。

*定義場所: docgen/collectors/project_info_collector.py:17*

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

*定義場所: docgen/collectors/project_info_collector.py:45*

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

*定義場所: docgen/collectors/project_info_collector.py:58*

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

*定義場所: docgen/collectors/project_info_collector.py:75*

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

*定義場所: docgen/collectors/project_info_collector.py:155*

---

### collect_coding_standards

**型**: `method`

**シグネチャ**:
```
def collect_coding_standards(self) -> dict[str, str | dict[str, Any] | bool]:
```

**説明**:

コーディング規約を収集

Returns:
    コーディング規約の辞書

*定義場所: docgen/collectors/project_info_collector.py:236*

---

### collect_ci_cd_info

**型**: `method`

**シグネチャ**:
```
def collect_ci_cd_info(self) -> dict[str, list[str]]:
```

**説明**:

CI/CD情報を収集

Returns:
    CI/CD情報の辞書

*定義場所: docgen/collectors/project_info_collector.py:314*

---

### collect_project_structure

**型**: `method`

**シグネチャ**:
```
def collect_project_structure(self) -> dict[str, list[str]]:
```

**説明**:

プロジェクト構造を収集

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/project_info_collector.py:334*

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

*定義場所: docgen/collectors/project_info_collector.py:366*

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

*定義場所: docgen/detectors/detector_patterns.py:180*

---

### get_source_extensions

**型**: `method`

**シグネチャ**:
```
def get_source_extensions(cls, language: str) -> list[str]:
```

**説明**:

Get source file extensions for a language.

*定義場所: docgen/detectors/detector_patterns.py:185*

---

### detect_by_package_files

**型**: `method`

**シグネチャ**:
```
def detect_by_package_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for package manager files.

*定義場所: docgen/detectors/detector_patterns.py:190*

---

### detect_by_source_files

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files.

*定義場所: docgen/detectors/detector_patterns.py:196*

---

### detect_by_source_files_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files_with_exclusions(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files, excluding common directories.

*定義場所: docgen/detectors/detector_patterns.py:208*

---

### detect_by_extensions_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_extensions_with_exclusions(cls, project_root: Path, extensions: list[str]) -> bool:
```

**説明**:

Detect files by extensions, excluding common directories.

*定義場所: docgen/detectors/detector_patterns.py:222*

---

### is_excluded_path

**型**: `method`

**シグネチャ**:
```
def is_excluded_path(cls, path: Path, project_root: Path) -> bool:
```

**説明**:

Check if a path should be excluded from detection.

*定義場所: docgen/detectors/detector_patterns.py:237*

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

*定義場所: docgen/detectors/detector_patterns.py:247*

---

### is_js_config_or_test

**型**: `method`

**シグネチャ**:
```
def is_js_config_or_test(cls, file_path: Path) -> bool:
```

**説明**:

Check if a file is likely a JavaScript config or test file.

*定義場所: docgen/detectors/detector_patterns.py:268*

---

### detect_python_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_python_package_manager(cls, project_root: Path) -> str | None:
```

**説明**:

Detect Python package manager with special handling for pyproject.toml.

*定義場所: docgen/detectors/detector_patterns.py:274*

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

*定義場所: docgen/detectors/generic_detector.py:10*

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

*定義場所: docgen/detectors/generic_detector.py:13*

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

*定義場所: docgen/detectors/generic_detector.py:25*

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

*定義場所: docgen/detectors/generic_detector.py:38*

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

*定義場所: docgen/detectors/generic_detector.py:51*

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

*定義場所: docgen/detectors/go_detector.py:29*

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

*定義場所: docgen/detectors/go_detector.py:33*

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

*定義場所: docgen/detectors/javascript_detector.py:46*

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

*定義場所: docgen/detectors/javascript_detector.py:60*

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

*定義場所: docgen/docgen.py:32*

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

*定義場所: docgen/docgen.py:35*

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

*定義場所: docgen/docgen.py:69*

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

*定義場所: docgen/docgen.py:83*

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

*定義場所: docgen/docgen.py:93*

---

### CommandLineInterface

**型**: `class`

**シグネチャ**:
```
class CommandLineInterface:
```

**説明**:

コマンドラインインターフェースクラス

*定義場所: docgen/docgen.py:112*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

*説明なし*

*定義場所: docgen/docgen.py:115*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self) -> int:
```

**説明**:

メイン実行メソッド

*定義場所: docgen/docgen.py:118*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メインエントリーポイント

*定義場所: docgen/docgen.py:283*

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

*定義場所: docgen/generators/agents_generator.py:19*

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

*定義場所: docgen/generators/agents_generator.py:22*

---

### agents_path

**型**: `method`

**シグネチャ**:
```
def agents_path(self):
```

*説明なし*

*定義場所: docgen/generators/agents_generator.py:41*

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

*定義場所: docgen/generators/base_generator.py:16*

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

*定義場所: docgen/generators/base_generator.py:19*

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

*定義場所: docgen/generators/base_generator.py:620*

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

*定義場所: docgen/generators/readme_generator.py:17*

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

*定義場所: docgen/utils/outlines_utils.py:37*

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

*定義場所: docgen/utils/outlines_utils.py:84*

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

*定義場所: docgen/utils/outlines_utils.py:103*

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

*定義場所: docgen/utils/outlines_utils.py:313*

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
