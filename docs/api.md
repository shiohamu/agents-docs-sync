# API ドキュメント

自動生成日時: 2025-11-20 10:34:13

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

*定義場所: tests/conftest.py:26*

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

*定義場所: tests/conftest.py:39*

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

*定義場所: tests/conftest.py:86*

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

*定義場所: tests/conftest.py:133*

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

*定義場所: tests/conftest.py:162*

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

*定義場所: tests/conftest.py:179*

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

*定義場所: tests/conftest.py:205*

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

*定義場所: tests/conftest.py:226*

---


## tests/test_config_manager.py

### TestConfigManager

**型**: `class`

**シグネチャ**:
```
class TestConfigManager
```

**説明**:

ConfigManagerのテストクラス

*定義場所: tests/test_config_manager.py:13*

---

### test_initialization

**型**: `function`

**シグネチャ**:
```
def test_initialization(self, config_manager)
```

**説明**:

ConfigManagerの初期化テスト

*定義場所: tests/test_config_manager.py:16*

---

### test_load_config_success

**型**: `function`

**シグネチャ**:
```
def test_load_config_success(self, temp_project)
```

**説明**:

設定ファイルの読み込み成功

*定義場所: tests/test_config_manager.py:22*

---

### test_load_config_invalid_yaml

**型**: `function`

**シグネチャ**:
```
def test_load_config_invalid_yaml(self, temp_project)
```

**説明**:

無効なYAMLファイルの場合、デフォルト設定を使用

*定義場所: tests/test_config_manager.py:30*

---

### test_get_default_config

**型**: `function`

**シグネチャ**:
```
def test_get_default_config(self, temp_project)
```

**説明**:

デフォルト設定の内容を確認

*定義場所: tests/test_config_manager.py:43*

---

### test_update_config

**型**: `function`

**シグネチャ**:
```
def test_update_config(self, temp_project, key, value)
```

**説明**:

設定更新のテスト（パラメータ化）

*定義場所: tests/test_config_manager.py:64*

---

### test_load_config_read_failure

**型**: `function`

**シグネチャ**:
```
def test_load_config_read_failure(self, mock_read_yaml, temp_project)
```

**説明**:

設定ファイル読み込み失敗

*定義場所: tests/test_config_manager.py:76*

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

*定義場所: tests/test_docgen.py:19*

---

### test_load_config_from_file

**型**: `function`

**シグネチャ**:
```
def test_load_config_from_file(self, temp_project, sample_config)
```

**説明**:

設定ファイルから設定を読み込めることを確認

*定義場所: tests/test_docgen.py:22*

---

### test_get_default_config

**型**: `function`

**シグネチャ**:
```
def test_get_default_config(self, temp_project)
```

**説明**:

デフォルト設定が正しいことを確認

*定義場所: tests/test_docgen.py:32*

---

### test_detect_languages_python

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_python(self, python_project)
```

**説明**:

Pythonプロジェクトの言語検出を確認

*定義場所: tests/test_docgen.py:44*

---

### test_detect_languages_empty_project

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_empty_project(self, temp_project)
```

**説明**:

空のプロジェクトで言語が検出されないことを確認

*定義場所: tests/test_docgen.py:61*

---

### test_generate_documents

**型**: `function`

**シグネチャ**:
```
def test_generate_documents(self, python_project, sample_config)
```

**説明**:

ドキュメント生成が実行されることを確認

*定義場所: tests/test_docgen.py:76*

---

### test_config_merges_with_defaults

**型**: `function`

**シグネチャ**:
```
def test_config_merges_with_defaults(self, temp_project)
```

**説明**:

部分的な設定がデフォルトとマージされることを確認

*定義場所: tests/test_docgen.py:119*

---

### test_load_config_invalid_yaml

**型**: `function`

**シグネチャ**:
```
def test_load_config_invalid_yaml(self, temp_project)
```

**説明**:

無効なYAMLファイルを処理

*定義場所: tests/test_docgen.py:131*

---

### test_load_config_missing_file

**型**: `function`

**シグネチャ**:
```
def test_load_config_missing_file(self, temp_project)
```

**説明**:

設定ファイルが存在しない場合

*定義場所: tests/test_docgen.py:143*

---

### test_detect_languages_parallel

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_parallel(self, python_project)
```

**説明**:

並列処理で言語検出

*定義場所: tests/test_docgen.py:150*

---

### test_detect_languages_sequential

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_sequential(self, python_project)
```

**説明**:

逐次処理で言語検出

*定義場所: tests/test_docgen.py:156*

---

### test_generate_documents_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project)
```

**説明**:

言語が検出されない場合のドキュメント生成

*定義場所: tests/test_docgen.py:162*

---

### test_generate_documents_api_doc_disabled

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_api_doc_disabled(self, python_project)
```

**説明**:

APIドキュメント生成が無効な場合

*定義場所: tests/test_docgen.py:177*

---

