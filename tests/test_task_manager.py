
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from task_manager import TaskManager


def test_task_manager_saves_task(tmp_path):
    manager = TaskManager()

    manager.data_folder = tmp_path
    manager.tasks_file = tmp_path / "tasks.json"
    manager.tasks_file.write_text("[]", encoding="utf-8")

    manager.assign_task(
        "SEO Researcher",
        "Research the client website"
    )

    tasks = manager.load_tasks()

    assert len(tasks) == 1
    assert tasks[0]["employee"] == "SEO Researcher"
    assert tasks[0]["status"] == "Pending"


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        test_task_manager_saves_task(Path(folder))

    print("All Task Manager tests passed!")
