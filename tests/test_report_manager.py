
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from report_manager import ReportManager


def test_report_manager_saves_report(tmp_path):
    manager = ReportManager()

    manager.data_folder = tmp_path
    manager.reports_file = tmp_path / "reports.json"
    manager.reports_file.write_text("[]", encoding="utf-8")

    manager.save_report("Daily SEO report")

    reports = manager.load_reports()

    assert len(reports) == 1
    assert reports[0]["report"] == "Daily SEO report"
    assert "date" in reports[0]


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        test_report_manager_saves_report(Path(folder))

    print("All Report Manager tests passed!")
