# リリース手順

このドキュメントでは、agents-docs-syncのリリース手順を説明します。

## リリース方法

### 方法1: タグを使用した自動リリース（推奨）

1. **バージョン番号の更新**
   ```bash
   # pyproject.tomlのversionを更新
   # 例: version = "0.0.2"
   ```

2. **変更をコミット**
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.0.2"
   ```

3. **タグを作成してプッシュ**
   ```bash
   git tag -a v0.0.2 -m "Release version 0.0.2"
   git push origin v0.0.2
   ```

4. **GitHub Actionsが自動的にリリースを作成**
   - `.github/workflows/release.yml`が自動実行されます
   - ビルド、パッケージング、GitHubリリースの作成が行われます

### 方法2: 手動リリース（GitHub Actions UI）

1. GitHubリポジトリの「Actions」タブに移動
2. 「Release」ワークフローを選択
3. 「Run workflow」をクリック
4. バージョン番号を入力（例: `0.0.2`）
5. 「Run workflow」をクリック

## PyPIへの公開（オプション）

PyPIに公開する場合は、以下の手順を実行してください：

1. **PyPI APIトークンの取得**
   - https://pypi.org/manage/account/token/ にアクセス
   - APIトークンを作成

2. **GitHub Secretsに追加**
   - リポジトリの「Settings」→「Secrets and variables」→「Actions」
   - 「New repository secret」をクリック
   - Name: `PYPI_API_TOKEN`
   - Value: PyPI APIトークンを貼り付け
   - 「Add secret」をクリック

3. **ワークフローの有効化**
   - `.github/workflows/release.yml`を編集
   - `Publish to PyPI`ステップの`if: false`を`if: true`に変更

4. **リリースを実行**
   - 上記の「方法1」または「方法2」でリリースを実行
   - PyPIへの公開が自動的に行われます

## ローカルでのビルドとテスト

リリース前に、ローカルでビルドとテストを実行することを推奨します：

```bash
# 依存関係のインストール
pip install build wheel setuptools

# パッケージのビルド
python -m build

# ビルド結果の確認
ls -la dist/

# テストインストール
pip install dist/agents_docs_sync-*.whl

# 動作確認
agents-docs-sync --help
```

## リリースノート

GitHub Actionsは自動的にリリースノートを生成しますが、手動で編集することもできます。

リリースノートには以下を含めることを推奨します：
- 新機能
- バグ修正
- 破壊的変更（あれば）
- 依存関係の更新

## バージョン番号の規則

[Semantic Versioning](https://semver.org/)に従います：
- **MAJOR**: 互換性のない変更
- **MINOR**: 後方互換性のある新機能
- **PATCH**: バグ修正

例: `0.1.0` → `0.1.1` (パッチ), `0.1.0` → `0.2.0` (マイナー), `0.1.0` → `1.0.0` (メジャー)

## トラブルシューティング

### リリースが作成されない

- タグが正しい形式か確認（`v`で始まる必要がある）
- GitHub Actionsのログを確認
- ワークフローファイルの構文エラーを確認

### PyPIへの公開が失敗する

- `PYPI_API_TOKEN`が正しく設定されているか確認
- トークンに適切な権限があるか確認
- バージョン番号が既に存在しないか確認

