
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from agent_runner import AgentRunner


def test_agent_runner_finds_agents():
    runner = AgentRunner()

    agent_files = list(runner.agents_folder.glob("*.md"))

    agent_files = [
        file for file in agent_files
        if file.name != "README.md"
    ]

    assert len(agent_files) == 8


def test_agent_runner_reads_seo_researcher():
    runner = AgentRunner()

    instructions = runner.read_agent_instructions(
        "seo-researcher"
    )

    assert instructions is not None
    assert "SEO Researcher" in instructions


if __name__ == "__main__":
    test_agent_runner_finds_agents()
    test_agent_runner_reads_seo_researcher()

    print("All Agent Runner tests passed!")
