import logging
from pathlib import Path
import sys
import time

from .config import ConfigLoader, TaskConfig
from .tasks.base import HookContext, TaskStatus

# ロガー設定
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class HookOrchestrator:
    """Git hook実行のオーケストレーター"""

    def __init__(self, hook_name: str, args: list[str] = None):
        self.hook_name = hook_name
        self.args = args or []
        self.project_root = self._find_project_root()
        self.config_loader = ConfigLoader(str(self.project_root))
        self.hooks_config = self.config_loader.load_config()
        self.task_registry = {}

    def _find_project_root(self) -> Path:
        """プロジェクトルートを見つける"""
        # 現在のディレクトリから親を辿って.gitを探す
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()  # フォールバック

    def register_task(self, name: str, task_class: type):
        """タスクを登録する"""
        self.task_registry[name] = task_class

    def run(self) -> int:
        """フックを実行する"""
        hook_config = self.hooks_config.get(self.hook_name)

        # 設定がない、または無効な場合は何もしない（成功扱い）
        if not hook_config or not hook_config.enabled:
            return 0

        logger.info(f"Running git hook: {self.hook_name}")

        context = HookContext(
            project_root=str(self.project_root), hook_name=self.hook_name, args=self.args
        )

        success = True

        for task_config in hook_config.tasks:
            if not task_config.enabled:
                continue

            if not self._run_task(task_config, context):
                success = False
                if not task_config.continue_on_error:
                    logger.error(f"Hook failed at task: {task_config.name}")
                    return 1

        return 0 if success else 1

    def _run_task(self, config: TaskConfig, context: HookContext) -> bool:
        """個別タスクを実行する"""
        task_class = self.task_registry.get(config.name)
        if not task_class:
            logger.warning(f"Unknown task: {config.name}")
            return True  # 未知のタスクはスキップして成功扱い（またはエラーにするか検討）

        try:
            task = task_class(config)

            if not task.should_run(context):
                return True

            logger.info(f"  Running task: {config.name}...")
            start_time = time.time()

            result = task.run(context)

            duration = time.time() - start_time

            if result.status == TaskStatus.SUCCESS:
                logger.info(f"  ✓ {config.name} passed ({duration:.2f}s)")
                return True
            elif result.status == TaskStatus.SKIPPED:
                logger.info(f"  - {config.name} skipped")
                return True
            else:
                logger.error(f"  ✗ {config.name} failed: {result.message}")
                return False

        except Exception as e:
            logger.error(f"  ✗ {config.name} error: {str(e)}")
            return False


def main():
    """エントリーポイント"""
    if len(sys.argv) < 2:
        print("Usage: python -m docgen.hooks.orchestrator <hook_name> [args...]")
        sys.exit(1)

    hook_name = sys.argv[1]
    args = sys.argv[2:]

    # ここでタスクの登録を行う（動的インポートなどが望ましいが、一旦静的に）
    orchestrator = HookOrchestrator(hook_name, args)

    # タスクのインポートと登録（遅延インポートで循環参照回避）
    from .tasks.commit_msg_generator import CommitMsgGeneratorTask
    from .tasks.doc_generator import DocGeneratorTask
    from .tasks.file_stager import FileStagerTask
    from .tasks.rag_generator import RagGeneratorTask
    from .tasks.test_runner import TestRunnerTask
    from .tasks.version_checker import VersionCheckerTask

    orchestrator.register_task("run_tests", TestRunnerTask)
    orchestrator.register_task("generate_docs", DocGeneratorTask)
    orchestrator.register_task("generate_rag", RagGeneratorTask)
    orchestrator.register_task("stage_changes", FileStagerTask)
    orchestrator.register_task("generate_commit_message", CommitMsgGeneratorTask)
    orchestrator.register_task("check_version", VersionCheckerTask)
    # 他のタスクも登録

    sys.exit(orchestrator.run())


if __name__ == "__main__":
    main()