### test_generate_documents_readme_disabled

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_readme_disabled(self, python_project)
```

**説明**:

README生成が無効な場合

*定義場所: tests/test_docgen.py:192*

---

### test_main_function_detect_only

**型**: `function`

**シグネチャ**:
```
def test_main_function_detect_only(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--detect-onlyオプションをテスト

*定義場所: tests/test_docgen.py:206*

---

### test_main_function_no_api_doc

**型**: `function`

**シグネチャ**:
```
def test_main_function_no_api_doc(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--no-api-docオプションをテスト

*定義場所: tests/test_docgen.py:230*

---

### test_main_function_no_readme

**型**: `function`

**シグネチャ**:
```
def test_main_function_no_readme(self, temp_project, monkeypatch)
```

**説明**:

main()関数の--no-readmeオプションをテスト

*定義場所: tests/test_docgen.py:252*

---

### test_main_function_with_config

**型**: `function`

**シグネチャ**:
```
def test_main_function_with_config(self, temp_project, monkeypatch, sample_config)
```

**説明**:

main()関数の--configオプションをテスト

*定義場所: tests/test_docgen.py:274*

---

### test_update_config

**型**: `function`

**シグネチャ**:
```
def test_update_config(self, temp_project)
```

**説明**:

設定更新機能のテスト

*定義場所: tests/test_docgen.py:296*

---

### test_update_config_validation

**型**: `function`

**シグネチャ**:
```
def test_update_config_validation(self, temp_project)
```

**説明**:

設定更新時のバリデーション機能テスト

*定義場所: tests/test_docgen.py:309*

---

### test_generate_documents_with_api_doc

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_with_api_doc(self, temp_project)
```

**説明**:

APIドキュメント生成機能のテスト

*定義場所: tests/test_docgen.py:323*

---

### test_generate_documents_with_readme

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_with_readme(self, temp_project)
```

**説明**:

README生成機能のテスト

*定義場所: tests/test_docgen.py:340*

---

### test_generate_documents_with_agents_doc

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_with_agents_doc(self, temp_project)
```

**説明**:

AGENTSドキュメント生成機能のテスト

*定義場所: tests/test_docgen.py:354*

---

### test_generate_documents_disabled_all

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_disabled_all(self, temp_project)
```

**説明**:

すべての生成が無効の場合のテスト

*定義場所: tests/test_docgen.py:368*

---

### test_detect_languages_with_cache

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_with_cache(self, temp_project)
```

**説明**:

言語検出のキャッシュ機能テスト

*定義場所: tests/test_docgen.py:388*

---

### test_detect_languages_parallel

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_parallel(self, temp_project)
```

**説明**:

並列言語検出のテスト

*定義場所: tests/test_docgen.py:399*

---

### test_detect_languages_sequential

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_sequential(self, temp_project)
```

**説明**:

順次言語検出のテスト

*定義場所: tests/test_docgen.py:407*

---

### test_main_function_commit_msg

**型**: `function`

**シグネチャ**:
```
def test_main_function_commit_msg(self, temp_project, monkeypatch)
```

**説明**:

main()関数のcommit-msgコマンドテスト

*定義場所: tests/test_docgen.py:415*

---

### test_main_function_with_invalid_config

**型**: `function`

**シグネチャ**:
```
def test_main_function_with_invalid_config(self, temp_project, monkeypatch)
```

**説明**:

無効な設定ファイルの場合のmain関数テスト

*定義場所: tests/test_docgen.py:441*

---

### test_main_function_detect_only_mode

**型**: `function`

**シグネチャ**:
```
def test_main_function_detect_only_mode(self, temp_project, monkeypatch)
```

**説明**:

detect-onlyモードのmain関数テスト

*定義場所: tests/test_docgen.py:458*

---


## tests/test_docgen_extended.py

### TestDocgenExtended

**型**: `class`

**シグネチャ**:
```
class TestDocgenExtended
```

**説明**:

Docgenメインモジュールの拡張テスト

*定義場所: tests/test_docgen_extended.py:20*

---

### test_update_config_add_missing_sections

**型**: `function`

**シグネチャ**:
```
def test_update_config_add_missing_sections(self)
```

**説明**:

欠落しているセクションを追加するテスト

*定義場所: tests/test_docgen_extended.py:23*

---

### test_update_config_preserve_existing

**型**: `function`

**シグネチャ**:
```
def test_update_config_preserve_existing(self)
```

**説明**:

既存の設定を保持するテスト

*定義場所: tests/test_docgen_extended.py:38*

---

### test_validate_config_valid

**型**: `function`

**シグネチャ**:
```
def test_validate_config_valid(self)
```

**説明**:

有効な設定の検証テスト

*定義場所: tests/test_docgen_extended.py:55*

---

### test_validate_config_missing_output

**型**: `function`

**シグネチャ**:
```
def test_validate_config_missing_output(self)
```

**説明**:

outputセクションがない場合の検証テスト

*定義場所: tests/test_docgen_extended.py:73*

---

### test_validate_config_missing_readme

**型**: `function`

**シグネチャ**:
```
def test_validate_config_missing_readme(self)
```

**説明**:

readmeセクションがない場合の検証テスト

*定義場所: tests/test_docgen_extended.py:84*

---

### test_validate_config_missing_agents

**型**: `function`

**シグネチャ**:
```
def test_validate_config_missing_agents(self)
```

**説明**:

agentsセクションがない場合の検証テスト

*定義場所: tests/test_docgen_extended.py:94*

---

### test_detect_languages_parallel

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_parallel(self, temp_project)
```

**説明**:

並列言語検出のテスト

*定義場所: tests/test_docgen_extended.py:104*

---

### test_detect_languages_sequential

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_sequential(self, temp_project)
```

**説明**:

逐次言語検出のテスト

*定義場所: tests/test_docgen_extended.py:118*

---

### test_detect_languages_no_files

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_no_files(self, temp_project)
```

**説明**:

ファイルがない場合の言語検出テスト

*定義場所: tests/test_docgen_extended.py:129*

---

### test_detect_languages_empty_directory

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_empty_directory(self, temp_project)
```

**説明**:

空ディレクトリでの言語検出テスト

*定義場所: tests/test_docgen_extended.py:136*

---

### test_generate_documents_success

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_success(self, temp_project)
```

**説明**:

ドキュメント生成成功テスト

*定義場所: tests/test_docgen_extended.py:146*

---

### test_generate_documents_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project)
```

**説明**:

言語なしでのドキュメント生成テスト

*定義場所: tests/test_docgen_extended.py:167*

---

### test_generate_documents_partial_failure

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_partial_failure(self, temp_project)
```

**説明**:

部分的な失敗のテスト

*定義場所: tests/test_docgen_extended.py:183*

---

### test_generate_documents_complete_failure

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_complete_failure(self, temp_project)
```

**説明**:

完全な失敗のテスト - 実際には例外処理をテスト

*定義場所: tests/test_docgen_extended.py:202*

---

### test_main_with_config_file

**型**: `function`

**シグネチャ**:
```
def test_main_with_config_file(self, temp_project)
```

**説明**:

設定ファイル付きでのmain関数テスト

*定義場所: tests/test_docgen_extended.py:223*

---

### test_main_with_directory_argument

**型**: `function`

**シグネチャ**:
```
def test_main_with_directory_argument(self, temp_project)
```

**説明**:

ディレクトリ引数付きでのmain関数テスト

*定義場所: tests/test_docgen_extended.py:255*

---

### test_main_missing_arguments

**型**: `function`

**シグネチャ**:
```
def test_main_missing_arguments(self)
```

**説明**:

引数がない場合のmain関数テスト

*定義場所: tests/test_docgen_extended.py:276*

---

### test_main_invalid_config_file

**型**: `function`

**シグネチャ**:
```
def test_main_invalid_config_file(self, temp_project)
```

**説明**:

無効な設定ファイルの場合のmain関数テスト

*定義場所: tests/test_docgen_extended.py:287*

---

### test_main_nonexistent_directory

**型**: `function`

**シグネチャ**:
```
def test_main_nonexistent_directory(self)
```

**説明**:

存在しないディレクトリの場合のmain関数テスト

*定義場所: tests/test_docgen_extended.py:302*

---

### test_main_help_argument

**型**: `function`

**シグネチャ**:
```
def test_main_help_argument(self)
```

**説明**:

ヘルプ引数の場合のmain関数テスト

*定義場所: tests/test_docgen_extended.py:313*

---

### test_main_version_argument

**型**: `function`

**シグネチャ**:
```
def test_main_version_argument(self)
```

**説明**:

バージョン引数の場合のmain関数テスト

*定義場所: tests/test_docgen_extended.py:320*

---

### test_detect_languages_with_hidden_files

**型**: `function`

**シグネチャ**:
```
def test_detect_languages_with_hidden_files(self, temp_project)
```

**説明**:

隠しファイルがある場合の言語検出テスト

*定義場所: tests/test_docgen_extended.py:327*

---

### test_generate_documents_with_custom_config

**型**: `function`

**シグネチャ**:
```
def test_generate_documents_with_custom_config(self, temp_project)
```

**説明**:

カスタム設定でのドキュメント生成テスト

*定義場所: tests/test_docgen_extended.py:341*

---

### test_error_handling_in_language_detection

**型**: `function`

**シグネチャ**:
```
def test_error_handling_in_language_detection(self, temp_project)
```

**説明**:

言語検出時のエラーハンドリングテスト

*定義場所: tests/test_docgen_extended.py:372*

---

### test_config_validation_edge_cases

**型**: `function`

**シグネチャ**:
```
def test_config_validation_edge_cases(self)
```

**説明**:

設定検証のエッジケーステスト

*定義場所: tests/test_docgen_extended.py:388*

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

*定義場所: tests/test_edge_cases.py:20*

---

### test_detector_with_nonexistent_directory

**型**: `function`

**シグネチャ**:
```
def test_detector_with_nonexistent_directory(self, tmp_path)
```

**説明**:

存在しないディレクトリでの検出をテスト

*定義場所: tests/test_edge_cases.py:23*

---

### test_parser_with_nonexistent_file

**型**: `function`

**シグネチャ**:
```
def test_parser_with_nonexistent_file(self, temp_project)
```

**説明**:

存在しないファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:31*

---

### test_parser_with_syntax_error

**型**: `function`

**シグネチャ**:
```
def test_parser_with_syntax_error(self, temp_project)
```

**説明**:

構文エラーを含むファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:39*

---

### test_parser_with_empty_file

**型**: `function`

**シグネチャ**:
```
def test_parser_with_empty_file(self, temp_project)
```

**説明**:

空のファイルの解析をテスト

*定義場所: tests/test_edge_cases.py:50*

---

### test_api_generator_with_empty_project

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_empty_project(self, temp_project)
```

**説明**:

空のプロジェクトでのAPI生成をテスト

*定義場所: tests/test_edge_cases.py:59*

---

### test_readme_generator_with_no_dependencies

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_no_dependencies(self, temp_project)
```

**説明**:

依存関係がないプロジェクトでのREADME生成をテスト

*定義場所: tests/test_edge_cases.py:73*

---

### test_readme_generator_with_invalid_manual_section

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_invalid_manual_section(self, temp_project)
```

**説明**:

無効な手動セクションマーカーの処理をテスト

*定義場所: tests/test_edge_cases.py:90*

---

### test_api_generator_with_custom_output_path

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_custom_output_path(self, temp_project)
```

**説明**:

カスタム出力パスでのAPI生成をテスト

*定義場所: tests/test_edge_cases.py:111*

---

### test_parser_excludes_directories

**型**: `function`

**シグネチャ**:
```
def test_parser_excludes_directories(self, temp_project)
```

**説明**:

除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_edge_cases.py:125*

---

### test_readme_generator_with_missing_config

**型**: `function`

**シグネチャ**:
```
def test_readme_generator_with_missing_config(self, temp_project)
```

**説明**:

設定が不完全な場合の処理をテスト

*定義場所: tests/test_edge_cases.py:142*

---

### test_api_generator_with_no_languages

**型**: `function`

**シグネチャ**:
```
def test_api_generator_with_no_languages(self, temp_project)
```

**説明**:

言語が指定されていない場合の処理をテスト

*定義場所: tests/test_edge_cases.py:151*

---

### test_config_file_nonexistent

**型**: `function`

**シグネチャ**:
```
def test_config_file_nonexistent(self, tmp_path)
```

**説明**:

存在しない設定ファイルの処理テスト

*定義場所: tests/test_edge_cases.py:186*

---

### test_config_file_invalid_yaml

**型**: `function`

**シグネチャ**:
```
def test_config_file_invalid_yaml(self, tmp_path)
```

**説明**:

無効なYAML設定ファイルの処理テスト

*定義場所: tests/test_edge_cases.py:197*

---

### test_large_project_processing

**型**: `function`

**シグネチャ**:
```
def test_large_project_processing(self, temp_project)
```

**説明**:

大規模プロジェクトの処理テスト

*定義場所: tests/test_edge_cases.py:209*

---

### test_special_characters_in_files

**型**: `function`

**シグネチャ**:
```
def test_special_characters_in_files(self, temp_project)
```

**説明**:

特殊文字を含むファイルの処理テスト

*定義場所: tests/test_edge_cases.py:223*

---

### test_network_error_fallback

**型**: `function`

**シグネチャ**:
```
def test_network_error_fallback(self, temp_project, monkeypatch)
```

**説明**:

ネットワークエラー時のLLMフォールバックテスト

*定義場所: tests/test_edge_cases.py:246*

---

### test_mixed_language_project

**型**: `function`

**シグネチャ**:
```
def test_mixed_language_project(self, temp_project)
```

**説明**:

複数言語混在プロジェクトの処理テスト

*定義場所: tests/test_edge_cases.py:265*

---

### test_deeply_nested_directory_structure

**型**: `function`

**シグネチャ**:
```
def test_deeply_nested_directory_structure(self, temp_project)
```

**説明**:

深くネストされたディレクトリ構造の処理テスト

*定義場所: tests/test_edge_cases.py:286*

---

### test_binary_files_ignored

**型**: `function`

**シグネチャ**:
```
def test_binary_files_ignored(self, temp_project)
```

**説明**:

バイナリファイルが無視されるテスト

*定義場所: tests/test_edge_cases.py:304*

---

### test_circular_import_handling

**型**: `function`

**シグネチャ**:
```
def test_circular_import_handling(self, temp_project)
```

**説明**:

循環インポートを含むファイルの処理テスト

*定義場所: tests/test_edge_cases.py:320*

---

### test_very_long_file_processing

**型**: `function`

**シグネチャ**:
```
def test_very_long_file_processing(self, temp_project)
```

**説明**:

非常に長いファイルの処理テスト

*定義場所: tests/test_edge_cases.py:341*

---

### test_unicode_file_names

**型**: `function`

**シグネチャ**:
```
def test_unicode_file_names(self, temp_project)
```

**説明**:

Unicodeファイル名の処理テスト

*定義場所: tests/test_edge_cases.py:356*

---

### test_hidden_files_ignored

**型**: `function`

**シグネチャ**:
```
def test_hidden_files_ignored(self, temp_project)
```

**説明**:

隠しファイルが無視されるテスト

*定義場所: tests/test_edge_cases.py:368*

---


## tests/test_exceptions.py

### TestDocGenError

**型**: `class`

**シグネチャ**:
```
class TestDocGenError
```

**説明**:

DocGenErrorクラスのテスト

*定義場所: tests/test_exceptions.py:16*

---

### test_init_with_message_only

**型**: `function`

**シグネチャ**:
```
def test_init_with_message_only(self)
```

**説明**:

メッセージのみで初期化

*定義場所: tests/test_exceptions.py:19*

---

### test_init_with_message_and_details

**型**: `function`

**シグネチャ**:
```
def test_init_with_message_and_details(self)
```

**説明**:

メッセージと詳細で初期化

*定義場所: tests/test_exceptions.py:26*

---

### test_str_with_details

**型**: `function`

**シグネチャ**:
```
def test_str_with_details(self)
```

**説明**:

__str__メソッドのテスト（詳細あり）

*定義場所: tests/test_exceptions.py:33*

---

### test_str_without_details

**型**: `function`

**シグネチャ**:
```
def test_str_without_details(self)
```

**説明**:

__str__メソッドのテスト（詳細なし）

*定義場所: tests/test_exceptions.py:38*

---

### test_inheritance_from_exception

**型**: `function`

**シグネチャ**:
```
def test_inheritance_from_exception(self)
```

**説明**:

Exceptionからの継承確認

*定義場所: tests/test_exceptions.py:43*

---

### TestConfigError

**型**: `class`

**シグネチャ**:
```
class TestConfigError
```

**説明**:

ConfigErrorクラスのテスト

*定義場所: tests/test_exceptions.py:49*

---

### test_inheritance

**型**: `function`

**シグネチャ**:
```
def test_inheritance(self)
```

**説明**:

DocGenErrorからの継承確認

*定義場所: tests/test_exceptions.py:52*

---

### test_message_preservation

**型**: `function`

**シグネチャ**:
```
def test_message_preservation(self)
```

**説明**:

メッセージの保持確認

*定義場所: tests/test_exceptions.py:58*

---

### TestLLMError

**型**: `class`

**シグネチャ**:
```
class TestLLMError
```

**説明**:

LLMErrorクラスのテスト

*定義場所: tests/test_exceptions.py:66*

---

### test_inheritance

**型**: `function`

**シグネチャ**:
```
def test_inheritance(self)
```

**説明**:

DocGenErrorからの継承確認

*定義場所: tests/test_exceptions.py:69*

---

### test_simple_message

**型**: `function`

**シグネチャ**:
```
def test_simple_message(self)
```

**説明**:

シンプルなメッセージテスト

*定義場所: tests/test_exceptions.py:75*

---

### TestParseError

**型**: `class`

**シグネチャ**:
```
class TestParseError
```

**説明**:

ParseErrorクラスのテスト

*定義場所: tests/test_exceptions.py:81*

---

### test_inheritance

**型**: `function`

**シグネチャ**:
```
def test_inheritance(self)
```

**説明**:

DocGenErrorからの継承確認

*定義場所: tests/test_exceptions.py:84*

---

### test_with_details

**型**: `function`

**シグネチャ**:
```
def test_with_details(self)
```

**説明**:

詳細付きエラーテスト

*定義場所: tests/test_exceptions.py:90*

---

### TestCacheError

**型**: `class`

**シグネチャ**:
```
class TestCacheError
```

**説明**:

CacheErrorクラスのテスト

*定義場所: tests/test_exceptions.py:96*

---

### test_inheritance

**型**: `function`

**シグネチャ**:
```
def test_inheritance(self)
```

**説明**:

DocGenErrorからの継承確認

*定義場所: tests/test_exceptions.py:99*

---

### test_message_only

**型**: `function`

**シグネチャ**:
```
def test_message_only(self)
```

**説明**:

メッセージのみのテスト

*定義場所: tests/test_exceptions.py:105*

---

### TestFileOperationError

**型**: `class`

**シグネチャ**:
```
class TestFileOperationError
```

**説明**:

FileOperationErrorクラスのテスト

*定義場所: tests/test_exceptions.py:111*

---

### test_inheritance

**型**: `function`

**シグネチャ**:
```
def test_inheritance(self)
```

**説明**:

DocGenErrorからの継承確認

*定義場所: tests/test_exceptions.py:114*

---

### test_with_details

**型**: `function`

**シグネチャ**:
```
def test_with_details(self)
```

**説明**:

詳細付きエラーテスト

*定義場所: tests/test_exceptions.py:120*

---

### TestExceptionHierarchy

**型**: `class`

**シグネチャ**:
```
class TestExceptionHierarchy
```

**説明**:

例外クラスの階層テスト

*定義場所: tests/test_exceptions.py:126*

---

### test_all_exceptions_are_docgen_errors

**型**: `function`

**シグネチャ**:
```
def test_all_exceptions_are_docgen_errors(self)
```

**説明**:

すべての例外がDocGenErrorのサブクラスであることを確認

*定義場所: tests/test_exceptions.py:129*

---

### test_exception_raising

**型**: `function`

**シグネチャ**:
```
def test_exception_raising(self)
```

**説明**:

例外のraiseとcatchテスト

*定義場所: tests/test_exceptions.py:143*

---


## tests/test_generators/test_agents_generator.py

### TestAgentsGenerator

**型**: `class`

**シグネチャ**:
```
class TestAgentsGenerator
```

**説明**:

AgentsGeneratorのテストクラス

*定義場所: tests/test_generators/test_agents_generator.py:11*

---

### test_initialization

**型**: `function`

**シグネチャ**:
```
def test_initialization(self, agents_generator)
```

**説明**:

AgentsGeneratorの初期化テスト

*定義場所: tests/test_generators/test_agents_generator.py:14*

---

### test_generate_agents_md

**型**: `function`

**シグネチャ**:
```
def test_generate_agents_md(self, agents_generator, python_project)
```

**説明**:

AGENTS.md生成テスト

*定義場所: tests/test_generators/test_agents_generator.py:22*

---

### test_should_use_outlines_enabled

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled(temp_project)
```

**説明**:

Outlines使用判定テスト - 有効

*定義場所: tests/test_generators/test_agents_generator.py:51*

---

### test_should_use_outlines_disabled

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_disabled(temp_project)
```

**説明**:

Outlines使用判定テスト - 無効

*定義場所: tests/test_generators/test_agents_generator.py:58*

---

### test_should_use_outlines_default

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_default(temp_project)
```

**説明**:

Outlines使用判定テスト - デフォルト

*定義場所: tests/test_generators/test_agents_generator.py:65*

---

### test_agents_document_creation

**型**: `function`

**シグネチャ**:
```
def test_agents_document_creation()
```

**説明**:

AgentsDocumentの作成テスト

*定義場所: tests/test_generators/test_agents_generator.py:72*

---

### test_convert_structured_data_to_markdown

**型**: `function`

**シグネチャ**:
```
def test_convert_structured_data_to_markdown(temp_project)
```

**説明**:

構造化データからマークダウン変換テスト

*定義場所: tests/test_generators/test_agents_generator.py:96*

---

### test_generate_with_outlines_success

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_success(temp_project)
```

**説明**:

Outlines生成成功テスト

*定義場所: tests/test_generators/test_agents_generator.py:124*

---

### test_generate_with_outlines_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_fallback(temp_project)
```

**説明**:

Outlines生成フォールバックテスト

*定義場所: tests/test_generators/test_agents_generator.py:158*

---

### test_llm_mode_api_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_api_only(temp_project)
```

**説明**:

llm_mode: 'api' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:174*

---

### test_llm_mode_local_only

**型**: `function`

**シグネチャ**:
```
def test_llm_mode_local_only(temp_project)
```

**説明**:

llm_mode: 'local' の場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:190*

---

### test_custom_instructions

**型**: `function`

**シグネチャ**:
```
def test_custom_instructions(temp_project)
```

**説明**:

カスタム指示のテスト

*定義場所: tests/test_generators/test_agents_generator.py:209*

---

### test_anthropic_provider

**型**: `function`

**シグネチャ**:
```
def test_anthropic_provider(temp_project)
```

**説明**:

Anthropicプロバイダーのテスト

*定義場所: tests/test_generators/test_agents_generator.py:228*

---

### test_no_agents_config

**型**: `function`

**シグネチャ**:
```
def test_no_agents_config(temp_project)
```

**説明**:

agentsセクションがない場合のテスト（デフォルト動作）

*定義場所: tests/test_generators/test_agents_generator.py:247*

---

### test_no_build_commands

**型**: `function`

**シグネチャ**:
```
def test_no_build_commands(temp_project)
```

**説明**:

ビルドコマンドがない場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:261*

---

### test_generate_markdown_template_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_template_mode(self, temp_project)
```

**説明**:

マークダウン生成 - templateモードのテスト

*定義場所: tests/test_generators/test_agents_generator.py:273*

---

### test_generate_markdown_llm_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_llm_mode(self, temp_project)
```

**説明**:

マークダウン生成 - llmモードのテスト

*定義場所: tests/test_generators/test_agents_generator.py:294*

---

### test_generate_markdown_hybrid_mode

**型**: `function`

**シグネチャ**:
```
def test_generate_markdown_hybrid_mode(self, temp_project)
```

**説明**:

マークダウン生成 - hybridモードのテスト

*定義場所: tests/test_generators/test_agents_generator.py:311*

---

### test_generate_with_llm_success

**型**: `function`

**シグネチャ**:
```
def test_generate_with_llm_success(self, temp_project)
```

**説明**:

LLMを使用した生成成功テスト

*定義場所: tests/test_generators/test_agents_generator.py:328*

---

### test_generate_with_llm_no_client

**型**: `function`

**シグネチャ**:
```
def test_generate_with_llm_no_client(self, temp_project)
```

**説明**:

LLMクライアントなしの場合のテスト

*定義場所: tests/test_generators/test_agents_generator.py:347*

---

### test_generate_hybrid_success

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_success(self, temp_project)
```

**説明**:

ハイブリッド生成成功テスト

*定義場所: tests/test_generators/test_agents_generator.py:362*

---

### test_create_agents_prompt

**型**: `function`

**シグネチャ**:
```
def test_create_agents_prompt(self, temp_project)
```

**説明**:

AGENTSプロンプト作成テスト

*定義場所: tests/test_generators/test_agents_generator.py:381*

---

### test_convert_structured_data_to_markdown

**型**: `function`

**シグネチャ**:
```
def test_convert_structured_data_to_markdown(self, temp_project)
```

**説明**:

構造化データをマークダウンに変換テスト

*定義場所: tests/test_generators/test_agents_generator.py:406*

---

### test_generate_template_success

**型**: `function`

**シグネチャ**:
```
def test_generate_template_success(self, temp_project)
```

**説明**:

テンプレート生成成功テスト

*定義場所: tests/test_generators/test_agents_generator.py:431*

---

### test_generate_with_outlines_success_agents

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_success_agents(self, mock_create_client, temp_project)
```

**説明**:

Outlinesを使用したAGENTS生成成功テスト

*定義場所: tests/test_generators/test_agents_generator.py:451*

---

### test_generate_with_outlines_fallback_agents

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_fallback_agents(self, mock_create_client, temp_project)
```

**説明**:

Outlines生成失敗時のフォールバックテスト（AGENTS）

*定義場所: tests/test_generators/test_agents_generator.py:473*

---


## tests/test_generators/test_agents_generator_extended.py

### TestAgentsGeneratorExtended

**型**: `class`

**シグネチャ**:
```
class TestAgentsGeneratorExtended
```

**説明**:

AgentsGeneratorの拡張テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:16*

---

### test_initialization_with_absolute_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_absolute_path(self)
```

**説明**:

絶対パスでの初期化テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:19*

---

### test_initialization_with_relative_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_relative_path(self)
```

**説明**:

相対パスでの初期化テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:28*

---

### test_collect_project_info_success

**型**: `function`

**シグネチャ**:
```
def test_collect_project_info_success(self, temp_project)
```

**説明**:

プロジェクト情報収集成功テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:37*

---

### test_collect_project_info_empty

**型**: `function`

**シグネチャ**:
```
def test_collect_project_info_empty(self, temp_project)
```

**説明**:

空プロジェクトの情報収集テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:49*

---

### test_should_use_outlines_integration

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_integration(self, mock_should_use)
```

**説明**:

should_use_outlines統合テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:57*

---

### test_create_agents_prompt_with_dependencies

**型**: `function`

**シグネチャ**:
```
def test_create_agents_prompt_with_dependencies(self, temp_project)
```

**説明**:

依存関係付きプロンプト作成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:69*

---

### test_convert_structured_data_to_markdown_empty_sections

**型**: `function`

**シグネチャ**:
```
def test_convert_structured_data_to_markdown_empty_sections(self, temp_project)
```

**説明**:

空セクションを持つ構造化データの変換テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:92*

---

### test_generate_template_with_minimal_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_minimal_info(self, temp_project)
```

**説明**:

最小情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:113*

---

### test_generate_template_with_full_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_full_info(self, temp_project)
```

**説明**:

完全情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:124*

---

### test_generate_with_llm_invalid_json

**型**: `function`

**シグネチャ**:
```
def test_generate_with_llm_invalid_json(self, mock_create_client, temp_project)
```

**説明**:

無効JSONを返すLLM生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:151*

---

### test_generate_with_llm_exception

**型**: `function`

**シグネチャ**:
```
def test_generate_with_llm_exception(self, mock_create_client, temp_project)
```

**説明**:

LLM生成例外テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:168*

---

### test_generate_hybrid_template_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_template_fallback(self, temp_project)
```

**説明**:

ハイブリッド生成のテンプレートフォールバックテスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:182*

---

### test_generate_hybrid_llm_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_llm_fallback(self, temp_project)
```

**説明**:

ハイブリッド生成のLLMフォールバックテスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:196*

---

### test_generate_hybrid_both_fail

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_both_fail(self, temp_project)
```

**説明**:

ハイブリッド生成の両方失敗テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:212*

---

### test_create_outlines_model_integration

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_integration(self, mock_should_use, mock_create_model, temp_project)
```

**説明**:

Outlinesモデル作成統合テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:228*

---

### test_write_output_file_creation

**型**: `function`

**シグネチャ**:
```
def test_write_output_file_creation(self, temp_project)
```

**説明**:

出力ファイル作成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:244*

---

### test_write_output_file_overwrite

**型**: `function`

**シグネチャ**:
```
def test_write_output_file_overwrite(self, temp_project)
```

**説明**:

出力ファイル上書きテスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:257*

---

### test_generate_with_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_no_languages(self, temp_project)
```

**説明**:

言語なしでの生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:271*

---

### test_generate_with_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_multiple_languages(self, temp_project)
```

**説明**:

複数言語での生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:280*

---

### test_agents_document_model_validation

**型**: `function`

**シグネチャ**:
```
def test_agents_document_model_validation(self)
```

**説明**:

AgentsDocumentモデル検証テスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:295*

---

### test_error_handling_in_generation

**型**: `function`

**シグネチャ**:
```
def test_error_handling_in_generation(self, temp_project)
```

**説明**:

生成時のエラーハンドリングテスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:313*

---

### test_missing_output_directory

**型**: `function`

**シグネチャ**:
```
def test_missing_output_directory(self, temp_project)
```

**説明**:

出力ディレクトリがない場合のテスト

*定義場所: tests/test_generators/test_agents_generator_extended.py:327*

---


## tests/test_generators/test_agents_generator_extended_fixed.py

### TestAgentsGeneratorExtended

**型**: `class`

**シグネチャ**:
```
class TestAgentsGeneratorExtended
```

**説明**:

AgentsGeneratorの拡張テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:16*

---

### test_initialization_with_absolute_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_absolute_path(self)
```

**説明**:

絶対パスでの初期化テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:19*

---

### test_initialization_with_relative_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_relative_path(self)
```

**説明**:

相対パスでの初期化テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:28*

---

### test_convert_structured_data_to_markdown_empty_sections

**型**: `function`

**シグネチャ**:
```
def test_convert_structured_data_to_markdown_empty_sections(self, temp_project)
```

**説明**:

空セクションを持つ構造化データの変換テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:37*

---

### test_generate_template_with_minimal_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_minimal_info(self, temp_project)
```

**説明**:

最小情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:58*

---

### test_generate_template_with_full_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_full_info(self, temp_project)
```

**説明**:

完全情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:69*

---

### test_generate_hybrid_template_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_template_fallback(self, temp_project)
```

**説明**:

ハイブリッド生成のテンプレートフォールバックテスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:92*

---

### test_generate_hybrid_both_fail

**型**: `function`

**シグネチャ**:
```
def test_generate_hybrid_both_fail(self, temp_project)
```

**説明**:

ハイブリッド生成の両方失敗テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:106*

---

### test_generate_with_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_no_languages(self, temp_project)
```

**説明**:

言語なしでの生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:120*

---

### test_generate_with_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_multiple_languages(self, temp_project)
```

**説明**:

複数言語での生成テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:129*

---

### test_agents_document_model_validation

**型**: `function`

**シグネチャ**:
```
def test_agents_document_model_validation(self)
```

**説明**:

AgentsDocumentモデル検証テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:144*

---

### test_missing_output_directory

**型**: `function`

**シグネチャ**:
```
def test_missing_output_directory(self, temp_project)
```

**説明**:

出力ディレクトリがない場合のテスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:162*

---

### test_should_use_outlines_integration

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_integration(self, mock_should_use, temp_project)
```

**説明**:

should_use_outlines統合テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:176*

---

### test_create_llm_prompt_with_project_info

**型**: `function`

**シグネチャ**:
```
def test_create_llm_prompt_with_project_info(self, temp_project)
```

**説明**:

プロジェクト情報付きLLMプロンプト作成テスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:188*

---

### test_error_handling_in_generate_method

**型**: `function`

**シグネチャ**:
```
def test_error_handling_in_generate_method(self, temp_project)
```

**説明**:

generateメソッドのエラーハンドリングテスト

*定義場所: tests/test_generators/test_agents_generator_extended_fixed.py:207*

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

*定義場所: tests/test_generators/test_api_generator.py:12*

---

### test_initialization

**型**: `function`

**シグネチャ**:
```
def test_initialization(self, api_generator)
```

**説明**:

APIGeneratorの初期化テスト

*定義場所: tests/test_generators/test_api_generator.py:15*

---

### test_generate_creates_api_doc

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_api_doc(self, api_generator, python_project, sample_python_file)
```

**説明**:

APIドキュメントが生成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:21*

---

### test_generate_api_doc_content

**型**: `function`

**シグネチャ**:
```
def test_generate_api_doc_content(self, api_generator, python_project, sample_python_file)
```

**説明**:

生成されたAPIドキュメントの内容を確認

*定義場所: tests/test_generators/test_api_generator.py:29*

---

### test_generate_with_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_multiple_languages(self, temp_project, multi_language_project)
```

**説明**:

複数言語のAPI情報が統合されることを確認

*定義場所: tests/test_generators/test_api_generator.py:36*

---

### test_generate_creates_output_directory

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_output_directory(self, temp_project)
```

**説明**:

出力ディレクトリが自動作成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:47*

---

### test_generate_with_no_apis

**型**: `function`

**シグネチャ**:
```
def test_generate_with_no_apis(self, temp_project)
```

**説明**:

APIが見つからない場合でもドキュメントが生成されることを確認

*定義場所: tests/test_generators/test_api_generator.py:60*

---


## tests/test_generators/test_commit_message_generator.py

### TestCommitMessageGenerator

**型**: `class`

**シグネチャ**:
```
class TestCommitMessageGenerator
```

**説明**:

CommitMessageGeneratorクラスのテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:11*

---

### test_initialization

**型**: `function`

**シグネチャ**:
```
def test_initialization(self, temp_project)
```

**説明**:

初期化テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:14*

---

### test_initialization_empty_config

**型**: `function`

**シグネチャ**:
```
def test_initialization_empty_config(self, temp_project)
```

**説明**:

空の設定での初期化テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:23*

---

### test_get_staged_changes_success

**型**: `function`

**シグネチャ**:
```
def test_get_staged_changes_success(self, mock_subprocess, temp_project)
```

**説明**:

ステージング済み変更の取得成功テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:31*

---

### test_get_staged_changes_no_changes

**型**: `function`

**シグネチャ**:
```
def test_get_staged_changes_no_changes(self, mock_subprocess, temp_project)
```

**説明**:

ステージング済み変更がない場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:57*

---

### test_get_staged_changes_git_error

**型**: `function`

**シグネチャ**:
```
def test_get_staged_changes_git_error(self, mock_subprocess, temp_project)
```

**説明**:

Gitコマンドエラーのテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:78*

---

### test_get_staged_changes_no_git

**型**: `function`

**シグネチャ**:
```
def test_get_staged_changes_no_git(self, temp_project, monkeypatch)
```

**説明**:

Gitコマンドが存在しない場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:91*

---

### mock_subprocess_run

**型**: `function`

**シグネチャ**:
```
def mock_subprocess_run()
```

*説明なし*

*定義場所: tests/test_generators/test_commit_message_generator.py:94*

---

### test_create_prompt

**型**: `function`

**シグネチャ**:
```
def test_create_prompt(self, temp_project)
```

**説明**:

プロンプト作成テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:107*

---

### test_generate_success

**型**: `function`

**シグネチャ**:
```
def test_generate_success(self, mock_create_client, temp_project)
```

**説明**:

コミットメッセージ生成成功テスト

*定義場所: tests/test_generators/test_commit_message_generator.py:123*

---

### test_generate_no_staged_changes

**型**: `function`

**シグネチャ**:
```
def test_generate_no_staged_changes(self, mock_create_client, temp_project)
```

**説明**:

ステージング済み変更がない場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:146*

---

### test_generate_no_client

**型**: `function`

**シグネチャ**:
```
def test_generate_no_client(self, mock_create_client, temp_project)
```

**説明**:

LLMクライアント作成失敗のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:161*

---

### test_generate_llm_returns_none

**型**: `function`

**シグネチャ**:
```
def test_generate_llm_returns_none(self, mock_create_client, temp_project)
```

**説明**:

LLMがNoneを返す場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:178*

---

### test_generate_llm_returns_multiline

**型**: `function`

**シグネチャ**:
```
def test_generate_llm_returns_multiline(self, mock_create_client, temp_project)
```

**説明**:

LLMが複数行のメッセージを返す場合のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:197*

---

### test_generate_exception_handling

**型**: `function`

**シグネチャ**:
```
def test_generate_exception_handling(self, mock_create_client, temp_project)
```

**説明**:

例外発生時のテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:218*

---

### test_generate_with_local_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_with_local_fallback(self, mock_create_client, temp_project)
```

**説明**:

ローカルLLMへのフォールバックテスト

*定義場所: tests/test_generators/test_commit_message_generator.py:237*

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

*定義場所: tests/test_generators/test_readme_generator.py:12*

---

### test_generate_creates_readme

**型**: `function`

**シグネチャ**:
```
def test_generate_creates_readme(self, readme_generator, python_project)
```

**説明**:

READMEが生成されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:15*

---

### test_generate_readme_content

**型**: `function`

**シグネチャ**:
```
def test_generate_readme_content(self, readme_generator, python_project)
```

**説明**:

生成されたREADMEの内容を確認

*定義場所: tests/test_generators/test_readme_generator.py:29*

---

### test_should_use_outlines_enabled_readme

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled_readme(self, temp_project)
```

**説明**:

ReadmeGenerator Outlines使用判定テスト - 有効

*定義場所: tests/test_generators/test_readme_generator.py:46*

---

### test_should_use_outlines_disabled_readme

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_disabled_readme(self, temp_project)
```

**説明**:

ReadmeGenerator Outlines使用判定テスト - 無効

*定義場所: tests/test_generators/test_readme_generator.py:55*

---

### test_readme_document_creation

**型**: `function`

**シグネチャ**:
```
def test_readme_document_creation(self)
```

**説明**:

ReadmeDocumentの作成テスト

*定義場所: tests/test_generators/test_readme_generator.py:64*

---

### test_convert_readme_structured_data_to_markdown

**型**: `function`

**シグネチャ**:
```
def test_convert_readme_structured_data_to_markdown(self, temp_project)
```

**説明**:

README構造化データからマークダウン変換テスト

*定義場所: tests/test_generators/test_readme_generator.py:95*

---

### test_generate_with_outlines_readme_success

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_readme_success(self, temp_project)
```

**説明**:

README Outlines生成成功テスト

*定義場所: tests/test_generators/test_readme_generator.py:130*

---

### test_generate_with_outlines_readme_fallback

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_readme_fallback(self, temp_project)
```

**説明**:

README Outlines生成フォールバックテスト

*定義場所: tests/test_generators/test_readme_generator.py:172*

---

### test_extract_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections(self, temp_project)
```

**説明**:

手動セクションが正しく抽出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:187*

---

### test_preserve_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_preserve_manual_sections(self, temp_project)
```

**説明**:

手動セクションが保持されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:208*

---

### test_detect_dependencies_python

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_python(self, python_project)
```

**説明**:

Pythonの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:232*

---

### test_detect_dependencies_python_pep440_specifiers

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_python_pep440_specifiers(self, temp_project)
```

**説明**:

PEP 440の様々なバージョン指定子が正しく処理されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:242*

---

### test_detect_dependencies_javascript

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_javascript(self, javascript_project)
```

**説明**:

JavaScriptの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:290*

---

### test_detect_dependencies_go_multiline_require

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_go_multiline_require(self, temp_project)
```

**説明**:

Goの複数行requireブロックの依存関係が検出されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:300*

---

### test_get_project_structure

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure(self, python_project)
```

**説明**:

プロジェクト構造が生成されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:331*

---

### test_get_project_structure_excludes_files

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure_excludes_files(self, temp_project)
```

**説明**:

プロジェクト構造から除外ファイルが除外されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:341*

---

### test_get_project_structure_excludes_dirs

**型**: `function`

**シグネチャ**:
```
def test_get_project_structure_excludes_dirs(self, temp_project)
```

**説明**:

プロジェクト構造から除外ディレクトリが除外されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:365*

---

### test_generate_with_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_generate_with_manual_sections(self, temp_project)
```

**説明**:

複数の手動セクションが保持されることを確認

*定義場所: tests/test_generators/test_readme_generator.py:393*

---

### test_format_project_info_for_prompt

**型**: `function`

**シグネチャ**:
```
def test_format_project_info_for_prompt(self, temp_project)
```

**説明**:

プロジェクト情報フォーマットテスト

*定義場所: tests/test_generators/test_readme_generator.py:420*

---

### test_format_manual_sections_for_prompt

**型**: `function`

**シグネチャ**:
```
def test_format_manual_sections_for_prompt(self, temp_project)
```

**説明**:

手動セクションのプロンプトフォーマットテスト

*定義場所: tests/test_generators/test_readme_generator.py:442*

---

### test_format_manual_sections_for_prompt_empty

**型**: `function`

**シグネチャ**:
```
def test_format_manual_sections_for_prompt_empty(self, temp_project)
```

**説明**:

空の手動セクションのプロンプトフォーマットテスト

*定義場所: tests/test_generators/test_readme_generator.py:457*

---

### test_convert_readme_structured_data_to_markdown

**型**: `function`

**シグネチャ**:
```
def test_convert_readme_structured_data_to_markdown(self, temp_project)
```

**説明**:

構造化データをマークダウンに変換テスト

*定義場所: tests/test_generators/test_readme_generator.py:466*

---

### test_detect_dependencies_python_new

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_python_new(self, temp_project)
```

**説明**:

Python依存関係検出テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:500*

---

### test_detect_dependencies_javascript_new

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_javascript_new(self, temp_project)
```

**説明**:

JavaScript依存関係検出テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:516*

---

### test_detect_dependencies_go_new

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_go_new(self, temp_project)
```

**説明**:

Go依存関係検出テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:535*

---

### test_detect_dependencies_empty_new

**型**: `function`

**シグネチャ**:
```
def test_detect_dependencies_empty_new(self, temp_project)
```

**説明**:

依存関係なしの場合のテスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:550*

---

### test_generate_with_outlines_success_readme_new

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_success_readme_new(self, mock_create_client, temp_project)
```

**説明**:

Outlinesを使用したREADME生成成功テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:560*

---

### test_generate_with_outlines_fallback_readme_new

**型**: `function`

**シグネチャ**:
```
def test_generate_with_outlines_fallback_readme_new(self, mock_create_client, temp_project)
```

**説明**:

Outlines生成失敗時のフォールバックテスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:587*

---

### test_extract_manual_sections_new

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections_new(self, temp_project)
```

**説明**:

手動セクション抽出テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:600*

---

### test_extract_manual_sections_no_manual_new

**型**: `function`

**シグネチャ**:
```
def test_extract_manual_sections_no_manual_new(self, temp_project)
```

**説明**:

手動セクションなしの場合のテスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:627*

---

### test_preserve_manual_sections_new

**型**: `function`

**シグネチャ**:
```
def test_preserve_manual_sections_new(self, temp_project)
```

**説明**:

手動セクション保持テスト（新規）

*定義場所: tests/test_generators/test_readme_generator.py:638*

---


## tests/test_generators/test_readme_generator_extended.py

### TestReadmeGeneratorExtended

**型**: `class`

**シグネチャ**:
```
class TestReadmeGeneratorExtended
```

**説明**:

ReadmeGeneratorの拡張テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:16*

---

### test_initialization_with_absolute_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_absolute_path(self)
```

**説明**:

絶対パスでの初期化テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:19*

---

### test_initialization_with_relative_path

**型**: `function`

**シグネチャ**:
```
def test_initialization_with_relative_path(self)
```

**説明**:

相対パスでの初期化テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:28*

---

### test_convert_readme_structured_data_to_markdown_empty_sections

**型**: `function`

**シグネチャ**:
```
def test_convert_readme_structured_data_to_markdown_empty_sections(self, temp_project)
```

**説明**:

空セクションを持つ構造化データの変換テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:37*

---

### test_generate_template_with_minimal_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_minimal_info(self, temp_project)
```

**説明**:

最小情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:60*

---

### test_generate_template_with_full_info

**型**: `function`

**シグネチャ**:
```
def test_generate_template_with_full_info(self, temp_project)
```

**説明**:

完全情報でのテンプレート生成テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:71*

---

### test_dependency_detection_python

**型**: `function`

**シグネチャ**:
```
def test_dependency_detection_python(self, temp_project)
```

**説明**:

Python依存関係検出テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:95*

---

### test_dependency_detection_javascript

**型**: `function`

**シグネチャ**:
```
def test_dependency_detection_javascript(self, temp_project)
```

**説明**:

JavaScript依存関係検出テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:112*

---

### test_dependency_detection_go

**型**: `function`

**シグネチャ**:
```
def test_dependency_detection_go(self, temp_project)
```

**説明**:

Go依存関係検出テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:126*

---

### test_manual_sections_extraction

**型**: `function`

**シグネチャ**:
```
def test_manual_sections_extraction(self, temp_project)
```

**説明**:

手動セクション抽出テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:139*

---

### test_manual_sections_preservation

**型**: `function`

**シグネチャ**:
```
def test_manual_sections_preservation(self, temp_project)
```

**説明**:

手動セクション保持テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:169*

---

### test_format_project_info_for_readme_prompt

**型**: `function`

**シグネチャ**:
```
def test_format_project_info_for_readme_prompt(self, temp_project)
```

**説明**:

READMEプロンプト用プロジェクト情報フォーマットテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:187*

---

### test_format_manual_sections_for_prompt

**型**: `function`

**シグネチャ**:
```
def test_format_manual_sections_for_prompt(self, temp_project)
```

**説明**:

手動セクションのプロンプトフォーマットテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:208*

---

### test_generate_with_no_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_no_languages(self, temp_project)
```

**説明**:

言語なしでの生成テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:222*

---

### test_generate_with_multiple_languages

**型**: `function`

**シグネチャ**:
```
def test_generate_with_multiple_languages(self, temp_project)
```

**説明**:

複数言語での生成テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:231*

---

### test_readme_document_model_validation

**型**: `function`

**シグネチャ**:
```
def test_readme_document_model_validation(self)
```

**説明**:

ReadmeDocumentモデル検証テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:246*

---

### test_error_handling_in_generation

**型**: `function`

**シグネチャ**:
```
def test_error_handling_in_generation(self, temp_project)
```

**説明**:

生成時のエラーハンドリングテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:264*

---

### test_missing_output_directory

**型**: `function`

**シグネチャ**:
```
def test_missing_output_directory(self, temp_project)
```

**説明**:

出力ディレクトリがない場合のテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:276*

---

### test_empty_manual_sections_handling

**型**: `function`

**シグネチャ**:
```
def test_empty_manual_sections_handling(self, temp_project)
```

**説明**:

空の手動セクション処理テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:289*

---

### test_malformed_manual_sections_handling

**型**: `function`

**シグネチャ**:
```
def test_malformed_manual_sections_handling(self, temp_project)
```

**説明**:

不正な形式の手動セクション処理テスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:311*

---

### test_dependency_detection_no_files

**型**: `function`

**シグネチャ**:
```
def test_dependency_detection_no_files(self, temp_project)
```

**説明**:

依存関係ファイルがない場合のテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:331*

---

### test_dependency_detection_empty_files

**型**: `function`

**シグネチャ**:
```
def test_dependency_detection_empty_files(self, temp_project)
```

**説明**:

空の依存関係ファイルの場合のテスト

*定義場所: tests/test_generators/test_readme_generator_extended.py:339*

---


## tests/test_init.py

### test_version_info

**型**: `function`

**シグネチャ**:
```
def test_version_info()
```

**説明**:

バージョン情報のテスト

*定義場所: tests/test_init.py:8*

---

### test_main_exports

**型**: `function`

**シグネチャ**:
```
def test_main_exports()
```

**説明**:

メインエクスポートのテスト

*定義場所: tests/test_init.py:17*

---

### test_all_exports

**型**: `function`

**シグネチャ**:
```
def test_all_exports()
```

**説明**:

__all__エクスポートのテスト

*定義場所: tests/test_init.py:34*

---

### test_package_import

**型**: `function`

**シグネチャ**:
```
def test_package_import()
```

**説明**:

パッケージ全体のインポートテスト

*定義場所: tests/test_init.py:51*

---

### test_docstring

**型**: `function`

**シグネチャ**:
```
def test_docstring()
```

**説明**:

パッケージのdocstringテスト

*定義場所: tests/test_init.py:68*

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

*定義場所: tests/test_integration.py:63*

---

### test_readme_preserves_manual_sections

**型**: `function`

**シグネチャ**:
```
def test_readme_preserves_manual_sections(self, temp_project)
```

**説明**:

READMEの手動セクションが保持されることを統合テストで確認

*定義場所: tests/test_integration.py:71*

---

### test_api_doc_includes_all_languages

**型**: `function`

**シグネチャ**:
```
def test_api_doc_includes_all_languages(self, multi_language_project)
```

**説明**:

複数言語のAPI情報が統合されることを確認

*定義場所: tests/test_integration.py:107*

---

### test_full_pipeline_execution

**型**: `function`

**シグネチャ**:
```
def test_full_pipeline_execution(self, temp_project)
```

**説明**:

完全なパイプライン実行テスト

*定義場所: tests/test_integration.py:152*

---

### test_performance_large_project

**型**: `function`

**シグネチャ**:
```
def test_performance_large_project(self, temp_project)
```

**説明**:

大規模プロジェクトのパフォーマンステスト

*定義場所: tests/test_integration.py:200*

---

### test_memory_usage_monitoring

**型**: `function`

**シグネチャ**:
```
def test_memory_usage_monitoring(self, temp_project)
```

**説明**:

メモリ使用量の監視テスト

*定義場所: tests/test_integration.py:232*

---

### test_error_recovery_and_fallbacks

**型**: `function`

**シグネチャ**:
```
def test_error_recovery_and_fallbacks(self, temp_project)
```

**説明**:

エラー回復とフォールバックのテスト

*定義場所: tests/test_integration.py:260*

---

### test_cross_language_integration

**型**: `function`

**シグネチャ**:
```
def test_cross_language_integration(self, temp_project)
```

**説明**:

クロス言語統合テスト

*定義場所: tests/test_integration.py:279*

---

### test_configuration_persistence

**型**: `function`

**シグネチャ**:
```
def test_configuration_persistence(self, temp_project)
```

**説明**:

設定の永続性テスト

*定義場所: tests/test_integration.py:316*

---

### test_idempotent_operations

**型**: `function`

**シグネチャ**:
```
def test_idempotent_operations(self, temp_project)
```

**説明**:

冪等性操作テスト（同じ操作を複数回実行しても結果が同じ）

*定義場所: tests/test_integration.py:337*

---

### test_backward_compatibility

**型**: `function`

**シグネチャ**:
```
def test_backward_compatibility(self, temp_project)
```

**説明**:

後方互換性テスト

*定義場所: tests/test_integration.py:362*

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

*定義場所: tests/test_parsers/test_base_parser.py:11*

---

### test_parse_project_exclude_dirs

**型**: `function`

**シグネチャ**:
```
def test_parse_project_exclude_dirs(self, temp_project)
```

**説明**:

除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_parsers/test_base_parser.py:14*

---

### test_parse_project_custom_exclude_dirs

**型**: `function`

**シグネチャ**:
```
def test_parse_project_custom_exclude_dirs(self, temp_project)
```

**説明**:

カスタム除外ディレクトリが正しく除外されることを確認

*定義場所: tests/test_parsers/test_base_parser.py:29*

---

### test_parse_project_parallel

**型**: `function`

**シグネチャ**:
```
def test_parse_project_parallel(self, temp_project)
```

**説明**:

並列処理でプロジェクトを解析

*定義場所: tests/test_parsers/test_base_parser.py:41*

---

### test_parse_project_sequential

**型**: `function`

**シグネチャ**:
```
def test_parse_project_sequential(self, temp_project)
```

**説明**:

逐次処理でプロジェクトを解析

*定義場所: tests/test_parsers/test_base_parser.py:52*

---

### test_parse_project_few_files_sequential

**型**: `function`

**シグネチャ**:
```
def test_parse_project_few_files_sequential(self, temp_project)
```

**説明**:

ファイル数が少ない場合は逐次処理になることを確認

*定義場所: tests/test_parsers/test_base_parser.py:61*

---

### test_parse_file_safe_with_error

**型**: `function`

**シグネチャ**:
```
def test_parse_file_safe_with_error(self, temp_project)
```

**説明**:

エラーが発生した場合の安全な処理

*定義場所: tests/test_parsers/test_base_parser.py:72*

---

### test_parse_project_symlink_skipped

**型**: `function`

**シグネチャ**:
```
def test_parse_project_symlink_skipped(self, temp_project)
```

**説明**:

シンボリックリンクがスキップされることを確認

*定義場所: tests/test_parsers/test_base_parser.py:84*

---

### test_parse_project_permission_error

**型**: `function`

**シグネチャ**:
```
def test_parse_project_permission_error(self, temp_project)
```

**説明**:

権限エラーが発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:95*

---

### test_parse_project_max_workers

**型**: `function`

**シグネチャ**:
```
def test_parse_project_max_workers(self, temp_project)
```

**説明**:

max_workersが指定された場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:106*

---

### test_parse_project_parallel_with_exception

**型**: `function`

**シグネチャ**:
```
def test_parse_project_parallel_with_exception(self, temp_project)
```

**説明**:

並列処理で例外が発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:116*

---

### test_parse_file_safe_exception_handling

**型**: `function`

**シグネチャ**:
```
def test_parse_file_safe_exception_handling(self, temp_project)
```

**説明**:

_parse_file_safeで例外が発生した場合の処理

*定義場所: tests/test_parsers/test_base_parser.py:133*

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

*定義場所: tests/test_parsers/test_generic_parser.py:13*

---

### test_parse_file_rust

**型**: `function`

**シグネチャ**:
```
def test_parse_file_rust(self, temp_project)
```

**説明**:

Rustファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:16*

---

### test_parse_file_java

**型**: `function`

**シグネチャ**:
```
def test_parse_file_java(self, temp_project)
```

**説明**:

Javaファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:31*

---

### test_parse_file_ruby

**型**: `function`

**シグネチャ**:
```
def test_parse_file_ruby(self, temp_project)
```

**説明**:

Rubyファイルを解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:55*

---

### test_get_supported_extensions_rust

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions_rust(self)
```

**説明**:

Rustの拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_generic_parser.py:73*

---

### test_get_supported_extensions_java

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions_java(self)
```

**説明**:

Javaの拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_generic_parser.py:80*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, temp_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_generic_parser.py:87*

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

*定義場所: tests/test_parsers/test_js_parser.py:13*

---

### test_parse_file_with_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_jsdoc(self, sample_javascript_file)
```

**説明**:

JSDocコメントを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:16*

---

### test_parse_file_extracts_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_jsdoc(self, sample_javascript_file)
```

**説明**:

JSDocコメントが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_js_parser.py:26*

---

### test_parse_file_with_class

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_class(self, sample_javascript_file)
```

**説明**:

クラスを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:38*

---

### test_parse_file_extracts_signature

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_signature(self, sample_javascript_file)
```

**説明**:

シグネチャが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_js_parser.py:47*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, javascript_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:57*

---

### test_get_supported_extensions

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions(self)
```

**説明**:

サポートする拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_js_parser.py:64*

---

### test_parse_file_without_jsdoc

**型**: `function`

**シグネチャ**:
```
def test_parse_file_without_jsdoc(self, temp_project)
```

**説明**:

JSDocなしの関数も解析できることを確認

*定義場所: tests/test_parsers/test_js_parser.py:74*

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

*定義場所: tests/test_parsers/test_python_parser.py:13*

---

### test_parse_file_with_function

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_function(self, sample_python_file)
```

**説明**:

関数を含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:16*

---

### test_parse_file_with_class

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_class(self, sample_python_file)
```

**説明**:

クラスを含むファイルを解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:29*

---

### test_parse_file_extracts_signature

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_signature(self, sample_python_file)
```

**説明**:

シグネチャが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_python_parser.py:39*

---

### test_parse_file_extracts_docstring

**型**: `function`

**シグネチャ**:
```
def test_parse_file_extracts_docstring(self, sample_python_file)
```

**説明**:

docstringが正しく抽出されることを確認

*定義場所: tests/test_parsers/test_python_parser.py:49*

---

### test_parse_file_includes_line_number

**型**: `function`

**シグネチャ**:
```
def test_parse_file_includes_line_number(self, sample_python_file)
```

**説明**:

行番号が含まれることを確認

*定義場所: tests/test_parsers/test_python_parser.py:59*

---

### test_parse_project

**型**: `function`

**シグネチャ**:
```
def test_parse_project(self, python_project)
```

**説明**:

プロジェクト全体を解析できることを確認

*定義場所: tests/test_parsers/test_python_parser.py:67*

---

### test_parse_file_skips_private_functions

**型**: `function`

**シグネチャ**:
```
def test_parse_file_skips_private_functions(self, temp_project)
```

**説明**:

プライベート関数（_で始まる）がスキップされることを確認

*定義場所: tests/test_parsers/test_python_parser.py:76*

---

### test_get_supported_extensions

**型**: `function`

**シグネチャ**:
```
def test_get_supported_extensions(self)
```

**説明**:

サポートする拡張子が正しいことを確認

*定義場所: tests/test_parsers/test_python_parser.py:94*

---

### test_parse_file_with_syntax_error

**型**: `function`

**シグネチャ**:
```
def test_parse_file_with_syntax_error(self, temp_project)
```

**説明**:

構文エラーがあるファイルでもエラーが発生しないことを確認

*定義場所: tests/test_parsers/test_python_parser.py:102*

---


## tests/test_project_info_collector.py

### TestProjectInfoCollector

**型**: `class`

**シグネチャ**:
```
class TestProjectInfoCollector
```

**説明**:

ProjectInfoCollectorのテストクラス

*定義場所: tests/test_project_info_collector.py:8*

---

### test_init

**型**: `function`

**シグネチャ**:
```
def test_init(self, temp_project)
```

**説明**:

初期化テスト

*定義場所: tests/test_project_info_collector.py:11*

---

### test_collect_all

**型**: `function`

**シグネチャ**:
```
def test_collect_all(self, temp_project)
```

**説明**:

全情報収集テスト

*定義場所: tests/test_project_info_collector.py:16*

---

### test_collect_build_commands_from_script

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_from_script(self, temp_project)
```

**説明**:

スクリプトからのビルドコマンド収集

*定義場所: tests/test_project_info_collector.py:34*

---

### test_collect_build_commands_no_script

**型**: `function`

**シグネチャ**:
```
def test_collect_build_commands_no_script(self, temp_project)
```

**説明**:

スクリプトが存在しない場合

*定義場所: tests/test_project_info_collector.py:52*

---

### test_collect_test_commands_from_script

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_from_script(self, temp_project)
```

**説明**:

スクリプトからのテストコマンド収集

*定義場所: tests/test_project_info_collector.py:59*

---

### test_collect_test_commands_no_script

**型**: `function`

**シグネチャ**:
```
def test_collect_test_commands_no_script(self, temp_project)
```

**説明**:

テストスクリプトが存在しない場合

*定義場所: tests/test_project_info_collector.py:76*

---

### test_collect_dependencies_python

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_python(self, temp_project)
```

**説明**:

Python依存関係の収集

*定義場所: tests/test_project_info_collector.py:83*

---

### test_collect_dependencies_nodejs

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_nodejs(self, temp_project)
```

**説明**:

Node.js依存関係の収集

*定義場所: tests/test_project_info_collector.py:97*

---

### test_collect_dependencies_go

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_go(self, temp_project)
```

**説明**:

Go依存関係の収集

*定義場所: tests/test_project_info_collector.py:115*

---

### test_collect_dependencies_no_files

**型**: `function`

**シグネチャ**:
```
def test_collect_dependencies_no_files(self, temp_project)
```

**説明**:

依存関係ファイルが存在しない場合

*定義場所: tests/test_project_info_collector.py:135*

---

### test_collect_coding_standards_with_pyproject

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_with_pyproject(self, temp_project)
```

**説明**:

pyproject.tomlからのコーディング規約収集

*定義場所: tests/test_project_info_collector.py:142*

---

### test_collect_coding_standards_no_files

**型**: `function`

**シグネチャ**:
```
def test_collect_coding_standards_no_files(self, temp_project)
```

**説明**:

コーディング規約ファイルが存在しない場合

*定義場所: tests/test_project_info_collector.py:159*

---

### test_collect_ci_cd_info_with_github_actions

**型**: `function`

**シグネチャ**:
```
def test_collect_ci_cd_info_with_github_actions(self, temp_project)
```

**説明**:

GitHub ActionsからのCI/CD情報収集

*定義場所: tests/test_project_info_collector.py:166*

---

### test_collect_ci_cd_info_no_files

**型**: `function`

**シグネチャ**:
```
def test_collect_ci_cd_info_no_files(self, temp_project)
```

**説明**:

CI/CDファイルが存在しない場合

*定義場所: tests/test_project_info_collector.py:187*

---

### test_collect_project_structure

**型**: `function`

**シグネチャ**:
```
def test_collect_project_structure(self, temp_project)
```

**説明**:

プロジェクト構造の収集

*定義場所: tests/test_project_info_collector.py:194*

---


## tests/test_utils.py

### create_sample_python_file

**型**: `function`

**シグネチャ**:
```
def create_sample_python_file(project_root: Path, filename: str) -> Path
```

**説明**:

サンプルPythonファイルを作成

Args:
    project_root: プロジェクトルート
    filename: ファイル名

Returns:
    Path: 作成されたファイルのパス

*定義場所: tests/test_utils.py:12*

---

### create_sample_javascript_file

**型**: `function`

**シグネチャ**:
```
def create_sample_javascript_file(project_root: Path, filename: str) -> Path
```

**説明**:

サンプルJavaScriptファイルを作成

Args:
    project_root: プロジェクトルート
    filename: ファイル名

Returns:
    Path: 作成されたファイルのパス

*定義場所: tests/test_utils.py:66*

---

### create_python_project_structure

**型**: `function`

**シグネチャ**:
```
def create_python_project_structure(project_root: Path) -> None
```

**説明**:

Pythonプロジェクトの基本構造を作成

Args:
    project_root: プロジェクトルート

*定義場所: tests/test_utils.py:121*

---

### create_javascript_project_structure

**型**: `function`

**シグネチャ**:
```
def create_javascript_project_structure(project_root: Path) -> None
```

**説明**:

JavaScriptプロジェクトの基本構造を作成

Args:
    project_root: プロジェクトルート

*定義場所: tests/test_utils.py:161*

---

### create_go_project_structure

**型**: `function`

**シグネチャ**:
```
def create_go_project_structure(project_root: Path) -> None
```

**説明**:

Goプロジェクトの基本構造を作成

Args:
    project_root: プロジェクトルート

*定義場所: tests/test_utils.py:181*

---

### create_config_file

**型**: `function`

**シグネチャ**:
```
def create_config_file(project_root: Path, config: dict[str, Any], filename: str) -> Path
```

**説明**:

設定ファイルを作成

Args:
    project_root: プロジェクトルート
    config: 設定内容
    filename: ファイル名

Returns:
    Path: 作成されたファイルのパス

*定義場所: tests/test_utils.py:235*

---

### assert_file_exists_and_not_empty

**型**: `function`

**シグネチャ**:
```
def assert_file_exists_and_not_empty(file_path: Path) -> None
```

**説明**:

ファイルが存在し、空でないことを確認

Args:
    file_path: 確認するファイルのパス

*定義場所: tests/test_utils.py:259*

---

### assert_file_contains_text

**型**: `function`

**シグネチャ**:
```
def assert_file_contains_text(file_path: Path) -> None
```

**説明**:

ファイルが指定されたテキストを含むことを確認

Args:
    file_path: 確認するファイルのパス
    texts: 含まれるべきテキスト

*定義場所: tests/test_utils.py:271*

---

### assert_file_not_contains_text

**型**: `function`

**シグネチャ**:
```
def assert_file_not_contains_text(file_path: Path) -> None
```

**説明**:

ファイルが指定されたテキストを含まないことを確認

Args:
    file_path: 確認するファイルのパス
    texts: 含まれないべきテキスト

*定義場所: tests/test_utils.py:284*

---

### create_test_data_factory

**型**: `function`

**シグネチャ**:
```
def create_test_data_factory()
```

**説明**:

テストデータ作成のファクトリ関数を返す

Returns:
    dict: 言語ごとのデータ作成関数

*定義場所: tests/test_utils.py:297*

---


## tests/test_utils/test_cache.py

### TestCacheManagerInit

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerInit
```

**説明**:

CacheManager初期化のテスト

*定義場所: tests/test_utils/test_cache.py:12*

---

### test_init_with_defaults

**型**: `function`

**シグネチャ**:
```
def test_init_with_defaults(self, tmp_path)
```

**説明**:

デフォルト設定での初期化

*定義場所: tests/test_utils/test_cache.py:15*

---

### test_init_with_custom_cache_dir

**型**: `function`

**シグネチャ**:
```
def test_init_with_custom_cache_dir(self, tmp_path)
```

**説明**:

カスタムキャッシュディレクトリでの初期化

*定義場所: tests/test_utils/test_cache.py:27*

---

### test_init_disabled

**型**: `function`

**シグネチャ**:
```
def test_init_disabled(self, tmp_path)
```

**説明**:

キャッシュ無効化での初期化

*定義場所: tests/test_utils/test_cache.py:35*

---

### test_init_creates_cache_dir

**型**: `function`

**シグネチャ**:
```
def test_init_creates_cache_dir(self, tmp_path)
```

**説明**:

キャッシュディレクトリが作成されることを確認

*定義場所: tests/test_utils/test_cache.py:42*

---

### TestCacheManagerFileHash

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerFileHash
```

**説明**:

ファイルハッシュ計算のテスト

*定義場所: tests/test_utils/test_cache.py:53*

---

### test_get_file_hash

**型**: `function`

**シグネチャ**:
```
def test_get_file_hash(self, tmp_path)
```

**説明**:

ファイルハッシュの計算

*定義場所: tests/test_utils/test_cache.py:56*

---

### test_get_file_hash_nonexistent_file

**型**: `function`

**シグネチャ**:
```
def test_get_file_hash_nonexistent_file(self, tmp_path)
```

**説明**:

存在しないファイルのハッシュ計算

*定義場所: tests/test_utils/test_cache.py:67*

---

### TestCacheManagerCacheKey

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerCacheKey
```

**説明**:

キャッシュキー生成のテスト

*定義場所: tests/test_utils/test_cache.py:77*

---

### test_get_cache_key_absolute_path

**型**: `function`

**シグネチャ**:
```
def test_get_cache_key_absolute_path(self, tmp_path)
```

**説明**:

絶対パスでのキャッシュキー生成

*定義場所: tests/test_utils/test_cache.py:80*

---

### test_get_cache_key_relative_path

**型**: `function`

**シグネチャ**:
```
def test_get_cache_key_relative_path(self, tmp_path)
```

**説明**:

相対パスでのキャッシュキー生成

*定義場所: tests/test_utils/test_cache.py:89*

---

### test_get_cache_key_outside_project

**型**: `function`

**シグネチャ**:
```
def test_get_cache_key_outside_project(self, tmp_path)
```

**説明**:

プロジェクト外のファイルのキャッシュキー生成

*定義場所: tests/test_utils/test_cache.py:98*

---

### TestCacheManagerCacheOperations

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerCacheOperations
```

**説明**:

キャッシュ操作のテスト

*定義場所: tests/test_utils/test_cache.py:108*

---

### test_get_cached_result_disabled

**型**: `function`

**シグネチャ**:
```
def test_get_cached_result_disabled(self, tmp_path)
```

**説明**:

キャッシュ無効時の結果取得

*定義場所: tests/test_utils/test_cache.py:111*

---

### test_get_cached_result_file_not_exists

**型**: `function`

**シグネチャ**:
```
def test_get_cached_result_file_not_exists(self, tmp_path)
```

**説明**:

ファイルが存在しない場合の結果取得

*定義場所: tests/test_utils/test_cache.py:118*

---

### test_get_cached_result_cache_hit

**型**: `function`

**シグネチャ**:
```
def test_get_cached_result_cache_hit(self, tmp_path)
```

**説明**:

キャッシュヒット時の結果取得

*定義場所: tests/test_utils/test_cache.py:125*

---

### test_get_cached_result_cache_miss_hash_changed

**型**: `function`

**シグネチャ**:
```
def test_get_cached_result_cache_miss_hash_changed(self, tmp_path)
```

**説明**:

ハッシュが変わった場合のキャッシュミス

*定義場所: tests/test_utils/test_cache.py:143*

---

### test_set_cached_result

**型**: `function`

**シグネチャ**:
```
def test_set_cached_result(self, tmp_path)
```

**説明**:

結果のキャッシュ保存

*定義場所: tests/test_utils/test_cache.py:164*

---

### test_set_cached_result_disabled

**型**: `function`

**シグネチャ**:
```
def test_set_cached_result_disabled(self, tmp_path)
```

**説明**:

キャッシュ無効時の保存（何もしない）

*定義場所: tests/test_utils/test_cache.py:183*

---

### test_clear_cache

**型**: `function`

**シグネチャ**:
```
def test_clear_cache(self, tmp_path)
```

**説明**:

キャッシュクリア

*定義場所: tests/test_utils/test_cache.py:193*

---

### test_invalidate_file

**型**: `function`

**シグネチャ**:
```
def test_invalidate_file(self, tmp_path)
```

**説明**:

ファイルキャッシュの無効化

*定義場所: tests/test_utils/test_cache.py:204*

---

### test_invalidate_file_all_parsers

**型**: `function`

**シグネチャ**:
```
def test_invalidate_file_all_parsers(self, tmp_path)
```

**説明**:

全パーサータイプでのファイルキャッシュ無効化

*定義場所: tests/test_utils/test_cache.py:223*

---

### TestCacheManagerStats

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerStats
```

**説明**:

キャッシュ統計情報のテスト

*定義場所: tests/test_utils/test_cache.py:240*

---

### test_get_cache_stats_enabled

**型**: `function`

**シグネチャ**:
```
def test_get_cache_stats_enabled(self, tmp_path)
```

**説明**:

キャッシュ有効時の統計情報

*定義場所: tests/test_utils/test_cache.py:243*

---

### test_get_cache_stats_disabled

**型**: `function`

**シグネチャ**:
```
def test_get_cache_stats_disabled(self, tmp_path)
```

**説明**:

キャッシュ無効時の統計情報

*定義場所: tests/test_utils/test_cache.py:258*

---

### TestCacheManagerSaveLoad

**型**: `class`

**シグネチャ**:
```
class TestCacheManagerSaveLoad
```

**説明**:

キャッシュの保存・読み込みテスト

*定義場所: tests/test_utils/test_cache.py:269*

---

### test_save_cache

**型**: `function`

**シグネチャ**:
```
def test_save_cache(self, tmp_path)
```

**説明**:

キャッシュの保存

*定義場所: tests/test_utils/test_cache.py:272*

---

### test_save_cache_io_error

**型**: `function`

**シグネチャ**:
```
def test_save_cache_io_error(self, mock_file, tmp_path)
```

**説明**:

保存時のIOエラー処理

*定義場所: tests/test_utils/test_cache.py:295*

---

### test_load_cache_file_exists

**型**: `function`

**シグネチャ**:
```
def test_load_cache_file_exists(self, tmp_path)
```

**説明**:

キャッシュファイルが存在する場合の読み込み

*定義場所: tests/test_utils/test_cache.py:307*

---

### test_load_cache_invalid_json

**型**: `function`

**シグネチャ**:
```
def test_load_cache_invalid_json(self, tmp_path)
```

**説明**:

無効なJSONファイルの場合の読み込み

*定義場所: tests/test_utils/test_cache.py:320*

---

### test_load_cache_file_not_exists

**型**: `function`

**シグネチャ**:
```
def test_load_cache_file_not_exists(self, tmp_path)
```

**説明**:

キャッシュファイルが存在しない場合

*定義場所: tests/test_utils/test_cache.py:332*

---


## tests/test_utils/test_llm_client.py

### MockLLMClient

**型**: `class`

**シグネチャ**:
```
class MockLLMClient(BaseLLMClient)
```

**説明**:

テスト用のBaseLLMClient実装

*定義場所: tests/test_utils/test_llm_client.py:17*

---

### generate

**型**: `function`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: Optional[str]) -> Optional[str]
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:20*

