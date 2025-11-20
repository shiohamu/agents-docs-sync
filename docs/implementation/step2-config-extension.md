# ステップ2: 設定ファイルの拡張

## 目的

AGENTS.md生成の設定を`docgen/config.yaml`に追加します。

## 作業内容

### 1. `docgen/config.yaml`を編集

`output`セクションと`generation`セクションに以下を追加：

```yaml
# 出力設定
output:
  # APIドキュメントの出力パス（プロジェクトルートからの相対パス）
  api_doc: docs/api.md

  # READMEファイルのパス（プロジェクトルートからの相対パス）
  readme: README.md

  # AGENTS.mdの出力パス（プロジェクトルートからの相対パス）
  agents_doc: AGENTS.md

# 生成設定
generation:
  # READMEを更新するかどうか
  update_readme: true

  # APIドキュメントを生成するかどうか
  generate_api_doc: true

  # AGENTS.mdを生成するかどうか
  generate_agents_doc: true

  # 既存READMEの手動セクションを保持するかどうか
  preserve_manual_sections: true
```

**注意**: 既存の設定を上書きせず、新しい設定を追加するだけにしてください。

## 確認事項

- [ ] YAMLの構文が正しいか
- [ ] 既存の設定を壊していないか
- [ ] インデントが正しいか（スペース2つ）

## 次のステップ

このステップが完了したら、[ステップ3: ドキュメント生成システムの拡張](./step3-docgen-extension.md)に進んでください。

