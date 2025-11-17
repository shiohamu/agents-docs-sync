# API ドキュメント

自動生成日時: 2025-11-17 14:19:37

---

## scripts/generate_requirements.py

### generate_requirements_file

**型**: `function`

**シグネチャ**:
```
def generate_requirements_file(extras: list[str], output_file: Path, include_base: bool) -> None
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
def main()
```

**説明**:

メイン処理

*定義場所: scripts/generate_requirements.py:72*

---


## tests/conftest.py

### temp_project

**型**: `function`

**シグネチャ**:
```
def temp_project(tmp_path)
```

**説明**:

テスト用の一時プロジェクトディレクトリを作成

Returns:
    Path: 一時プロジェクトのルートディレクトリ

*定義場所: tests/conftest.py:16*

---

### sample_python_file

**型**: `function`

**シグネチャ**:
```
def sample_python_file(temp_project)
```

**説明**:

サンプルPythonファイル（docstring付き関数）を作成

Returns:
    Path: 作成されたPythonファイルのパス

*定義場所: tests/conftest.py:29*

---

### sample_javascript_file

**型**: `function`

**シグネチャ**:
```
def sample_javascript_file(temp_project)
```

**説明**:

サンプルJavaScriptファイル（JSDoc付き関数）を作成

Returns:
    Path: 作成されたJavaScriptファイルのパス

*定義場所: tests/conftest.py:76*

---

### sample_config

**型**: `function`

**シグネチャ**:
```
def sample_config(temp_project)
```

**説明**:

サンプル設定ファイルを作成

Returns:
    Path: 作成された設定ファイルのパス

*定義場所: tests/conftest.py:123*

---

### python_project

**型**: `function`

**シグネチャ**:
```
def python_project(temp_project)
```

**説明**:

Pythonプロジェクトの構造を作成

Returns:
    Path: プロジェクトルート

*定義場所: tests/conftest.py:157*

---

### javascript_project

**型**: `function`

**シグネチャ**:
```
def javascript_project(temp_project)
```

**説明**:

JavaScriptプロジェクトの構造を作成

Returns:
    Path: プロジェクトルート

*定義場所: tests/conftest.py:174*

---

### go_project

**型**: `function`

**シグネチャ**:
```
def go_project(temp_project)
```

**説明**:

Goプロジェクトの構造を作成

Returns:
    Path: プロジェクトルート

*定義場所: tests/conftest.py:202*

---

### multi_language_project

**型**: `function`

**シグネチャ**:
```
def multi_language_project(temp_project)
```

**説明**:

複数言語プロジェクトの構造を作成

Returns:
    Path: プロジェクトルート

*定義場所: tests/conftest.py:225*

---


## tests/test_collectors/test_project_info_collector.py

### TestProjectInfoCollector

**型**: `class`

**シグネチャ**:
```
class TestProjectInfoCollector
```

**説明**:

ProjectInfoCollectorのテストクラス

*定義場所: tests/test_collectors/test_project_info_collector.py:13*

---

### test_collect_all

**型**: `function`

**シグネチャ**:
```
def test_collect_all(self, temp_project)
```

**説明**:

collect_all()がすべての情報を収集することを確認

*定義場所: tests/test_collectors/test_project_info_collector.py:16*

---

### test_collect_build_commands_from_makefile

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_from_makefile(self, temp_project)
```

**説明**:

Makefileからビルドコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:32*

---

### test_collect_build_commands_from_package_json

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_from_package_json(self, temp_project)
```

**説明**:

package.jsonからビルドコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:50*

---

### test_collect_build_commands_from_script

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_from_script(self, temp_project)
```

**説明**:

scripts/run_pipeline.shからビルドコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:66*

---

### test_collect_test_commands_from_pytest_ini

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_from_pytest_ini(self, temp_project)
```

**説明**:

pytest.iniからテストコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:77*

---

### test_collect_test_commands_from_package_json

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_from_package_json(self, temp_project)
```

**説明**:

package.jsonからテストコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:86*

---

### test_collect_test_commands_from_script

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_from_script(self, temp_project)
```

**説明**:

scripts/run_tests.shからテストコマンドを収集

