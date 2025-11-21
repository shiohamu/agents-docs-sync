# API ドキュメント

自動生成日時: 2025-11-21 14:50:14

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

*定義場所: tests/conftest.py:18*

---

### sample_config

**型**: `function`

**シグネチャ**:
```
def sample_config():
```

**説明**:

Return a sample configuration dictionary.

*定義場所: tests/conftest.py:51*

---

### mock_llm_client

**型**: `function`

**シグネチャ**:
```
def mock_llm_client(mocker):
```

**説明**:

Mock LLMクライアント

*定義場所: tests/conftest.py:73*

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

*定義場所: tests/test_config_manager.py:18*

---

### test_config_manager_initialization_with_config_path

**型**: `method`

**シグネチャ**:
```
def test_config_manager_initialization_with_config_path(self, temp_project):
```

**説明**:

設定ファイルパス指定での初期化テスト

*定義場所: tests/test_config_manager.py:21*

---

### test_config_manager_initialization_default_config_path

**型**: `method`

**シグネチャ**:
```
def test_config_manager_initialization_default_config_path(self, temp_project):
```

**説明**:

デフォルト設定ファイルパスでの初期化テスト

*定義場所: tests/test_config_manager.py:33*

---

### test_load_config_existing_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_existing_file(self, mock_safe_read_yaml, temp_project):
```

**説明**:

既存の設定ファイル読み込みテスト

*定義場所: tests/test_config_manager.py:43*

---

### test_load_config_nonexistent_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_nonexistent_file(self, mock_safe_read_yaml, temp_project):
```

**説明**:

存在しない設定ファイルのテスト

*定義場所: tests/test_config_manager.py:58*

---

### test_create_default_config_with_sample

**型**: `method`

**シグネチャ**:
```
def test_create_default_config_with_sample(self, mock_safe_read_yaml, temp_project):
```

**説明**:

サンプル設定ファイルからのデフォルト設定作成テスト

*定義場所: tests/test_config_manager.py:75*

---

### test_create_default_config_without_sample

**型**: `method`

**シグネチャ**:
```
def test_create_default_config_without_sample(self, mock_safe_read_yaml, temp_project):
```

**説明**:

サンプル設定ファイルなしの場合のデフォルト設定作成テスト

*定義場所: tests/test_config_manager.py:99*

---

### test_copy_sample_config_success

**型**: `method`

**シグネチャ**:
```
def test_copy_sample_config_success(self, temp_project):
```

**説明**:

サンプル設定ファイルのコピー成功テスト

*定義場所: tests/test_config_manager.py:120*

---

### test_copy_sample_config_failure

**型**: `method`

**シグネチャ**:
```
def test_copy_sample_config_failure(self, temp_project):
```

**説明**:

サンプル設定ファイルのコピー失敗テスト

*定義場所: tests/test_config_manager.py:140*

---

### test_get_default_config

**型**: `method`

**シグネチャ**:
```
def test_get_default_config(self, temp_project):
```

**説明**:

デフォルト設定の取得テスト

*定義場所: tests/test_config_manager.py:159*

---

### test_get_config

**型**: `method`

**シグネチャ**:
```
def test_get_config(self, temp_project):
```

**説明**:

設定取得テスト

*定義場所: tests/test_config_manager.py:176*

---

### test_update_config_simple

**型**: `method`

**シグネチャ**:
```
def test_update_config_simple(self, temp_project):
```

**説明**:

シンプルな設定更新テスト

*定義場所: tests/test_config_manager.py:188*

---

### test_update_config_nested

**型**: `method`

**シグネチャ**:
```
def test_update_config_nested(self, temp_project):
```

**説明**:

ネストされた設定更新テスト

*定義場所: tests/test_config_manager.py:200*

---

### test_set_nested_value_existing

**型**: `method`

**シグネチャ**:
```
def test_set_nested_value_existing(self, temp_project):
```

**説明**:

既存のネストされた値設定テスト

