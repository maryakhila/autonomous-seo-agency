from pathlib import Path
from openai_agent import OpenAIAgent


class AgentRunner:

    def __init__(self):
        self.agents_folder = Path(__file__).parent.parent / "agents"

    def list_agents(self):
        print("AVAILABLE SEO AGENTS")

        for agent_file in sorted(self.agents_folder.glob("*.md")):
            if agent_file.name == "README.md":
                continue

            print(f"- {agent_file.stem}")

    def read_agent_instructions(self, agent_name):
        agent_file = self.agents_folder / f"{agent_name}.md"

        if not agent_file.exists():
            print("Agent instruction file not found.")
            return None

        return agent_file.read_text(encoding="utf-8")

    def create_agent(self, agent_name):
        instructions = self.read_agent_instructions(agent_name)

        if not instructions:
            return None

        return OpenAIAgent(
            employee_name=agent_name,
            instructions=instructions
        )


if __name__ == "__main__":
    runner = AgentRunner()

    runner.list_agents()

    agent = runner.create_agent("seo-researcher")

    if agent:
        print(f"\nAI employee created: {agent.employee_name}")
