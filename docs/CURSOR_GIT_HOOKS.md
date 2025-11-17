# CursorでのGitフックの使用

## 問題: CursorでGitフックが実行されない

CursorでGit操作（コミット、プッシュなど）を行う場合、一部のGitフックが実行されないことがあります。これは以下の理由によるものです：

1. **Cursorの最適化**: CursorはGit操作を最適化するため、一部のフックをスキップする場合があります
2. **非対話的実行**: Cursorは非対話的にGitコマンドを実行するため、対話的なフック（`read`コマンドを含む）が正常に動作しない場合があります
3. **環境変数の継承**: Cursorから実行されるGitコマンドは、ターミナルの環境変数を継承しない場合があります

## 解決策

### 方法1: ターミナルからGit操作を実行（推奨）

Cursorの統合Git機能ではなく、ターミナルから直接Gitコマンドを実行することで、フックが確実に実行されます：

```bash
# ターミナルで実行
git add .
git commit -m "Your message"
git push
```

### 方法2: Cursorのターミナル統合を使用

Cursorの統合ターミナルを使用してGitコマンドを実行：

1. Cursorで `Ctrl+`` (バッククォート) または `View > Terminal` を開く
2. ターミナルでGitコマンドを実行

### 方法3: フックを非対話的にする

対話的なフック（`read`コマンドを含む）を非対話的に変更する：

```bash
# pre-pushフックを非対話的にする場合
# 環境変数で自動的に実行するように設定
export AUTO_RELEASE_ENABLED=1
export AUTO_RELEASE_AUTO_YES=1  # 確認なしで実行
```

### 方法4: リリーススクリプトを使用

フックに依存せず、リリーススクリプトを直接実行：

```bash
./scripts/release.sh
```

## フックの確認方法

フックが正しくインストールされているか確認：

```bash
# フックファイルの存在確認
ls -la .git/hooks/pre-*

# フックの実行権限確認
test -x .git/hooks/pre-push && echo "実行可能" || echo "実行不可"

# フックの内容確認
cat .git/hooks/pre-push
```

## フックの再インストール

フックが正しく動作しない場合、再インストール：

```bash
./scripts/install_hooks.sh
```

または

```bash
./setup.sh
```

## トラブルシューティング

### フックが実行されない

1. **フックがインストールされているか確認**
   ```bash
   ls -la .git/hooks/pre-*
   ```

2. **実行権限があるか確認**
   ```bash
   chmod +x .git/hooks/pre-push
   ```

3. **ターミナルから直接Gitコマンドを実行**
   ```bash
   git push
   ```

### フックがエラーで終了する

1. **フックを直接実行してエラーを確認**
   ```bash
   .git/hooks/pre-push
   ```

2. **環境変数が設定されているか確認**
   ```bash
   echo $AUTO_RELEASE_ENABLED
   ```

3. **フックのログを確認**
   ```bash
   bash -x .git/hooks/pre-push
   ```

## 推奨ワークフロー

Cursorを使用する場合の推奨ワークフロー：

1. **開発作業**: Cursorの統合Git機能を使用（フックは実行されない可能性がある）
2. **コミット**: ターミナルから `git commit` を実行（pre-commitフックが実行される）
3. **リリース**: リリーススクリプトを使用（`./scripts/release.sh`）
4. **プッシュ**: ターミナルから `git push` を実行（pre-pushフックが実行される）

## 注意事項

- Cursorの統合Git機能を使用する場合、フックが実行されない可能性があります
- 重要な操作（リリースなど）は、ターミナルから直接実行することを推奨します
- フックが対話的（`read`コマンドを含む）場合、Cursorからは正常に動作しない可能性があります

