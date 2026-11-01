
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from client_manager import ClientManager


def test_client_manager_saves_client(tmp_path):
    manager = ClientManager()

    manager.data_folder = tmp_path
    manager.clients_file = tmp_path / "clients.json"
    manager.clients_file.write_text("[]", encoding="utf-8")

    manager.add_client(
        "Test Client",
        "https://example.com",
        "test@example.com"
    )

    clients = manager.load_clients()

    assert len(clients) == 1
    assert clients[0]["name"] == "Test Client"
    assert clients[0]["website"] == "https://example.com"
    assert clients[0]["status"] == "Active"


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        test_client_manager_saves_client(Path(folder))

    print("All Client Manager tests passed!")
