
import json
from pathlib import Path
from datetime import datetime


class TaskManager:

    def __init__(self):
        self.data_folder = Path(__file__).parent.parent / "data"
        self.data_folder.mkdir(exist_ok=True)

        self.tasks_file = self.data_folder / "tasks.json"

        if not self.tasks_file.exists():
            self.tasks_file.write_text("[]", encoding="utf-8")

    def load_tasks(self):
        with open(self.tasks_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def assign_task(self, employee, task):
        tasks = self.load_tasks()

        new_task = {
            "employee": employee,
            "task": task,
            "status": "Pending",
            "created_at": datetime.now().isoformat()
        }

        tasks.append(new_task)

        with open(self.tasks_file, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

        print(f"Task assigned to {employee} successfully!")

    def show_tasks(self):
        tasks = self.load_tasks()

        for task in tasks:
            print(task)


if __name__ == "__main__":
    manager = TaskManager()

    manager.assign_task(
        "SEO Researcher",
        "Research the client website"
    )

    manager.show_tasks()
