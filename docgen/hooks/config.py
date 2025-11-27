from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TaskConfig:
    """タスク設定"""

    name: str
    enabled: bool = True
    continue_on_error: bool = False
    timeout: int | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class HookConfig:
    """フック設定"""

    name: str
    tasks: list[TaskConfig]
    enabled: bool = True


class ConfigLoader:
    """フック設定ローダー"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.hooks_config_path = self.project_root / "docgen" / "hooks.yaml"

    def load_config(self) -> dict[str, HookConfig]:
        """設定を読み込む"""
        config_data = self._read_yaml()
        hooks = {}

        hooks_data = config_data.get("hooks", {})
        for hook_name, hook_data in hooks_data.items():
            if not isinstance(hook_data, dict):
                continue

            tasks = []
            for task_data in hook_data.get("tasks", []):
                tasks.append(
                    TaskConfig(
                        name=task_data.get("name"),
                        enabled=task_data.get("enabled", True),
                        continue_on_error=task_data.get("continue_on_error", False),
                        timeout=task_data.get("timeout"),
                        params=task_data.get("params", {}),
                    )
                )

            hooks[hook_name] = HookConfig(
                name=hook_name, enabled=hook_data.get("enabled", True), tasks=tasks
            )

        return hooks

    def _read_yaml(self) -> dict[str, Any]:
        """YAMLファイルを読み込む"""
        if not self.hooks_config_path.exists():
            return {}

        try:
            with open(self.hooks_config_path) as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load hooks config: {e}")
            return {}