---

### TestBaseLLMClient

**型**: `class`

**シグネチャ**:
```
class TestBaseLLMClient
```

**説明**:

BaseLLMClientのテスト

*定義場所: tests/test_utils/test_llm_client.py:29*

---

### test_init_with_defaults

**型**: `function`

**シグネチャ**:
```
def test_init_with_defaults(self)
```

**説明**:

デフォルト設定での初期化

*定義場所: tests/test_utils/test_llm_client.py:32*

---

### test_init_with_custom_config

**型**: `function`

**シグネチャ**:
```
def test_init_with_custom_config(self)
```

**説明**:

カスタム設定での初期化

*定義場所: tests/test_utils/test_llm_client.py:42*

---

### test_create_outlines_model_not_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_not_available(self)
```

**説明**:

Outlinesが利用できない場合

*定義場所: tests/test_utils/test_llm_client.py:51*

---

### test_create_outlines_model_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_available(self)
```

**説明**:

Outlinesが利用可能な場合

*定義場所: tests/test_utils/test_llm_client.py:63*

---

### test_create_outlines_model_internal_exception

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_internal_exception(self)
```

**説明**:

Outlines作成時の例外処理

*定義場所: tests/test_utils/test_llm_client.py:74*

---

### TestOpenAIClient

**型**: `class`

**シグネチャ**:
```
class TestOpenAIClient
```

**説明**:

OpenAIClientのテスト

*定義場所: tests/test_utils/test_llm_client.py:90*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client.py:93*

---

### mock_import

**型**: `function`

**シグネチャ**:
```
def mock_import(name)
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:103*

