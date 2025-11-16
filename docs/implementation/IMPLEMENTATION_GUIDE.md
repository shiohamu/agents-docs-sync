# CI/CD統合パイプライン実装手順書

この手順書では、GitHubプッシュをトリガーにテスト実行、ドキュメント生成、AGENTS.md自動更新を行う統合パイプラインを、ステップバイステップで実装する方法を説明します。

## 前提条件

- Python 3.12以上がインストールされていること
- Gitリポジトリとして初期化されていること
- 既存のドキュメント生成システム（`.docgen`）が動作していること

## 実装ステップ一覧

各ステップの詳細な手順は、以下の個別ファイルを参照してください：

1. **[ステップ1: AGENTS.md生成モジュールの実装](./docs/implementation/step1-agents-generator.md)**
   - コードベースからエージェント情報を抽出してAGENTS.mdを生成するモジュールを作成

2. **[ステップ2: 設定ファイルの拡張](./docs/implementation/step2-config-extension.md)**
   - AGENTS.md生成の設定を`.docgen/config.yaml`に追加

3. **[ステップ3: ドキュメント生成システムの拡張](./docs/implementation/step3-docgen-extension.md)**
   - `DocGen`クラスにAGENTS.md生成機能を統合

4. **[ステップ4: テスト実行スクリプトの作成](./docs/implementation/step4-test-script.md)**
   - テスト実行を標準化し、CI/CDで使用できるスクリプトを作成

5. **[ステップ5: 統合パイプラインスクリプトの作成](./docs/implementation/step5-pipeline-script.md)**
   - テスト実行→ドキュメント生成→AGENTS.md更新を順次実行するスクリプトを作成

6. **[ステップ6: GitHub Actionsワークフローの作成](./docs/implementation/step6-github-actions.md)**
   - GitHubプッシュ時に自動実行されるCI/CDパイプラインを作成

7. **[ステップ7: ローカルでの動作確認](./docs/implementation/step7-local-testing.md)**
   - 各コンポーネントが正常に動作することを確認

8. **[ステップ8: GitHub Actionsでの動作確認](./docs/implementation/step8-github-testing.md)**
   - GitHub上でワークフローが正常に動作することを確認

## トラブルシューティング

詳細は各ステップのドキュメントを参照してください。一般的な問題については以下を確認：

- **AGENTS.mdが生成されない**: ステップ1、2、3の確認事項を再確認
- **テストが失敗する**: ステップ4の確認事項を再確認
- **GitHub Actionsが動作しない**: ステップ6の確認事項を再確認
- **自動コミットが機能しない**: ステップ6の確認事項を再確認

## まとめ

この手順書に従って実装することで、以下の機能が実現されます：

- ✅ GitHubプッシュ時に自動でテスト実行
- ✅ テスト成功後にドキュメント自動生成
- ✅ AGENTS.mdの自動更新
- ✅ 生成されたドキュメントの自動コミット（オプション）

各ステップを順番に実行し、各段階で動作確認を行うことで、問題を早期に発見し、スムーズに実装を完了できます。
