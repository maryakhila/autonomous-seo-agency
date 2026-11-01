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

    print("\nCREATING SEO EMPLOYEES...")

    employees = [
        "seo-researcher",
        "keyword-analyst",
         "technical-auditor",
          "competitor-analyst",
        "content-writer",
        "on-page-specialist",
        "performance-analyst",
        "project_manager"
    ]

    for employee_name in employees:
        agent = runner.create_agent(employee_name)

        if agent:
            print(f"\nAI employee ready: {agent.employee_name}")

            result = agent.perform_task(
                "Prepare a beginner-friendly SEO report for a small local bakery."
            )

            print("\nEMPLOYEE REPORT:")
            print(result)


if __name__ == "__main__":
    main()
