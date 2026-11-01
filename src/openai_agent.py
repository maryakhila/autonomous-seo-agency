import os
from openai import OpenAI


class OpenAIAgent:
    def __init__(self, employee_name, instructions):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Please configure your API key."
            )

        self.client = OpenAI(api_key=api_key)
        self.employee_name = employee_name
        self.instructions = instructions

    def perform_task(self, task):
        response = self.client.responses.create(
            model="gpt-5-mini",
            instructions=self.instructions,
            input=task
        )

        return response.output_text
