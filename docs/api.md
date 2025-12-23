# API ドキュメント

自動生成日時: 2025-12-24 06:58:48

---

## docgen/archgen/cli.py

### generate_architecture

**型**: `function`

**シグネチャ**:
```
def generate_architecture(project_root: Path, output_dir: Path, exclude_directories: list[str] | None) -> bool:
```

**説明**:

アーキテクチャを生成

Args:
    project_root: プロジェクトルート
    output_dir: 出力ディレクトリ
    exclude_directories: スキャンから除外するディレクトリのリスト

*定義場所: docgen/archgen/cli.py:15*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

CLI エントリポイント

*定義場所: docgen/archgen/cli.py:54*

---


## docgen/archgen/detectors/docker_detector.py

### DockerDetector

**型**: `class`

**シグネチャ**:
```
class DockerDetector:
```

**説明**:

Docker 構成を検出

*定義場所: docgen/archgen/detectors/docker_detector.py:11*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self, project_root: Path) -> list[Service]:
```

*説明なし*

*定義場所: docgen/archgen/detectors/docker_detector.py:14*

---


## docgen/archgen/detectors/generic_detector.py

### GenericDetector

**型**: `class`

**シグネチャ**:
```
class GenericDetector:
```

**説明**:

様々なプログラミング言語のプロジェクトを検出

*定義場所: docgen/archgen/detectors/generic_detector.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, exclude_directories: list[str] | None, exclude_patterns: set[str] | None):
```

**説明**:

初期化

Args:
    exclude_directories: 除外するディレクトリのリスト
    exclude_patterns: 依存関係から除外するパターンのセット

*定義場所: docgen/archgen/detectors/generic_detector.py:16*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self, project_root: Path) -> list[Service]:
```

**説明**:

プロジェクトをスキャンしてサービスを検出

*定義場所: docgen/archgen/detectors/generic_detector.py:33*

---


## docgen/archgen/detectors/python_detector.py

### PythonDetector

**型**: `class`

**シグネチャ**:
```
class PythonDetector:
```

**説明**:

Python プロジェクトを検出

*定義場所: docgen/archgen/detectors/python_detector.py:11*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, exclude_directories: list[str] | None, exclude_patterns: set[str] | None):
```

**説明**:

初期化

Args:
    exclude_directories: 除外するディレクトリのリスト
    exclude_patterns: 依存関係から除外するパターンのセット

*定義場所: docgen/archgen/detectors/python_detector.py:17*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self, project_root: Path) -> list[Service]:
```

*説明なし*

*定義場所: docgen/archgen/detectors/python_detector.py:34*

---


## docgen/archgen/generators/mermaid_generator.py

### MermaidGenerator

**型**: `class`

**シグネチャ**:
```
class MermaidGenerator:
```

**説明**:

Mermaid.js形式でアーキテクチャ図を生成（依存なし）

*定義場所: docgen/archgen/generators/mermaid_generator.py:11*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, manifest: ArchitectureManifest, output_dir: Path) -> Path:
```

**説明**:

Mermaid形式のアーキテクチャ図を生成

*定義場所: docgen/archgen/generators/mermaid_generator.py:23*

---


## docgen/archgen/models.py

### Module

**型**: `class`

**シグネチャ**:
```
class Module:
```

**説明**:

モジュール/パッケージ

*定義場所: docgen/archgen/models.py:12*

---

### Service

**型**: `class`

**シグネチャ**:
```
class Service:
```

**説明**:

個別サービス/コンポーネント

*定義場所: docgen/archgen/models.py:22*

---

### ArchitectureManifest

**型**: `class`

**シグネチャ**:
```
class ArchitectureManifest:
```

**説明**:

アーキテクチャマニフェスト

*定義場所: docgen/archgen/models.py:34*

---

### to_yaml

**型**: `method`

**シグネチャ**:
```
def to_yaml(self, path: Path) -> None:
```

**説明**:

YAML形式で保存

*定義場所: docgen/archgen/models.py:42*

---

### from_yaml

**型**: `method`

**シグネチャ**:
```
def from_yaml(cls, path: Path) -> 'ArchitectureManifest':
```

**説明**:

YAML形式から読み込み

*定義場所: docgen/archgen/models.py:49*

---

### deduplicate_services

**型**: `method`

**シグネチャ**:
```
def deduplicate_services(self, preferred_languages: list[str] | None) -> 'ArchitectureManifest':
```

**説明**:

サービス重複除去と優先順位付け

Args:
    preferred_languages: 優先する言語のリスト（languages.preferred設定）

Returns:
    重複除去後のArchitectureManifest（selfを変更）

*定義場所: docgen/archgen/models.py:55*

---


## docgen/archgen/renderer.py

### ArchitectureRenderer

**型**: `class`

**シグネチャ**:
```
class ArchitectureRenderer:
```

**説明**:

アーキテクチャ図のレンダリングを管理

*定義場所: docgen/archgen/renderer.py:11*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, generator_type: str, image_formats: list[str] | None):
```

**説明**:

初期化

Args:
    generator_type: 生成器の種類 ("mermaid", "blockdiag", "matplotlib")
    image_formats: 画像出力形式のリスト

*定義場所: docgen/archgen/renderer.py:14*

---

### render

**型**: `method`

**シグネチャ**:
```
def render(self, manifest: ArchitectureManifest, output_dir: Path) -> dict[str, Path]:
```

**説明**:

図を生成

Args:
    manifest: アーキテクチャマニフェスト
    output_dir: 出力ディレクトリ

Returns:
    生成されたファイルのパス辞書

*定義場所: docgen/archgen/renderer.py:28*

---


## docgen/archgen/scanner.py

### ProjectScanner

**型**: `class`

**シグネチャ**:
```
class ProjectScanner:
```

**説明**:

プロジェクトをスキャンしてアーキテクチャを抽出

*定義場所: docgen/archgen/scanner.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, exclude_directories: list[str] | None, config: dict[str, Any] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートディレクトリ
    exclude_directories: 除外するディレクトリのリスト
    config: 設定辞書（依存関係フィルタリング用）

*定義場所: docgen/archgen/scanner.py:17*

---

### scan

**型**: `method`

**シグネチャ**:
```
def scan(self) -> ArchitectureManifest:
```

**説明**:

プロジェクトをスキャン

Returns:
    アーキテクチャマニフェスト（サービス重複除去済み）

*定義場所: docgen/archgen/scanner.py:100*

---


## docgen/benchmark/comparator.py

### BenchmarkComparator

**型**: `class`

**シグネチャ**:
```
class BenchmarkComparator:
```

**説明**:

ベンチマーク結果の比較クラス

*定義場所: docgen/benchmark/comparator.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, baseline_path: Path, current_path: Path):
```

**説明**:

初期化

Args:
    baseline_path: ベースライン（比較元）のJSONファイルパス
    current_path: 現在の（比較先）のJSONファイルパス

*定義場所: docgen/benchmark/comparator.py:16*

---

### compare

**型**: `method`

**シグネチャ**:
```
def compare(self) -> dict[str, Any]:
```

**説明**:

ベンチマーク結果を比較

Returns:
    比較結果の辞書

*定義場所: docgen/benchmark/comparator.py:45*

---

### generate_comparison_report

**型**: `method`

**シグネチャ**:
```
def generate_comparison_report(self) -> str:
```

**説明**:

比較レポートをMarkdown形式で生成

Returns:
    Markdown形式のレポート

*定義場所: docgen/benchmark/comparator.py:160*

---

### save_comparison_report

**型**: `method`

**シグネチャ**:
```
def save_comparison_report(self, path: Path) -> None:
```

**説明**:

比較レポートをファイルに保存

Args:
    path: 保存先のパス

*定義場所: docgen/benchmark/comparator.py:253*

---


## docgen/benchmark/core.py

### BenchmarkContext

**型**: `class`

**シグネチャ**:
```
class BenchmarkContext:
```

**説明**:

ベンチマーク測定用のコンテキストマネージャー

*定義場所: docgen/benchmark/core.py:20*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, name: str, recorder: BenchmarkRecorder | None, enabled: bool):
```

**説明**:

初期化

Args:
    name: 測定対象の処理名
    recorder: ベンチマークレコーダー（Noneの場合はグローバルレコーダーを使用）
    enabled: 測定を有効にするかどうか

*定義場所: docgen/benchmark/core.py:23*

---

### __enter__

**型**: `method`

**シグネチャ**:
```
def __enter__(self) -> 'BenchmarkContext':
```

**説明**:

測定開始

*定義場所: docgen/benchmark/core.py:40*

---

### __exit__

**型**: `method`

**シグネチャ**:
```
def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
```

**説明**:

測定終了と結果記録

*定義場所: docgen/benchmark/core.py:51*

---

### benchmark

**型**: `function`

**シグネチャ**:
```
def benchmark(name: str | None, enabled: bool) -> Callable:
```

**説明**:

関数の実行時間を測定するデコレータ

Args:
    name: 測定対象の処理名（Noneの場合は関数名を使用）
    enabled: 測定を有効にするかどうか

Returns:
    デコレータ関数

Example:
    @benchmark("my_function")
    def my_function():
        # 処理
        pass

*定義場所: docgen/benchmark/core.py:84*

---

### benchmark_context

**型**: `function`

**シグネチャ**:
```
def benchmark_context(name: str, recorder: BenchmarkRecorder | None, enabled: bool) -> Generator[BenchmarkContext, None, None]:
```

**説明**:

ベンチマークコンテキストマネージャー（関数形式）

Args:
    name: 測定対象の処理名
    recorder: ベンチマークレコーダー
    enabled: 測定を有効にするかどうか

Yields:
    BenchmarkContextインスタンス

Example:
    with benchmark_context("my_operation"):
        # 処理
        pass

*定義場所: docgen/benchmark/core.py:116*

---


## docgen/benchmark/models.py

### BenchmarkResult

**型**: `class`

**シグネチャ**:
```
class BenchmarkResult:
```

**説明**:

ベンチマーク測定結果

*定義場所: docgen/benchmark/models.py:11*

---

### BenchmarkSummary

**型**: `class`

**シグネチャ**:
```
class BenchmarkSummary:
```

**説明**:

ベンチマーク結果の集計情報

*定義場所: docgen/benchmark/models.py:30*

---


## docgen/benchmark/recorder.py

### BenchmarkRecorder

**型**: `class`

**シグネチャ**:
```
class BenchmarkRecorder:
```

**説明**:

ベンチマーク結果の記録と集計を行うクラス

*定義場所: docgen/benchmark/recorder.py:10*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

**説明**:

初期化

*定義場所: docgen/benchmark/recorder.py:15*

---

### get_global

**型**: `method`

**シグネチャ**:
```
def get_global(cls) -> 'BenchmarkRecorder':
```

**説明**:

グローバルレコーダーインスタンスを取得

Returns:
    グローバルレコーダーインスタンス

*定義場所: docgen/benchmark/recorder.py:20*

---

### reset_global

**型**: `method`

**シグネチャ**:
```
def reset_global(cls) -> None:
```

**説明**:

グローバルレコーダーをリセット

*定義場所: docgen/benchmark/recorder.py:32*

---

### record

**型**: `method`

**シグネチャ**:
```
def record(self, result: BenchmarkResult) -> None:
```

**説明**:

ベンチマーク結果を記録

Args:
    result: ベンチマーク結果

*定義場所: docgen/benchmark/recorder.py:36*

---

### get_results

**型**: `method`

**シグネチャ**:
```
def get_results(self) -> list[BenchmarkResult]:
```

**説明**:

記録された結果を取得

Returns:
    ベンチマーク結果のリスト

*定義場所: docgen/benchmark/recorder.py:45*

---

### clear

**型**: `method`

**シグネチャ**:
```
def clear(self) -> None:
```

**説明**:

記録をクリア

*定義場所: docgen/benchmark/recorder.py:54*

---

### get_summary

**型**: `method`

**シグネチャ**:
```
def get_summary(self) -> BenchmarkSummary:
```

**説明**:

ベンチマーク結果の集計情報を取得

Returns:
    ベンチマーク集計情報

*定義場所: docgen/benchmark/recorder.py:58*

---

### export_json

**型**: `method`

**シグネチャ**:
```
def export_json(self) -> dict[str, Any]:
```

**説明**:

結果をJSON形式でエクスポート

Returns:
    JSON形式の辞書

*定義場所: docgen/benchmark/recorder.py:92*

---


## docgen/benchmark/reporter.py

### BenchmarkReporter

**型**: `class`

**シグネチャ**:
```
class BenchmarkReporter:
```

**説明**:

ベンチマーク結果のレポート生成クラス

*定義場所: docgen/benchmark/reporter.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, recorder: BenchmarkRecorder | None):
```

**説明**:

初期化

Args:
    recorder: ベンチマークレコーダー（Noneの場合はグローバルレコーダーを使用）

*定義場所: docgen/benchmark/reporter.py:18*

---

### generate_markdown

**型**: `method`

**シグネチャ**:
```
def generate_markdown(self, include_children: bool) -> str:
```

**説明**:

Markdown形式のレポートを生成

Args:
    include_children: 子処理の結果を含めるかどうか

Returns:
    Markdown形式のレポート

*定義場所: docgen/benchmark/reporter.py:27*

---

### generate_json

**型**: `method`

**シグネチャ**:
```
def generate_json(self) -> dict[str, Any]:
```

**説明**:

JSON形式のレポートを生成

Returns:
    JSON形式の辞書

*定義場所: docgen/benchmark/reporter.py:111*

---

### save_markdown

**型**: `method`

**シグネチャ**:
```
def save_markdown(self, path: Path) -> None:
```

**説明**:

Markdownレポートをファイルに保存

Args:
    path: 保存先のパス

*定義場所: docgen/benchmark/reporter.py:120*

---

### save_json

**型**: `method`

**シグネチャ**:
```
def save_json(self, path: Path) -> None:
```

