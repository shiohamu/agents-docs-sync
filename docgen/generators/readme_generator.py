"""
README生成モジュール
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Any

# ロガーのインポート
try:
    from ..utils.logger import get_logger
    from ..utils.uv_utils import detect_uv_usage
    from ..utils.project_utils import get_project_structure
except ImportError:
    import sys

    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from utils.logger import get_logger
    from utils.uv_utils import detect_uv_usage
    from utils.project_utils import get_project_structure

logger = get_logger("readme_generator")


class ReadmeGenerator:
    """README生成クラス"""

    def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any]):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
        """
        self.project_root = project_root
        self.languages = languages
        self.config = config
        self.readme_path = project_root / "README.md"
        self.preserve_manual = config.get("generation", {}).get("preserve_manual_sections", True)

        try:
            import tomllib

            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
                return "tool" in data and "uv" in data["tool"]
        except ImportError:
            # tomllibが利用できない場合、テキスト検索で確認
            try:
                with open(pyproject, encoding="utf-8") as f:
                    content = f.read()
                    return "[tool.uv]" in content
            except Exception:
                return False
        except Exception:
            return False

    def generate(self) -> bool:
        """
        READMEを生成または更新

        Returns:
            成功したかどうか
        """
        try:
            # 既存のREADMEを読み込む
            existing_content = ""
            manual_sections = {}
            if self.readme_path.exists() and self.preserve_manual:
                existing_content = self.readme_path.read_text(encoding="utf-8")
                manual_sections = self._extract_manual_sections(existing_content)

            # 新しいREADMEを生成
            new_content = self._generate_readme(manual_sections)

            # ファイルに書き込み
            self.readme_path.write_text(new_content, encoding="utf-8")

            return True
        except Exception as e:
            logger.error(f"README生成に失敗しました: {e}", exc_info=True)
            return False

    def _extract_manual_sections(self, content: str) -> dict[str, str]:
        """
        既存READMEから手動セクションを抽出

        Args:
            content: 既存のREADME内容

        Returns:
            セクション名をキー、内容を値とする辞書
        """
        sections = {}

        # 手動セクションのマーカーを探す
        # <!-- MANUAL_START:section_name --> ... <!-- MANUAL_END:section_name -->
        pattern = r"<!--\s*MANUAL_START:(\w+)\s*-->(.*?)<!--\s*MANUAL_END:\1\s*-->"
        for match in re.finditer(pattern, content, re.DOTALL):
            section_name = match.group(1)
            section_content = match.group(2).strip()
            sections[section_name] = section_content

        return sections

    def _generate_readme(self, manual_sections: dict[str, str]) -> str:
        """
        READMEを生成

        Args:
            manual_sections: 保持する手動セクション

        Returns:
            READMEの内容
        """
        lines = []

        # プロジェクト名（ディレクトリ名から推測）
        project_name = self.project_root.name
        lines.append(f"# {project_name}")
        lines.append("")

        # 手動セクション: 説明
        lines.append("<!-- MANUAL_START:description -->")
        if "description" in manual_sections:
            lines.append(manual_sections["description"])
        else:
            lines.append("## 概要")
            lines.append("")
            lines.append("このプロジェクトの説明をここに記述してください。")
        lines.append("<!-- MANUAL_END:description -->")
        lines.append("")

        # 自動生成セクション: 使用技術
        lines.append("## 使用技術")
        lines.append("")
        if self.languages:
            lang_display = {
                "python": "Python",
                "javascript": "JavaScript",
                "typescript": "TypeScript",
                "go": "Go",
                "rust": "Rust",
                "java": "Java",
                "cpp": "C++",
                "c": "C",
                "ruby": "Ruby",
                "php": "PHP",
            }
            for lang in self.languages:
                display_name = lang_display.get(lang, lang.capitalize())
                lines.append(f"- {display_name}")
        else:
            lines.append("- 検出されませんでした")
        lines.append("")

        # 依存関係の情報
        dependencies = self._detect_dependencies()
        if dependencies:
            lines.append("## 依存関係")
            lines.append("")
            for dep_type, deps in dependencies.items():
                if deps:
                    lines.append(f"### {dep_type}")
                    lines.append("")
                    for dep in deps[:10]:  # 最大10個まで表示
                        lines.append(f"- {dep}")
                    if len(deps) > 10:
                        lines.append(f"- ... 他 {len(deps) - 10} 個")
                    lines.append("")

        # セットアップ手順
        lines.append("## セットアップ")
        lines.append("")
        lines.append("<!-- MANUAL_START:setup -->")
        if "setup" in manual_sections:
            lines.append(manual_sections["setup"])
        else:
            lines.append("### 必要な環境")
            lines.append("")
            if "python" in self.languages:
                lines.append("- Python 3.8以上")
            if "javascript" in self.languages or "typescript" in self.languages:
                lines.append("- Node.js (推奨バージョン: 18以上)")
            if "go" in self.languages:
                lines.append("- Go 1.16以上")
            lines.append("")
            lines.append("### インストール")
            lines.append("")

            # uvの使用を確認
            uses_uv = detect_uv_usage(self.project_root)

            if "python" in self.languages:
                lines.append("```bash")
                if uses_uv:
                    lines.append("uv sync")
                else:
                    lines.append("pip install -r requirements.txt")
                lines.append("```")
                lines.append("")
            if "javascript" in self.languages or "typescript" in self.languages:
                lines.append("```bash")
                lines.append("npm install")
                lines.append("```")
                lines.append("")
            if "go" in self.languages:
                lines.append("```bash")
                lines.append("go mod download")
                lines.append("```")
                lines.append("")
        lines.append("<!-- MANUAL_END:setup -->")
        lines.append("")

        # 使用方法
        if "usage" in manual_sections:
            lines.append("## 使用方法")
            lines.append("")
            lines.append("<!-- MANUAL_START:usage -->")
            lines.append(manual_sections["usage"])
            lines.append("<!-- MANUAL_END:usage -->")
            lines.append("")

        # プロジェクト構造
        structure = get_project_structure(self.project_root)
        if structure:
            lines.append("## プロジェクト構造")
            lines.append("")
            lines.append("```")
            for line in structure[:20]:  # 最大20行まで
                lines.append(line)
            if len(structure) > 20:
                lines.append("...")
            lines.append("```")
            lines.append("")

        # 手動セクション: その他
        if "other" in manual_sections:
            lines.append("<!-- MANUAL_START:other -->")
            lines.append(manual_sections["other"])
            lines.append("<!-- MANUAL_END:other -->")
            lines.append("")

        # フッター
        lines.append("---")
        lines.append("")
        lines.append(
            f"*このREADMEは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )
        lines.append("")

        return "\n".join(lines)

    def _detect_dependencies(self) -> dict[str, list[str]]:
        """
        依存関係を検出

        Returns:
            依存関係タイプをキー、依存関係リストを値とする辞書
        """
        dependencies = {}

        # Python依存関係
        if "python" in self.languages:
            req_file = self.project_root / "requirements.txt"
            if req_file.exists():
                import re

                deps = []
                # PEP 440バージョン指定子のパターン（==, >=, <=, !=, ~=, >, <, ===）
                version_spec_pattern = re.compile(r"[=!<>~]+")

                for line in req_file.read_text(encoding="utf-8").split("\n"):
                    line = line.strip()
                    # コメント行や空行をスキップ
                    if not line or line.startswith("#"):
                        continue

                    # URLやファイルパスの場合はスキップ（-e, @などで始まる行）
                    if line.startswith("-e ") or line.startswith("@") or "://" in line:
                        continue

                    # バージョン指定子の前までをパッケージ名として抽出
                    # 例: "requests!=2.28.0" -> "requests"
                    # 例: "django~=4.0" -> "django"
                    match = version_spec_pattern.search(line)
                    if match:
                        package_name = line[: match.start()].strip()
                    else:
                        # バージョン指定子がない場合（パッケージ名のみ）
                        package_name = line.split()[0] if line.split() else line

                    # パッケージ名が有効な場合のみ追加
                    if package_name:
                        deps.append(package_name)

                if deps:
                    dependencies["Python"] = deps

        # JavaScript依存関係
        if "javascript" in self.languages or "typescript" in self.languages:
            package_file = self.project_root / "package.json"
            if package_file.exists():
                import json

                try:
                    with open(package_file, encoding="utf-8") as f:
                        package_data = json.load(f)
                        deps = []
                        if "dependencies" in package_data:
                            deps.extend(list(package_data["dependencies"].keys()))
                        if "devDependencies" in package_data:
                            deps.extend(list(package_data["devDependencies"].keys()))
                        if deps:
                            dependencies["Node.js"] = deps
                except:
                    pass

        # Go依存関係
        if "go" in self.languages:
            go_mod = self.project_root / "go.mod"
            if go_mod.exists():
                deps = []
                lines = go_mod.read_text(encoding="utf-8").split("\n")
                in_require_block = False

                for line in lines:
                    line = line.strip()

                    # 複数行のrequireブロックの開始を検出
                    if line.startswith("require ("):
                        in_require_block = True
                        continue

                    # 複数行のrequireブロックの終了を検出
                    if in_require_block and line == ")":
                        in_require_block = False
                        continue

                    # ブロック内の依存関係を抽出
                    if in_require_block:
                        # 空行やコメントをスキップ
                        if not line or line.startswith("//"):
                            continue
                        parts = line.split()
                        if len(parts) >= 1:
                            deps.append(parts[0])

                    # 単一行のrequireを検出
                    elif line.startswith("require ") and not line.startswith("require ("):
                        parts = line.split()
                        if len(parts) >= 2:
                            deps.append(parts[1])

                if deps:
                    dependencies["Go"] = deps

        return dependencies
