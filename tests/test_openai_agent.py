import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from openai_agent import OpenAIAgent


def test_openai_agent_initialization():
    with patch("openai_agent.OpenAI"):
        agent = OpenAIAgent(
            "SEO Researcher",
            "Research websites and SEO topics."
        )

        assert agent.employee_name == "SEO Researcher"
        assert agent.instructions == "Research websites and SEO topics."
