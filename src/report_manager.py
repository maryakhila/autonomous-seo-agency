
import json
from pathlib import Path
from datetime import datetime


class ReportManager:

    def __init__(self):
        self.data_folder = Path(__file__).parent.parent / "data"
        self.data_folder.mkdir(exist_ok=True)

        self.reports_file = self.data_folder / "reports.json"

        if not self.reports_file.exists():
            self.reports_file.write_text("[]", encoding="utf-8")

    def load_reports(self):
        with open(self.reports_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_report(self, report):
        reports = self.load_reports()

        new_report = {
            "date": datetime.now().isoformat(),
            "report": report
        }

        reports.append(new_report)

        with open(self.reports_file, "w", encoding="utf-8") as file:
            json.dump(reports, file, indent=4)

        print("Daily report saved successfully!")

    def show_reports(self):
        reports = self.load_reports()

        for report in reports:
            print(report)


if __name__ == "__main__":
    manager = ReportManager()

    manager.save_report("SEO agency daily report")

    manager.show_reports()