*定義場所: tests/test_collectors/test_project_info_collector.py:100*

---

### test_collect_dependencies_python

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_python(self, temp_project)
```

**説明**:

Python依存関係を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:111*

---

### test_collect_dependencies_nodejs

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_nodejs(self, temp_project)
```

**説明**:

Node.js依存関係を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:124*

---

### test_collect_dependencies_invalid_json

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_invalid_json(self, temp_project)
```

**説明**:

無効なJSONファイルを処理

*定義場所: tests/test_collectors/test_project_info_collector.py:141*

---

### test_collect_coding_standards_from_pyproject_toml

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_from_pyproject_toml(self, temp_project)
```

**説明**:

pyproject.tomlからコーディング規約を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:151*

---

### test_collect_coding_standards_invalid_toml

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_invalid_toml(self, temp_project)
```

**説明**:

無効なTOMLファイルの処理（フォールバック処理をテスト）

*定義場所: tests/test_collectors/test_project_info_collector.py:167*

---

### test_collect_coding_standards_toml_with_black_and_ruff

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_toml_with_black_and_ruff(self, temp_project)
```

**説明**:

pyproject.tomlにblackとruffの両方が含まれる場合

*定義場所: tests/test_collectors/test_project_info_collector.py:182*

---

### test_collect_coding_standards_from_editorconfig

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_from_editorconfig(self, temp_project)
```

**説明**:

`.editorconfig`からコーディング規約を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:198*

---

### test_collect_coding_standards_from_prettier

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_from_prettier(self, temp_project)
```

**説明**:

Prettier設定ファイルからコーディング規約を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:207*

---

### test_collect_ci_cd_info_github_actions

**型**: `function`

**シグネチャ**:
```
def test_collect_ci_cd_info_github_actions(self, temp_project)
```

**説明**:

GitHub Actionsの情報を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:216*

---

### test_collect_project_structure

**型**: `function`

**シグネチャ**:
```
def test_collect_project_structure(self, temp_project)
```

**説明**:

プロジェクト構造を収集

*定義場所: tests/test_collectors/test_project_info_collector.py:230*

---

### test_collect_project_structure_no_languages

**型**: `function`

**シグネチャ**:
```
def test_collect_project_structure_no_languages(self, temp_project)
```

**説明**:

言語が検出されない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:249*

---

### test_collect_build_commands_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_empty(self, temp_project)
```

**説明**:

ビルドコマンドが存在しない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:257*

---

### test_collect_test_commands_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_empty(self, temp_project)
```

**説明**:

テストコマンドが存在しない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:265*

---

### test_collect_dependencies_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_empty(self, temp_project)
```

**説明**:

依存関係が存在しない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:272*

---

### test_collect_coding_standards_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_empty(self, temp_project)
```

**説明**:

コーディング規約が存在しない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:280*

---

