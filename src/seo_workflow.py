
class SEOWorkflow:

    def __init__(self):

        self.workflow = [
            {
                "step": 1,
                "employee": "SEO Researcher",
                "task": "Research the client's business and website"
            },
            {
                "step": 2,
                "employee": "Keyword Analyst",
                "task": "Find and organize SEO keywords"
            },
            {
                "step": 3,
                "employee": "Technical SEO Auditor",
                "task": "Identify technical SEO problems"
            },
            {
                "step": 4,
                "employee": "Competitor Analyst",
                "task": "Analyze competing websites"
            },
            {
                "step": 5,
                "employee": "Content Writer",
                "task": "Prepare SEO-friendly content"
            },
            {
                "step": 6,
                "employee": "On-Page SEO Specialist",
                "task": "Review and improve page optimization"
            },
            {
                "step": 7,
                "employee": "Performance Analyst",
                "task": "Review SEO performance"
            }
        ]

    def show_workflow(self):

        print("AUTONOMOUS SEO AGENCY WORKFLOW")
        print("--------------------------------")

        for item in self.workflow:
            print(
                f"{item['step']}. "
                f"{item['employee']}: "
                f"{item['task']}"
            )


if __name__ == "__main__":

    workflow = SEOWorkflow()

    workflow.show_workflow()