**説明**:

JSONレポートをファイルに保存

Args:
    path: 保存先のパス

*定義場所: docgen/benchmark/reporter.py:130*

---

### generate_csv

**型**: `method`

**シグネチャ**:
```
def generate_csv(self, include_children: bool) -> str:
```

**説明**:

CSV形式のレポートを生成

Args:
    include_children: 子処理の結果を含めるかどうか

Returns:
    CSV形式の文字列

*定義場所: docgen/benchmark/reporter.py:140*

---

### save_csv

**型**: `method`

**シグネチャ**:
```
def save_csv(self, path: Path, include_children: bool) -> None:
```

**説明**:

CSVレポートをファイルに保存

Args:
    path: 保存先のパス
    include_children: 子処理の結果を含めるかどうか

*定義場所: docgen/benchmark/reporter.py:209*

---

### detect_bottlenecks

**型**: `method`

**シグネチャ**:
```
def detect_bottlenecks(self, threshold_percent: float) -> list[str]:
```

**説明**:

ボトルネックを検出

Args:
    threshold_percent: ボトルネックとみなす実行時間の割合（%）

Returns:
    ボトルネックの処理名のリスト

*定義場所: docgen/benchmark/reporter.py:220*

---


## docgen/benchmark/utils.py

### get_current_process

**型**: `function`

**シグネチャ**:
```
def get_current_process() -> psutil.Process:
```

**説明**:

現在のプロセスを取得

Returns:
    現在のプロセス

*定義場所: docgen/benchmark/utils.py:10*

---

### format_duration

**型**: `function`

**シグネチャ**:
```
def format_duration(seconds: float) -> str:
```

**説明**:

実行時間をフォーマット

Args:
    seconds: 秒数

Returns:
    フォーマットされた文字列

*定義場所: docgen/benchmark/utils.py:20*

---

### format_memory

**型**: `function`

**シグネチャ**:
```
def format_memory(bytes_size: int) -> str:
```

**説明**:

メモリサイズをフォーマット

Args:
    bytes_size: バイト数

Returns:
    フォーマットされた文字列

*定義場所: docgen/benchmark/utils.py:38*

---


## docgen/cli/commands/base.py

### BaseCommand

**型**: `class`

**シグネチャ**:
```
class BaseCommand:
```

**説明**:

コマンドハンドラーの基底クラス

*定義場所: docgen/cli/commands/base.py:10*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

コマンドを実行

Args:
    args: コマンドライン引数
    project_root: プロジェクトルートディレクトリ

Returns:
    終了コード（0=成功、1=失敗）

*定義場所: docgen/cli/commands/base.py:14*

---


## docgen/cli/commands/benchmark.py

### BenchmarkCommand

**型**: `class`

**シグネチャ**:
```
class BenchmarkCommand:
```

**説明**:

ベンチマークコマンド

*定義場所: docgen/cli/commands/benchmark.py:15*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Run benchmarks and generate reports

Args:
    args: Command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/commands/benchmark.py:18*

---


## docgen/cli/commands/build_index.py

### BuildIndexCommand

**型**: `class`

**シグネチャ**:
```
class BuildIndexCommand:
```

**説明**:

RAGインデックス構築コマンド

*定義場所: docgen/cli/commands/build_index.py:14*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Build RAG index

Args:
    args: Command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/commands/build_index.py:17*

---


## docgen/cli/commands/generate.py

### GenerateCommand

**型**: `class`

**シグネチャ**:
```
class GenerateCommand:
```

**説明**:

ドキュメント生成コマンド

*定義場所: docgen/cli/commands/generate.py:14*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Generate documentation

Args:
    args: Command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/commands/generate.py:17*

---


## docgen/cli/commands/hooks.py

### HooksCommand

**型**: `class`

**シグネチャ**:
```
class HooksCommand:
```

**説明**:

Git hooks管理コマンド

*定義場所: docgen/cli/commands/hooks.py:17*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Handle Git hooks management actions

Args:
    args: Command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/commands/hooks.py:20*

---


## docgen/cli/commands/init.py

### InitCommand

**型**: `class`

**シグネチャ**:
```
class InitCommand:
```

**説明**:

プロジェクト初期化コマンド

*定義場所: docgen/cli/commands/init.py:18*

---

### execute

**型**: `method`

**シグネチャ**:
```
def execute(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Initialize the project

Args:
    args: Command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/commands/init.py:21*

---


## docgen/cli/parser.py

### create_parser

**型**: `function`

**シグネチャ**:
```
def create_parser() -> argparse.ArgumentParser:
```

**説明**:

Create and configure the CLI argument parser

Returns:
    Configured ArgumentParser instance

*定義場所: docgen/cli/parser.py:9*

---


## docgen/cli/runner.py

### CommandRunner

**型**: `class`

**シグネチャ**:
```
class CommandRunner:
```

**説明**:

コマンド実行を管理するオーケストレーター

*定義場所: docgen/cli/runner.py:21*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

*説明なし*

*定義場所: docgen/cli/runner.py:24*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, args: Namespace, project_root: Path) -> int:
```

**説明**:

Execute the appropriate command based on parsed arguments

Args:
    args: Parsed command line arguments
    project_root: Project root directory

Returns:
    Exit code (0 for success, 1 for failure)

*定義場所: docgen/cli/runner.py:36*

---


## docgen/collectors/base_collector.py

### BaseCollector

**型**: `class`

**シグネチャ**:
```
class BaseCollector:
```

**説明**:

ベースコレクタークラス

Generic[T]を使用して、各collectorが返す型を明示的に定義可能にする。

Type Parameters:
    T: このコレクターが収集して返すデータの型

*定義場所: docgen/collectors/base_collector.py:12*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    logger: ロガーインスタンス（Noneの場合はデフォルトロガーを使用）

*定義場所: docgen/collectors/base_collector.py:21*

---

### collect

**型**: `method`

**シグネチャ**:
```
def collect(self) -> T:
```

**説明**:

情報を収集（サブクラスで実装）

Returns:
    収集した情報（型Tのインスタンス）

*定義場所: docgen/collectors/base_collector.py:33*

---


## docgen/collectors/coding_standards_collector.py

### CodingStandardsCollector

**型**: `class`

**シグネチャ**:
```
class CodingStandardsCollector:
```

**説明**:

Coding standards collector class

*定義場所: docgen/collectors/coding_standards_collector.py:12*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    logger: Logger instance

*定義場所: docgen/collectors/coding_standards_collector.py:19*

---

### collect_coding_standards

**型**: `method`

**シグネチャ**:
```
def collect_coding_standards(self) -> dict[str, str | dict[str, Any] | bool]:
```

**説明**:

Collect coding standards

Returns:
    Dictionary of coding standards

*定義場所: docgen/collectors/coding_standards_collector.py:30*

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

### TestingCommandScanner

**型**: `class`

**シグネチャ**:
```
class TestingCommandScanner:
```

**説明**:

Test command scanner class

*定義場所: docgen/collectors/collector_utils.py:203*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    package_managers: Dictionary of detected package managers
    logger: Logger instance

*定義場所: docgen/collectors/collector_utils.py:212*

---

### collect_test_commands

**型**: `method`

**シグネチャ**:
```
def collect_test_commands(self) -> list[str]:
```

**説明**:

Collect test commands

Returns:
    List of test commands

*定義場所: docgen/collectors/collector_utils.py:231*

---


## docgen/collectors/command_help_extractor.py

### CommandHelpExtractor

**型**: `class`

**シグネチャ**:
```
class CommandHelpExtractor:
```

**説明**:

Extract help text from Python CLI entry points

*定義場所: docgen/collectors/command_help_extractor.py:17*

---

### extract_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_from_entry_point(entry_point: str, project_root: Path | None) -> str:
```

**説明**:

Extract description from a Python entry point

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    Description string, or empty string if extraction fails

*定義場所: docgen/collectors/command_help_extractor.py:21*

---

### extract_options_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_options_from_entry_point(entry_point: str, project_root: Path | None) -> list[dict[str, str]]:
```

**説明**:

Extract command options from a Python entry point

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    List of option dicts with 'name' and 'help' keys

*定義場所: docgen/collectors/command_help_extractor.py:116*

---

### extract_structured_commands_from_entry_point

**型**: `method`

**シグネチャ**:
```
def extract_structured_commands_from_entry_point(entry_point: str, project_root: Path | None) -> dict[str, Any]:
```

**説明**:

Extract structured command hierarchy from a Python entry point.

Returns a structured dict with:
- options: list of main CLI options (e.g., --config, --detect-only)
- subcommands: dict of subcommand name -> {help, options, subcommands}

Args:
    entry_point: Entry point string in format "module.path:function"
    project_root: Project root directory to add to sys.path

Returns:
    Structured command hierarchy dict

*定義場所: docgen/collectors/command_help_extractor.py:231*

---


## docgen/collectors/dependency_collector.py

### DependencyCollector

**型**: `class`

**シグネチャ**:
```
class DependencyCollector:
```

**説明**:

Dependency collector class

*定義場所: docgen/collectors/dependency_collector.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

**説明**:

Initialize

Args:
    project_root: Project root directory
    logger: Logger instance

*定義場所: docgen/collectors/dependency_collector.py:20*

---

### collect_dependencies

**型**: `method`

**シグネチャ**:
```
def collect_dependencies(self) -> dict[str, list[str]]:
```

**説明**:

Collect dependencies

Returns:
    Dictionary of dependencies per language

*定義場所: docgen/collectors/dependency_collector.py:31*

---


## docgen/collectors/language_info_collector.py

### LanguageInfoCollector

**型**: `class`

**シグネチャ**:
```
class LanguageInfoCollector:
```

**説明**:

言語固有情報収集クラス

*定義場所: docgen/collectors/language_info_collector.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None):
```

*説明なし*

*定義場所: docgen/collectors/language_info_collector.py:24*

---

### collect

**型**: `method`

**シグネチャ**:
```
def collect(self) -> dict[str, Any]:
```

**説明**:

言語固有情報を収集

Returns:
    収集した情報の辞書

*定義場所: docgen/collectors/language_info_collector.py:27*

---

### collect_scripts

**型**: `method`

**シグネチャ**:
```
def collect_scripts(self) -> dict[str, dict[str, str]]:
```

**説明**:

実行可能なスクリプトを収集

Returns:
    スクリプト名と詳細情報の辞書 {name: {command: str, description: str}}

*定義場所: docgen/collectors/language_info_collector.py:39*

---

### collect_project_description

**型**: `method`

**シグネチャ**:
```
def collect_project_description(self) -> str | None:
```

**説明**:

プロジェクトの説明を収集

優先順位:
1. package.json (JavaScript/TypeScript プロジェクト)
2. pyproject.toml (Python プロジェクト)
3. setup.py (古いPythonプロジェクト)
4. README.md (上記が存在しない場合のみ)

Returns:
    プロジェクトの説明文（見つからない場合はNone）

*定義場所: docgen/collectors/language_info_collector.py:141*

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

*定義場所: docgen/collectors/project_info_collector.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, package_managers: dict[str, str] | None, logger: Any | None, exclude_directories: list[str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    package_managers: 言語ごとのパッケージマネージャ辞書
    logger: ロガーインスタンス
    exclude_directories: 除外するディレクトリのリスト

*定義場所: docgen/collectors/project_info_collector.py:23*

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

*定義場所: docgen/collectors/project_info_collector.py:61*

---

### collect_key_features

**型**: `method`

**シグネチャ**:
```
def collect_key_features(self) -> list[str]:
```

**説明**:

主要機能を収集（プレースホルダー）

Returns:
    主要機能のリスト

*定義場所: docgen/collectors/project_info_collector.py:97*

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

*定義場所: docgen/collectors/project_info_collector.py:107*

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

*定義場所: docgen/collectors/project_info_collector.py:116*

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

*定義場所: docgen/collectors/project_info_collector.py:125*

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

*定義場所: docgen/collectors/project_info_collector.py:134*

---

### collect_project_structure

**型**: `method`

**シグネチャ**:
```
def collect_project_structure(self) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を収集

StructureAnalyzerに委譲して詳細な構造分析を実行

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/project_info_collector.py:155*

---


## docgen/collectors/structure_analyzer.py

### StructureAnalyzer

**型**: `class`

**シグネチャ**:
```
class StructureAnalyzer:
```

**説明**:

プロジェクト構造分析クラス