---

### test_init_missing_openai

**型**: `function`

**シグネチャ**:
```
def test_init_missing_openai(self)
```

**説明**:

openaiパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client.py:117*

---

### test_init_openai_error

**型**: `function`

**シグネチャ**:
```
def test_init_openai_error(self)
```

**説明**:

OpenAIクライアント初期化エラー

*定義場所: tests/test_utils/test_llm_client.py:135*

---

### test_generate_success

**型**: `function`

**シグネチャ**:
```
def test_generate_success(self)
```

**説明**:

正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client.py:149*

---

### mock_import

**型**: `function`

**シグネチャ**:
```
def mock_import(name)
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:155*

---

### test_generate_with_system_prompt

**型**: `function`

**シグネチャ**:
```
def test_generate_with_system_prompt(self)
```

**説明**:

システムプロンプト付きの生成

*定義場所: tests/test_utils/test_llm_client.py:174*

---

### test_generate_no_choices

**型**: `function`

**シグネチャ**:
```
def test_generate_no_choices(self)
```

**説明**:

レスポンスにchoicesがない場合

*定義場所: tests/test_utils/test_llm_client.py:193*

---

### test_generate_exception

**型**: `function`

**シグネチャ**:
```
def test_generate_exception(self)
```

**説明**:

API呼び出し時の例外

*定義場所: tests/test_utils/test_llm_client.py:206*

---

### TestAnthropicClient

**型**: `class`

**シグネチャ**:
```
class TestAnthropicClient
```

**説明**:

AnthropicClientのテスト

*定義場所: tests/test_utils/test_llm_client.py:218*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self, mock_anthropic)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client.py:222*

---

### test_init_missing_anthropic

**型**: `function`

**シグネチャ**:
```
def test_init_missing_anthropic(self, mock_anthropic)
```

**説明**:

anthropicパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client.py:233*

---

### test_generate_success

**型**: `function`

**シグネチャ**:
```
def test_generate_success(self, mock_anthropic)
```

**説明**:

正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client.py:242*

---

### test_generate_no_content

**型**: `function`

**シグネチャ**:
```
def test_generate_no_content(self, mock_anthropic)
```

**説明**:

レスポンスにcontentがない場合

*定義場所: tests/test_utils/test_llm_client.py:257*

---

### TestLocalLLMClient

**型**: `class`

**シグネチャ**:
```
class TestLocalLLMClient
```

**説明**:

LocalLLMClientのテスト

*定義場所: tests/test_utils/test_llm_client.py:271*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self, mock_httpx)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client.py:275*

---

### test_init_missing_httpx

**型**: `function`

**シグネチャ**:
```
def test_init_missing_httpx(self, mock_httpx)
```

**説明**:

httpxパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client.py:289*

---

### test_generate_ollama_success

**型**: `function`

**シグネチャ**:
```
def test_generate_ollama_success(self, mock_httpx)
```

**説明**:

Ollamaでの正常な生成

*定義場所: tests/test_utils/test_llm_client.py:298*

---

### test_generate_ollama_with_system_prompt

**型**: `function`

**シグネチャ**:
```
def test_generate_ollama_with_system_prompt(self, mock_httpx)
```

**説明**:

システムプロンプト付きのOllama生成

*定義場所: tests/test_utils/test_llm_client.py:314*

---

### test_generate_openai_compatible_success

**型**: `function`

**シグネチャ**:
```
def test_generate_openai_compatible_success(self, mock_httpx)
```

**説明**:

OpenAI互換APIでの生成

*定義場所: tests/test_utils/test_llm_client.py:332*

---

### test_generate_api_error

**型**: `function`

**シグネチャ**:
```
def test_generate_api_error(self, mock_httpx)
```

**説明**:

APIエラーの場合

*定義場所: tests/test_utils/test_llm_client.py:349*

---

### test_generate_unsupported_provider

**型**: `function`

**シグネチャ**:
```
def test_generate_unsupported_provider(self, mock_httpx)
```

**説明**:

サポートされていないプロバイダー

*定義場所: tests/test_utils/test_llm_client.py:364*

---

### TestLLMClientFactory

**型**: `class`

**シグネチャ**:
```
class TestLLMClientFactory
```

**説明**:

LLMClientFactoryのテスト

*定義場所: tests/test_utils/test_llm_client.py:374*

---

### test_create_client_openai

**型**: `function`

**シグネチャ**:
```
def test_create_client_openai(self)
```

**説明**:

OpenAIクライアントの作成

*定義場所: tests/test_utils/test_llm_client.py:377*

---

### test_create_client_anthropic

**型**: `function`

**シグネチャ**:
```
def test_create_client_anthropic(self, mock_anthropic_client)
```

**説明**:

Anthropicクライアントの作成

*定義場所: tests/test_utils/test_llm_client.py:388*

---

### test_create_client_local

**型**: `function`

**シグネチャ**:
```
def test_create_client_local(self, mock_local_client)
```

**説明**:

ローカルクライアントの作成

*定義場所: tests/test_utils/test_llm_client.py:399*

---

### test_create_client_unsupported_provider

**型**: `function`

**シグネチャ**:
```
def test_create_client_unsupported_provider(self)
```

**説明**:

サポートされていないプロバイダー

*定義場所: tests/test_utils/test_llm_client.py:409*

---

### test_create_client_unsupported_mode

**型**: `function`

**シグネチャ**:
```
def test_create_client_unsupported_mode(self)
```

**説明**:

サポートされていないモード

*定義場所: tests/test_utils/test_llm_client.py:418*

---

### test_create_client_import_error

**型**: `function`

**シグネチャ**:
```
def test_create_client_import_error(self)
```

**説明**:

インポートエラーの場合

*定義場所: tests/test_utils/test_llm_client.py:427*

---

### test_create_client_with_fallback_success

**型**: `function`

**シグネチャ**:
```
def test_create_client_with_fallback_success(self, mock_create_client)
```

**説明**:

フォールバック成功の場合

*定義場所: tests/test_utils/test_llm_client.py:439*

---

### test_create_client_with_fallback_switch_to_local

**型**: `function`

**シグネチャ**:
```
def test_create_client_with_fallback_switch_to_local(self, mock_create_client)
```

**説明**:

API失敗時にローカルにフォールバック

*定義場所: tests/test_utils/test_llm_client.py:452*

---

### TestRetryMechanism

**型**: `class`

**シグネチャ**:
```
class TestRetryMechanism
```

**説明**:

リトライ機能のテスト

*定義場所: tests/test_utils/test_llm_client.py:466*

---

### test_retry_with_backoff_success

**型**: `function`

**シグネチャ**:
```
def test_retry_with_backoff_success(self)
```

**説明**:

リトライ成功

*定義場所: tests/test_utils/test_llm_client.py:469*

---

### failing_function

**型**: `function`

**シグネチャ**:
```
def failing_function()
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:476*

