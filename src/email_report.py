
from datetime import datetime


class EmailReporter:

    def create_daily_report(self, completed_tasks, pending_tasks, issues):

        report = f"""
AUTONOMOUS SEO AGENCY
DAILY PROGRESS REPORT

Date: {datetime.now().strftime("%Y-%m-%d")}

COMPLETED TASKS:
{completed_tasks}

PENDING TASKS:
{pending_tasks}

ISSUES:
{issues}

--------------------------------
End of Daily Report
"""

        return report

    def preview_report(self, report):
        print(report)


if __name__ == "__main__":

    reporter = EmailReporter()

    daily_report = reporter.create_daily_report(
        completed_tasks="Website research completed",
        pending_tasks="Keyword research pending",
        issues="No major issues"
    )

    reporter.preview_report(daily_report)
