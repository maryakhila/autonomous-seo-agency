import os
from openai import OpenAI


class OpenAIAgent:
    def __init__(self, employee_name, instructions):
        self.employee_name = employee_name
        self.instructions = instructions

        self.mock_mode = (
            os.getenv("MOCK_AI_MODE", "true").lower() == "true"
        )

        self.client = None

        if not self.mock_mode:
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing.")

            self.client = OpenAI(api_key=api_key)

    def perform_task(self, task):
        if self.mock_mode:
            return (
                f"MOCK SEO REPORT - {self.employee_name}\n"
                f"Task: {task}\n\n"
                "This is a simulated result for testing. "
                "No OpenAI API request was made."
            )

        response = self.client.responses.create(
            model="gpt-5-mini",
            instructions=self.instructions,
            input=task
        )

        return response.output_text
