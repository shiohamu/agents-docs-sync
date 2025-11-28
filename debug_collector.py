from pathlib import Path

from docgen.collectors.project_info_collector import ProjectInfoCollector

root = Path("/home/user/projects/hamu/agents-docs-sync")
collector = ProjectInfoCollector(root)
info = collector.collect_all()
print(f"Project Structure: {info.project_structure}")
print(f"Key Features: {info.key_features}")
