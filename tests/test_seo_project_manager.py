
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from seo_project_manager import SEOProjectManager


def test_project_creates_seven_specialist_tasks(tmp_path):
    agency = SEOProjectManager()

    agency.tasks.data_folder = tmp_path
    agency.tasks.tasks_file = tmp_path / "tasks.json"
    agency.tasks.tasks_file.write_text("[]", encoding="utf-8")

    agency.clients.data_folder = tmp_path
    agency.clients.clients_file = tmp_path / "clients.json"
    agency.clients.clients_file.write_text("[]", encoding="utf-8")

    agency.start_project(
        "Test Client",
        "https://example.com",
        "test@example.com"
    )

    tasks = agency.tasks.load_tasks()
    clients = agency.clients.load_clients()

    assert len(tasks) == 7
    assert len(clients) == 1
    assert clients[0]["name"] == "Test Client"


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        test_project_creates_seven_specialist_tasks(Path(folder))

    print("All SEO Project Manager tests passed!")
