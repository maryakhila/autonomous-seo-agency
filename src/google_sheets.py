
class GoogleSheetsManager:

    def __init__(self, spreadsheet_id=None):
        self.spreadsheet_id = spreadsheet_id

    def connect(self):
        if not self.spreadsheet_id:
            print("Google Sheets ID is missing.")
            return False

        print("Google Sheets ID is configured.")
        print("API authentication is not connected yet.")

        return False

    def save_task(self, employee, task, status):
        print("Task information:")
        print(f"Employee: {employee}")
        print(f"Task: {task}")
        print(f"Status: {status}")
        print("Google Sheets connection is required to save this task.")

    def save_report(self, report):
        print("Report prepared:")
        print(report)
        print("Google Sheets connection is not connected yet.")


if __name__ == "__main__":
    sheets = GoogleSheetsManager()

    sheets.connect()

    sheets.save_task(
        "SEO Researcher",
        "Research the client website",
        "Pending"
    )