---

### test_retry_with_backoff_max_retries_exceeded

**型**: `function`

**シグネチャ**:
```
def test_retry_with_backoff_max_retries_exceeded(self)
```

**説明**:

最大リトライ回数を超過

*定義場所: tests/test_utils/test_llm_client.py:488*

---

### always_failing

**型**: `function`

**シグネチャ**:
```
def always_failing()
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:493*

---


## tests/test_utils/test_llm_client_fixed.py

### MockLLMClient

**型**: `class`

**シグネチャ**:
```
class MockLLMClient(BaseLLMClient)
```

**説明**:

テスト用のBaseLLMClient実装

*定義場所: tests/test_utils/test_llm_client_fixed.py:22*

---

### generate

**型**: `function`

**シグネチャ**:
```
def generate(self, prompt: str, system_prompt: Optional[str]) -> Optional[str]
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client_fixed.py:25*

---

### TestBaseLLMClient

**型**: `class`

**シグネチャ**:
```
class TestBaseLLMClient
```

**説明**:

BaseLLMClientのテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:34*

---

### test_init_with_defaults

**型**: `function`

**シグネチャ**:
```
def test_init_with_defaults(self)
```

**説明**:

デフォルト設定での初期化

*定義場所: tests/test_utils/test_llm_client_fixed.py:37*

