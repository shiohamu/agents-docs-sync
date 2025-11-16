#!/usr/bin/env python3
"""
汎用ドキュメント自動生成システム
コミット時にAPIドキュメントとREADME.mdを自動更新します。
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Optional, Dict, Any

# プロジェクトルートのパスを取得
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCGEN_DIR = Path(__file__).parent.resolve()

# モジュールパスを追加
sys.path.insert(0, str(DOCGEN_DIR))

from detectors.python_detector import PythonDetector
from detectors.javascript_detector import JavaScriptDetector
from detectors.go_detector import GoDetector
from detectors.generic_detector import GenericDetector
from generators.api_generator import APIGenerator
from generators.readme_generator import ReadmeGenerator


class DocGen:
    """ドキュメント自動生成メインクラス"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初期化

        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        self.project_root = PROJECT_ROOT
        self.docgen_dir = DOCGEN_DIR
        self.config_path = config_path or self.docgen_dir / "config.yaml"
        self.config = self._load_config()
        self.detected_languages = []

    def _load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
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
                'readme': 'README.md'
            },
            'generation': {
                'update_readme': True,
                'generate_api_doc': True,
                'preserve_manual_sections': True
            }
        }

    def detect_languages(self) -> list:
        """
        プロジェクトの使用言語を自動検出

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
        for detector in detectors:
            if detector.detect():
                lang = detector.get_language()
                if lang not in detected:
                    detected.append(lang)
                    print(f"✓ 検出: {lang}")

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
            print("警告: サポートされている言語が検出されませんでした")
            return False

        success = True

        # APIドキュメント生成
        if self.config.get('generation', {}).get('generate_api_doc', True):
            print("\n[APIドキュメント生成]")
            api_generator = APIGenerator(
                self.project_root,
                self.detected_languages,
                self.config
            )
            if api_generator.generate():
                print("✓ APIドキュメントを生成しました")
            else:
                print("✗ APIドキュメントの生成に失敗しました")
                success = False

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

        return success


def main():
    """メインエントリーポイント"""
    import argparse

    parser = argparse.ArgumentParser(
        description='汎用ドキュメント自動生成システム'
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

    args = parser.parse_args()

    docgen = DocGen(config_path=args.config)

    if args.detect_only:
        languages = docgen.detect_languages()
        print(f"\n検出された言語: {', '.join(languages) if languages else 'なし'}")
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

