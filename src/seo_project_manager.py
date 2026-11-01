
from task_manager import TaskManager
from client_manager import ClientManager
from project_manager import ProjectManager


class SEOProjectManager:

    def __init__(self):
        self.tasks = TaskManager()
        self.clients = ClientManager()
        self.team = ProjectManager()

    def start_project(self, client_name, website, email):

        print("\nSTARTING NEW SEO PROJECT")
        print("------------------------")

        self.clients.add_client(
            client_name,
            website,
            email
        )

        project_tasks = {
            "SEO Researcher": "Research the client's website",
            "Keyword Analyst": "Perform keyword research",
            "Technical SEO Auditor": "Audit technical SEO",
            "Content Writer": "Prepare SEO content",
            "On-Page SEO Specialist": "Review on-page SEO",
            "Competitor Analyst": "Analyze competitors",
            "Performance Analyst": "Review SEO performance"
        }

        for employee, task in project_tasks.items():
            self.tasks.assign_task(employee, task)

        print("\nProject setup completed!")
        print("Seven specialist tasks have been created.")


if __name__ == "__main__":

    agency = SEOProjectManager()

    agency.start_project(
        "Demo Client",
        "https://example.com",
        "client@example.com"
    )
