# 汎用ドキュメント自動更新システム

コミット時にAPIドキュメントとREADME.mdを自動更新する汎用的なシステムです。どのプロジェクトにも追加するだけで使用できます。

## 特徴

- **汎用性**: Python、JavaScript/TypeScript、Go、Rust、Java、C/C++など、15言語以上をサポート
- **自動検出**: プロジェクトの使用言語を自動検出
- **Git統合**: pre-commitフックでコミット前に自動実行
- **カスタマイズ可能**: YAML設定ファイルで動作をカスタマイズ
- **手動セクション保護**: 既存READMEの手動セクションを自動的に保持

## クイックスタート

### 1. セットアップ

プロジェクトルートで以下のコマンドを実行：

```bash
./setup.sh
```

これにより：
- 環境チェック（Python 3.8+、Git）
- 必要なパッケージの確認・インストール
- Git hooksのインストール
- 初回ドキュメント生成（オプション）

が自動的に実行されます。

### 2. 使用方法

セットアップ後、通常通りコードをコミットするだけで、ドキュメントが自動更新されます：

```bash
git add .
git commit -m "機能追加"
# → コミット前に自動的にドキュメントが生成・更新されます
```

## 手動実行

ドキュメントを手動で生成する場合：

```bash
# ドキュメントを生成
python3 .docgen/docgen.py

# 言語検出のみ実行
python3 .docgen/docgen.py --detect-only

# APIドキュメントのみ生成
python3 .docgen/docgen.py --no-readme

# READMEのみ更新
python3 .docgen/docgen.py --no-api-doc
```

## 設定

設定ファイル（`.docgen/config.yaml`）で動作をカスタマイズできます：

```yaml
# 言語設定
languages:
  auto_detect: true
  preferred: []  # 優先する言語のリスト

# 出力設定
output:
  api_doc: docs/api.md    # APIドキュメントの出力パス
  readme: README.md        # READMEファイルのパス

# 生成設定
generation:
  update_readme: true
  generate_api_doc: true
  preserve_manual_sections: true  # 手動セクションを保持
```

詳細は `.docgen/config.yaml` を参照してください。

## サポートされている言語

### 完全サポート
- **Python**: docstring（Google/NumPy/Sphinx形式）を解析
- **JavaScript/TypeScript**: JSDocコメントを解析

### 基本サポート
- **Go**: 関数・構造体定義を抽出
- **Rust**: 関数・構造体定義を抽出
- **Java**: Javadocコメントを抽出
- **C/C++**: 関数・クラス定義を抽出
- **Ruby**: 関数・クラス定義を抽出
- **PHP**: 関数・クラス定義を抽出

その他、15言語以上をサポートしています。

## 生成されるドキュメント

### APIドキュメント

`docs/api.md`（設定で変更可能）に以下の情報が自動生成されます：

- 関数・クラスの一覧
- シグネチャ
- ドキュメント文字列（docstring/JSDoc）
- 定義場所（ファイル名・行番号）

### README.md

以下のセクションが自動生成・更新されます：

- **使用技術**: 検出された言語のリスト
- **依存関係**: requirements.txt、package.json、go.modから自動抽出
- **セットアップ手順**: 言語に応じた基本的なセットアップ手順
- **プロジェクト構造**: ディレクトリ構造の自動生成

既存のREADMEがある場合、`<!-- MANUAL_START:section_name -->` と `<!-- MANUAL_END:section_name -->` で囲まれたセクションは保持されます。

## Git Hooks

### pre-commit

コミット前に自動的にドキュメントを生成し、変更があればステージングに追加します。

### post-commit（オプション）

コミット後にドキュメントを更新し、別コミットとして追加します。デフォルトでは無効です。

有効にする場合：

```bash
export DOCGEN_ENABLE_POST_COMMIT=1
```

## プロジェクト構造

```
プロジェクトルート/
├── .docgen/
│   ├── docgen.py              # メインスクリプト
│   ├── config.yaml            # 設定ファイル
│   ├── detectors/              # 言語検出モジュール
│   ├── generators/            # ドキュメント生成モジュール
│   │   └── parsers/           # コード解析パーサー
│   └── hooks/                 # Git hooks
├── setup.sh                   # セットアップスクリプト
└── README.md                  # このファイル
```

## 要件

- Python 3.8以上
- Git（オプション、Git hooksを使用する場合）
- PyYAML（自動インストール可能）

## トラブルシューティング

### ドキュメントが生成されない

1. Python 3.8以上がインストールされているか確認：
   ```bash
   python3 --version
   ```

2. 必要なパッケージがインストールされているか確認：
   ```bash
   python3 -c "import yaml"
   ```

3. 手動で実行してエラーメッセージを確認：
   ```bash
   python3 .docgen/docgen.py
   ```

### Git hooksが動作しない

1. Gitリポジトリであることを確認：
   ```bash
   git rev-parse --git-dir
   ```

2. hooksがインストールされているか確認：
   ```bash
   ls -la .git/hooks/pre-commit
   ```

3. 再セットアップ：
   ```bash
   ./setup.sh
   ```

### 特定のファイルが解析されない

`.docgen/config.yaml` の `exclude` セクションで除外設定を確認してください（将来の拡張機能）。

## カスタマイズ

### 新しい言語のサポート

1. `.docgen/detectors/` に新しい検出モジュールを追加
2. `.docgen/generators/parsers/` に新しいパーサーを追加
3. `docgen.py` に登録

詳細は既存のモジュールを参考にしてください。

### ドキュメントテンプレートのカスタマイズ

将来的に、`.docgen/config.yaml` でテンプレートを指定できるようになる予定です。

## ライセンス

このプロジェクトは汎用的なドキュメント自動生成システムです。自由に使用・改変してください。

## 貢献

バグ報告や機能要望は、Issueでお知らせください。

## 更新履歴

- 初版: 汎用ドキュメント自動更新システムのリリース

---

*このREADMEは自動生成されています。最終更新: 2024-01-01*