*定義場所: tests/test_config_manager.py:212*

---

### test_set_nested_value_new_structure

**型**: `method`

**シグネチャ**:
```
def test_set_nested_value_new_structure(self, temp_project):
```

**説明**:

新規ネスト構造作成テスト

*定義場所: tests/test_config_manager.py:224*

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

### test_initialization_with_config

**型**: `method`

**シグネチャ**:
```
def test_initialization_with_config(self, temp_project):
```

**説明**:

設定ファイル指定での初期化テスト

*定義場所: tests/test_docgen.py:31*

---

### test_load_config_existing_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_existing_file(self, temp_project):
```

**説明**:

既存の設定ファイル読み込みテスト

*定義場所: tests/test_docgen.py:44*

---

### test_load_config_missing_file

**型**: `method`

**シグネチャ**:
```
def test_load_config_missing_file(self, temp_project):
```

**説明**:

設定ファイルが存在しない場合のテスト

*定義場所: tests/test_docgen.py:58*

---

### test_validate_config_missing_sections

**型**: `method`

**シグネチャ**:
```
def test_validate_config_missing_sections(self, temp_project):
```

**説明**:

設定セクションが不足している場合のテスト

*定義場所: tests/test_docgen.py:68*

---

### test_update_config

**型**: `method`

**シグネチャ**:
```
def test_update_config(self, temp_project):
```

**説明**:

設定更新テスト

*定義場所: tests/test_docgen.py:80*

---

### test_detect_languages_parallel

**型**: `method`

**シグネチャ**:
```
def test_detect_languages_parallel(self, mock_generic, mock_go, mock_js, mock_python, temp_project):
```

**説明**:

並列言語検出テスト

*定義場所: tests/test_docgen.py:95*

---

### test_detect_languages_sequential

**型**: `method`

**シグネチャ**:
```
def test_detect_languages_sequential(self, mock_generic, mock_go, mock_js, mock_python, temp_project):
```

**説明**:

逐次言語検出テスト

*定義場所: tests/test_docgen.py:124*

---

### test_generate_documents_success

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_success(self, mock_agents, mock_readme, mock_api, temp_project):
```

**説明**:

ドキュメント生成成功テスト

*定義場所: tests/test_docgen.py:151*

---

### test_generate_documents_partial_failure

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_partial_failure(self, mock_agents, mock_readme, mock_api, temp_project):
```

**説明**:

ドキュメント生成一部失敗テスト

*定義場所: tests/test_docgen.py:171*

---

### test_generate_documents_no_languages

**型**: `method`

**シグネチャ**:
```
def test_generate_documents_no_languages(self, temp_project):
```

**説明**:

言語が検出されない場合のテスト

*定義場所: tests/test_docgen.py:187*

---

### test_main_commit_msg_command

**型**: `method`

**シグネチャ**:
```
def test_main_commit_msg_command(self, mock_generator, temp_project, capsys):
```

**説明**:

commit-msgコマンドのテスト

*定義場所: tests/test_docgen.py:198*

---

### test_main_detect_only

**型**: `method`

**シグネチャ**:
```
def test_main_detect_only(self, temp_project, caplog):
```

**説明**:

detect-onlyオプションのテスト

*定義場所: tests/test_docgen.py:212*

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

*定義場所: tests/test_edge_cases.py:24*

---

### test_empty_project_root

**型**: `method`

**シグネチャ**:
```
def test_empty_project_root(self):
```

**説明**:

空のプロジェクトルートでのテスト

*定義場所: tests/test_edge_cases.py:27*

---

### test_nonexistent_project_root

**型**: `method`

**シグネチャ**:
```
def test_nonexistent_project_root(self):
```

**説明**:

存在しないプロジェクトルートでのテスト

*定義場所: tests/test_edge_cases.py:32*

---

### test_python_parser_with_malformed_ast

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_malformed_ast(self, temp_project):
```

**説明**:

不正なASTを持つPythonファイルの解析テスト