### test_collect_ci_cd_info_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_ci_cd_info_empty(self, temp_project)
```

**説明**:

CI/CD情報が存在しない場合

*定義場所: tests/test_collectors/test_project_info_collector.py:288*

---


## tests/test_detectors/test_generic_detector.py

### TestGenericDetector

**型**: `class`

**シグネチャ**:
```
class TestGenericDetector
```

**説明**:

GenericDetectorのテストクラス

*定義場所: tests/test_detectors/test_generic_detector.py:11*

---

### test_detect_rust

**型**: `function`

**シグネチャ**:
```
def test_detect_rust(self, temp_project)
```

**説明**:

Rustファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_generic_detector.py:14*

---

### test_detect_java

**型**: `function`

**シグネチャ**:
```
def test_detect_java(self, temp_project)
```

**説明**:

Javaファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_generic_detector.py:21*

---

### test_detect_ruby

**型**: `function`

**シグネチャ**:
```
def test_detect_ruby(self, temp_project)
```

**説明**:

Rubyファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_generic_detector.py:28*

---

### test_detect_cpp

**型**: `function`

**シグネチャ**:
```
def test_detect_cpp(self, temp_project)
```

**説明**:

C++ファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_generic_detector.py:35*

---

### test_detect_without_supported_language

**型**: `function`

**シグネチャ**:
```
def test_detect_without_supported_language(self, temp_project)
```

**説明**:

サポートされていない言語の場合に検出されないことを確認

*定義場所: tests/test_detectors/test_generic_detector.py:42*

---

### test_get_all_detected_languages

**型**: `function`

**シグネチャ**:
```
def test_get_all_detected_languages(self, temp_project)
```

**説明**:

複数言語が検出された場合にすべて返すことを確認

*定義場所: tests/test_detectors/test_generic_detector.py:48*

---


## tests/test_detectors/test_go_detector.py

### TestGoDetector

**型**: `class`

**シグネチャ**:
```
class TestGoDetector
```

**説明**:

GoDetectorのテストクラス

*定義場所: tests/test_detectors/test_go_detector.py:11*

---

### test_detect_with_go_mod

**型**: `function`

**シグネチャ**:
```
def test_detect_with_go_mod(self, go_project)
```

**説明**:

go.modがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_go_detector.py:14*

---

### test_detect_with_go_files

**型**: `function`

**シグネチャ**:
```
def test_detect_with_go_files(self, temp_project)
```

**説明**:

Goファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_go_detector.py:20*

---

### test_detect_without_go

**型**: `function`

**シグネチャ**:
```
def test_detect_without_go(self, temp_project)
```

**説明**:

Goプロジェクトでない場合に検出されないことを確認

*定義場所: tests/test_detectors/test_go_detector.py:26*

---

### test_get_language

**型**: `function`

**シグネチャ**:
```
def test_get_language(self, go_project)
```

**説明**:

get_language()が'go'を返すことを確認

*定義場所: tests/test_detectors/test_go_detector.py:31*

---


## tests/test_detectors/test_javascript_detector.py

### TestJavaScriptDetector

**型**: `class`

**シグネチャ**:
```
class TestJavaScriptDetector
```

**説明**:

JavaScriptDetectorのテストクラス

*定義場所: tests/test_detectors/test_javascript_detector.py:11*

---

### test_detect_with_package_json

**型**: `function`

**シグネチャ**:
```
def test_detect_with_package_json(self, javascript_project)
```

**説明**:

package.jsonがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:14*

---

### test_detect_with_js_files

**型**: `function`

**シグネチャ**:
```
def test_detect_with_js_files(self, temp_project)
```

**説明**:

JavaScriptファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:19*

---

### test_detect_with_ts_files

**型**: `function`

**シグネチャ**:
```
def test_detect_with_ts_files(self, temp_project)
```

**説明**:

TypeScriptファイルがある場合にTypeScriptとして検出されることを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:26*

---

### test_detect_with_tsconfig_json

**型**: `function`

**シグネチャ**:
```
def test_detect_with_tsconfig_json(self, temp_project)
```

**説明**:

tsconfig.jsonがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:33*

---

### test_detect_without_javascript

**型**: `function`

**シグネチャ**:
```
def test_detect_without_javascript(self, temp_project)
```

**説明**:

JavaScriptプロジェクトでない場合に検出されないことを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:40*

---

### test_get_language_javascript

**型**: `function`

**シグネチャ**:
```
def test_get_language_javascript(self, javascript_project)
```

**説明**:

JavaScriptプロジェクトの場合に'javascript'を返すことを確認

*定義場所: tests/test_detectors/test_javascript_detector.py:45*

---


## tests/test_detectors/test_python_detector.py

### TestPythonDetector

**型**: `class`

**シグネチャ**:
```
class TestPythonDetector
```

**説明**:

PythonDetectorのテストクラス

*定義場所: tests/test_detectors/test_python_detector.py:11*

---

### test_detect_with_requirements_txt

**型**: `function`

**シグネチャ**:
```
def test_detect_with_requirements_txt(self, python_project)
```

**説明**:

requirements.txtがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_python_detector.py:14*

---

### test_detect_with_setup_py

**型**: `function`

**シグネチャ**:
```
def test_detect_with_setup_py(self, temp_project)
```

**説明**:

setup.pyがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_python_detector.py:20*

---

### test_detect_with_pyproject_toml

**型**: `function`

**シグネチャ**:
```
def test_detect_with_pyproject_toml(self, temp_project)
```

**説明**:

pyproject.tomlがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_python_detector.py:26*

---

### test_detect_with_py_files

**型**: `function`

**シグネチャ**:
```
def test_detect_with_py_files(self, temp_project)
```

**説明**:

Pythonファイルがある場合に検出されることを確認

*定義場所: tests/test_detectors/test_python_detector.py:32*

---

### test_detect_without_python

**型**: `function`

**シグネチャ**:
```
def test_detect_without_python(self, temp_project)
```

**説明**:

Pythonプロジェクトでない場合に検出されないことを確認

*定義場所: tests/test_detectors/test_python_detector.py:38*

---

### test_get_language

**型**: `function`

**シグネチャ**:
```
def test_get_language(self, python_project)
```

**説明**:

get_language()が'python'を返すことを確認

*定義場所: tests/test_detectors/test_python_detector.py:43*

---


## tests/test_docgen.py

### TestDocGen

**型**: `class`

**シグネチャ**:
```
class TestDocGen
```

**説明**:

DocGenのテストクラス

*定義場所: tests/test_docgen.py:18*

---

### test_load_config_from_file

**型**: `function`

**シグネチャ**:
```
def test_load_config_from_file(self, temp_project, sample_config)
```

**説明**:

設定ファイルから設定を読み込めることを確認

*定義場所: tests/test_docgen.py:21*

---

### test_get_default_config

**型**: `function`

**シグネチャ**:
```
def test_get_default_config(self, temp_project)
```

**説明**:

デフォルト設定が正しいことを確認

*定義場所: tests/test_docgen.py:30*

---

### test_detect_languages_python

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_python(self, python_project)
```