*定義場所: docgen/collectors/structure_analyzer.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, logger: Any | None, exclude_directories: list[str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    logger: ロガーインスタンス
    exclude_directories: 除外するディレクトリのリスト（追加分）

*定義場所: docgen/collectors/structure_analyzer.py:51*

---

### collect

**型**: `method`

**シグネチャ**:
```
def collect(self, max_depth: int) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を収集（BaseCollectorインターフェース実装）

Args:
    max_depth: ディレクトリの最大探索深度

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/structure_analyzer.py:71*

---

### count_symbols_in_file

**型**: `method`

**シグネチャ**:
```
def count_symbols_in_file(self, file_path: Path) -> int:
```

**説明**:

Pythonファイルのシンボル数をカウント

Args:
    file_path: Pythonファイルのパス

Returns:
    シンボル数（クラス、関数、非同期関数の合計）

*定義場所: docgen/collectors/structure_analyzer.py:83*

---

### collect_directory_structure

**型**: `method`

**シグネチャ**:
```
def collect_directory_structure(self, directory: Path, max_depth: int, current_depth: int) -> dict[str, Any] | str:
```

**説明**:

ディレクトリ構造を再帰的に収集

Args:
    directory: 対象ディレクトリ
    max_depth: 最大探索深度
    current_depth: 現在の深度

Returns:
    ディレクトリ構造の辞書、またはネストしないディレクトリの場合は "directory"

*定義場所: docgen/collectors/structure_analyzer.py:106*

---

### analyze

**型**: `method`

**シグネチャ**:
```
def analyze(self, max_depth: int) -> dict[str, Any]:
```

**説明**:

プロジェクト構造を分析

Args:
    max_depth: ディレクトリの最大探索深度

Returns:
    プロジェクト構造の辞書

*定義場所: docgen/collectors/structure_analyzer.py:168*

---


## docgen/config/config_accessor.py

### ConfigKeys

**型**: `class`

**シグネチャ**:
```
class ConfigKeys:
```

**説明**:

Configuration key constants to avoid hardcoding.

*定義場所: docgen/config/config_accessor.py:10*

---

### ConfigAccessor

**型**: `class`

**シグネチャ**:
```
class ConfigAccessor:
```

**説明**:

Type-safe configuration accessor.
Wraps the raw configuration dictionary and provides typed properties.

*定義場所: docgen/config/config_accessor.py:26*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:32*

---

### raw_config

**型**: `method`

**シグネチャ**:
```
def raw_config(self) -> dict[str, Any]:
```

**説明**:

Get raw configuration dictionary

*定義場所: docgen/config/config_accessor.py:36*

---

### generation

**型**: `method`

**シグネチャ**:
```
def generation(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:44*

---

### generate_api_doc

**型**: `method`

**シグネチャ**:
```
def generate_api_doc(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:48*

---

### update_readme

**型**: `method`

**シグネチャ**:
```
def update_readme(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:52*

---

### generate_agents_doc

**型**: `method`

**シグネチャ**:
```
def generate_agents_doc(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:56*

---

### preserve_manual_sections

**型**: `method`

**シグネチャ**:
```
def preserve_manual_sections(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:60*

---

### llm

**型**: `method`

**シグネチャ**:
```
def llm(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:67*

---

### llm_provider

**型**: `method`

**シグネチャ**:
```
def llm_provider(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:71*

---

### llm_model

**型**: `method`

**シグネチャ**:
```
def llm_model(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:75*

---

### llm_temperature

**型**: `method`

**シグネチャ**:
```
def llm_temperature(self) -> float:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:79*

---

### output

**型**: `method`

**シグネチャ**:
```
def output(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:86*

---

### output_dir

**型**: `method`

**シグネチャ**:
```
def output_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:90*

---

### api_doc_dir

**型**: `method`

**シグネチャ**:
```
def api_doc_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:94*

---

### readme_path

**型**: `method`

**シグネチャ**:
```
def readme_path(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:98*

---

### agents_doc_path

**型**: `method`

**シグネチャ**:
```
def agents_doc_path(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:102*

---

### rag

**型**: `method`

**シグネチャ**:
```
def rag(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:109*

---

### rag_enabled

**型**: `method`

**シグネチャ**:
```
def rag_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:113*

---

### rag_auto_build_index

**型**: `method`

**シグネチャ**:
```
def rag_auto_build_index(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:117*

---

### rag_embedding

**型**: `method`

**シグネチャ**:
```
def rag_embedding(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:121*

---

### rag_retrieval

**型**: `method`

**シグネチャ**:
```
def rag_retrieval(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:125*

---

### cache

**型**: `method`

**シグネチャ**:
```
def cache(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:132*

---

### cache_enabled

**型**: `method`

**シグネチャ**:
```
def cache_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:136*

---

### debug

**型**: `method`

**シグネチャ**:
```
def debug(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:143*

---

### debug_enabled

**型**: `method`

**シグネチャ**:
```
def debug_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:147*

---

### agents

**型**: `method`

**シグネチャ**:
```
def agents(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:154*

---

### agents_llm_mode

**型**: `method`

**シグネチャ**:
```
def agents_llm_mode(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:158*

---

### agents_generation

**型**: `method`

**シグネチャ**:
```
def agents_generation(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:162*

---

### architecture

**型**: `method`

**シグネチャ**:
```
def architecture(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:169*

---

### architecture_enabled

**型**: `method`

**シグネチャ**:
```
def architecture_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:173*

---

### architecture_output_dir

**型**: `method`

**シグネチャ**:
```
def architecture_output_dir(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:177*

---

### architecture_generator

**型**: `method`

**シグネチャ**:
```
def architecture_generator(self) -> str:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:181*

---

### exclude

**型**: `method`

**シグネチャ**:
```
def exclude(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:188*

---

### exclude_directories

**型**: `method`

**シグネチャ**:
```
def exclude_directories(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:192*

---

### exclude_patterns

**型**: `method`

**シグネチャ**:
```
def exclude_patterns(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:196*

---

### use_gitignore

**型**: `method`

**シグネチャ**:
```
def use_gitignore(self) -> bool:
```

**説明**:

`.gitignore`を適用するかどうか

*定義場所: docgen/config/config_accessor.py:200*

---

### hooks

**型**: `method`

**シグネチャ**:
```
def hooks(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:208*

---

### hooks_enabled

**型**: `method`

**シグネチャ**:
```
def hooks_enabled(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:212*

---

### languages

**型**: `method`

**シグネチャ**:
```
def languages(self) -> dict[str, Any]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:219*

---

### languages_auto_detect

**型**: `method`

**シグネチャ**:
```
def languages_auto_detect(self) -> bool:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:223*

---

### languages_preferred

**型**: `method`

**シグネチャ**:
```
def languages_preferred(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:227*

---

### languages_ignored

**型**: `method`

**シグネチャ**:
```
def languages_ignored(self) -> list[str]:
```

*説明なし*

*定義場所: docgen/config/config_accessor.py:231*

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

*定義場所: docgen/config_manager.py:45*

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

*定義場所: docgen/config_manager.py:48*

---

### get_config

**型**: `method`

**シグネチャ**:
```
def get_config(self) -> dict[str, Any]:
```

**説明**:

現在の設定を取得

*定義場所: docgen/config_manager.py:172*

---

### accessor

**型**: `method`

**シグネチャ**:
```
def accessor(self) -> ConfigAccessor:
```

**説明**:

型安全な設定アクセサを取得（遅延初期化）

*定義場所: docgen/config_manager.py:177*

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

*定義場所: docgen/config_manager.py:211*

---

### load_detector_defaults

**型**: `method`

**シグネチャ**:
```
def load_detector_defaults(self) -> dict[str, Any]:
```

**説明**:

Detectorのデフォルト設定を読み込み

*定義場所: docgen/config_manager.py:236*

---

### load_detector_user_overrides

**型**: `method`

**シグネチャ**:
```
def load_detector_user_overrides(self) -> dict[str, Any]:
```

**説明**:

ユーザー設定ファイルを読み込み

*定義場所: docgen/config_manager.py:240*

---

### merge_detector_configs

**型**: `method`

**シグネチャ**:
```
def merge_detector_configs(self, defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
```

**説明**:

Detectorのデフォルト設定とユーザー設定をマージ

*定義場所: docgen/config_manager.py:244*

---


## docgen/detector_config_loader.py

### DetectorConfigLoader

**型**: `class`

**シグネチャ**:
```
class DetectorConfigLoader:
```

**説明**:

Loader for detector configurations

*定義場所: docgen/detector_config_loader.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

*説明なし*

*定義場所: docgen/detector_config_loader.py:16*

---

### load_defaults

**型**: `method`

**シグネチャ**:
```
def load_defaults(self) -> dict[str, Any]:
```

**説明**:

Load default detector configurations

Returns:
    Dictionary of language configurations

*定義場所: docgen/detector_config_loader.py:19*

---

### load_user_overrides

**型**: `method`

**シグネチャ**:
```
def load_user_overrides(self) -> dict[str, Any]:
```

**説明**:

Load detector configuration from config.toml

Returns:
    Detector configuration dictionary

*定義場所: docgen/detector_config_loader.py:46*

---

### merge_configs

**型**: `method`

**シグネチャ**:
```
def merge_configs(self, defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
```

**説明**:

Merge default and user configurations

Args:
    defaults: Default configurations
    overrides: User configurations

Returns:
    Merged configurations

*定義場所: docgen/detector_config_loader.py:74*

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

*定義場所: docgen/detectors/detector_patterns.py:7*

---

### get_package_files

**型**: `method`

**シグネチャ**:
```
def get_package_files(cls, language: str) -> list[str]:
```

**説明**:

Get package manager files for a language.

*定義場所: docgen/detectors/detector_patterns.py:195*

---

### get_source_extensions

**型**: `method`

**シグネチャ**:
```
def get_source_extensions(cls, language: str) -> list[str]:
```

**説明**:

Get source file extensions for a language.

*定義場所: docgen/detectors/detector_patterns.py:200*

---

### detect_by_package_files

**型**: `method`

**シグネチャ**:
```
def detect_by_package_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for package manager files.

*定義場所: docgen/detectors/detector_patterns.py:205*

---

### detect_by_source_files

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files.

*定義場所: docgen/detectors/detector_patterns.py:211*

---

### detect_by_source_files_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_source_files_with_exclusions(cls, project_root: Path, language: str) -> bool:
```

**説明**:

Detect language by checking for source files, excluding common directories.

*定義場所: docgen/detectors/detector_patterns.py:223*

---

### detect_by_extensions_with_exclusions

**型**: `method`

**シグネチャ**:
```
def detect_by_extensions_with_exclusions(cls, project_root: Path, extensions: list[str], max_file_size: int) -> bool:
```

**説明**:

Detect files by extensions, excluding common directories.

Args:
    project_root: プロジェクトルートディレクトリ
    extensions: 検索する拡張子のリスト
    max_file_size: スキップする最大ファイルサイズ（バイト、デフォルト: 10MB）
                  大きなファイルは検出対象外として扱う

*定義場所: docgen/detectors/detector_patterns.py:299*

---

### is_excluded_path

**型**: `method`

**シグネチャ**:
```
def is_excluded_path(cls, path: Path, project_root: Path) -> bool:
```

**説明**:

Check if a path should be excluded from detection.

*定義場所: docgen/detectors/detector_patterns.py:347*

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

*定義場所: docgen/detectors/detector_patterns.py:357*

---

### is_js_config_or_test

**型**: `method`

**シグネチャ**:
```
def is_js_config_or_test(cls, file_path: Path) -> bool:
```

**説明**:

Check if a file is likely a JavaScript config or test file.

*定義場所: docgen/detectors/detector_patterns.py:378*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(cls, project_root: Path | None) -> None:
```

**説明**:

Clear file detection cache.

Args:
    project_root: If provided, clear cache for this project only.
                 If None, clear all caches.

*定義場所: docgen/detectors/detector_patterns.py:384*

---

### set_custom_exclude_dirs

**型**: `method`

**シグネチャ**:
```
def set_custom_exclude_dirs(cls, directories: list[str]) -> None:
```

**説明**:

設定ファイルからのカスタム除外ディレクトリを設定.

Args:
    directories: 除外するディレクトリ名のリスト

*定義場所: docgen/detectors/detector_patterns.py:402*

---

### get_all_exclude_dirs

**型**: `method`

**シグネチャ**:
```
def get_all_exclude_dirs(cls) -> set[str]:
```

**説明**:

デフォルトとカスタムの除外ディレクトリをマージして取得.

Returns:
    除外ディレクトリのセット

*定義場所: docgen/detectors/detector_patterns.py:414*

---

### detect_python_package_manager

**型**: `method`

**シグネチャ**:
```
def detect_python_package_manager(cls, project_root: Path) -> str | None:
```

**説明**:

Detect Python package manager with special handling for pyproject.toml.

*定義場所: docgen/detectors/detector_patterns.py:423*

---


## docgen/detectors/plugin_registry.py

### PluginRegistry

**型**: `class`

**シグネチャ**:
```
class PluginRegistry:
```

**説明**:

カスタムdetectorプラグインのレジストリ

*定義場所: docgen/detectors/plugin_registry.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self):
```

**説明**:

初期化

*定義場所: docgen/detectors/plugin_registry.py:18*

---

### discover_plugins

**型**: `method`

**シグネチャ**:
```
def discover_plugins(self, project_root: Path):
```

**説明**:

プロジェクトのプラグインディレクトリからdetectorを発見

Args:
    project_root: プロジェクトのルートディレクトリ

*定義場所: docgen/detectors/plugin_registry.py:22*

---

### register

**型**: `method`

**シグネチャ**:
```
def register(self, detector_class: type[BaseDetector]):
```

**説明**:

Detectorクラスを登録

Args:
    detector_class: BaseDetectorを継承したクラス

*定義場所: docgen/detectors/plugin_registry.py:44*

---

### get_detector

**型**: `method`

**シグネチャ**:
```
def get_detector(self, language: str, project_root: Path) -> BaseDetector | None:
```

**説明**:

指定された言語のdetectorインスタンスを取得

Args:
    language: 言語名
    project_root: プロジェクトルート

Returns:
    Detectorインスタンスまたは None

*定義場所: docgen/detectors/plugin_registry.py:60*

---

### get_all_languages

**型**: `method`

**シグネチャ**:
```
def get_all_languages(self) -> list[str]:
```

**説明**:

登録されている全ての言語名を取得

Returns:
    言語名のリスト

*定義場所: docgen/detectors/plugin_registry.py:76*

---


## docgen/detectors/unified_detector.py

### UnifiedDetector

**型**: `class`

**シグネチャ**:
```
class UnifiedDetector:
```

**説明**:

パターンベースの統一言語検出クラス

DetectorPatterns で定義されたすべての言語を検出します。

*定義場所: docgen/detectors/unified_detector.py:15*

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
    language: 検出対象の言語名

*定義場所: docgen/detectors/unified_detector.py:21*

---

### detect

**型**: `method`

**シグネチャ**:
```
def detect(self) -> bool:
```

**説明**:

指定された言語が使用されているか検出

Returns:
    検出された場合True

*定義場所: docgen/detectors/unified_detector.py:33*

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

*定義場所: docgen/detectors/unified_detector.py:56*

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

*定義場所: docgen/detectors/unified_detector.py:65*

---

### get_detected_language_object

**型**: `method`

**シグネチャ**:
```
def get_detected_language_object(self) -> DetectedLanguage:
```

**説明**:

検出された言語のオブジェクトを返す

Returns:
    DetectedLanguage オブジェクト

*定義場所: docgen/detectors/unified_detector.py:87*

---

### UnifiedDetectorFactory

**型**: `class`

**シグネチャ**:
```
class UnifiedDetectorFactory:
```

**説明**:

UnifiedDetector のファクトリークラス

サポートされているすべての言語の detector を生成します。

*定義場所: docgen/detectors/unified_detector.py:103*

---

### get_all_languages

**型**: `method`

**シグネチャ**:
```
def get_all_languages(cls) -> list[str]:
```

**説明**:

サポートされているすべての言語を取得

Returns:
    言語名のリスト（よく使われる言語を優先）

*定義場所: docgen/detectors/unified_detector.py:110*

---

### create_detector

**型**: `method`

**シグネチャ**:
```
def create_detector(cls, project_root: Path, language: str) -> UnifiedDetector:
```

**説明**:

指定された言語の detector を作成

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 言語名

Returns:
    UnifiedDetector インスタンス

*定義場所: docgen/detectors/unified_detector.py:136*

---

### create_all_detectors

**型**: `method`

**シグネチャ**:
```
def create_all_detectors(cls, project_root: Path) -> list[UnifiedDetector]:
```

**説明**:

すべての言語の detector を作成

Args:
    project_root: プロジェクトのルートディレクトリ

Returns:
    UnifiedDetector インスタンスのリスト

*定義場所: docgen/detectors/unified_detector.py:150*

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
def detect_languages(self, use_parallel: bool) -> list[DetectedLanguage]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語オブジェクトのリスト

*定義場所: docgen/docgen.py:70*

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

*定義場所: docgen/docgen.py:86*

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

*定義場所: docgen/docgen.py:96*

---

### run_cli

**型**: `function`

**シグネチャ**:
```
def run_cli() -> int:
```

**説明**:

Run the command line interface

Returns:
    Exit code

*定義場所: docgen/docgen.py:152*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

メインエントリーポイント

*定義場所: docgen/docgen.py:177*

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

*定義場所: docgen/document_generator.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, detected_languages: list[DetectedLanguage], config: dict[str, Any], detected_package_managers: dict[str, str] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    detected_languages: 検出された言語リスト
    config: 設定辞書
    detected_package_managers: 検出されたパッケージマネージャ辞書

*定義場所: docgen/document_generator.py:19*

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

*定義場所: docgen/document_generator.py:40*

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

*定義場所: docgen/generator_factory.py:24*

---

### get_available_generators

**型**: `method`

**シグネチャ**:
```
def get_available_generators(cls) -> list[str]:
```

**説明**:

利用可能なジェネレーターのリストを取得

*定義場所: docgen/generator_factory.py:52*

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

*定義場所: docgen/generators/agents_generator.py:20*

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
    **kwargs: BaseGeneratorに渡す追加引数（サービスなど）

*定義場所: docgen/generators/agents_generator.py:23*

---

### agents_path

**型**: `method`

**シグネチャ**:
```
def agents_path(self):
```

*説明なし*

*定義場所: docgen/generators/agents_generator.py:47*

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


## docgen/generators/base_generator.py

### BaseGenerator

**型**: `class`

**シグネチャ**:
```
class BaseGenerator:
```

**説明**:

ベースジェネレータークラス（AGENTS.mdとREADME.mdの共通部分）

DI対応: コンストラクタでサービスを注入可能。

*定義場所: docgen/generators/base_generator.py:23*

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
    llm_service: LLMサービス（DI）
    template_service: テンプレートサービス（DI）
    rag_service: RAGサービス（DI）
    formatting_service: フォーマットサービス（DI）
    manual_section_service: 手動セクションサービス（DI）

*定義場所: docgen/generators/base_generator.py:29*

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
    生成に成功した場合True

*定義場所: docgen/generators/base_generator.py:216*

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

*定義場所: docgen/generators/commit_message_generator.py:16*

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

*定義場所: docgen/generators/commit_message_generator.py:19*

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

*定義場所: docgen/generators/commit_message_generator.py:32*

---


## docgen/generators/contributing_generator.py

### ContributingGenerator

**型**: `class`

**シグネチャ**:
```
class ContributingGenerator:
```

**説明**:

CONTRIBUTING.md generation class

*定義場所: docgen/generators/contributing_generator.py:12*

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

Template Methodパターンにより、解析フローの共通部分を定義します。
サブクラスでは以下の抽象メソッドを実装します：
- `_parse_to_ast`: コンテンツをASTにパース
- `_extract_elements`: ASTからAPI要素を抽出
- `get_supported_extensions`: サポートする拡張子を返す

Attributes:
    PARSER_TYPE: パーサーの種類を示すクラス変数

*定義場所: docgen/generators/parsers/base_parser.py:25*

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

*定義場所: docgen/generators/parsers/base_parser.py:40*

---

### parse_file

**型**: `method`

**シグネチャ**:
```
def parse_file(self, file_path: Path) -> list[APIInfo]:
```

**説明**:

ファイルを解析してAPI情報を抽出 (Template Method)

Args:
    file_path: 解析するファイルのパス

Returns:
    API情報のリスト

*定義場所: docgen/generators/parsers/base_parser.py:49*

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

*定義場所: docgen/generators/parsers/base_parser.py:94*

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

*定義場所: docgen/generators/parsers/base_parser.py:103*

---

### parse_project

**型**: `method`

**シグネチャ**:
```
def parse_project(self, exclude_dirs: list[str] | None, use_parallel: bool, max_workers: int | None, use_cache: bool, cache_manager: 'CacheManager | None', files_to_parse: list[tuple[Path, Path]] | None, skip_cache_save: bool, gitignore_matcher: 'GitIgnoreMatcher | None') -> list[APIInfo]:
```

**説明**:

プロジェクト全体を解析

Args:
    exclude_dirs: 除外するディレクトリ（例: ['.git', 'node_modules']）
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）
    max_workers: 並列処理の最大ワーカー数（Noneの場合は自動）
    use_cache: キャッシュを使用するかどうか（デフォルト: True）
    cache_manager: キャッシュマネージャー（Noneの場合はキャッシュを使用しない）
    files_to_parse: 既にスキャン済みのファイルリスト（Noneの場合は新規スキャン）
    skip_cache_save: キャッシュ保存をスキップするか（デフォルト: False）
    gitignore_matcher: .gitignoreマッチャー（Noneの場合は.gitignoreを適用しない）

Returns:
    全API情報のリスト

*定義場所: docgen/generators/parsers/base_parser.py:112*

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

*定義場所: docgen/generators/parsers/generic_parser.py:16*

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

*定義場所: docgen/generators/parsers/generic_parser.py:36*

---

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す
DetectorPatternsから拡張子を取得して一元管理

Returns:
    言語に応じた拡張子のリスト

*定義場所: docgen/generators/parsers/generic_parser.py:168*

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

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/js_parser.py:212*

---


## docgen/generators/parsers/parser_factory.py

### ParserFactory

**型**: `class`

**シグネチャ**:
```
class ParserFactory:
```

**説明**:

パーサーファクトリークラス

言語名から適切なパーサーを選択して生成します。

*定義場所: docgen/generators/parsers/parser_factory.py:22*

---

### create_parser

**型**: `method`

**シグネチャ**:
```
def create_parser(cls, project_root: Path, language: str) -> BaseParser:
```

**説明**:

指定された言語のパーサーを作成

Args:
    project_root: プロジェクトのルートディレクトリ
    language: 言語名（例: 'python', 'javascript', 'go'）

Returns:
    パーサーインスタンス

Raises:
    ValueError: サポートされていない言語が指定された場合

*定義場所: docgen/generators/parsers/parser_factory.py:36*

---

### create_parsers

**型**: `method`

**シグネチャ**:
```
def create_parsers(cls, project_root: Path, languages: list[str]) -> list[BaseParser]:
```

**説明**:

複数の言語のパーサーを作成

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 言語名のリスト

Returns:
    パーサーインスタンスのリスト

*定義場所: docgen/generators/parsers/parser_factory.py:59*

---

### get_supported_languages

**型**: `method`

**シグネチャ**:
```
def get_supported_languages(cls) -> list[str]:
```

**説明**:

サポートされている言語のリストを取得

Returns:
    言語名のリスト

*定義場所: docgen/generators/parsers/parser_factory.py:85*

---

### is_language_supported

**型**: `method`

**シグネチャ**:
```
def is_language_supported(cls, language: str) -> bool:
```

**説明**:

指定された言語がサポートされているかチェック

Args:
    language: 言語名

Returns:
    サポートされている場合True

*定義場所: docgen/generators/parsers/parser_factory.py:101*

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

### get_supported_extensions

**型**: `method`

**シグネチャ**:
```
def get_supported_extensions(self) -> list[str]:
```

**説明**:

サポートする拡張子を返す

*定義場所: docgen/generators/parsers/python_parser.py:51*

---

### PythonASTVisitor

**型**: `class`

**シグネチャ**:
```
class PythonASTVisitor:
```

**説明**:

Python AST訪問クラス

*定義場所: docgen/generators/parsers/python_parser.py:58*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, file_path: Path, project_root: Path):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:61*

---

### visit_ClassDef

**型**: `method`

**シグネチャ**:
```
def visit_ClassDef(self, node: ast.ClassDef):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:67*

---

### visit_FunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_FunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:90*

---

### visit_AsyncFunctionDef

**型**: `method`

**シグネチャ**:
```
def visit_AsyncFunctionDef(self, node):
```

*説明なし*

*定義場所: docgen/generators/parsers/python_parser.py:93*

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

*定義場所: docgen/generators/readme_generator.py:16*

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
    **kwargs: Additional arguments passed to BaseGenerator (services, etc.)

*定義場所: docgen/generators/readme_generator.py:19*

---

### readme_path

**型**: `method`

**シグネチャ**:
```
def readme_path(self):
```

*説明なし*

*定義場所: docgen/generators/readme_generator.py:47*

---


## docgen/generators/service_factory.py

### GeneratorServiceFactory

**型**: `class`

**シグネチャ**:
```
class GeneratorServiceFactory:
```

**説明**:

ジェネレーターサービスファクトリ

*定義場所: docgen/generators/service_factory.py:20*

---

### create_container

**型**: `method`

**シグネチャ**:
```
def create_container(project_root: Path, config: dict[str, Any], logger: Logger | None) -> ServiceContainer:
```

**説明**:

ServiceContainerを生成して返す

Args:
    project_root: プロジェクトルートディレクトリ
    config: 設定辞書
    logger: ロガー（各サービスに渡される）

Returns:
    ServiceContainerインスタンス

*定義場所: docgen/generators/service_factory.py:24*

---

### create_services

**型**: `method`

**シグネチャ**:
```
def create_services(project_root: Path, config: dict[str, Any], logger: Logger | None) -> dict[str, Any]:
```

**説明**:

全サービスを生成して返す（後方互換性のため）

Args:
    project_root: プロジェクトルートディレクトリ
    config: 設定辞書
    logger: ロガー（各サービスに渡される）

Returns:
    サービスインスタンスの辞書

*定義場所: docgen/generators/service_factory.py:51*

---

### create_llm_service

**型**: `method`

**シグネチャ**:
```
def create_llm_service(config: dict[str, Any], logger: Logger | None) -> LLMService:
```

**説明**:

LLMServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:78*

---

### create_template_service

**型**: `method`

**シグネチャ**:
```
def create_template_service(template_dir: Path | None) -> TemplateService:
```

**説明**:

TemplateServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:83*

---

### create_rag_service

**型**: `method`

**シグネチャ**:
```
def create_rag_service(project_root: Path, config: dict[str, Any], logger: Logger | None) -> RAGService:
```

**説明**:

RAGServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:88*

---

### create_formatting_service

**型**: `method`

**シグネチャ**:
```
def create_formatting_service() -> FormattingService:
```

**説明**:

FormattingServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:95*

---

### create_manual_section_service

**型**: `method`

**シグネチャ**:
```
def create_manual_section_service() -> ManualSectionService:
```

**説明**:

ManualSectionServiceを個別に生成

*定義場所: docgen/generators/service_factory.py:100*

---


## docgen/generators/services/formatting_service.py

### FormattingService

**型**: `class`

**シグネチャ**:
```
class FormattingService:
```

**説明**:

フォーマット・マークダウン処理サービス

*定義場所: docgen/generators/services/formatting_service.py:15*

---

### format_languages

**型**: `method`

**シグネチャ**:
```
def format_languages(self, languages: list[str]) -> str:
```

**説明**:

言語リストをフォーマット

Args:
    languages: 言語のリスト

Returns:
    フォーマットされた言語リスト

*定義場所: docgen/generators/services/formatting_service.py:36*

---

### format_commands

**型**: `method`

**シグネチャ**:
```
def format_commands(self, commands: list[str] | None) -> str:
```

**説明**:

コマンドリストをフォーマット

Args:
    commands: コマンドのリスト

Returns:
    フォーマットされたコマンド

*定義場所: docgen/generators/services/formatting_service.py:55*

---

### format_project_structure

**型**: `method`

**シグネチャ**:
```
def format_project_structure(self, structure: dict | None) -> str:
```

**説明**:

プロジェクト構造をツリー形式でフォーマット

Args:
    structure: プロジェクト構造の辞書

Returns:
    フォーマットされたプロジェクト構造

*定義場所: docgen/generators/services/formatting_service.py:69*

---

### clean_llm_output

**型**: `method`

**シグネチャ**:
```
def clean_llm_output(self, content: str) -> str:
```

**説明**:

LLMの出力をクリーニング

Args:
    content: LLM出力

Returns:
    クリーニングされたコンテンツ

*定義場所: docgen/generators/services/formatting_service.py:114*

---

### validate_output

**型**: `method`

**シグネチャ**:
```
def validate_output(self, content: str) -> bool:
```

**説明**:

生成されたコンテンツを検証

Args:
    content: 生成されたコンテンツ

Returns:
    検証に成功した場合True

*定義場所: docgen/generators/services/formatting_service.py:134*

---

### generate_footer

**型**: `method`

**シグネチャ**:
```
def generate_footer(self, document_type: str) -> str:
```

**説明**:

フッターを生成

Args:
    document_type: ドキュメントタイプ

Returns:
    フッター文字列

*定義場所: docgen/generators/services/formatting_service.py:150*

---

### extract_description_section

**型**: `method`

**シグネチャ**:
```
def extract_description_section(self, content: str) -> str:
```

**説明**:

コンテンツから説明セクションを抽出

Args:
    content: ドキュメントコンテンツ

Returns:
    説明セクションのテキスト

*定義場所: docgen/generators/services/formatting_service.py:162*

---


## docgen/generators/services/llm_service.py

### LLMService

**型**: `class`

**シグネチャ**:
```
class LLMService:
```

**説明**:

LLM生成サービス

*定義場所: docgen/generators/services/llm_service.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any], logger: Logger | None):
```

**説明**:

初期化

Args:
    config: 設定辞書（agents設定を含む）
    logger: ロガー

*定義場所: docgen/generators/services/llm_service.py:18*

---

### agents_config

**型**: `method`

**シグネチャ**:
```
def agents_config(self) -> dict[str, Any]:
```

**説明**:

agents設定を取得

*定義場所: docgen/generators/services/llm_service.py:35*

---

### get_client

**型**: `method`

**シグネチャ**:
```
def get_client(self) -> Any:
```

**説明**:

LLMクライアントを取得（フォールバック付き）

Returns:
    LLMクライアント（取得できない場合はNone）

*定義場所: docgen/generators/services/llm_service.py:39*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str) -> str:
```

**説明**:

LLMを使用してテキストを生成

Args:
    prompt: 入力プロンプト

Returns:
    生成されたテキスト

Raises:
    RuntimeError: LLMクライアントが利用できない場合

*定義場所: docgen/generators/services/llm_service.py:57*

---

### should_use_outlines

**型**: `method`

**シグネチャ**:
```
def should_use_outlines(self) -> bool:
```

**説明**:

Outlinesを使用するかどうかを判定

Returns:
    Outlinesを使用するかどうか

*定義場所: docgen/generators/services/llm_service.py:76*

---

### create_outlines_model

**型**: `method`

**シグネチャ**:
```
def create_outlines_model(self, client: Any) -> Any:
```

**説明**:

Outlinesモデルを作成

Args:
    client: LLMクライアント

Returns:
    Outlinesモデル（サポートされない場合はNone）

*定義場所: docgen/generators/services/llm_service.py:87*

---

### format_project_info

**型**: `method`

**シグネチャ**:
```
def format_project_info(self, project_info: Any, languages: list[str], package_managers: dict[str, str] | None) -> str:
```

**説明**:

プロジェクト情報をプロンプト用に整形

Args:
    project_info: プロジェクト情報
    languages: 言語リスト
    package_managers: パッケージマネージャ辞書

Returns:
    整形された文字列

*定義場所: docgen/generators/services/llm_service.py:101*

---

### generate_content

**型**: `method`

**シグネチャ**:
```
def generate_content(self, prompt_file: str, prompt_name: str, project_info_str: str, rag_context: str) -> str:
```

**説明**:

LLMを使用して特定のコンテンツを生成

Args:
    prompt_file: プロンプトファイル名
    prompt_name: プロンプト名
    project_info_str: 整形済みプロジェクト情報
    rag_context: RAGコンテキスト

Returns:
    生成されたコンテンツ

*定義場所: docgen/generators/services/llm_service.py:146*

---


## docgen/generators/services/manual_section_service.py

### ManualSectionService

**型**: `class`

**シグネチャ**:
```
class ManualSectionService:
```

**説明**:

手動セクション管理サービス

*定義場所: docgen/generators/services/manual_section_service.py:11*

---

### extract

**型**: `method`

**シグネチャ**:
```
def extract(self, content: str) -> dict[str, str]:
```

**説明**:

既存のコンテンツから手動セクションを抽出

Args:
    content: 既存のドキュメントコンテンツ

Returns:
    セクションIDとコンテンツの辞書

*定義場所: docgen/generators/services/manual_section_service.py:14*

---

### merge

**型**: `method`

**シグネチャ**:
```
def merge(self, generated_content: str, manual_sections: dict[str, str]) -> str:
```

**説明**:

生成されたコンテンツに手動セクションをマージ

Args:
    generated_content: 自動生成されたコンテンツ
    manual_sections: 抽出された手動セクションの辞書

Returns:
    マージされたコンテンツ

*定義場所: docgen/generators/services/manual_section_service.py:53*

---


## docgen/generators/services/rag_service.py

### RAGService

**型**: `class`

**シグネチャ**:
```
class RAGService:
```

**説明**:

RAGコンテキスト取得サービス

*定義場所: docgen/generators/services/rag_service.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, config: dict[str, Any], logger: Logger | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートディレクトリ
    config: 設定辞書
    logger: ロガー

*定義場所: docgen/generators/services/rag_service.py:18*

---

### is_enabled

**型**: `method`

**シグネチャ**:
```
def is_enabled(self) -> bool:
```

**説明**:

RAGが有効かどうか

*定義場所: docgen/generators/services/rag_service.py:37*

---

### build_enhanced_query

**型**: `method`

**シグネチャ**:
```
def build_enhanced_query(self, prompt_name: str, project_name: str, languages: list[str] | None, project_info: dict[str, Any] | None) -> str:
```

**説明**:

プロジェクト情報を含む詳細なクエリを生成

Args:
    prompt_name: プロンプト名（例: "project overview", "key_features"）
    project_name: プロジェクト名
    languages: 検出された言語のリスト
    project_info: プロジェクト情報の辞書（オプション）

Returns:
    改善されたクエリ文字列

*定義場所: docgen/generators/services/rag_service.py:41*

---

### get_context_with_multi_query

**型**: `method`

**シグネチャ**:
```
def get_context_with_multi_query(self, base_query: str, project_name: str, languages: list[str] | None, project_info: dict[str, Any] | None, top_k: int | None) -> str:
```

**説明**:

マルチクエリ検索を使用してRAGコンテキストを取得

Args:
    base_query: ベースクエリ
    project_name: プロジェクト名
    languages: 検出された言語のリスト
    project_info: プロジェクト情報の辞書
    top_k: 取得するチャンク数

Returns:
    フォーマット済みのコンテキスト文字列

*定義場所: docgen/generators/services/rag_service.py:140*

---

### get_context

**型**: `method`

**シグネチャ**:
```
def get_context(self, query: str, top_k: int | None, use_enhanced_query: bool, project_name: str | None, languages: list[str] | None, project_info: dict[str, Any] | None) -> str:
```

**説明**:

RAGコンテキストを取得してフォーマット

Args:
    query: 検索クエリ
    top_k: 取得するチャンク数（Noneの場合は設定ファイルから読み取る）
    use_enhanced_query: 改善されたクエリを使用するかどうか
    project_name: プロジェクト名（改善されたクエリを使用する場合）
    languages: 検出された言語のリスト（改善されたクエリを使用する場合）
    project_info: プロジェクト情報の辞書（改善されたクエリを使用する場合）

Returns:
    フォーマット済みのコンテキスト文字列（RAG無効時は空文字列）

*定義場所: docgen/generators/services/rag_service.py:240*

---


## docgen/generators/services/service_container.py

### ServiceContainer

**型**: `class`

**シグネチャ**:
```
class ServiceContainer:
```

**説明**:

サービスコンテナ

全てのジェネレーター用サービスを一箇所に集約し、
依存関係を明示的に管理します。

Attributes:
    llm_service: LLM連携サービス
    template_service: テンプレートレンダリングサービス
    formatting_service: テキスト整形サービス
    manual_section_service: 手動セクション管理サービス
    rag_service: RAGコンテキスト取得サービス（オプショナル）

*定義場所: docgen/generators/services/service_container.py:18*

---

### __post_init__

**型**: `method`

**シグネチャ**:
```
def __post_init__(self):
```

**説明**:

初期化後の検証

*定義場所: docgen/generators/services/service_container.py:38*

---


## docgen/generators/services/template_service.py

### TemplateService

**型**: `class`

**シグネチャ**:
```
class TemplateService:
```

**説明**:

テンプレートレンダリングサービス

*定義場所: docgen/generators/services/template_service.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, template_dir: Path | None):
```

**説明**:

初期化

Args:
    template_dir: テンプレートディレクトリのパス（Noneの場合は自動検出）

*定義場所: docgen/generators/services/template_service.py:17*

---

### render

**型**: `method`

**シグネチャ**:
```
def render(self, template_name: str, context: dict[str, Any]) -> str:
```

**説明**:

テンプレートをレンダリング

Args:
    template_name: テンプレートファイル名
    context: テンプレート変数

Returns:
    レンダリングされた文字列

*定義場所: docgen/generators/services/template_service.py:47*

---

### format_commands

**型**: `method`

**シグネチャ**:
```
def format_commands(self, commands: list[str]) -> str:
```

**説明**:

コマンドリストをマークダウンのコードブロックとしてフォーマット

Args:
    commands: コマンドのリスト

Returns:
    フォーマットされたマークダウン文字列

*定義場所: docgen/generators/services/template_service.py:62*

---

### format_custom_instructions

**型**: `method`

**シグネチャ**:
```
def format_custom_instructions(self, custom_instructions: str | dict[str, Any]) -> list[str]:
```

**説明**:

カスタム指示セクションを生成

Args:
    custom_instructions: カスタム指示の内容（文字列または辞書）

Returns:
    生成された行のリスト

*定義場所: docgen/generators/services/template_service.py:82*

---


## docgen/hooks/config.py

### TaskConfig

**型**: `class`

**シグネチャ**:
```
class TaskConfig:
```

**説明**:

タスク設定

*定義場所: docgen/hooks/config.py:20*

---

### HookConfig

**型**: `class`

**シグネチャ**:
```
class HookConfig:
```

**説明**:

フック設定

*定義場所: docgen/hooks/config.py:31*

---

### ConfigLoader

**型**: `class`

**シグネチャ**:
```
class ConfigLoader:
```

**説明**:

フック設定ローダー

*定義場所: docgen/hooks/config.py:39*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: str):
```

*説明なし*

*定義場所: docgen/hooks/config.py:42*

---

### load_config

**型**: `method`

**シグネチャ**:
```
def load_config(self) -> dict[str, HookConfig]:
```

**説明**:

設定を読み込む

*定義場所: docgen/hooks/config.py:47*

---


## docgen/hooks/orchestrator.py

### HookOrchestrator

**型**: `class`

**シグネチャ**:
```
class HookOrchestrator:
```

**説明**:

Git hook実行のオーケストレーター

*定義場所: docgen/hooks/orchestrator.py:19*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, hook_name: str, args: list[str]):
```

*説明なし*

*定義場所: docgen/hooks/orchestrator.py:22*

---

### register_task

**型**: `method`

**シグネチャ**:
```
def register_task(self, name: str, task_class: type):
```

**説明**:

タスクを登録する

*定義場所: docgen/hooks/orchestrator.py:40*

---

### run_async

**型**: `method`

**シグネチャ**:
```
async def run_async(self) -> int:
```

**説明**:

フックを非同期実行する

*定義場所: docgen/hooks/orchestrator.py:44*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self) -> int:
```

**説明**:

同期実行ラッパー

*定義場所: docgen/hooks/orchestrator.py:122*

---

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

**説明**:

エントリーポイント

*定義場所: docgen/hooks/orchestrator.py:127*

---


## docgen/hooks/registry.py

### TaskRegistry

**型**: `class`

**シグネチャ**:
```
class TaskRegistry:
```

**説明**:

フックタスクのレジストリ

*定義場所: docgen/hooks/registry.py:4*

---

### register

**型**: `method`

**シグネチャ**:
```
def register(cls, name: str):
```

**説明**:

タスクを登録するデコレータ

*定義場所: docgen/hooks/registry.py:10*

---

### get_task

**型**: `method`

**シグネチャ**:
```
def get_task(cls, name: str) -> type[HookTask] | None:
```

**説明**:

タスククラスを取得

*定義場所: docgen/hooks/registry.py:20*

---

### get_all_tasks

**型**: `method`

**シグネチャ**:
```
def get_all_tasks(cls) -> dict[str, type[HookTask]]:
```

**説明**:

全タスクを取得

*定義場所: docgen/hooks/registry.py:25*

---


## docgen/hooks/tasks/base.py

### TaskStatus

**型**: `class`

**シグネチャ**:
```
class TaskStatus:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:9*

---

### TaskResult

**型**: `class`

**シグネチャ**:
```
class TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:16*

---

### HookContext

**型**: `class`

**シグネチャ**:
```
class HookContext:
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:23*

---

### HookTask

**型**: `class`

**シグネチャ**:
```
class HookTask:
```

**説明**:

フックタスクの基底クラス

*定義場所: docgen/hooks/tasks/base.py:29*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: TaskConfig):
```

*説明なし*

*定義場所: docgen/hooks/tasks/base.py:32*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

**説明**:

タスクを実行

*定義場所: docgen/hooks/tasks/base.py:36*

---

### should_run

**型**: `method`

**シグネチャ**:
```
def should_run(self, context: HookContext) -> bool:
```

**説明**:

タスクを実行すべきか判定

*定義場所: docgen/hooks/tasks/base.py:40*

---

### run_async

**型**: `method`

**シグネチャ**:
```
async def run_async(self, context: HookContext) -> TaskResult:
```

**説明**:

タスクを非同期実行（デフォルトは同期実行をラップ）

*定義場所: docgen/hooks/tasks/base.py:44*

---


## docgen/hooks/tasks/commit_msg_generator.py

### CommitMsgGeneratorTask

**型**: `class`

**シグネチャ**:
```
class CommitMsgGeneratorTask:
```

**説明**:

コミットメッセージ生成タスク

*定義場所: docgen/hooks/tasks/commit_msg_generator.py:9*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/commit_msg_generator.py:12*

---


## docgen/hooks/tasks/doc_generator.py

### DocGeneratorTask

**型**: `class`

**シグネチャ**:
```
class DocGeneratorTask:
```

**説明**:

ドキュメント生成タスク

*定義場所: docgen/hooks/tasks/doc_generator.py:7*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/doc_generator.py:10*

---


## docgen/hooks/tasks/file_stager.py

### FileStagerTask

**型**: `class`

**シグネチャ**:
```
class FileStagerTask:
```

**説明**:

ファイルステージングタスク

*定義場所: docgen/hooks/tasks/file_stager.py:9*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/file_stager.py:12*

---


## docgen/hooks/tasks/rag_generator.py

### RagGeneratorTask

**型**: `class`

**シグネチャ**:
```
class RagGeneratorTask:
```

**説明**:

RAG生成タスク

*定義場所: docgen/hooks/tasks/rag_generator.py:7*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/rag_generator.py:10*

---


## docgen/hooks/tasks/version_checker.py

### VersionCheckerTask

**型**: `class`

**シグネチャ**:
```
class VersionCheckerTask:
```

**説明**:

バージョンチェック＆リリースタグ作成タスク

*定義場所: docgen/hooks/tasks/version_checker.py:10*

---

### run

**型**: `method`

**シグネチャ**:
```
def run(self, context: HookContext) -> TaskResult:
```

*説明なし*

*定義場所: docgen/hooks/tasks/version_checker.py:13*

---


## docgen/hooks/utils.py

### get_python_command

**型**: `function`

**シグネチャ**:
```
def get_python_command() -> str:
```

**説明**:

利用可能なPythonコマンドを取得する（uv優先）

*定義場所: docgen/hooks/utils.py:4*

---

### run_command

**型**: `function`

**シグネチャ**:
```
def run_command(command: list[str], cwd: str | None, capture_output: bool) -> tuple[int, str, str]:
```

**説明**:

コマンドを実行する

*定義場所: docgen/hooks/utils.py:23*

---

### get_changed_files

**型**: `function`

**シグネチャ**:
```
def get_changed_files(staged: bool) -> list[str]:
```

**説明**:

変更されたファイルを取得する

*定義場所: docgen/hooks/utils.py:36*

---

### is_git_repo

**型**: `function`

**シグネチャ**:
```
def is_git_repo(path: str) -> bool:
```

**説明**:

Gitリポジトリか確認する

*定義場所: docgen/hooks/utils.py:49*

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
def __init__(self, project_root: Path, config_manager):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートパス
    config_manager: 設定マネージャー（Noneの場合は新規作成）

*定義場所: docgen/language_detector.py:20*

---

### detect_languages

**型**: `method`

**シグネチャ**:
```
def detect_languages(self, use_parallel: bool) -> list[DetectedLanguage]:
```

**説明**:

プロジェクトの使用言語を自動検出

Args:
    use_parallel: 並列処理を使用するかどうか（デフォルト: True）

Returns:
    検出された言語オブジェクトのリスト

*定義場所: docgen/language_detector.py:73*

---

### get_detected_languages

**型**: `method`

**シグネチャ**:
```
def get_detected_languages(self) -> list[str]:
```

**説明**:

検出された言語名のリストを取得（後方互換性用）

*定義場所: docgen/language_detector.py:213*

---

### get_detected_language_objects

**型**: `method`

**シグネチャ**:
```
def get_detected_language_objects(self) -> list[DetectedLanguage]:
```

**説明**:

検出された言語オブジェクトのリストを取得

*定義場所: docgen/language_detector.py:217*

---

### get_detected_package_managers

**型**: `method`

**シグネチャ**:
```
def get_detected_package_managers(self) -> dict[str, str]:
```

**説明**:

検出されたパッケージマネージャを取得

*定義場所: docgen/language_detector.py:221*

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

*定義場所: docgen/models/agents.py:10*

---

### ProjectOverview

**型**: `class`

**シグネチャ**:
```
class ProjectOverview:
```

**説明**:

Project overview model.

*定義場所: docgen/models/agents.py:28*

---

### LLMSetup

**型**: `class`

**シグネチャ**:
```
class LLMSetup:
```

**説明**:

LLM setup model.

*定義場所: docgen/models/agents.py:36*

---

### SetupInstructions

**型**: `class`

**シグネチャ**:
```
class SetupInstructions:
```

**説明**:

Setup instructions model.

*定義場所: docgen/models/agents.py:43*

---

### BuildTestInstructions

**型**: `class`

**シグネチャ**:
```
class BuildTestInstructions:
```

**説明**:

Build and test instructions model.

*定義場所: docgen/models/agents.py:51*

---

### CodingStandards

**型**: `class`

**シグネチャ**:
```
class CodingStandards:
```

**説明**:

Coding standards model.

*定義場所: docgen/models/agents.py:59*

---

### PRGuidelines

**型**: `class`

**シグネチャ**:
```
class PRGuidelines:
```

**説明**:

PR guidelines model.

*定義場所: docgen/models/agents.py:66*

---

### AgentsConfig

**型**: `class`

**シグネチャ**:
```
class AgentsConfig:
```

**説明**:

Configuration model for agents documentation.

*定義場所: docgen/models/agents.py:74*

---

### AgentsGenerationConfig

**型**: `class`

**シグネチャ**:
```
class AgentsGenerationConfig:
```

**説明**:

Agents generation configuration model.

*定義場所: docgen/models/agents.py:91*

---

### AgentsConfigSection

**型**: `class`

**シグネチャ**:
```
class AgentsConfigSection:
```

**説明**:

Agents configuration section model.

*定義場所: docgen/models/agents.py:99*

---

### AgentsDocument

**型**: `class`

**シグネチャ**:
```
class AgentsDocument:
```

**説明**:

AGENTS.mdドキュメントの構造化データモデル

*定義場所: docgen/models/agents.py:112*

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


## docgen/models/base.py

### DocgenBaseModel

**型**: `class`

**シグネチャ**:
```
class DocgenBaseModel:
```

**説明**:

Base model for all docgen models.

Provides common configuration and methods for all Pydantic models
used throughout the docgen system.

Features:
- Extra fields forbidden to catch typos
- Assignment validation enabled
- Enum values automatically used
- Template context conversion method

*定義場所: docgen/models/base.py:8*

---

### to_template_context

**型**: `method`

**シグネチャ**:
```
def to_template_context(self) -> dict[str, Any]:
```

**説明**:

Convert model to template rendering context.

Returns:
    Dictionary suitable for Jinja2 template rendering.

*定義場所: docgen/models/base.py:27*

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

### GeneralConfig

**型**: `class`

**シグネチャ**:
```
class GeneralConfig:
```

**説明**:

General configuration model.

*定義場所: docgen/models/config.py:11*

---

### MessagesConfig

**型**: `class`

**シグネチャ**:
```
class MessagesConfig:
```

**説明**:

Messages configuration model.

*定義場所: docgen/models/config.py:17*

---

### TechnicalKeywordsConfig

**型**: `class`

**シグネチャ**:
```
class TechnicalKeywordsConfig:
```

**説明**:

Technical keywords configuration model.

*定義場所: docgen/models/config.py:23*

---

### ValidatorConfig

**型**: `class`

**シグネチャ**:
```
class ValidatorConfig:
```

**説明**:

Validator configuration model.

*定義場所: docgen/models/config.py:54*

---

### ImplementationValidationConfig

**型**: `class`

**シグネチャ**:
```
class ImplementationValidationConfig:
```

**説明**:

Implementation validation configuration model.

*定義場所: docgen/models/config.py:60*

---

### ValidationConfig

**型**: `class`

**シグネチャ**:
```
class ValidationConfig:
```

**説明**:

Validation configuration model.

*定義場所: docgen/models/config.py:69*

---

### LanguagesConfig

**型**: `class`

**シグネチャ**:
```
class LanguagesConfig:
```

**説明**:

Languages configuration model.

*定義場所: docgen/models/config.py:82*

---

### OutputConfig

**型**: `class`

**シグネチャ**:
```
class OutputConfig:
```

**説明**:

Output configuration model.

*定義場所: docgen/models/config.py:90*

---

### GenerationConfig

**型**: `class`

**シグネチャ**:
```
class GenerationConfig:
```

**説明**:

Generation configuration model.

*定義場所: docgen/models/config.py:98*

---

### ExcludeConfig

**型**: `class`

**シグネチャ**:
```
class ExcludeConfig:
```

**説明**:

Exclude configuration model.

*定義場所: docgen/models/config.py:107*

---

### CacheConfig

**型**: `class`

**シグネチャ**:
```
class CacheConfig:
```

**説明**:

Cache configuration model.

*定義場所: docgen/models/config.py:115*

---

### BenchmarkConfig

**型**: `class`

**シグネチャ**:
```
class BenchmarkConfig:
```

**説明**:

Benchmark configuration model.

*定義場所: docgen/models/config.py:121*

---

### DebugConfig

**型**: `class`

**シグネチャ**:
```
class DebugConfig:
```

**説明**:

Debug configuration model.

*定義場所: docgen/models/config.py:127*

---

### EmbeddingConfig

**型**: `class`

**シグネチャ**:
```
class EmbeddingConfig:
```

**説明**:

Embedding configuration model.

*定義場所: docgen/models/config.py:133*

---

### IndexConfig

**型**: `class`

**シグネチャ**:
```
class IndexConfig:
```

**説明**:

Index configuration model.

*定義場所: docgen/models/config.py:140*

---

### RetrievalConfig

**型**: `class`

**シグネチャ**:
```
class RetrievalConfig:
```

**説明**:

Retrieval configuration model.

*定義場所: docgen/models/config.py:148*

---

### ChunkingConfig

**型**: `class`

**シグネチャ**:
```
class ChunkingConfig:
```

**説明**:

Chunking configuration model.

*定義場所: docgen/models/config.py:156*

---

### RagExcludeConfig

**型**: `class`

**シグネチャ**:
```
class RagExcludeConfig:
```

*説明なし*

*定義場所: docgen/models/config.py:163*

---

### RagConfig

**型**: `class`

**シグネチャ**:
```
class RagConfig:
```

**説明**:

RAG configuration model.

*定義場所: docgen/models/config.py:175*

---

### ArchitecturePythonConfig

**型**: `class`

**シグネチャ**:
```
class ArchitecturePythonConfig:
```

**説明**:

Python architecture configuration.

*定義場所: docgen/models/config.py:187*

---

### ArchitectureJavascriptConfig

**型**: `class`

**シグネチャ**:
```
class ArchitectureJavascriptConfig:
```

**説明**:

JavaScript architecture configuration.

*定義場所: docgen/models/config.py:194*

---

### ArchitectureConfig

**型**: `class`

**シグネチャ**:
```
class ArchitectureConfig:
```

**説明**:

Architecture diagram generation configuration.

*定義場所: docgen/models/config.py:200*

---

### DocgenConfig

**型**: `class`

**シグネチャ**:
```
class DocgenConfig:
```

**説明**:

Main configuration model for docgen.

*定義場所: docgen/models/config.py:211*

---


## docgen/models/detected_language.py

### DetectedLanguage

**型**: `class`

**シグネチャ**:
```
class DetectedLanguage:
```

**説明**:

検出された言語の詳細情報を保持するクラス

Attributes:
    name: 言語名 (例: 'python', 'javascript')
    version: 検出されたバージョン (例: '3.11', '18.0.0')
    package_manager: 使用されているパッケージマネージャ (例: 'poetry', 'npm')
    source_extensions: ソースコードの拡張子リスト (例: ['.py', '.pyi'])
    rag_enabled: RAGインデックスに含めるかどうか
    doc_config: ドキュメント生成に関する設定

*定義場所: docgen/models/detected_language.py:6*

---

### get_rag_patterns

**型**: `method`

**シグネチャ**:
```
def get_rag_patterns(self) -> list[str]:
```

**説明**:

RAGインデックスに含めるためのglobパターンリストを取得

*定義場所: docgen/models/detected_language.py:27*

---


## docgen/models/detector.py

### PackageManagerRule

**型**: `class`

**シグネチャ**:
```
class PackageManagerRule:
```

**説明**:

Package manager detection rule.

*定義場所: docgen/models/detector.py:9*

---

### validate_files

**型**: `method`

**シグネチャ**:
```
def validate_files(cls, v: tuple[str, ...]) -> tuple[str, ...]:
```

*説明なし*

*定義場所: docgen/models/detector.py:21*

---

### validate_manager

**型**: `method`

**シグネチャ**:
```
def validate_manager(cls, v: str) -> str:
```

*説明なし*

*定義場所: docgen/models/detector.py:28*

---

### LanguageConfig

**型**: `class`

**シグネチャ**:
```
class LanguageConfig:
```

**説明**:

Language detection configuration.

*定義場所: docgen/models/detector.py:34*

---

### validate_name

**型**: `method`

**シグネチャ**:
```
def validate_name(cls, v: str) -> str:
```

*説明なし*

*定義場所: docgen/models/detector.py:54*

---

### get_sorted_package_manager_rules

**型**: `method`

**シグネチャ**:
```
def get_sorted_package_manager_rules(self) -> list[PackageManagerRule]:
```

**説明**:

Return package manager rules sorted by priority.

*定義場所: docgen/models/detector.py:59*

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

*定義場所: docgen/models/project.py:10*

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

*定義場所: docgen/models/readme.py:8*

---

### ReadmeSetupInstructions

**型**: `class`

**シグネチャ**:
```
class ReadmeSetupInstructions:
```

**説明**:

Setup instructions for README.

*定義場所: docgen/models/readme.py:16*

---

### ReadmeConfig

**型**: `class`

**シグネチャ**:
```
class ReadmeConfig:
```

**説明**:

Configuration model for README documentation.

*定義場所: docgen/models/readme.py:23*

---

### ReadmeDocument

**型**: `class`

**シグネチャ**:
```
class ReadmeDocument:
```

**説明**:

READMEドキュメントの構造化データモデル

*定義場所: docgen/models/readme.py:42*

---


## docgen/rag/chunker.py

### CodeChunker

**型**: `class`

**シグネチャ**:
```
class CodeChunker:
```

**説明**:

コードベースをチャンク化するクラス

*定義場所: docgen/rag/chunker.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | None):
```

**説明**:

初期化

Args:
    config: RAG設定（config.toml の rag セクション）

*定義場所: docgen/rag/chunker.py:48*

---

### should_process_file

**型**: `method`

**シグネチャ**:
```
def should_process_file(self, file_path: Path) -> bool:
```

**説明**:

ファイルを処理すべきかどうかを判定

Args:
    file_path: ファイルパス

Returns:
    処理すべき場合True

*定義場所: docgen/rag/chunker.py:74*

---

### chunk_file

**型**: `method`

**シグネチャ**:
```
def chunk_file(self, file_path: Path, project_root: Path) -> list[dict[str, Any]]:
```

**説明**:

ファイルをチャンク化

Args:
    file_path: ファイルパス
    project_root: プロジェクトルート

Returns:
    チャンクのリスト

*定義場所: docgen/rag/chunker.py:148*

---

### chunk_codebase

**型**: `method`

**シグネチャ**:
```
def chunk_codebase(self, project_root: Path, allowed_patterns: list[str] | None) -> list[dict[str, Any]]:
```

**説明**:

プロジェクト全体をチャンク化

Args:
    project_root: プロジェクトルート
    allowed_patterns: 許可するファイルパターンのリスト（Noneの場合はすべて許可/設定依存）

Returns:
    すべてのチャンクのリスト

*定義場所: docgen/rag/chunker.py:194*

---


## docgen/rag/embedder.py

### Embedder

**型**: `class`

**シグネチャ**:
```
class Embedder:
```

**説明**:

テキスト埋め込み生成クラス

*定義場所: docgen/rag/embedder.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any] | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    config: RAG設定（config.toml の rag セクション）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/embedder.py:19*

---

### model

**型**: `method`

**シグネチャ**:
```
def model(self):
```

**説明**:

埋め込みモデルをLazy load

*定義場所: docgen/rag/embedder.py:40*

---

### embedding_dim

**型**: `method`

**シグネチャ**:
```
def embedding_dim(self) -> int:
```

**説明**:

埋め込みベクトルの次元数

*定義場所: docgen/rag/embedder.py:58*

---

### embed_text

**型**: `method`

**シグネチャ**:
```
def embed_text(self, text: str) -> np.ndarray:
```

**説明**:

テキストを埋め込みベクトルに変換

Args:
    text: 入力テキスト

Returns:
    埋め込みベクトル（numpy配列）

*定義場所: docgen/rag/embedder.py:62*

---

### embed_batch

**型**: `method`

**シグネチャ**:
```
def embed_batch(self, texts: list[str], batch_size: int) -> np.ndarray:
```

**説明**:

複数のテキストをバッチ処理で埋め込み（キャッシュ対応）

Args:
    texts: 入力テキストのリスト
    batch_size: バッチサイズ

Returns:
    埋め込みベクトルの配列（shape: [len(texts), embedding_dim]）

*定義場所: docgen/rag/embedder.py:88*

---


## docgen/rag/indexer.py

### VectorIndexer

**型**: `class`

**シグネチャ**:
```
class VectorIndexer:
```

**説明**:

ベクトルインデックス管理クラス

*定義場所: docgen/rag/indexer.py:16*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, index_dir: Path, embedding_dim: int, config: dict[str, Any] | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    index_dir: インデックス保存ディレクトリ
    embedding_dim: 埋め込みベクトルの次元数
    config: RAG設定（config.toml の rag セクション）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/indexer.py:19*

---

### build

**型**: `method`

**シグネチャ**:
```
def build(self, embeddings: np.ndarray, metadata: list[dict[str, Any]]):
```

**説明**:

インデックスを構築

Args:
    embeddings: 埋め込みベクトルの配列（shape: [n_samples, embedding_dim]）
    metadata: 各埋め込みに対応するメタデータのリスト

*定義場所: docgen/rag/indexer.py:50*

---

### save

**型**: `method`

**シグネチャ**:
```
def save(self):
```

**説明**:

インデックスとメタデータを保存

*定義場所: docgen/rag/indexer.py:101*

---

### load

**型**: `method`

**シグネチャ**:
```
def load(self):
```

**説明**:

インデックスとメタデータを読み込み

*定義場所: docgen/rag/indexer.py:130*

---

### search

**型**: `method`

**シグネチャ**:
```
def search(self, query_embedding: np.ndarray, k: int) -> list[tuple[dict[str, Any], float]]:
```

**説明**:

類似ベクトルを検索

Args:
    query_embedding: クエリの埋め込みベクトル
    k: 取得する件数

Returns:
    (メタデータ, スコア) のタプルのリスト

*定義場所: docgen/rag/indexer.py:169*

---

### incremental_update

**型**: `method`

**シグネチャ**:
```
def incremental_update(self, new_embeddings: np.ndarray, new_metadata: list[dict[str, Any]]):
```

**説明**:

インデックスに新しいデータを追加（増分更新）

Args:
    new_embeddings: 新しい埋め込みベクトル
    new_metadata: 新しいメタデータ

*定義場所: docgen/rag/indexer.py:199*

---


## docgen/rag/retriever.py

### DocumentRetriever

**型**: `class`

**シグネチャ**:
```
class DocumentRetriever:
```

**説明**:

ドキュメント検索クラス

*定義場所: docgen/rag/retriever.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any], project_root: Path | None, logger: Logger | None):
```

**説明**:

初期化

Args:
    config: 設定辞書（config.toml全体）
    project_root: プロジェクトルート（指定しない場合は現在のディレクトリ）
    logger: ロガーインスタンス（Noneの場合は新規作成）

*定義場所: docgen/rag/retriever.py:18*

---

### embedder

**型**: `method`

**シグネチャ**:
```
def embedder(self) -> Embedder:
```

**説明**:

Embedderインスタンスを取得（Lazy loading）

*定義場所: docgen/rag/retriever.py:51*

---

### indexer

**型**: `method`

**シグネチャ**:
```
def indexer(self) -> VectorIndexer:
```

**説明**:

VectorIndexerインスタンスを取得（Lazy loading）

*定義場所: docgen/rag/retriever.py:58*

---

### retrieve

**型**: `method`

**シグネチャ**:
```
def retrieve(self, query: str, top_k: int | None) -> list[dict[str, Any]]:
```

**説明**:

クエリに類似するチャンクを検索

Args:
    query: 検索クエリ
    top_k: 取得する件数（Noneの場合はデフォルト値）

Returns:
    チャンクのリスト（スコア付き）

*定義場所: docgen/rag/retriever.py:84*

---

### format_context

**型**: `method`

**シグネチャ**:
```
def format_context(self, chunks: list[dict[str, Any]]) -> str:
```

**説明**:

チャンクをコンテキスト文字列にフォーマット

Args:
    chunks: チャンクのリスト

Returns:
    フォーマット済みのコンテキスト文字列

*定義場所: docgen/rag/retriever.py:184*

---

### retrieve_with_rerank

**型**: `method`

**シグネチャ**:
```
def retrieve_with_rerank(self, query: str, top_k: int, rerank_k: int) -> list[dict[str, Any]]:
```

**説明**:

再ランキング付き検索（将来の拡張用）

Args:
    query: 検索クエリ
    top_k: 最終的に取得する件数
    rerank_k: 初期検索で取得する件数（再ランク対象）

Returns:
    再ランク済みのチャンクのリスト

*定義場所: docgen/rag/retriever.py:216*

---


## docgen/rag/strategies/base_strategy.py

### BaseChunkStrategy

**型**: `class`

**シグネチャ**:
```
class BaseChunkStrategy:
```

**説明**:

Base class for chunking strategies.

*定義場所: docgen/rag/strategies/base_strategy.py:10*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path):
```

*説明なし*

*定義場所: docgen/rag/strategies/base_strategy.py:13*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk the content.

Args:
    content: File content
    file_path: Path to the file

Returns:
    List of chunks

*定義場所: docgen/rag/strategies/base_strategy.py:17*

---


## docgen/rag/strategies/code_strategy.py

### CodeChunkStrategy

**型**: `class`

**シグネチャ**:
```
class CodeChunkStrategy:
```

**説明**:

Strategy for chunking code files (Python, JavaScript/TypeScript, YAML, TOML).

*定義場所: docgen/rag/strategies/code_strategy.py:16*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk code content based on file extension.

*定義場所: docgen/rag/strategies/code_strategy.py:19*

---


## docgen/rag/strategies/markdown_strategy.py

### MarkdownChunkStrategy

**型**: `class`

**シグネチャ**:
```
class MarkdownChunkStrategy:
```

**説明**:

Strategy for chunking Markdown files.

*定義場所: docgen/rag/strategies/markdown_strategy.py:11*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk Markdown files by headers.

*定義場所: docgen/rag/strategies/markdown_strategy.py:14*

---


## docgen/rag/strategies/text_strategy.py

### TextChunkStrategy

**型**: `class`

**シグネチャ**:
```
class TextChunkStrategy:
```

**説明**:

Strategy for chunking generic text files.

*定義場所: docgen/rag/strategies/text_strategy.py:11*

---

### chunk

**型**: `method`

**シグネチャ**:
```
def chunk(self, content: str, file_path: Path) -> list[dict[str, Any]]:
```

**説明**:

Chunk generic files as a single chunk.

*定義場所: docgen/rag/strategies/text_strategy.py:14*

---


## docgen/rag/validator.py

### DocumentValidator

**型**: `class`

**シグネチャ**:
```
class DocumentValidator:
```

**説明**:

ドキュメント検証クラス

*定義場所: docgen/rag/validator.py:15*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path | None, config: dict[str, Any] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルート
    config: 設定辞書（技術キーワードの設定を含む）

*定義場所: docgen/rag/validator.py:54*

---

### validate_citations

**型**: `method`

**シグネチャ**:
```
def validate_citations(self, document: str, strict: bool) -> list[str]:
```

**説明**:

ドキュメント内の出典を検証

Args:
    document: 検証対象のドキュメント
    strict: 厳格モード（技術的主張に出典がない場合もエラー）

Returns:
    エラーメッセージのリスト

*定義場所: docgen/rag/validator.py:99*

---

### detect_secrets

**型**: `method`

**シグネチャ**:
```
def detect_secrets(self, document: str) -> list[str]:
```

**説明**:

ドキュメント内の機密情報を検出

Args:
    document: 検証対象のドキュメント

Returns:
    警告メッセージのリスト

*定義場所: docgen/rag/validator.py:179*

---

### validate

**型**: `method`

**シグネチャ**:
```
def validate(self, document: str, check_citations: bool, check_secrets: bool, strict: bool) -> dict[str, Any]:
```

**説明**:

ドキュメントの総合検証

Args:
    document: 検証対象のドキュメント
    check_citations: 出典チェックを行うか
    check_secrets: 機密情報チェックを行うか
    strict: 厳格モード

Returns:
    検証結果の辞書

*定義場所: docgen/rag/validator.py:214*

---

### print_report

**型**: `method`

**シグネチャ**:
```
def print_report(self, validation_result: dict[str, Any]):
```

**説明**:

検証結果をコンソールに出力

*定義場所: docgen/rag/validator.py:260*

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

*定義場所: docgen/utils/cache.py:177*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(self) -> None:
```

**説明**:

キャッシュをクリア

*定義場所: docgen/utils/cache.py:207*

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

*定義場所: docgen/utils/cache.py:214*

---

### save

**型**: `method`

**シグネチャ**:
```
def save(self) -> None:
```

**説明**:

キャッシュを保存（明示的に保存する場合）

*定義場所: docgen/utils/cache.py:250*

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

*定義場所: docgen/utils/cache.py:254*

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

### get_message

**型**: `function`

**シグネチャ**:
```
def get_message(config: dict[str, Any] | None, message_key: str, language: str | None) -> str:
```

**説明**:

メッセージを取得

Args:
    config: 設定辞書（Noneの場合はデフォルト値を使用）
    message_key: メッセージキー（例: "default_description"）
    language: 言語コード（互換性のため残しているが、現在は使用されない）

Returns:
    メッセージ文字列

*定義場所: docgen/utils/config_utils.py:101*

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

### GenerationError

**型**: `class`

**シグネチャ**:
```
class GenerationError:
```

**説明**:

ドキュメント生成関連のエラー

*定義場所: docgen/utils/exceptions.py:134*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, doc_type: str | None, generator: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:137*

---

### HookError

**型**: `class`

**シグネチャ**:
```
class HookError:
```

**説明**:

フック関連のエラー

*定義場所: docgen/utils/exceptions.py:157*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, hook_name: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:160*

---

### TemplateError

**型**: `class`

**シグネチャ**:
```
class TemplateError:
```

**説明**:

テンプレート関連のエラー

*定義場所: docgen/utils/exceptions.py:171*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, message: str, template_name: str | None):
```

*説明なし*

*定義場所: docgen/utils/exceptions.py:174*

---


## docgen/utils/file_scanner.py

### UnifiedFileScanner

**型**: `class`

**シグネチャ**:
```
class UnifiedFileScanner:
```

**説明**:

プロジェクト全体を一度だけ走査して、必要な情報を収集するクラス

*定義場所: docgen/utils/file_scanner.py:17*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, exclude_dirs: set[str] | None, exclude_files: set[str] | None, gitignore_matcher: GitIgnoreMatcher | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートディレクトリ
    exclude_dirs: 除外するディレクトリ名のセット
    exclude_files: 除外するファイル名のセット
    gitignore_matcher: .gitignoreマッチャー（Noneの場合は.gitignoreを読み込まない）

*定義場所: docgen/utils/file_scanner.py:20*

---

### scan_once

**型**: `method`

**シグネチャ**:
```
def scan_once(self) -> dict[str, Any]:
```

**説明**:

一度だけ走査して結果をキャッシュ

Returns:
    走査結果の辞書:
    - 'files_by_extension': 拡張子ごとのファイルリスト
    - 'all_files': すべてのファイルのリスト
    - 'files_by_relative_path': 相対パス -> 絶対パスのマッピング

*定義場所: docgen/utils/file_scanner.py:45*

---

### get_files_by_extensions

**型**: `method`

**シグネチャ**:
```
def get_files_by_extensions(self, extensions: set[str] | list[str]) -> list[tuple[Path, Path]]:
```

**説明**:

指定された拡張子のファイルを取得

Args:
    extensions: 拡張子のセットまたはリスト（例: {'.py', '.js'}）

Returns:
    (絶対パス, 相対パス) のタプルのリスト

*定義場所: docgen/utils/file_scanner.py:162*

---

### get_all_files

**型**: `method`

**シグネチャ**:
```
def get_all_files(self) -> list[tuple[Path, Path]]:
```

**説明**:

すべてのファイルを取得

Returns:
    (絶対パス, 相対パス) のタプルのリスト

*定義場所: docgen/utils/file_scanner.py:191*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(self):
```

**説明**:

キャッシュをクリア（再スキャンが必要な場合）

*定義場所: docgen/utils/file_scanner.py:211*

---

### get_unified_scanner

**型**: `function`

**シグネチャ**:
```
def get_unified_scanner(project_root: Path, exclude_dirs: set[str] | None, exclude_files: set[str] | None, use_gitignore: bool) -> UnifiedFileScanner:
```

**説明**:

統一ファイルスキャナーのインスタンスを取得（シングルトン的な動作）

Args:
    project_root: プロジェクトルートディレクトリ
    exclude_dirs: 除外するディレクトリ名のセット
    exclude_files: 除外するファイル名のセット
    use_gitignore: .gitignoreを適用するかどうか

Returns:
    UnifiedFileScannerインスタンス

*定義場所: docgen/utils/file_scanner.py:223*

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

### save_toml_file

**型**: `function`

**シグネチャ**:
```
def save_toml_file(file_path: Path, content: str) -> bool:
```

**説明**:

TOMLファイルを保存

Args:
    file_path: 保存先ファイルパス
    content: TOML形式の文字列

Returns:
    成功した場合はTrue

*定義場所: docgen/utils/file_utils.py:61*

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

*定義場所: docgen/utils/file_utils.py:80*

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

*定義場所: docgen/utils/file_utils.py:119*

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

*定義場所: docgen/utils/file_utils.py:136*

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

Raises:
    tomllib.TOMLDecodeError: TOMLパースエラーが発生した場合（詳細なエラー情報を含む）

*定義場所: docgen/utils/file_utils.py:157*

---


## docgen/utils/gitignore_parser.py

### GitIgnoreMatcher

**型**: `class`

**シグネチャ**:
```
class GitIgnoreMatcher:
```

**説明**:

`.gitignore`パターンを解析してマッチングを行うクラス

*定義場所: docgen/utils/gitignore_parser.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, gitignore_path: Path | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトルートディレクトリ
    gitignore_path: .gitignoreファイルのパス（Noneの場合はproject_root/.gitignore）

*定義場所: docgen/utils/gitignore_parser.py:17*

---

### is_ignored

**型**: `method`

**シグネチャ**:
```
def is_ignored(self, file_path: Path) -> bool:
```

**説明**:

ファイルパスが.gitignoreで無視されるかどうかを判定

Args:
    file_path: チェックするファイルパス（絶対パスまたは相対パス）

Returns:
    無視される場合True

*定義場所: docgen/utils/gitignore_parser.py:202*

---

### should_exclude_dir

**型**: `method`

**シグネチャ**:
```
def should_exclude_dir(self, dir_path: Path) -> bool:
```

**説明**:

ディレクトリを除外すべきかどうかを判定

Args:
    dir_path: チェックするディレクトリパス

Returns:
    除外すべき場合True

*定義場所: docgen/utils/gitignore_parser.py:236*

---

### load_gitignore_patterns

**型**: `function`

**シグネチャ**:
```
def load_gitignore_patterns(project_root: Path) -> GitIgnoreMatcher | None:
```

**説明**:

.gitignoreファイルを読み込んでマッチャーを作成

Args:
    project_root: プロジェクトルートディレクトリ

Returns:
    GitIgnoreMatcherインスタンス、またはNone（.gitignoreが存在しない場合）

*定義場所: docgen/utils/gitignore_parser.py:265*

---


## docgen/utils/llm/anthropic_client.py

### AnthropicClient

**型**: `class`

**シグネチャ**:
```
class AnthropicClient:
```

**説明**:

Anthropic APIクライアント

*定義場所: docgen/utils/llm/anthropic_client.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/anthropic_client.py:16*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

Anthropic APIを使用してテキストを生成

*定義場所: docgen/utils/llm/anthropic_client.py:35*

---


## docgen/utils/llm/base.py

### LLMClientInitializer

**型**: `class`

**シグネチャ**:
```
class LLMClientInitializer:
```

**説明**:

Common initialization patterns for LLM clients.

*定義場所: docgen/utils/llm/base.py:25*

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

*定義場所: docgen/utils/llm/base.py:29*

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

*定義場所: docgen/utils/llm/base.py:46*

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

*定義場所: docgen/utils/llm/base.py:63*

---

### BaseLLMClient

**型**: `class`

**シグネチャ**:
```
class BaseLLMClient:
```

**説明**:

LLMクライアントの抽象基底クラス

*定義場所: docgen/utils/llm/base.py:100*

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

*定義場所: docgen/utils/llm/base.py:103*

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

*定義場所: docgen/utils/llm/base.py:120*

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

*定義場所: docgen/utils/llm/base.py:134*

---


## docgen/utils/llm/factory.py

### LLMClientFactory

**型**: `class`

**シグネチャ**:
```
class LLMClientFactory:
```

**説明**:

LLMクライアントのファクトリークラス

*定義場所: docgen/utils/llm/factory.py:18*

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

*定義場所: docgen/utils/llm/factory.py:22*

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

*定義場所: docgen/utils/llm/factory.py:81*

---


## docgen/utils/llm/local_client.py

### LocalLLMClient

**型**: `class`

**シグネチャ**:
```
class LocalLLMClient:
```

**説明**:

ローカルLLMクライアント（Ollama、LM Studio対応）

*定義場所: docgen/utils/llm/local_client.py:14*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/local_client.py:17*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

ローカルLLMを使用してテキストを生成

*定義場所: docgen/utils/llm/local_client.py:43*

---


## docgen/utils/llm/openai_client.py

### OpenAIClient

**型**: `class`

**シグネチャ**:
```
class OpenAIClient:
```

**説明**:

OpenAI APIクライアント

*定義場所: docgen/utils/llm/openai_client.py:13*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, config: dict[str, Any]):
```

*説明なし*

*定義場所: docgen/utils/llm/openai_client.py:16*

---

### generate

**型**: `method`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: str | None) -> str | None:
```

**説明**:

OpenAI APIを使用してテキストを生成

*定義場所: docgen/utils/llm/openai_client.py:36*

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

*定義場所: docgen/utils/logger.py:70*

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

*定義場所: docgen/utils/markdown_utils.py:32*

---

### extract_project_description

**型**: `function`

**シグネチャ**:
```
def extract_project_description(project_root: Path, project_info_description: str | None, exclude_readme_path: Path | None, config: dict[str, Any] | None) -> str:
```

**説明**:

Extract project description from package manager files or README.md.

Priority order:
1. package.json (if exists)
2. pyproject.toml (if exists)
3. setup.py (if exists)
4. project_info_description (from LanguageInfoCollector)
5. README.md (if not excluded)
6. Default message

Args:
    project_root: Project root directory
    project_info_description: Description from project info (already prioritized by package manager)
    exclude_readme_path: README path to exclude (to prevent circular reference)
    config: Configuration dictionary (for multilingual messages)

Returns:
    Project description text

*定義場所: docgen/utils/markdown_utils.py:39*

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

*定義場所: docgen/utils/markdown_utils.py:162*

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

*定義場所: docgen/utils/outlines_utils.py:17*

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

*定義場所: docgen/utils/outlines_utils.py:35*

---


## docgen/utils/prompt_loader.py

### PromptLoader

**型**: `class`

**シグネチャ**:
```
class PromptLoader:
```

**説明**:

プロンプトをTOMLファイルから読み込むクラス

*定義場所: docgen/utils/prompt_loader.py:25*

---

### load_prompt

**型**: `method`

**シグネチャ**:
```
def load_prompt(cls, file_name: str, key: str, language: str | None, config: dict[str, Any] | None) -> str:
```

**説明**:

プロンプトを読み込む（多言語対応）

Args:
    file_name: TOMLファイル名（例: 'agents_prompts.toml'）
    key: プロンプトのキー（例: 'overview', 'full'）
    language: 言語コード（Noneの場合は設定から取得）
    config: 設定辞書
    **kwargs: テンプレート変数の置換用パラメータ

Returns:
    読み込んだプロンプト文字列（テンプレート変数が置換済み）

Raises:
    FileNotFoundError: ファイルが見つからない場合
    KeyError: 指定されたキーが見つからない場合

*定義場所: docgen/utils/prompt_loader.py:153*

---

### load_system_prompt

**型**: `method`

**シグネチャ**:
```
def load_system_prompt(cls, file_name: str, key: str, language: str | None, config: dict[str, Any] | None) -> str:
```

**説明**:

システムプロンプトを読み込む（多言語対応）

Args:
    file_name: TOMLファイル名（例: 'agents_prompts.toml'）
    key: システムプロンプトのキー（例: 'overview', 'generate'）
    language: 言語コード（Noneの場合は設定から取得）
    config: 設定辞書
    **kwargs: テンプレート変数の置換用パラメータ

Returns:
    読み込んだシステムプロンプト文字列（テンプレート変数が置換済み）

Raises:
    FileNotFoundError: ファイルが見つからない場合
    KeyError: 指定されたキーが見つからない場合

*定義場所: docgen/utils/prompt_loader.py:197*

---

### clear_cache

**型**: `method`

**シグネチャ**:
```
def clear_cache(cls):
```

**説明**:

キャッシュをクリア（主にテスト用）

*定義場所: docgen/utils/prompt_loader.py:241*

---


## docgen/validators/implementation_validator.py

### EntityReference

**型**: `class`

**シグネチャ**:
```
class EntityReference:
```

**説明**:

ドキュメント内で参照されているエンティティ

*定義場所: docgen/validators/implementation_validator.py:24*

---

### ValidationResult

**型**: `class`

**シグネチャ**:
```
class ValidationResult:
```

**説明**:

検証結果

*定義場所: docgen/validators/implementation_validator.py:35*

---

### ImplementationValidator

**型**: `class`

**シグネチャ**:
```
class ImplementationValidator:
```

**説明**:

実装検証クラス

ドキュメント内で言及されている関数、クラス、メソッドが
実際のコードベースに存在するかを検証します。

*定義場所: docgen/validators/implementation_validator.py:45*

---

### __init__

**型**: `method`

**シグネチャ**:
```
def __init__(self, project_root: Path, languages: list[str] | None, parsers: list[BaseParser] | None, config: dict[str, Any] | None):
```

**説明**:

初期化

Args:
    project_root: プロジェクトのルートディレクトリ
    languages: 検出された言語のリスト（Noneの場合は自動検出）
    parsers: パーサーのリスト（Noneの場合は自動生成）
    config: 設定辞書

*定義場所: docgen/validators/implementation_validator.py:84*

---

### build_api_index

**型**: `method`

**シグネチャ**:
```
def build_api_index(self) -> dict[str, set[str]]:
```

**説明**:

実装済みAPIのインデックスを構築

Returns:
    {entity_type: {name1, name2, ...}} の形式の辞書

*定義場所: docgen/validators/implementation_validator.py:130*

---

### extract_referenced_entities

**型**: `method`

**シグネチャ**:
```
def extract_referenced_entities(self, document: str) -> list[EntityReference]:
```

**説明**:

ドキュメントから参照されているエンティティを抽出

Args:
    document: 検証対象のドキュメント（Markdown形式）

Returns:
    参照されているエンティティのリスト

*定義場所: docgen/validators/implementation_validator.py:292*

---

### validate_implementation

**型**: `method`

**シグネチャ**:
```
def validate_implementation(self, document: str) -> ValidationResult:
```

**説明**:

実装の存在を検証

Args:
    document: 検証対象のドキュメント

Returns:
    検証結果

*定義場所: docgen/validators/implementation_validator.py:375*

---

### get_implemented_api_summary

**型**: `method`

**シグネチャ**:
```
def get_implemented_api_summary(self) -> str:
```

**説明**:

実装済みAPIのサマリーを取得（LLMプロンプト用）

Returns:
    実装済みAPIのサマリーテキスト

*定義場所: docgen/validators/implementation_validator.py:451*

---

### print_report

**型**: `method`

**シグネチャ**:
```
def print_report(self, validation_result: ValidationResult):
```

**説明**:

検証結果をコンソールに出力

*定義場所: docgen/validators/implementation_validator.py:492*

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


## scripts/verify_language_detector.py

### main

**型**: `function`

**シグネチャ**:
```
def main():
```

*説明なし*

*定義場所: scripts/verify_language_detector.py:13*

---
