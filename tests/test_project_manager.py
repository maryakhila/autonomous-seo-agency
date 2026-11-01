

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from project_manager import ProjectManager


def test_project_manager_has_seven_specialists():
    manager = ProjectManager()

    assert len(manager.employees) == 7


def test_project_manager_has_correct_team():
    manager = ProjectManager()

    assert "SEO Researcher" in manager.employees
    assert "Keyword Analyst" in manager.employees
    assert "Performance Analyst" in manager.employees


if __name__ == "__main__":
    test_project_manager_has_seven_specialists()
    test_project_manager_has_correct_team()

    print("All Project Manager tests passed!")
