"""Employee registry and adapter hook.

This starter does not pretend to execute AI work. Connect each employee to your
existing implementation inside run_employee_task(), then persist its output/status.
"""
EMPLOYEES = {
    "Project Manager": "Chief of Staff",
    "Keyword Analyst": "Keyword research",
    "SEO Content Writer": "SEO content production",
    "Technical SEO Auditor": "Technical SEO audits",
    "On-Page SEO Specialist": "On-page optimization",
    "Off-Page SEO Specialist": "Backlink research and outreach",
    "SEO Performance Analyst": "SEO analytics",
    "Reporting Specialist": "Reports and documentation",
}

def run_employee_task(employee_name, task):
    """Replace this function body with a call to the matching real agent module."""
    raise NotImplementedError(
        f"{employee_name} has no execution adapter connected yet. "
        "Do not mark the task completed until the real agent returns a verifiable output."
    )