---

### test_init_with_custom_config

**型**: `function`

**シグネチャ**:
```
def test_init_with_custom_config(self)
```

**説明**:

カスタム設定での初期化

*定義場所: tests/test_utils/test_llm_client_fixed.py:47*

---

### test_create_outlines_model_not_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_not_available(self)
```

**説明**:

Outlinesが利用できない場合

*定義場所: tests/test_utils/test_llm_client_fixed.py:56*

---

### test_create_outlines_model_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_available(self)
```

**説明**:

Outlinesが利用可能な場合

*定義場所: tests/test_utils/test_llm_client_fixed.py:68*

---

### test_create_outlines_model_internal_exception

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_internal_exception(self)
```

**説明**:

Outlines作成時の例外処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:77*

---

### TestOpenAIClient

**型**: `class`

**シグネチャ**:
```
class TestOpenAIClient
```

**説明**:

OpenAIClientのテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:93*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self, mock_openai)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client_fixed.py:97*

---

### test_init_missing_openai

**型**: `function`

**シグネチャ**:
```
def test_init_missing_openai(self)
```

**説明**:

openaiパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client_fixed.py:114*

---

### test_init_openai_error

**型**: `function`

**シグネチャ**:
```
def test_init_openai_error(self, mock_openai)
```

**説明**:

OpenAIクライアント初期化エラー

*定義場所: tests/test_utils/test_llm_client_fixed.py:121*

---

### test_generate_success

**型**: `function`

**シグネチャ**:
```
def test_generate_success(self, mock_openai)
```

**説明**:

正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:132*

---

### test_generate_with_system_prompt

**型**: `function`

**シグネチャ**:
```
def test_generate_with_system_prompt(self, mock_openai)
```

**説明**:

システムプロンプト付きのテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:151*

---

### test_generate_no_choices

**型**: `function`

**シグネチャ**:
```
def test_generate_no_choices(self, mock_openai)
```

**説明**:

選択肢がない場合の処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:169*

---

### test_generate_exception

**型**: `function`

**シグネチャ**:
```
def test_generate_exception(self, mock_openai)
```

**説明**:

生成時の例外処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:186*

---

### TestAnthropicClient

**型**: `class`

**シグネチャ**:
```
class TestAnthropicClient
```

**説明**:

AnthropicClientのテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:200*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self, mock_anthropic)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client_fixed.py:204*

---

### test_init_missing_anthropic

**型**: `function`

**シグネチャ**:
```
def test_init_missing_anthropic(self)
```

**説明**:

anthropicパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client_fixed.py:218*

---

### test_generate_success

**型**: `function`

**シグネチャ**:
```
def test_generate_success(self, mock_anthropic)
```

**説明**:

正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:225*

---

### test_generate_no_content

**型**: `function`

**シグネチャ**:
```
def test_generate_no_content(self, mock_anthropic)
```

**説明**:

コンテンツがない場合の処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:243*

---

### TestLocalLLMClient

**型**: `class`

**シグネチャ**:
```
class TestLocalLLMClient
```

**説明**:

LocalLLMClientのテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:260*

---

### test_init_success

**型**: `function`

**シグネチャ**:
```
def test_init_success(self, mock_httpx)
```

**説明**:

正常な初期化

*定義場所: tests/test_utils/test_llm_client_fixed.py:264*

---

### test_init_missing_httpx

**型**: `function`

**シグネチャ**:
```
def test_init_missing_httpx(self)
```

**説明**:

httpxパッケージが存在しない場合

*定義場所: tests/test_utils/test_llm_client_fixed.py:279*

---

### test_generate_ollama_success

**型**: `function`

**シグネチャ**:
```
def test_generate_ollama_success(self, mock_httpx)
```

**説明**:

Ollamaでの正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:286*

---

### test_generate_ollama_with_system_prompt

**型**: `function`

**シグネチャ**:
```
def test_generate_ollama_with_system_prompt(self, mock_httpx)
```

**説明**:

Ollamaでのシステムプロンプト付きテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:304*

---

### test_generate_openai_compatible_success

**型**: `function`

**シグネチャ**:
```
def test_generate_openai_compatible_success(self, mock_httpx)
```

**説明**:

OpenAI互換APIでの正常なテキスト生成

*定義場所: tests/test_utils/test_llm_client_fixed.py:322*

---

### test_generate_api_error

**型**: `function`

**シグネチャ**:
```
def test_generate_api_error(self, mock_httpx)
```

**説明**:

APIエラーの処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:342*

---

### test_generate_unsupported_provider

**型**: `function`

**シグネチャ**:
```
def test_generate_unsupported_provider(self, mock_httpx)
```

**説明**:

未対応プロバイダの処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:358*

---

### TestLLMClientFactory

**型**: `class`

**シグネチャ**:
```
class TestLLMClientFactory
```

**説明**:

LLMClientFactoryのテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:372*

---

### test_create_client_openai

**型**: `function`

**シグネチャ**:
```
def test_create_client_openai(self, mock_openai)
```

**説明**:

OpenAIクライアントの作成

*定義場所: tests/test_utils/test_llm_client_fixed.py:376*

---

### test_create_client_anthropic

**型**: `function`

**シグネチャ**:
```
def test_create_client_anthropic(self, mock_anthropic)
```

**説明**:

Anthropicクライアントの作成

*定義場所: tests/test_utils/test_llm_client_fixed.py:386*

---

### test_create_client_local

**型**: `function`

**シグネチャ**:
```
def test_create_client_local(self, mock_httpx)
```

**説明**:

ローカルLLMクライアントの作成

*定義場所: tests/test_utils/test_llm_client_fixed.py:396*

---

### test_create_client_unsupported_provider

**型**: `function`

**シグネチャ**:
```
def test_create_client_unsupported_provider(self)
```

**説明**:

未対応プロバイダの処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:405*

---

### test_create_client_unsupported_mode

**型**: `function`

**シグネチャ**:
```
def test_create_client_unsupported_mode(self)
```

**説明**:

未対応モードの処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:413*

---

### test_create_client_import_error

**型**: `function`

**シグネチャ**:
```
def test_create_client_import_error(self, mock_openai)
```

**説明**:

インポートエラーの処理

*定義場所: tests/test_utils/test_llm_client_fixed.py:422*

---

### test_create_client_with_fallback_success

**型**: `function`

**シグネチャ**:
```
def test_create_client_with_fallback_success(self, mock_openai)
```

**説明**:

フォールバック成功のテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:433*

---

### test_create_client_with_fallback_switch_to_local

**型**: `function`

**シグネチャ**:
```
def test_create_client_with_fallback_switch_to_local(self, mock_httpx, mock_openai)
```

**説明**:

フォールバックでローカルLLMに切り替えるテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:444*

---

### TestRetryMechanism

**型**: `class`

**シグネチャ**:
```
class TestRetryMechanism
```

**説明**:

リトライ機構のテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:458*

---

### test_retry_with_backoff_success

**型**: `function`

**シグネチャ**:
```
def test_retry_with_backoff_success(self)
```

**説明**:

リトライ成功のテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:461*

---

### mock_generate

**型**: `function`

**シグネチャ**:
```
def mock_generate()
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client_fixed.py:469*

