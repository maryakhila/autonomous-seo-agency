from database import init_db
from email_report import send_daily_report

if __name__ == "__main__":
    init_db()
    send_daily_report()
    print("Daily report email sent.")
