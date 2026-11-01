from openai import OpenAI


class OpenAIAgent:
    def __init__(self, employee_name, instructions):
        self.client = OpenAI()
        self.employee_name = employee_name
        self.instructions = instructions

    def perform_task(self, task):
        response = self.client.responses.create(
            model="gpt-5-mini",
            instructions=self.instructions,
            input=task
        )

        return response.output_text