*定義場所: tests/test_edge_cases.py:39*

---

### test_python_parser_with_unicode_content

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_unicode_content(self, temp_project):
```

**説明**:

Unicode文字を含むPythonファイルの解析テスト

*定義場所: tests/test_edge_cases.py:54*

---

### test_python_parser_with_very_long_docstring

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_very_long_docstring(self, temp_project):
```

**説明**:

非常に長いdocstringの解析テスト

*定義場所: tests/test_edge_cases.py:74*

---

### test_agents_generator_with_invalid_config

**型**: `method`

**シグネチャ**:
```
def test_agents_generator_with_invalid_config(self, temp_project):
```

**説明**:

無効な設定でのAgentsGeneratorテスト

*定義場所: tests/test_edge_cases.py:92*

---

### test_api_generator_with_empty_languages

**型**: `method`

**シグネチャ**:
```
def test_api_generator_with_empty_languages(self, temp_project):
```

**説明**:

空の言語リストでのAPIGeneratorテスト

*定義場所: tests/test_edge_cases.py:106*

---

### test_readme_generator_with_readonly_filesystem

**型**: `method`

**シグネチャ**:
```
def test_readme_generator_with_readonly_filesystem(self, temp_project, monkeypatch):
```

**説明**:

読み取り専用ファイルシステムでのReadmeGeneratorテスト

*定義場所: tests/test_edge_cases.py:117*

---

### test_docgen_with_circular_imports

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_circular_imports(self, temp_project):
```

**説明**:

循環インポートのあるプロジェクトのテスト

*定義場所: tests/test_edge_cases.py:133*

---

### test_docgen_with_very_deep_directory_structure

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_very_deep_directory_structure(self, temp_project):
```

**説明**:

非常に深いディレクトリ構造のテスト

*定義場所: tests/test_edge_cases.py:156*

---

### test_docgen_with_special_characters_in_paths

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_special_characters_in_paths(self, temp_project):
```

**説明**:

パスに特殊文字を含む場合のテスト

*定義場所: tests/test_edge_cases.py:177*

---

### test_docgen_with_symlink_loops

**型**: `method`

**シグネチャ**:
```
def test_docgen_with_symlink_loops(self, temp_project):
```

**説明**:

シンボリックリンクのループがある場合のテスト

*定義場所: tests/test_edge_cases.py:195*

---

### test_python_parser_with_binary_file_extension

**型**: `method`

**シグネチャ**:
```
def test_python_parser_with_binary_file_extension(self, temp_project):
```

**説明**:

.pycファイルなどのバイナリ拡張子のテスト

*定義場所: tests/test_edge_cases.py:217*

---

### test_agents_generator_with_very_long_custom_instructions

**型**: `method`

**シグネチャ**:
```
def test_agents_generator_with_very_long_custom_instructions(self, temp_project):
```

**説明**:

非常に長いカスタム指示のテスト

*定義場所: tests/test_edge_cases.py:229*

---

### test_api_generator_with_mixed_file_types

**型**: `method`

**シグネチャ**:
```
def test_api_generator_with_mixed_file_types(self, temp_project):
```

**説明**:

混在したファイルタイプのテスト

*定義場所: tests/test_edge_cases.py:244*

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

*定義場所: tests/test_project_info_collector.py:70*

---

### test_collect_build_commands_with_package_managers

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_with_package_managers(self, temp_project):
```

**説明**:

パッケージマネージャ考慮のビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:90*

---

### test_collect_build_commands_from_makefile

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_from_makefile(self, temp_project):
```

**説明**:

Makefileからのビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:109*

---

### test_collect_build_commands_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのビルドコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:135*

---

### test_collect_test_commands_from_makefile

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_from_makefile(self, temp_project):
```

**説明**:

Makefileからのテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:155*

---

