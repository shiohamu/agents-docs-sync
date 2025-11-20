"""Test fixtures for test suite (simplified path handling)."""

from pathlib import Path
import shutil

# Minimal: always ensure repo root is on sys.path so imports like test_utils.common work
import sys
import tempfile

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="function")
def temp_project():
    """Create a temporary project directory with basic structure."""
    temp_dir = Path(tempfile.mkdtemp())

    (temp_dir / "docgen").mkdir()
    (temp_dir / "docgen" / "config.yaml").write_text("""
output:
  agents_doc: AGENTS.md
  api_doc: api.md
  readme: README.md

agents:
  llm_mode: both
  api:
    provider: openai
    api_key_env: OPENAI_API_KEY
  local:
    provider: ollama
    model: llama3
    base_url: http://localhost:11434

project:
  name: test-project
  description: Test project for agents-docs-sync
  languages: [python]
""")
    yield temp_dir

    # Clean up
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def sample_config():
    """Return a sample configuration dictionary."""
    return {
        "output": {"agents_doc": "AGENTS.md", "api_doc": "api.md", "readme": "README.md"},
        "agents": {
            " llm_mode": "both",
            "api": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
            "local": {
                "provider": "ollama",
                "model": "llama3",
                "base_url": "http://localhost:11434",
            },
        },
        "project": {
            "name": "test-project",
            "description": "Test project for agents-docs-sync",
            "languages": ["python"],
        },
    }


@pytest.fixture(scope="function")
def mock_llm_client(mocker):
    """Mock LLMクライアント"""
    mock_client = mocker.Mock()
    mock_client.generate.return_value = "Mocked LLM response"
    return mock_client