---

### test_retry_with_backoff_max_retries_exceeded

**型**: `function`

**シグネチャ**:
```
def test_retry_with_backoff_max_retries_exceeded(self)
```

**説明**:

最大リトライ回数超過のテスト

*定義場所: tests/test_utils/test_llm_client_fixed.py:482*

---


## tests/test_utils/test_outlines_utils.py

### TestShouldUseOutlines

**型**: `class`

**シグネチャ**:
```
class TestShouldUseOutlines
```

**説明**:

should_use_outlines関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:16*

---

### test_should_use_outlines_enabled_and_available

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled_and_available(self)
```

**説明**:

Outlinesが有効で利用可能な場合

*定義場所: tests/test_utils/test_outlines_utils.py:19*

---

### test_should_use_outlines_enabled_but_not_available

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled_but_not_available(self)
```

**説明**:

Outlinesが有効だが利用できない場合

*定義場所: tests/test_utils/test_outlines_utils.py:26*

---

### test_should_use_outlines_disabled

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_disabled(self)
```

**説明**:

Outlinesが無効の場合

*定義場所: tests/test_utils/test_outlines_utils.py:33*

---

### test_should_use_outlines_default_false

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_default_false(self)
```

**説明**:

use_outlinesが設定されていない場合（デフォルトFalse）