### test_collect_test_commands_with_package_managers

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_with_package_managers(self, temp_project):
```

**説明**:

パッケージマネージャ考慮のテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:176*

---

### test_collect_build_commands_with_uv_run

**型**: `method`

**シグネチャ**:
```
def test_collect_build_commands_with_uv_run(self, temp_project):
```

**説明**:

uvプロジェクトでのpythonコマンドにuv runがつくテスト

*定義場所: tests/test_project_info_collector.py:200*

---

### test_collect_test_commands_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_test_commands_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのテストコマンド収集テスト

*定義場所: tests/test_project_info_collector.py:218*

---

### test_collect_dependencies_from_requirements_txt

**型**: `method`

**シグネチャ**:
```
def test_collect_dependencies_from_requirements_txt(self, temp_project):
```

**説明**:

requirements.txtからの依存関係収集テスト

*定義場所: tests/test_project_info_collector.py:236*

---

### test_collect_dependencies_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_dependencies_from_package_json(self, temp_project):
```

**説明**:

package.jsonからの依存関係収集テスト

*定義場所: tests/test_project_info_collector.py:256*

---

### test_collect_coding_standards_from_pyproject_toml

**型**: `method`

**シグネチャ**:
```
def test_collect_coding_standards_from_pyproject_toml(self, temp_project):
```

**説明**:

pyproject.tomlからのコーディング規約収集テスト

*定義場所: tests/test_project_info_collector.py:280*

---

### test_collect_ci_cd_info_github_actions

**型**: `method`

**シグネチャ**:
```
def test_collect_ci_cd_info_github_actions(self, temp_project):
```

**説明**:

GitHub Actions CI/CD情報収集テスト

*定義場所: tests/test_project_info_collector.py:307*

---

### test_collect_project_structure

**型**: `method`

**シグネチャ**:
```
def test_collect_project_structure(self, temp_project):
```

**説明**:

プロジェクト構造収集テスト

*定義場所: tests/test_project_info_collector.py:330*

---

### test_collect_project_description_from_readme

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_readme(self, temp_project):
```

**説明**:

READMEからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:349*

---

### test_collect_project_description_from_setup_py

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_setup_py(self, temp_project):
```

**説明**:

setup.pyからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:368*

---

### test_collect_project_description_from_package_json

**型**: `method`

**シグネチャ**:
```
def test_collect_project_description_from_package_json(self, temp_project):
```

**説明**:

package.jsonからのプロジェクト説明収集テスト

*定義場所: tests/test_project_info_collector.py:388*

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

### OpenAIClient

**型**: `class`

**シグネチャ**:
```
class OpenAIClient:
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:30*

---

### AnthropicClient

**型**: `class`

**シグネチャ**:
```
class AnthropicClient:
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:33*

---

### LocalLLMClient

**型**: `class`

**シグネチャ**:
```
class LocalLLMClient:
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:36*

---

### LLMClientFactory

**型**: `class`

**シグネチャ**:
```
class LLMClientFactory:
```

*説明なし*

*定義場所: tests/test_utils/test_llm_client.py:39*

---

### TestBaseLLMClient

**型**: `class`

**シグネチャ**:
```
class TestBaseLLMClient:
```

**説明**:

BaseLLMClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:43*

---

### test_base_llm_client_initialization

**型**: `method`

**シグネチャ**:
```
def test_base_llm_client_initialization(self):
```

**説明**:

BaseLLMClientの初期化テスト

*定義場所: tests/test_utils/test_llm_client.py:46*

---

### TestOpenAIClient

**型**: `class`

**シグネチャ**:
```
class TestOpenAIClient:
```

**説明**:

OpenAIClientクラスのテスト

*定義場所: tests/test_utils/test_llm_client.py:65*

---

### test_ollama_client_error_handling

**型**: `method`

**シグネチャ**:
```
def test_ollama_client_error_handling(self, mock_httpx):
```

**説明**:

Ollamaクライアントのエラーハンドリングテスト

*定義場所: tests/test_utils/test_llm_client.py:71*

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
