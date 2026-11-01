import os
from dotenv import load_dotenv
from agent_runner import AgentRunner
from seo_workflow import SEOWorkflow

load_dotenv()


def main():
    print("WELCOME TO YOUR AUTONOMOUS SEO AGENCY")
    print("=====================================")

    if not os.getenv("OPENAI_API_KEY"):
        print("OpenAI API key is not configured.")
        return

    print("OpenAI API key found.")

    workflow = SEOWorkflow()
    workflow.show_workflow()

    runner = AgentRunner()

    print("\nCREATING YOUR FIRST AI EMPLOYEE...")

    agent = runner.create_agent("seo-researcher")

    if agent:
        print(f"AI employee ready: {agent.employee_name}")
        print("\nRunning a test SEO task...")

        result = agent.perform_task(
            "Give me three important SEO factors for a small business website."
        )

        print("\nSEO RESEARCH RESULT:")
        print(result)


if __name__ == "__main__":
    main()
