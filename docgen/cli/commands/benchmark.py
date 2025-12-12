"""
Benchmark command - Run benchmarks and generate reports
"""

from argparse import Namespace
from pathlib import Path

from ...benchmark import BenchmarkRecorder, BenchmarkReporter
from ...utils.logger import get_logger
from .base import BaseCommand

logger = get_logger("docgen.cli.benchmark")


class BenchmarkCommand(BaseCommand):
    """ベンチマークコマンド"""

    def execute(self, args: Namespace, project_root: Path) -> int:
        """
        Run benchmarks and generate reports

        Args:
            args: Command line arguments
            project_root: Project root directory

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        from ... import DocGen

        # ベンチマークを有効化
        config_updates = {"benchmark.enabled": True}

        # Initialize DocGen
        config_path = getattr(args, "config", None)
        docgen = DocGen(project_root=project_root, config_path=config_path)
        docgen.update_config(config_updates)

        # レコーダーをリセット
        BenchmarkRecorder.reset_global()
        recorder = BenchmarkRecorder.get_global()

        # 測定対象の決定
        targets = getattr(args, "targets", None) or []
        if not targets:
            # デフォルト: 全ての処理を測定
            targets = ["all"]

        # ベンチマーク実行
        try:
            if "all" in targets or "generate" in targets:
                logger.info("ドキュメント生成のベンチマークを実行中...")
                success = docgen.generate_documents()
                if not success:
                    logger.warning("ドキュメント生成中にエラーが発生しましたが、ベンチマークは続行します")

            # 結果の取得
            results = recorder.get_results()
            if not results:
                logger.warning("ベンチマーク結果が記録されていません")
                return 1

            # レポート生成
            reporter = BenchmarkReporter(recorder)
            output_format = getattr(args, "format", "markdown")
            output_path = getattr(args, "output", None)

            if output_format == "json":
                if output_path:
                    path = Path(output_path)
                    reporter.save_json(path)
                    logger.info(f"JSONレポートを保存しました: {path}")
                else:
                    import json

                    content = reporter.generate_json()
                    print(json.dumps(content, indent=2, ensure_ascii=False))
            else:  # markdown
                if output_path:
                    path = Path(output_path)
                    reporter.save_markdown(path)
                    logger.info(f"Markdownレポートを保存しました: {path}")
                else:
                    # 標準出力に表示
                    markdown = reporter.generate_markdown()
                    print("\n" + markdown)

            # ボトルネックの表示
            bottlenecks = reporter.detect_bottlenecks()
            if bottlenecks:
                logger.info("\n⚠️  ボトルネックが検出されました:")
                for bottleneck in bottlenecks:
                    logger.info(f"  - {bottleneck}")

            return 0

        except Exception as e:
            logger.error(f"ベンチマーク実行中にエラーが発生しました: {e}", exc_info=True)
            return 1

