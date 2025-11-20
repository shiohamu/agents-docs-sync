# ステップ3: ドキュメント生成システムの拡張

## 目的

`DocGen`クラスにAGENTS.md生成機能を統合します。

## 作業内容

### 1. `docgen/docgen.py`を編集

#### a. インポート文の追加（25行目付近）

```python
from generators.api_generator import APIGenerator
from generators.readme_generator import ReadmeGenerator
from generators.agents_generator import AgentsGenerator  # 追加
```

#### b. `_get_default_config()`メソッドの更新（51-67行目）

```python
def _get_default_config(self) -> Dict[str, Any]:
    """デフォルト設定を返す"""
    return {
        'languages': {
            'auto_detect': True,
            'preferred': []
        },
        'output': {
            'api_doc': 'docs/api.md',
            'readme': 'README.md',
            'agents_doc': 'AGENTS.md'  # 追加
        },
        'generation': {
            'update_readme': True,
            'generate_api_doc': True,
            'generate_agents_doc': True,  # 追加
            'preserve_manual_sections': True
        }
    }
```

#### c. `generate_documents()`メソッドに追加（137行目の後）

```python
# README生成
if self.config.get('generation', {}).get('update_readme', True):
    print("\n[README生成]")
    readme_generator = ReadmeGenerator(
        self.project_root,
        self.detected_languages,
        self.config
    )
    if readme_generator.generate():
        print("✓ READMEを更新しました")
    else:
        print("✗ READMEの更新に失敗しました")
        success = False

# AGENTS.md生成（追加）
if self.config.get('generation', {}).get('generate_agents_doc', True):
    print("\n[AGENTS.md生成]")
    agents_generator = AgentsGenerator(
        self.project_root,
        self.detected_languages,
        self.config
    )
    if agents_generator.generate():
        print("✓ AGENTS.mdを生成しました")
    else:
        print("✗ AGENTS.mdの生成に失敗しました")
        success = False

return success
```

## 確認事項

- [ ] インポートエラーがないか
- [ ] 既存の機能が壊れていないか
- [ ] 手動実行でAGENTS.mdが生成されるか
  ```bash
  python3 docgen/docgen.py
  ```

## 次のステップ

このステップが完了したら、[ステップ4: テスト実行スクリプトの作成](./step4-test-script.md)に進んでください。