**説明**:

Pythonプロジェクトの言語検出を確認

*定義場所: tests/test_docgen.py:41*

---

### test_detect_languages_empty_project

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_empty_project(self, temp_project)
```

**説明**:

空のプロジェクトで言語が検出されないことを確認

*定義場所: tests/test_docgen.py:58*

---

### test_generate_documents

**型**: `function`

**シグネチャ**:
```
def test_generate_documents(self, python_project, sample_config)
```

**説明**:

ドキュメント生成が実行されることを確認

*定義場所: tests/test_docgen.py:73*

---

### test_config_merges_with_defaults

**型**: `function`

**シグネチャ**:
```
def test_config_merges_with_defaults(self, temp_project)
```

**説明**:

部分的な設定がデフォルトとマージされることを確認

*定義場所: tests/test_docgen.py:116*

---

### test_load_config_invalid_yaml

**型**: `function`

**シグネチャ**:
```
def test_load_config_invalid_yaml(self, temp_project)
```

**説明**:

無効なYAMLファイルを処理

*定義場所: tests/test_docgen.py:135*

---

### test_load_config_missing_file

**型**: `function`

**シグネチャ**:
```
def test_load_config_missing_file(self, temp_project)
```

**説明**:

設定ファイルが存在しない場合

*定義場所: tests/test_docgen.py:147*

---

### test_detect_languages_parallel

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_parallel(self, python_project)
```

**説明**:

並列処理で言語検出

*定義場所: tests/test_docgen.py:154*

---

### test_detect_languages_sequential

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_sequential(self, python_project)
```

**説明**:

逐次処理で言語検出

*定義場所: tests/test_docgen.py:160*

---

### test_generate_documents_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project)
```

**説明**:

言語が検出されない場合のドキュメント生成

*定義場所: tests/test_docgen.py:166*

---

### test_generate_documents_api_doc_disabled

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_api_doc_disabled(self, python_project)
```

**説明**:

APIドキュメント生成が無効な場合

*定義場所: tests/test_docgen.py:181*

---

### test_generate_documents_readme_disabled

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_readme_disabled(self, python_project)
```

**説明**:

README生成が無効な場合

*定義場所: tests/test_docgen.py:196*

---

### test_main_function_detect_only

**型**: `function`

