"""
README生成モジュール
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# ロガーのインポート
try:
    from ..utils.logger import get_logger
    from ..utils.llm_client import LLMClientFactory
    from ..collectors.project_info_collector import ProjectInfoCollector
except ImportError:
    import sys
    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from utils.logger import get_logger
    from utils.llm_client import LLMClientFactory
    from collectors.project_info_collector import ProjectInfoCollector

logger = get_logger("readme_generator")


class ReadmeGenerator:
    """README生成クラス"""

    def __init__(self, project_root: Path, languages: List[str], config: Dict[str, Any]):
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
        self.preserve_manual = config.get('generation', {}).get('preserve_manual_sections', True)
        self.agents_config = config.get('agents', {})
        self.collector = ProjectInfoCollector(project_root)

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
                existing_content = self.readme_path.read_text(encoding='utf-8')
                manual_sections = self._extract_manual_sections(existing_content)

            # 新しいREADMEを生成
            new_content = self._generate_readme(manual_sections)

            # ファイルに書き込み
            self.readme_path.write_text(new_content, encoding='utf-8')

            return True
        except Exception as e:
            logger.error(f"README生成に失敗しました: {e}", exc_info=True)
            return False

    def _extract_manual_sections(self, content: str) -> Dict[str, str]:
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
        pattern = r'<!--\s*MANUAL_START:(\w+)\s*-->(.*?)<!--\s*MANUAL_END:\1\s*-->'
        for match in re.finditer(pattern, content, re.DOTALL):
            section_name = match.group(1)
            section_content = match.group(2).strip()
            sections[section_name] = section_content

        return sections

    def _generate_readme(self, manual_sections: Dict[str, str]) -> str:
        """
        READMEを生成

        Args:
            manual_sections: 保持する手動セクション

        Returns:
            READMEの内容
        """
        # 生成モードを取得（デフォルトは'template'）
        generation_config = self.agents_config.get('generation', {})
        mode = generation_config.get('readme_mode', 'template')

        if mode == 'llm':
            # LLM完全生成
            return self._generate_with_llm(manual_sections)
        elif mode == 'hybrid':
            # ハイブリッド生成
            return self._generate_hybrid(manual_sections)
        else:
            # テンプレート生成（デフォルト）
            return self._generate_template(manual_sections)

    def _generate_template(self, manual_sections: Dict[str, str]) -> str:
        """
        テンプレートベースでREADMEを生成（既存の実装）

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
        if 'description' in manual_sections:
            lines.append(manual_sections['description'])
        else:
            # プロジェクトの説明を収集
            description = self._collect_project_description()
            if description:
                lines.append("## 概要")
                lines.append("")
                lines.append(description)
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
                'python': 'Python',
                'javascript': 'JavaScript',
                'typescript': 'TypeScript',
                'go': 'Go',
                'rust': 'Rust',
                'java': 'Java',
                'cpp': 'C++',
                'c': 'C',
                'ruby': 'Ruby',
                'php': 'PHP',
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
        if 'setup' in manual_sections:
            lines.append(manual_sections['setup'])
        else:
            lines.append("### 必要な環境")
            lines.append("")
            if 'python' in self.languages:
                lines.append("- Python 3.8以上")
            if 'javascript' in self.languages or 'typescript' in self.languages:
                lines.append("- Node.js (推奨バージョン: 18以上)")
            if 'go' in self.languages:
                lines.append("- Go 1.16以上")
            lines.append("")
            lines.append("### インストール")
            lines.append("")
            if 'python' in self.languages:
                lines.append("```bash")
                lines.append("pip install -r requirements.txt")
                lines.append("```")
                lines.append("")
            if 'javascript' in self.languages or 'typescript' in self.languages:
                lines.append("```bash")
                lines.append("npm install")
                lines.append("```")
                lines.append("")
            if 'go' in self.languages:
                lines.append("```bash")
                lines.append("go mod download")
                lines.append("```")
                lines.append("")
        lines.append("<!-- MANUAL_END:setup -->")
        lines.append("")

        # 使用方法
        if 'usage' in manual_sections:
            lines.append("## 使用方法")
            lines.append("")
            lines.append("<!-- MANUAL_START:usage -->")
            lines.append(manual_sections['usage'])
            lines.append("<!-- MANUAL_END:usage -->")
            lines.append("")

        # プロジェクト構造
        structure = self._get_project_structure()
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
        if 'other' in manual_sections:
            lines.append("<!-- MANUAL_START:other -->")
            lines.append(manual_sections['other'])
            lines.append("<!-- MANUAL_END:other -->")
            lines.append("")

        # フッター
        lines.append("---")
        lines.append("")
        lines.append(f"*このREADMEは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

        return '\n'.join(lines)

    def _generate_with_llm(self, manual_sections: Dict[str, str]) -> str:
        """
        LLMを使用してREADME.mdを生成

        Args:
            manual_sections: 保持する手動セクション

        Returns:
            READMEの内容（エラー時はテンプレート生成にフォールバック）
        """
        try:
            # LLMクライアントを取得
            llm_mode = self.agents_config.get('llm_mode', 'api')
            preferred_mode = 'api' if llm_mode in ['api', 'both'] else 'local'

            client = LLMClientFactory.create_client_with_fallback(
                self.agents_config,
                preferred_mode=preferred_mode
            )

            if not client:
                logger.warning("LLMクライアントの作成に失敗しました。テンプレート生成にフォールバックします。")
                return self._generate_template(manual_sections)

            # 既存READMEを読み込む（コンテキストとして使用）
            existing_readme = ""
            if self.readme_path.exists():
                existing_readme = self.readme_path.read_text(encoding='utf-8')

            # プロジェクト情報を収集
            project_info = self.collector.collect_all()

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info, existing_readme, manual_sections)

            # システムプロンプト
            system_prompt = """あなたは技術ドキュメント作成の専門家です。
プロジェクトのREADME.mdを生成してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は必ず保持してください。"""

            # LLMで生成
            logger.info("LLMを使用してREADME.mdを生成中...")
            generated_text = client.generate(prompt, system_prompt=system_prompt)

            if generated_text:
                # LLM出力をクリーンアップ
                cleaned_text = self._clean_llm_output(generated_text)

                # 出力を検証
                if not self._validate_output(cleaned_text):
                    logger.warning("LLM出力の検証に失敗しました。テンプレート生成にフォールバックします。")
                    return self._generate_template(manual_sections)

                # 手動セクションを確実に保持
                result = self._preserve_manual_sections_in_generated(cleaned_text, manual_sections)
                return result
            else:
                logger.warning("LLM生成が空でした。テンプレート生成にフォールバックします。")
                return self._generate_template(manual_sections)

        except Exception as e:
            logger.error(f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。", exc_info=True)
            return self._generate_template(manual_sections)

    def _generate_hybrid(self, manual_sections: Dict[str, str]) -> str:
        """
        テンプレートとLLMを組み合わせて生成

        Args:
            manual_sections: 保持する手動セクション

        Returns:
            READMEの内容
        """
        # まずテンプレートを生成
        template_content = self._generate_template(manual_sections)

        try:
            # LLMクライアントを取得
            llm_mode = self.agents_config.get('llm_mode', 'api')
            preferred_mode = 'api' if llm_mode in ['api', 'both'] else 'local'

            client = LLMClientFactory.create_client_with_fallback(
                self.agents_config,
                preferred_mode=preferred_mode
            )

            if not client:
                logger.warning("LLMクライアントの作成に失敗しました。テンプレートのみを使用します。")
                return template_content

            # 説明セクションのみLLMで改善
            project_info = self.collector.collect_all()
            description = project_info.get('description') or self._collect_project_description()

            prompt = f"""以下のプロジェクト情報を基に、README.mdの「概要」セクションを改善してください。
既存のテンプレート生成内容を参考に、より詳細で有用な説明を生成してください。

プロジェクト情報:
- プロジェクト名: {self.project_root.name}
- 使用言語: {', '.join(self.languages) if self.languages else '不明'}
- 説明: {description or 'なし'}

既存のテンプレート生成内容:
{self._extract_description_section(template_content)}

改善された「概要」セクションをマークダウン形式で出力してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
手動セクション（<!-- MANUAL_START:description --> と <!-- MANUAL_END:description -->）は保持してください。"""

            system_prompt = """あなたは技術ドキュメント作成の専門家です。プロジェクト概要を明確で有用な形で記述してください。
最終的な出力のみを生成し、思考過程や試行錯誤の痕跡を含めないでください。"""

            logger.info("LLMを使用して概要セクションを改善中...")
            improved_description = client.generate(prompt, system_prompt=system_prompt)

            if improved_description:
                # LLM出力をクリーンアップ
                cleaned_description = self._clean_llm_output(improved_description)

                # 出力を検証
                if not self._validate_output(cleaned_description):
                    logger.warning("LLM出力の検証に失敗しました。テンプレートのみを使用します。")
                    return template_content

                # テンプレートの説明セクションを置き換え
                lines = template_content.split('\n')
                new_lines = []
                skip_until_end = False

                for line in lines:
                    if '<!-- MANUAL_START:description -->' in line:
                        new_lines.append(line)
                        new_lines.append("")
                        # 改善された説明を挿入
                        new_lines.extend(cleaned_description.split('\n'))
                        skip_until_end = True
                    elif skip_until_end and '<!-- MANUAL_END:description -->' in line:
                        skip_until_end = False
                        new_lines.append("")
                        new_lines.append(line)
                    elif not skip_until_end:
                        new_lines.append(line)

                return '\n'.join(new_lines)
            else:
                return template_content

        except Exception as e:
            logger.warning(f"ハイブリッド生成中にエラーが発生しました: {e}。テンプレートのみを使用します。", exc_info=True)
            return template_content

    def _create_llm_prompt(self, project_info: Dict[str, Any], existing_readme: str, manual_sections: Dict[str, str]) -> str:
        """
        LLM用のプロンプトを作成

        Args:
            project_info: プロジェクト情報の辞書
            existing_readme: 既存のREADME内容
            manual_sections: 手動セクション

        Returns:
            プロンプト文字列
        """
        prompt = f"""以下のプロジェクト情報を基に、README.mdドキュメントを生成してください。

プロジェクト情報:
- プロジェクト名: {self.project_root.name}
- 使用言語: {', '.join(self.languages) if self.languages else '不明'}
- 説明: {project_info.get('description') or 'なし'}

依存関係:
"""
        dependencies = project_info.get('dependencies', {})
        for dep_type, deps in dependencies.items():
            prompt += f"- {dep_type}: {', '.join(deps[:10])}\n"

        if existing_readme:
            prompt += f"\n既存のREADME（参考）:\n{existing_readme[:1000]}...\n"

        prompt += """
以下のセクションを含めてください:
1. プロジェクト名（見出し）
2. 概要（手動セクションを保持）
3. 使用技術
4. 依存関係（検出された場合）
5. セットアップ手順（手動セクションを保持）
6. 使用方法（手動セクションがある場合）
7. プロジェクト構造

重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は必ず保持してください。"""

        return prompt

    def _preserve_manual_sections_in_generated(self, generated_text: str, manual_sections: Dict[str, str]) -> str:
        """
        生成されたテキストに手動セクションを保持

        Args:
            generated_text: LLMで生成されたテキスト
            manual_sections: 保持する手動セクション

        Returns:
            手動セクションが保持されたテキスト
        """
        lines = generated_text.split('\n')
        new_lines = []
        line_index = 0

        while line_index < len(lines):
            line = lines[line_index]
            replaced = False

            # 手動セクションの開始マーカーを検出
            for section_name, section_content in manual_sections.items():
                if f'<!-- MANUAL_START:{section_name} -->' in line:
                    new_lines.append(line)
                    new_lines.append("")
                    # 既存の手動セクション内容を使用（思考過程を除外）
                    cleaned_content = self._clean_manual_section_content(section_content)
                    new_lines.append(cleaned_content)
                    # 次のMANUAL_ENDまでスキップ
                    line_index += 1
                    while line_index < len(lines):
                        if f'<!-- MANUAL_END:{section_name} -->' in lines[line_index]:
                            new_lines.append("")
                            new_lines.append(lines[line_index])
                            line_index += 1
                            replaced = True
                            break
                        line_index += 1
                    if not replaced:
                        new_lines.append("")
                        new_lines.append(f"<!-- MANUAL_END:{section_name} -->")
                    break

            if not replaced:
                new_lines.append(line)
                line_index += 1

        return '\n'.join(new_lines)

    def _clean_manual_section_content(self, content: str) -> str:
        """
        手動セクションの内容から思考過程を削除

        Args:
            content: 手動セクションの内容

        Returns:
            クリーンアップされた内容
        """
        # 思考過程のパターンを削除
        lines = content.split('\n')
        cleaned_lines = []

        for line in lines:
            # 思考過程のパターンを検出
            if any(pattern in line.lower() for pattern in [
                'we need to', 'thus final answer', 'let\'s generate', 'let\'s do',
                'but we need', 'hence final answer', 'thus final output',
                'i will produce', 'i think', 'ok i\'ll', 'let\'s finalize',
                'but i think', 'but we need to', 'thus final answer will',
                'we should produce', 'we will output', 'we must produce',
                'thus the final', 'but the actual', 'so i will',
                'i\'m going to', 'i\'m still not sure', 'but it\'s enough',
                'let\'s output', 'let\'s produce', 'let\'s final answer'
            ]):
                continue

            # マークダウンコードブロック内の思考過程をスキップ
            if line.strip().startswith('```') and 'markdown' in line.lower():
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _clean_llm_output(self, text: str) -> str:
        """
        LLMの出力から思考過程や試行錯誤の痕跡を削除

        Args:
            text: LLMで生成されたテキスト

        Returns:
            クリーンアップされたテキスト
        """
        if not text:
            return text

        lines = text.split('\n')
        cleaned_lines = []
        skip_block = False
        in_code_block = False
        code_block_lang = None

        i = 0
        while i < len(lines):
            line = lines[i]
            original_line = line

            # コードブロックの開始/終了を検出
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip().lower()
                    # マークダウンコードブロック内の思考過程をスキップ
                    if 'markdown' in code_block_lang:
                        skip_block = True
                        i += 1
                        # 次の```までスキップ
                        while i < len(lines) and not lines[i].strip().startswith('```'):
                            i += 1
                        if i < len(lines):
                            i += 1  # ```をスキップ
                        skip_block = False
                        in_code_block = False
                        continue
                    else:
                        cleaned_lines.append(line)
                        i += 1
                        continue
                else:
                    in_code_block = False
                    code_block_lang = None
                    cleaned_lines.append(line)
                    i += 1
                    continue

            # コードブロック内はそのまま保持
            if in_code_block:
                cleaned_lines.append(line)
                i += 1
                continue

            # 思考過程のパターンを検出
            line_lower = line.lower().strip()

            # 特殊なマーカーパターン（最初にチェック）
            if '<|channel|>' in line or '<|message|>' in line or 'commentary/analysis' in line_lower:
                i += 1
                # 次の空行または通常のコンテンツまでスキップ
                while i < len(lines) and not lines[i].strip().startswith('##') and not lines[i].strip().startswith('<!--'):
                    if lines[i].strip() and not any(pattern in lines[i].lower() for pattern in ['let\'s', 'we need', 'but we', 'thus final']):
                        break
                    i += 1
                continue

            # 思考過程の開始パターン
            thinking_patterns = [
                'we need to', 'thus final answer', 'let\'s generate', 'let\'s do',
                'but we need', 'hence final answer', 'thus final output',
                'i will produce', 'i think', 'ok i\'ll', 'let\'s finalize',
                'but i think', 'but we need to', 'thus final answer will',
                'we should produce', 'we will output', 'we must produce',
                'thus the final', 'but the actual', 'so i will',
                'i\'m going to', 'i\'m still not sure', 'but it\'s enough',
                'let\'s output', 'let\'s produce', 'let\'s final answer',
                'but we need the final', 'thus final answer is', 'we now produce',
                'this content includes', 'but we also mention', 'ok, i will',
                'thus we must', 'but we need to ensure', 'let\'s generate:',
                'we should produce final', 'thus final answer will be',
                'but i\'m still not sure', 'but i think it\'s', 'let\'s finalize:',
                'we need the final answer', 'thus final answer:', 'ok i\'ll produce',
                'we will not include', 'should we keep', 'possibly they want',
                'but we must keep', 'but we might need', 'however, user wrote',
                'also note', 'but the user', 'ok final output', 'ok. i\'ll generate',
                'let\'s create final output', 'check that it doesn\'t', 'now i will provide',
                'the user wants', 'they gave', 'so we should', 'so we can',
                'also keep', 'we must not include', 'so final output',
                'but we must also keep', 'we must only output', 'but we must'
            ]

            # 思考過程の行をスキップ
            if any(pattern in line_lower for pattern in thinking_patterns):
                i += 1
                continue

            # プレースホルダーや不完全な記述を検出
            placeholder_patterns = [
                '???', '(??)', '... ...', '|  | |', '---‐‐‐', 'continue',
                'we should now', 'this content, while present'
            ]

            if any(pattern in line_lower for pattern in placeholder_patterns):
                i += 1
                continue

            # 空行の連続を制限（3行以上は2行に）
            if not line.strip():
                if cleaned_lines and not cleaned_lines[-1].strip():
                    if len(cleaned_lines) >= 2 and not cleaned_lines[-2].strip():
                        i += 1
                        continue

            cleaned_lines.append(line)
            i += 1

        # 結果を結合
        result = '\n'.join(cleaned_lines)

        # 先頭と末尾の空行を削除
        result = result.strip()

        # 重複した説明を削除（同じ行が3回以上続く場合）
        lines_result = result.split('\n')
        deduplicated = []
        prev_line = None
        repeat_count = 0

        for line in lines_result:
            if line == prev_line:
                repeat_count += 1
                if repeat_count < 3:
                    deduplicated.append(line)
            else:
                repeat_count = 0
                deduplicated.append(line)
            prev_line = line

        return '\n'.join(deduplicated)

    def _validate_output(self, text: str) -> bool:
        """
        LLMの出力を検証して、不適切な内容が含まれていないかチェック

        Args:
            text: 検証するテキスト

        Returns:
            検証に合格したかどうか
        """
        if not text or not text.strip():
            return False

        text_lower = text.lower()

        # 特殊なマーカーパターンをチェック
        if '<|channel|>' in text or '<|message|>' in text or 'commentary/analysis' in text_lower:
            logger.warning("特殊なマーカーパターンが検出されました")
            return False

        # 思考過程のパターンが含まれていないかチェック
        thinking_patterns = [
            'thus final answer', 'let\'s generate', 'but we need',
            'i will produce', 'i think', 'let\'s finalize',
            'we should produce', 'we will output', 'thus the final',
            'i\'m going to', 'let\'s output', 'let\'s produce',
            'but i think it\'s', 'thus final answer will be',
            'we will not include', 'should we keep', 'possibly they want',
            'but we must keep', 'but we might need', 'however, user wrote',
            'also note', 'but the user', 'ok final output', 'ok. i\'ll generate',
            'let\'s create final output', 'check that it doesn\'t', 'now i will provide',
            'the user wants', 'they gave', 'so we should', 'so we can',
            'also keep', 'we must not include', 'so final output',
            'but we must also keep', 'we must only output', 'but we must'
        ]

        for pattern in thinking_patterns:
            if pattern in text_lower:
                logger.warning(f"思考過程のパターンが検出されました: {pattern}")
                return False

        # プレースホルダーが含まれていないかチェック
        placeholder_patterns = [
            '???', '(??)', '... ...', '|  | |', '---‐‐‐'
        ]

        for pattern in placeholder_patterns:
            if pattern in text:
                logger.warning(f"プレースホルダーが検出されました: {pattern}")
                return False

        # マークダウンコードブロック内に思考過程が含まれていないかチェック
        lines = text.split('\n')
        in_markdown_block = False
        for line in lines:
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip().lower()
                if 'markdown' in lang:
                    in_markdown_block = True
                elif in_markdown_block:
                    in_markdown_block = False
            elif in_markdown_block:
                if any(pattern in line.lower() for pattern in thinking_patterns):
                    logger.warning("マークダウンコードブロック内に思考過程が検出されました")
                    return False

        return True

    def _extract_description_section(self, content: str) -> str:
        """
        コンテンツから説明セクションを抽出

        Args:
            content: READMEコンテンツ

        Returns:
            説明セクションのテキスト
        """
        lines = content.split('\n')
        description_lines = []
        in_description = False

        for line in lines:
            if '<!-- MANUAL_START:description -->' in line:
                in_description = True
                continue
            elif '<!-- MANUAL_END:description -->' in line:
                break
            elif in_description:
                description_lines.append(line)

        return '\n'.join(description_lines)

    def _detect_dependencies(self) -> Dict[str, List[str]]:
        """
        依存関係を検出

        Returns:
            依存関係タイプをキー、依存関係リストを値とする辞書
        """
        dependencies = {}

        # Python依存関係
        if 'python' in self.languages:
            req_file = self.project_root / 'requirements.txt'
            if req_file.exists():
                import re
                deps = []
                # PEP 440バージョン指定子のパターン（==, >=, <=, !=, ~=, >, <, ===）
                version_spec_pattern = re.compile(r'[=!<>~]+')

                for line in req_file.read_text(encoding='utf-8').split('\n'):
                    line = line.strip()
                    # コメント行や空行をスキップ
                    if not line or line.startswith('#'):
                        continue

                    # URLやファイルパスの場合はスキップ（-e, @などで始まる行）
                    if line.startswith('-e ') or line.startswith('@') or '://' in line:
                        continue

                    # バージョン指定子の前までをパッケージ名として抽出
                    # 例: "requests!=2.28.0" -> "requests"
                    # 例: "django~=4.0" -> "django"
                    match = version_spec_pattern.search(line)
                    if match:
                        package_name = line[:match.start()].strip()
                    else:
                        # バージョン指定子がない場合（パッケージ名のみ）
                        package_name = line.split()[0] if line.split() else line

                    # パッケージ名が有効な場合のみ追加
                    if package_name:
                        deps.append(package_name)

                if deps:
                    dependencies['Python'] = deps

        # JavaScript依存関係
        if 'javascript' in self.languages or 'typescript' in self.languages:
            package_file = self.project_root / 'package.json'
            if package_file.exists():
                import json
                try:
                    with open(package_file, 'r', encoding='utf-8') as f:
                        package_data = json.load(f)
                        deps = []
                        if 'dependencies' in package_data:
                            deps.extend(list(package_data['dependencies'].keys()))
                        if 'devDependencies' in package_data:
                            deps.extend(list(package_data['devDependencies'].keys()))
                        if deps:
                            dependencies['Node.js'] = deps
                except:
                    pass

        # Go依存関係
        if 'go' in self.languages:
            go_mod = self.project_root / 'go.mod'
            if go_mod.exists():
                deps = []
                lines = go_mod.read_text(encoding='utf-8').split('\n')
                in_require_block = False

                for line in lines:
                    line = line.strip()

                    # 複数行のrequireブロックの開始を検出
                    if line.startswith('require ('):
                        in_require_block = True
                        continue

                    # 複数行のrequireブロックの終了を検出
                    if in_require_block and line == ')':
                        in_require_block = False
                        continue

                    # ブロック内の依存関係を抽出
                    if in_require_block:
                        # 空行やコメントをスキップ
                        if not line or line.startswith('//'):
                            continue
                        parts = line.split()
                        if len(parts) >= 1:
                            deps.append(parts[0])

                    # 単一行のrequireを検出
                    elif line.startswith('require ') and not line.startswith('require ('):
                        parts = line.split()
                        if len(parts) >= 2:
                            deps.append(parts[1])

                if deps:
                    dependencies['Go'] = deps

        return dependencies

    def _get_project_structure(self) -> List[str]:
        """
        プロジェクト構造を取得（重要なディレクトリとファイルのみ）

        Returns:
            構造の行リスト
        """
        structure = []

        # 重要なディレクトリ（表示する）
        important_dirs = {'docgen', '.github', 'docs', 'scripts', 'tests'}

        # 除外するディレクトリ（キャッシュ、仮想環境など）
        exclude_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.idea', '.vscode', '.pytest_cache', '.mypy_cache',
            'htmlcov', '.coverage', 'dist', 'build', '*.egg-info'
        }

        # 重要なルートレベルのファイル
        important_files = {
            'README.md', 'AGENTS.md', 'pyproject.toml', 'pytest.ini',
            'requirements.txt', 'requirements-docgen.txt', 'requirements-test.txt',
            'setup.sh', 'package.json', 'go.mod', 'Makefile'
        }

        def _should_include(item: Path, is_root: bool = False) -> bool:
            """アイテムを含めるべきか判定"""
            if item.is_dir():
                # 重要なディレクトリは含める
                if item.name in important_dirs:
                    return True
                # 除外ディレクトリは含めない（隠しディレクトリも除外）
                if item.name in exclude_dirs or item.name.startswith('.'):
                    return False
                return True  # その他の通常ディレクトリは含める
            else:
                # ルートレベルの重要なファイルは含める
                if is_root and item.name in important_files:
                    return True
                return False

        def _walk_dir(path: Path, prefix: str = "", max_depth: int = 2, current_depth: int = 0, is_root: bool = False):
            """ディレクトリを再帰的に走査"""
            if current_depth >= max_depth:
                return

            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
                filtered_items = []

                for item in items:
                    if _should_include(item, is_root=(current_depth == 0)):
                        filtered_items.append(item)

                for i, item in enumerate(filtered_items):
                    is_last = i == len(filtered_items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    structure.append(f"{prefix}{current_prefix}{item.name}")

                    # ディレクトリの場合、重要なサブディレクトリのみ表示
                    if item.is_dir() and current_depth < max_depth - 1:
                        # docgen, .github, docs, scripts, tests の主要サブディレクトリのみ
                        if item.name == 'docgen':
                            # docgenの主要サブディレクトリ
                            subdirs = ['detectors', 'generators', 'collectors', 'hooks', 'templates']
                            sub_items = []
                            for subdir in subdirs:
                                sub_path = item / subdir
                                if sub_path.exists() and sub_path.is_dir():
                                    sub_items.append(sub_path)
                            if sub_items:
                                for j, sub_item in enumerate(sub_items):
                                    sub_is_last = j == len(sub_items) - 1
                                    sub_prefix = "└── " if sub_is_last else "├── "
                                    next_prefix = prefix + ("    " if is_last else "│   ")
                                    structure.append(f"{next_prefix}{sub_prefix}{sub_item.name}")
                        elif item.name == '.github':
                            # .github/workflows のみ
                            workflows = item / 'workflows'
                            if workflows.exists():
                                next_prefix = prefix + ("    " if is_last else "│   ")
                                structure.append(f"{next_prefix}└── workflows")
                        elif item.name == 'docs':
                            # docsの主要サブディレクトリ（implementationは省略）
                            subdirs = ['implementation']
                            for subdir in subdirs:
                                sub_path = item / subdir
                                if sub_path.exists() and sub_path.is_dir():
                                    next_prefix = prefix + ("    " if is_last else "│   ")
                                    structure.append(f"{next_prefix}└── {subdir}/")
                                    break
                        elif item.name in important_dirs:
                            # 重要なディレクトリ（scripts, testsなど）は再帰的に走査
                            next_prefix = prefix + ("    " if is_last else "│   ")
                            _walk_dir(item, next_prefix, max_depth, current_depth + 1, is_root=False)
                        # その他の通常ディレクトリ（srcなど）は表示するが、中身は走査しない
            except PermissionError:
                pass

        _walk_dir(self.project_root, is_root=True)
        return structure

    def _collect_project_description(self) -> Optional[str]:
        """
        プロジェクトの説明を収集

        Returns:
            プロジェクトの説明文（見つからない場合はNone）
        """
        # main.pyのdocstringから取得
        main_py = self.project_root / 'main.py'
        if main_py.exists():
            try:
                import re
                content = main_py.read_text(encoding='utf-8')
                # モジュールレベルのdocstringを抽出
                docstring_pattern = r'"""(.*?)"""'
                match = re.search(docstring_pattern, content, re.DOTALL)
                if match:
                    docstring = match.group(1).strip()
                    if docstring and len(docstring) > 10:  # 短すぎる場合はスキップ
                        return docstring.split('\n')[0]  # 最初の行のみ
            except Exception:
                pass

        # __init__.pyのdocstringから取得
        init_py = self.project_root / '__init__.py'
        if init_py.exists():
            try:
                import re
                content = init_py.read_text(encoding='utf-8')
                docstring_pattern = r'"""(.*?)"""'
                match = re.search(docstring_pattern, content, re.DOTALL)
                if match:
                    docstring = match.group(1).strip()
                    if docstring and len(docstring) > 10:
                        return docstring.split('\n')[0]
            except Exception:
                pass

        # pyproject.tomlのdescriptionから取得
        pyproject = self.project_root / 'pyproject.toml'
        if pyproject.exists():
            try:
                import sys
                if sys.version_info >= (3, 11):
                    import tomllib
                    with open(pyproject, 'rb') as f:
                        data = tomllib.load(f)
                else:
                    try:
                        import tomli
                        with open(pyproject, 'rb') as f:
                            data = tomli.load(f)
                    except ImportError:
                        data = {}

                if 'project' in data and 'description' in data['project']:
                    description = data['project']['description']
                    if description and len(description) > 10:
                        return description
            except Exception:
                pass

        return None