*定義場所: tests/test_utils/test_outlines_utils.py:40*

---

### TestCreateOutlinesModel

**型**: `class`

**シグネチャ**:
```
class TestCreateOutlinesModel
```

**説明**:

create_outlines_model関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:48*

---

### test_create_outlines_model_not_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_not_available(self)
```

**説明**:

Outlinesが利用できない場合

*定義場所: tests/test_utils/test_outlines_utils.py:52*

---

### test_create_outlines_model_openai_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_openai_client(self)
```

**説明**:

OpenAIクライアントの場合

*定義場所: tests/test_utils/test_outlines_utils.py:59*

---

### test_create_outlines_model_local_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_local_client(self)
```

**説明**:

ローカルLLMクライアントの場合 - スキップ（動的インポートがモックしにくい）

*定義場所: tests/test_utils/test_outlines_utils.py:79*

---

### test_create_outlines_model_unsupported_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_unsupported_client(self)
```

**説明**:

サポートされていないクライアントの場合

*定義場所: tests/test_utils/test_outlines_utils.py:84*

---

### test_create_outlines_model_exception

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_exception(self)
```

**説明**:

例外発生時のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:94*

---

### TestGetLlmClientWithFallback

**型**: `class`

**シグネチャ**:
```
class TestGetLlmClientWithFallback
```

**説明**:

get_llm_client_with_fallback関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:109*

---

### test_get_llm_client_with_fallback_api_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_api_mode(self, mock_create_client)
```

**説明**:

APIモードの場合

*定義場所: tests/test_utils/test_outlines_utils.py:113*

---

### test_get_llm_client_with_fallback_local_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_local_mode(self, mock_create_client)
```

**説明**:

ローカルモードの場合

*定義場所: tests/test_utils/test_outlines_utils.py:126*

---

### test_get_llm_client_with_fallback_both_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_both_mode(self, mock_create_client)
```

**説明**:

bothモードの場合（API優先）

*定義場所: tests/test_utils/test_outlines_utils.py:141*

---

### test_get_llm_client_with_fallback_default_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_default_mode(self, mock_create_client)
```

**説明**:

デフォルトモードの場合（API）

*定義場所: tests/test_utils/test_outlines_utils.py:154*

---

### TestCleanLlmOutput

**型**: `class`

**シグネチャ**:
```
class TestCleanLlmOutput
```

**説明**:

clean_llm_output関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:167*

---

### test_clean_llm_output_empty_text

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_empty_text(self)
```

**説明**:

空のテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:170*

---

### test_clean_llm_output_none_text

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_none_text(self)
```

**説明**:

Noneの場合

*定義場所: tests/test_utils/test_outlines_utils.py:175*

---

### test_clean_llm_output_no_thinking

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_no_thinking(self)
```

**説明**:

思考過程を含まないテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:180*

---

### test_clean_llm_output_with_thinking_patterns

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_with_thinking_patterns(self)
```

**説明**:

思考過程のパターンを含むテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:186*

---

### test_clean_llm_output_with_placeholders

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_with_placeholders(self)
```

**説明**:

プレースホルダーを含むテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:194*

---

### test_clean_llm_output_markdown_code_block

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_markdown_code_block(self)
```

**説明**:

マークダウンコードブロック内の思考過程をスキップ

*定義場所: tests/test_utils/test_outlines_utils.py:203*

---

### test_clean_llm_output_duplicate_lines

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_duplicate_lines(self)
```

**説明**:

重複した行を削除

*定義場所: tests/test_utils/test_outlines_utils.py:211*

---

### test_clean_llm_output_empty_lines_cleanup

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_empty_lines_cleanup(self)
```

**説明**:

空行の連続を制限

*定義場所: tests/test_utils/test_outlines_utils.py:219*

---

### TestValidateOutput

**型**: `class`

**シグネチャ**:
```
class TestValidateOutput
```

**説明**:

validate_output関数のテスト

*定義場所: tests/test_utils/test_outlines_utils.py:238*

---

### test_validate_output_empty_text

**型**: `function`

**シグネチャ**:
```
def test_validate_output_empty_text(self)
```

**説明**:

空のテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:241*

---

### test_validate_output_valid_text

**型**: `function`

**シグネチャ**:
```
def test_validate_output_valid_text(self)
```

**説明**:

有効なテキストの場合

*定義場所: tests/test_utils/test_outlines_utils.py:247*

---

### test_validate_output_with_special_markers

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_special_markers(self)
```

**説明**:

特殊なマーカーを含む場合

*定義場所: tests/test_utils/test_outlines_utils.py:252*

---

### test_validate_output_with_thinking_patterns

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_thinking_patterns(self)
```

**説明**:

思考過程のパターンを含む場合

*定義場所: tests/test_utils/test_outlines_utils.py:258*

---

### test_validate_output_with_placeholders

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_placeholders(self)
```

**説明**:

プレースホルダーを含む場合

*定義場所: tests/test_utils/test_outlines_utils.py:265*

---

### test_validate_output_markdown_block_with_thinking

**型**: `function`

**シグネチャ**:
```
def test_validate_output_markdown_block_with_thinking(self)
```

**説明**:

マークダウンブロック内に思考過程を含む場合

*定義場所: tests/test_utils/test_outlines_utils.py:271*

---

### test_validate_output_markdown_block_clean

**型**: `function`

**シグネチャ**:
```
def test_validate_output_markdown_block_clean(self)
```

**説明**:

マークダウンブロックがクリーンな場合

*定義場所: tests/test_utils/test_outlines_utils.py:276*

---


## tests/test_utils/test_outlines_utils_fixed.py

### TestShouldUseOutlines

**型**: `class`

**シグネチャ**:
```
class TestShouldUseOutlines
```

**説明**:

should_use_outlines関数のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:21*

---

### test_should_use_outlines_enabled_and_available

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled_and_available(self)
```

**説明**:

Outlinesが有効で利用可能な場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:24*

---

### test_should_use_outlines_enabled_but_not_available

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_enabled_but_not_available(self)
```

**説明**:

Outlinesが有効だが利用できない場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:31*

---

### test_should_use_outlines_disabled

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_disabled(self)
```

**説明**:

Outlinesが無効の場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:38*

---

### test_should_use_outlines_default_false

**型**: `function`

**シグネチャ**:
```
def test_should_use_outlines_default_false(self)
```

**説明**:

use_outlinesが設定されていない場合（デフォルトFalse）

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:45*

---

### TestCreateOutlinesModel

**型**: `class`

**シグネチャ**:
```
class TestCreateOutlinesModel
```

**説明**:

create_outlines_model関数のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:53*

---

### test_create_outlines_model_not_available

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_not_available(self)
```

**説明**:

Outlinesが利用できない場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:57*

---

### test_create_outlines_model_openai_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_openai_client(self)
```

**説明**:

OpenAIクライアントの場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:64*

---

### test_create_outlines_model_local_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_local_client(self)
```

**説明**:

ローカルLLMクライアントの場合 - スキップ（動的インポートがモックしにくい）

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:84*

---

### test_create_outlines_model_unsupported_client

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_unsupported_client(self)
```

**説明**:

サポートされていないクライアントの場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:89*

---

### test_create_outlines_model_exception

**型**: `function`

**シグネチャ**:
```
def test_create_outlines_model_exception(self)
```

**説明**:

例外発生時のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:99*

---

### TestGetLlmClientWithFallback

**型**: `class`

**シグネチャ**:
```
class TestGetLlmClientWithFallback
```

**説明**:

get_llm_client_with_fallback関数のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:114*

---

### test_get_llm_client_with_fallback_api_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_api_mode(self, mock_create_client)
```

**説明**:

APIモードの場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:120*

---

### test_get_llm_client_with_fallback_local_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_local_mode(self, mock_create_client)
```

**説明**:

ローカルモードの場合

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:135*

---

### test_get_llm_client_with_fallback_both_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_both_mode(self, mock_create_client)
```

**説明**:

bothモードの場合（API優先）

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:152*

---

### test_get_llm_client_with_fallback_default_mode

**型**: `function`

**シグネチャ**:
```
def test_get_llm_client_with_fallback_default_mode(self, mock_create_client)
```

**説明**:

デフォルトモードの場合（API）

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:167*

---

### TestCleanLlmOutput

**型**: `class`

**シグネチャ**:
```
class TestCleanLlmOutput
```

**説明**:

clean_llm_output関数のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:180*

---

### test_clean_llm_output_empty_text

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_empty_text(self)
```

**説明**:

空テキストの処理

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:183*

---

### test_clean_llm_output_none_text

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_none_text(self)
```

**説明**:

Noneテキストの処理

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:188*

---

### test_clean_llm_output_no_thinking

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_no_thinking(self)
```

**説明**:

思考パターンがないテキスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:193*

---

### test_clean_llm_output_with_thinking_patterns

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_with_thinking_patterns(self)
```

**説明**:

思考パターンを含むテキスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:199*

---

### test_clean_llm_output_with_placeholders

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_with_placeholders(self)
```

**説明**:

プレースホルダーを含むテキスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:205*

---

### test_clean_llm_output_markdown_code_block

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_markdown_code_block(self)
```

**説明**:

マークダウンコードブロックを含むテキスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:211*

---

### test_clean_llm_output_duplicate_lines

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_duplicate_lines(self)
```

**説明**:

重複行を含むテキスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:217*

---

### test_clean_llm_output_empty_lines_cleanup

**型**: `function`

**シグネチャ**:
```
def test_clean_llm_output_empty_lines_cleanup(self)
```

**説明**:

空行のクリーンアップ

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:223*

---

### TestValidateOutput

**型**: `class`

**シグネチャ**:
```
class TestValidateOutput
```

**説明**:

validate_output関数のテスト

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:230*

---

### test_validate_output_empty_text

**型**: `function`

**シグネチャ**:
```
def test_validate_output_empty_text(self)
```

**説明**:

空テキストの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:233*

---

### test_validate_output_valid_text

**型**: `function`

**シグネチャ**:
```
def test_validate_output_valid_text(self)
```

**説明**:

有効なテキストの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:238*

---

### test_validate_output_with_special_markers

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_special_markers(self)
```

**説明**:

特殊マーカーを含むテキストの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:243*

---

### test_validate_output_with_thinking_patterns

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_thinking_patterns(self)
```

**説明**:

思考パターンを含むテキストの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:249*

---

### test_validate_output_with_placeholders

**型**: `function`

**シグネチャ**:
```
def test_validate_output_with_placeholders(self)
```

**説明**:

プレースホルダーを含むテキストの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:255*

---

### test_validate_output_markdown_block_with_thinking

**型**: `function`

**シグネチャ**:
```
def test_validate_output_markdown_block_with_thinking(self)
```

**説明**:

思考を含むマークダウンブロックの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:261*

---

### test_validate_output_markdown_block_clean

**型**: `function`

**シグネチャ**:
```
def test_validate_output_markdown_block_clean(self)
```

**説明**:

クリーンなマークダウンブロックの検証

*定義場所: tests/test_utils/test_outlines_utils_fixed.py:267*

---