**シグネチャ**:
```
def test_main_function_detect_only(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--detect-onlyオプションをテスト

*定義場所: tests/test_docgen.py:210*

---

### test_main_function_no_api_doc

**型**: `function`

**シグネチャ**:
```
def test_main_function_no_api_doc(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--no-api-docオプションをテスト

*定義場所: tests/test_docgen.py:233*

---

### test_main_function_no_readme

**型**: `function`

**シグネチャ**:
```
def test_main_function_no_readme(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--no-readmeオプションをテスト

*定義場所: tests/test_docgen.py:253*

---

### test_main_function_with_config

**型**: `function`

**シグネチャ**:
```
def test_main_function_with_config(self, temp_project, monkeypatch, sample_config)
```

**説明**:

main()関数の--configオプションをテスト

*定義場所: tests/test_docgen.py:272*

---


## tests/test_edge_cases.py

### TestEdgeCases

**型**: `class`

**シグネチャ**:
```
class TestEdgeCases
```

**説明**:

エッジケースとエラーハンドリングのテストクラス

*定義場所: tests/test_edge_cases.py:19*

---

### test_detector_with_nonexistent_directory

**型**: `function`

**シグネチャ**:
```
def test_detector_with_nonexistent_directory(self, tmp_path)
```

**説明**:

存在しないディレクトリでの検出をテスト

*定義場所: tests/test_edge_cases.py:22*

---

### test_parser_with_nonexistent_file

**型**: `function`

**シグネチャ**:
```
def test_parser_with_nonexistent_file(self, temp_project)
```

**説明**:

存在しないファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:30*

---

### test_parser_with_syntax_error

**型**: `function`

**シグネチャ**:
```
def test_parser_with_syntax_error(self, temp_project)
```

**説明**:

構文エラーを含むファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:38*

---

### test_parser_with_empty_file

**型**: `function`

**シグネチャ**:
```
def test_parser_with_empty_file(self, temp_project)
```

**説明**:

空のファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:49*

---

### test_api_generator_with_empty_project

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_empty_project(self, temp_project)
```

**説明**:

空のプロジェクトでのAPI生成をテスト

*定義場所: tests/test_edge_cases.py:58*

---

### test_readme_generator_with_no_dependencies

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_no_dependencies(self, temp_project)
```

**説明**:

依存関係がないプロジェクトでのREADME生成をテスト

*定義場所: tests/test_edge_cases.py:76*

---

### test_readme_generator_with_invalid_manual_section

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_invalid_manual_section(self, temp_project)
```

**説明**:

無効な手動セクションマーカーの処理をテスト

*定義場所: tests/test_edge_cases.py:98*

---

### test_api_generator_with_custom_output_path

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_custom_output_path(self, temp_project)
```

**説明**:

カスタム出力パスでのAPI生成をテスト

*定義場所: tests/test_edge_cases.py:124*

---

### test_parser_excludes_directories

**型**: `function`

**シグネチャ**:
```
def test_parser_excludes_directories(self, temp_project)
```

**説明**:

除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_edge_cases.py:142*

---

### test_readme_generator_with_missing_config

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_missing_config(self, temp_project)
```

**説明**:

設定が不完全な場合の処理をテスト

*定義場所: tests/test_edge_cases.py:159*

---

### test_api_generator_with_no_languages

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_no_languages(self, temp_project)
```

**説明**:

言語が指定されていない場合の処理をテスト

*定義場所: tests/test_edge_cases.py:168*

---


## tests/test_generators/test_agents_generator.py

### test_agents_generator_initialization

**型**: `function`

**シグネチャ**:
```
def test_agents_generator_initialization(temp_project)
```

**説明**:

AgentsGeneratorの初期化テスト

*定義場所: tests/test_generators/test_agents_generator.py:13*

---

### test_generate_agents_md

**型**: `function`

**シグネチャ**:
```
def test_generate_agents_md(temp_project)
```

**説明**:

AGENTS.md生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:24*

---

### test_llm_mode_api_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_api_only(temp_project)
```

**説明**:

llm_mode: 'api' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:53*

---

### test_llm_mode_local_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_local_only(temp_project)
```

**説明**:

llm_mode: 'local' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:72*

---

### test_custom_instructions

**型**: `function`

**シグネチャ**:
```
def test_custom_instructions(temp_project)
```

**説明**:

カスタム指示のテスト

*定義場所: tests/test_generators/test_agents_generator.py:91*

---

### test_anthropic_provider

**型**: `function`

**シグネチャ**:
```
def test_anthropic_provider(temp_project)
```

**説明**:

Anthropicプロバイダーのテスト

*定義場所: tests/test_generators/test_agents_generator.py:113*

---

### test_no_agents_config

**型**: `function`

**シグネチャ**:
```
def test_no_agents_config(temp_project)
```

**説明**:

agentsセクションがない場合のテスト（デフォルト動作）

*定義場所: tests/test_generators/test_agents_generator.py:132*

---

### test_no_build_commands

**型**: `function`

**シグネチャ**:
```
def test_no_build_commands(temp_project)
```

**説明**:

ビルドコマンドがない場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:148*

---


## tests/test_generators/test_api_generator.py

### TestAPIGenerator

**型**: `class`

**シグネチャ**:
```
class TestAPIGenerator
```

**説明**:

APIGeneratorのテストクラス

*定義場所: tests/test_generators/test_api_generator.py:11*

---

### test_generate_creates_api_doc

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_api_doc(self, python_project, sample_python_file)
```

**説明**:

APIドキュメントが生成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:14*

---

### test_generate_api_doc_content

**型**: `function`

**シグネチャ**:
```
def test_generate_api_doc_content(self, python_project, sample_python_file)
```

**説明**:

生成されたAPIドキュメントの内容を確認

*定義場所: tests/test_generators/test_api_generator.py:32*

---

### test_generate_with_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_multiple_languages(self, multi_language_project)
```

**説明**:

複数言語のAPI情報が統合されることを確認

*定義場所: tests/test_generators/test_api_generator.py:52*

---

### test_generate_creates_output_directory

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_output_directory(self, temp_project)
```

**説明**:

出力ディレクトリが自動作成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:70*

---

### test_generate_with_no_apis

**型**: `function`

**シグネチャ**:
```
def test_generate_with_no_apis(self, temp_project)
```

**説明**:

APIが見つからない場合でもドキュメントが生成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:87*

---


## tests/test_generators/test_readme_generator.py

### TestReadmeGenerator

**型**: `class`

**シグネチャ**:
```
class TestReadmeGenerator
```

**説明**:

ReadmeGeneratorのテストクラス

*定義場所: tests/test_generators/test_readme_generator.py:11*

---

### test_generate_creates_readme

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_readme(self, python_project)
```

**説明**:

READMEが生成されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:14*

---

### test_generate_readme_content

**型**: `function`

**シグネチャ**:
```
def test_generate_readme_content(self, python_project)
```

**説明**:

生成されたREADMEの内容を確認

*定義場所: tests/test_generators/test_readme_generator.py:33*

---

### test_extract_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections(self, temp_project)
```

**説明**:

手動セクションが正しく抽出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:55*

---

### test_preserve_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_preserve_manual_sections(self, temp_project)
```

**説明**:

手動セクションが保持されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:80*

---

### test_detect_dependencies_python

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_python(self, python_project)
```

**説明**:

Pythonの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:109*

---

### test_detect_dependencies_python_pep440_specifiers

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_python_pep440_specifiers(self, temp_project)
```

**説明**:

PEP 440の様々なバージョン指定子が正しく処理されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:123*

---

### test_detect_dependencies_javascript

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_javascript(self, javascript_project)
```

**説明**:

JavaScriptの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:173*

---

### test_detect_dependencies_go_multiline_require

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_go_multiline_require(self, temp_project)
```

**説明**:

Goの複数行requireブロックの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:187*

---

### test_get_project_structure

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure(self, python_project)
```

**説明**:

プロジェクト構造が生成されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:222*

---

### test_get_project_structure_excludes_files

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure_excludes_files(self, temp_project)
```

**説明**:

プロジェクト構造から除外ファイルが除外されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:236*

---

### test_get_project_structure_excludes_dirs

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure_excludes_dirs(self, temp_project)
```

**説明**:

プロジェクト構造から除外ディレクトリが除外されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:264*

---

### test_generate_with_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_generate_with_manual_sections(self, temp_project)
```

**説明**:

複数の手動セクションが保持されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:294*

---


## tests/test_integration.py

### TestIntegration

**型**: `class`

**シグネチャ**:
```
class TestIntegration
```

**説明**:

統合テストクラス

*定義場所: tests/test_integration.py:22*

---

### test_end_to_end_python_project

**型**: `function`

**シグネチャ**:
```
def test_end_to_end_python_project(self, python_project, sample_config)
```

**説明**:

Pythonプロジェクトのエンドツーエンドテスト

*定義場所: tests/test_integration.py:25*

---

### test_multiple_languages_detection

**型**: `function`

**シグネチャ**:
```
def test_multiple_languages_detection(self, multi_language_project)
```

**説明**:

複数言語プロジェクトでの検出をテスト

*定義場所: tests/test_integration.py:68*

---

### test_readme_preserves_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_readme_preserves_manual_sections(self, temp_project)
```

**説明**:

READMEの手動セクションが保持されることを統合テストで確認

*定義場所: tests/test_integration.py:76*

---

### test_api_doc_includes_all_languages

**型**: `function`

**シグネチャ**:
```
def test_api_doc_includes_all_languages(self, multi_language_project)
```

**説明**:

複数言語のAPI情報が統合されることを確認

*定義場所: tests/test_integration.py:118*

---


## tests/test_parsers/test_base_parser.py

### TestBaseParser

**型**: `class`

**シグネチャ**:
```
class TestBaseParser
```

**説明**:

BaseParserのテストクラス

*定義場所: tests/test_parsers/test_base_parser.py:12*

---

### test_parse_project_exclude_dirs

**型**: `function`

**シグネチャ**:
```
def test_parse_project_exclude_dirs(self, temp_project)
```

**説明**:

除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_parsers/test_base_parser.py:15*

---

### test_parse_project_custom_exclude_dirs

**型**: `function`

**シグネチャ**:
```
def test_parse_project_custom_exclude_dirs(self, temp_project)
```

**説明**:

カスタム除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_parsers/test_base_parser.py:30*

---

### test_parse_project_parallel

**型**: `function`

**シグネチャ**:
```
def test_parse_project_parallel(self, temp_project)
```

**説明**:

並列処理でプロジェクトを解析

*定義場所: tests/test_parsers/test_base_parser.py:42*

---

### test_parse_project_sequential

**型**: `function`

**シグネチャ**:
```
def test_parse_project_sequential(self, temp_project)
```

**説明**:

逐次処理でプロジェクトを解析

*定義場所: tests/test_parsers/test_base_parser.py:53*

---

### test_parse_project_few_files_sequential

**型**: `function`

**シグネチャ**:
```
def test_parse_project_few_files_sequential(self, temp_project)
```

**説明**:

ファイル数が少ない場合は逐次処理になることを確認

*定義場所: tests/test_parsers/test_base_parser.py:62*

---

### test_parse_file_safe_with_error

**型**: `function`

**シグネチャ**:
```
def test_parse_file_safe_with_error(self, temp_project)
```

**説明**:

エラーが発生した場合の安全な処理

*定義場所: tests/test_parsers/test_base_parser.py:73*

---

### test_parse_project_symlink_skipped

**型**: `function`

**シグネチャ**:
```
def test_parse_project_symlink_skipped(self, temp_project)
```

**説明**:

シンボリックリンクがスキップされることを確認

*定義場所: tests/test_parsers/test_base_parser.py:85*

---

### test_parse_project_permission_error

**型**: `function`

**シグネチャ**:
```
def test_parse_project_permission_error(self, temp_project)
```

**説明**:

権限エラーが発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:96*

---

### test_parse_project_max_workers

**型**: `function`

**シグネチャ**:
```
def test_parse_project_max_workers(self, temp_project)
```

**説明**:

max_workersが指定された場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:107*

---

### test_parse_project_parallel_with_exception

**型**: `function`

**シグネチャ**:
```
def test_parse_project_parallel_with_exception(self, temp_project)
```

**説明**:

並列処理で例外が発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:117*

---

### test_parse_file_safe_exception_handling

**型**: `function`

**シグネチャ**:
```
def test_parse_file_safe_exception_handling(self, temp_project)
```

**説明**:

_parse_file_safeで例外が発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:134*

---


## tests/test_parsers/test_generic_parser.py

### TestGenericParser

**型**: `class`

**シグネチャ**:
```
class TestGenericParser
```

**説明**:

GenericParserのテストクラス

*定義場所: tests/test_parsers/test_generic_parser.py:11*

---

### test_parse_file_rust

**型**: `function`

**シグネチャ**:
```
def test_parse_file_rust(self, temp_project)
```

**説明**:

Rustファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:14*

---

### test_parse_file_java

**型**: `function`

**シグネチャ**:
```
def test_parse_file_java(self, temp_project)
```

**説明**:

Javaファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:29*

---

### test_parse_file_ruby

**型**: `function`

**シグネチャ**:
```
def test_parse_file_ruby(self, temp_project)
```

**説明**:

Rubyファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:53*

---

### test_get_supported_extensions_rust

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions_rust(self)
```

**説明**:

Rustの拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_generic_parser.py:71*

---

### test_get_supported_extensions_java

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions_java(self)
```

**説明**:

Javaの拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_generic_parser.py:78*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, temp_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:85*

---


## tests/test_parsers/test_js_parser.py

### TestJSParser

**型**: `class`

**シグネチャ**:
```
class TestJSParser
```

**説明**:

JSParserのテストクラス

*定義場所: tests/test_parsers/test_js_parser.py:11*

---

### test_parse_file_with_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_jsdoc(self, sample_javascript_file)
```

**説明**:

JSDocコメントを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:14*

---

### test_parse_file_extracts_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_jsdoc(self, sample_javascript_file)
```

**説明**:

JSDocコメントが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_js_parser.py:24*

---

### test_parse_file_with_class

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_class(self, sample_javascript_file)
```

**説明**:

クラスを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:36*

---

### test_parse_file_extracts_signature

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_signature(self, sample_javascript_file)
```

**説明**:

シグネチャが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_js_parser.py:45*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, javascript_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:55*

---

### test_get_supported_extensions

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions(self)
```

**説明**:

サポートする拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_js_parser.py:62*

---

### test_parse_file_without_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_without_jsdoc(self, temp_project)
```

**説明**:

JSDocなしの関数も解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:72*

---


## tests/test_parsers/test_python_parser.py

### TestPythonParser

**型**: `class`

**シグネチャ**:
```
class TestPythonParser
```

**説明**:

PythonParserのテストクラス

*定義場所: tests/test_parsers/test_python_parser.py:11*

---

### test_parse_file_with_function

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_function(self, sample_python_file)
```

**説明**:

関数を含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:14*

---

### test_parse_file_with_class

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_class(self, sample_python_file)
```

**説明**:

クラスを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:27*

---

### test_parse_file_extracts_signature

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_signature(self, sample_python_file)
```

**説明**:

シグネチャが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_python_parser.py:37*

---

### test_parse_file_extracts_docstring

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_docstring(self, sample_python_file)
```

**説明**:

docstringが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_python_parser.py:47*

---

### test_parse_file_includes_line_number

**型**: `function`

**シグネチャ**:
```
def test_parse_file_includes_line_number(self, sample_python_file)
```

**説明**:

行番号が含まれることを確認

*定義場所: tests/test_parsers/test_python_parser.py:57*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, python_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:65*

---

### test_parse_file_skips_private_functions

**型**: `function`

**シグネチャ**:
```
def test_parse_file_skips_private_functions(self, temp_project)
```

**説明**:

プライベート関数（_で始まる）がスキップされることを確認

*定義場所: tests/test_parsers/test_python_parser.py:74*

---

### test_get_supported_extensions

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions(self)
```

**説明**:

サポートする拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_python_parser.py:92*

---

### test_parse_file_with_syntax_error

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_syntax_error(self, temp_project)
```

**説明**:

構文エラーがあるファイルでもエラーが発生しないことを確認

*定義場所: tests/test_parsers/test_python_parser.py:100*

---
