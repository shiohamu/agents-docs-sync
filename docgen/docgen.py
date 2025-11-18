#!/usr/bin/env python3
"""
汎用ドキュメント自動生成システム
コミット時にAPIドキュメントとREADME.mdを自動更新します。
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# プロジェクトルートのパスを取得
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCGEN_DIR = Path(__file__).parent.resolve()

# モジュールパスを追加（メインエントリーポイントとして実行される場合に必要）
# 注意: このファイルは直接実行されることを想定しているため、sys.path.insertが必要
# パッケージとしてインストールされた場合は相対インポートを使用
try:
    from .detectors.python_detector import PythonDetector
    from .detectors.javascript_detector import JavaScriptDetector
    from .detectors.go_detector import GoDetector
    from .detectors.generic_detector import GenericDetector
    from .generators.api_generator import APIGenerator
    from .generators.readme_generator import ReadmeGenerator
    from .generators.agents_generator import AgentsGenerator
    from .utils.logger import get_logger
except (ImportError, ValueError, SystemError):
    # 直接実行される場合のフォールバック
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from detectors.python_detector import PythonDetector
    from detectors.javascript_detector import JavaScriptDetector
    from detectors.go_detector import GoDetector
    from detectors.generic_detector import GenericDetector
    from generators.api_generator import APIGenerator
    from generators.readme_generator import ReadmeGenerator
    from generators.agents_generator import AgentsGenerator
    from utils.logger import get_logger

# ロガーの初期化
logger = get_logger("docgen")


class DocGen:
    """ドキュメント自動生成メインクラス"""

    def __init__(self, project_root: Optional[Path] = None, config_path: Optional[Path] = None):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ（Noneの場合は現在の作業ディレクトリ）
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        # プロジェクトルートの決定
        # パッケージとしてインストールされた場合、実行時のカレントディレクトリを使用
        if project_root is None:
            self.project_root = Path.cwd().resolve()
        else:
            self.project_root = Path(project_root).resolve()

        # docgenディレクトリはプロジェクトルート内のdocgenディレクトリ
        self.docgen_dir = self.project_root / "docgen"

        # 設定ファイルのパス決定
        if config_path is not None:
            self.config_path = Path(config_path).resolve()
        else:
            # プロジェクトルート内のdocgen/config.yamlを優先
            self.config_path = self.docgen_dir / "config.yaml"
            # パッケージ内のconfig.yaml.sampleを参照するためのパス
            self._package_config_sample = DOCGEN_DIR / "config.yaml.sample"

        self.config = self._load_config()
        self.detected_languages = []

    def _load_config(self) -> Dict[str, Any]:
        """
        設定ファイルを読み込む

        Returns:
            設定辞書。ファイルが存在しない場合はデフォルト設定を返す
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                    return config
            except yaml.YAMLError as e:
                logger.warning(f"設定ファイルの解析に失敗しました: {e}")
                logger.info("デフォルト設定を使用します。")
                return self._get_default_config()
            except Exception as e:
                logger.warning(f"設定ファイルの読み込みに失敗しました: {e}")
                logger.info("デフォルト設定を使用します。")
                return self._get_default_config()
        else:
            # 設定ファイルが存在しない場合、sampleからコピーを試みる
            # まず、プロジェクトルート内のdocgen/config.yaml.sampleを確認
            sample_path = self.docgen_dir / "config.yaml.sample"
            if not sample_path.exists():
                # プロジェクト内にない場合は、パッケージ内のsampleを参照
                sample_path = getattr(self, '_package_config_sample', None)
                if sample_path is None:
                    sample_path = DOCGEN_DIR / "config.yaml.sample"

            if sample_path.exists():
                try:
                    import shutil
                    # docgenディレクトリが存在しない場合は作成
                    self.docgen_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(sample_path, self.config_path)
                    logger.info(f"{sample_path.name}から{self.config_path.name}を作成しました。")
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f) or {}
                except Exception as e:
                    logger.warning(f"設定ファイルの作成に失敗しました: {e}")
                    logger.info("デフォルト設定を使用します。")
            else:
                logger.warning(f"設定ファイルが見つかりません: {self.config_path}")
                logger.info("デフォルト設定を使用します。")
            return self._get_default_config()

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
                'agents_doc': 'AGENTS.md'
            },
            'generation': {
                'update_readme': True,
                'generate_api_doc': True,
                'generate_agents_doc': True,
                'preserve_manual_sections': True
            }
        }

    def detect_languages(self, use_parallel: bool = True) -> List[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        detectors = [
            PythonDetector(self.project_root),
            JavaScriptDetector(self.project_root),
            GoDetector(self.project_root),
            GenericDetector(self.project_root)
        ]

        detected = []

        if use_parallel:
            # 並列処理で検出
            with ThreadPoolExecutor(max_workers=len(detectors)) as executor:
                future_to_detector = {
                    executor.submit(detector.detect): detector
                    for detector in detectors
                }

                for future in as_completed(future_to_detector):
                    detector = future_to_detector[future]
                    try:
                        if future.result():
                            lang = detector.get_language()
                            if lang not in detected:
                                detected.append(lang)
                                logger.info(f"✓ 検出: {lang}")
                    except Exception as e:
                        logger.warning(f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}")
        else:
            # 逐次処理で検出
            for detector in detectors:
                try:
                    if detector.detect():
                        lang = detector.get_language()
                        if lang not in detected:
                            detected.append(lang)
                            logger.info(f"✓ 検出: {lang}")
                except Exception as e:
                    logger.warning(f"言語検出中にエラーが発生しました ({detector.__class__.__name__}): {e}")

        self.detected_languages = detected
        return detected

    def generate_documents(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        if not self.detected_languages:
            self.detect_languages()

        if not self.detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        success = True

        # APIドキュメント生成
        if self.config.get('generation', {}).get('generate_api_doc', True):
            logger.info("[APIドキュメント生成]")
            try:
                api_generator = APIGenerator(
                    self.project_root,
                    self.detected_languages,
                    self.config
                )
                if api_generator.generate():
                    logger.info("✓ APIドキュメントを生成しました")
                else:
                    logger.error("✗ APIドキュメントの生成に失敗しました")
                    success = False
            except Exception as e:
                logger.error(f"✗ APIドキュメントの生成中にエラーが発生しました: {e}", exc_info=True)
                success = False

        # README生成
        if self.config.get('generation', {}).get('update_readme', True):
            logger.info("[README生成]")
            try:
                readme_generator = ReadmeGenerator(
                    self.project_root,
                    self.detected_languages,
                    self.config
                )
                if readme_generator.generate():
                    logger.info("✓ READMEを更新しました")
                else:
                    logger.error("✗ READMEの更新に失敗しました")
                    success = False
            except Exception as e:
                logger.error(f"✗ READMEの更新中にエラーが発生しました: {e}", exc_info=True)
                success = False

        # AGENTS.md生成
        if self.config.get('generation', {}).get('generate_agents_doc', True):
            logger.info("[AGENTS.md生成]")
            try:
                agents_generator = AgentsGenerator(
                    self.project_root,
                    self.detected_languages,
                    self.config
                )
                if agents_generator.generate():
                    logger.info("✓ AGENTS.mdを生成しました")
                else:
                    logger.error("✗ AGENTS.mdの生成に失敗しました")
                    success = False
            except Exception as e:
                logger.error(f"✗ AGENTS.mdの生成中にエラーが発生しました: {e}", exc_info=True)
                success = False

        return success


def main():
    """メインエントリーポイント"""
    import argparse
    try:
        from . import __version__
    except (ImportError, ValueError, SystemError):
        __version__ = "0.0.1"

    parser = argparse.ArgumentParser(
        description='汎用ドキュメント自動生成システム'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='設定ファイルのパス'
    )
    parser.add_argument(
        '--detect-only',
        action='store_true',
        help='言語検出のみ実行'
    )
    parser.add_argument(
        '--no-api-doc',
        action='store_true',
        help='APIドキュメントを生成しない'
    )
    parser.add_argument(
        '--no-readme',
        action='store_true',
        help='READMEを更新しない'
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=['commit-msg'],
        help='実行するコマンド（commit-msg: コミットメッセージ生成）'
    )

    args = parser.parse_args()

    # 実行時のカレントディレクトリをプロジェクトルートとして使用
    project_root = Path.cwd().resolve()
    docgen = DocGen(project_root=project_root, config_path=args.config)

    # コミットメッセージ生成コマンド
    if args.command == 'commit-msg':
        try:
            from .generators.commit_message_generator import CommitMessageGenerator
        except (ImportError, ValueError, SystemError):
            from generators.commit_message_generator import CommitMessageGenerator

        generator = CommitMessageGenerator(project_root, docgen.config)
        message = generator.generate()
        if message:
            print(message)
            return 0
        else:
            return 1

    if args.detect_only:
        languages = docgen.detect_languages()
        logger.info(f"\n検出された言語: {', '.join(languages) if languages else 'なし'}")
        return 0

    # 設定を一時的に上書き
    if args.no_api_doc:
        docgen.config.setdefault('generation', {})['generate_api_doc'] = False
    if args.no_readme:
        docgen.config.setdefault('generation', {})['update_readme'] = False

    if docgen.generate_documents():
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())

