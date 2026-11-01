
class ProjectManager:

    def __init__(self):
        self.employees = {
            "SEO Researcher": "seo-researcher",
            "Keyword Analyst": "keyword-analyst",
            "Technical SEO Auditor": "technical-auditor",
            "Content Writer": "content-writer",
            "On-Page SEO Specialist": "on-page-specialist",
            "Competitor Analyst": "competitor-analyst",
            "Performance Analyst": "performance-analyst"
        }

    def show_team(self):
        print("PROJECT MANAGER: Team Overview")

        for number, employee in enumerate(self.employees, start=1):
            print(f"{number}. {employee}")

    def assign_task(self, employee, task):
        if employee not in self.employees:
            print("Employee not found.")
            return

        print(f"\nTask assigned to: {employee}")
        print(f"Task: {task}")


if __name__ == "__main__":
    manager = ProjectManager()

    manager.show_team()

    manager.assign_task(
        "SEO Researcher",
        "Research the client's website"
    )
