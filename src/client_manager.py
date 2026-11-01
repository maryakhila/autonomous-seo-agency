
import json
from pathlib import Path
from datetime import datetime


class ClientManager:

    def __init__(self):
        self.data_folder = Path(__file__).parent.parent / "data"
        self.data_folder.mkdir(exist_ok=True)

        self.clients_file = self.data_folder / "clients.json"

        if not self.clients_file.exists():
            self.clients_file.write_text("[]", encoding="utf-8")

    def load_clients(self):
        with open(self.clients_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def add_client(self, name, website, email):
        clients = self.load_clients()

        new_client = {
            "name": name,
            "website": website,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "status": "Active"
        }

        clients.append(new_client)

        with open(self.clients_file, "w", encoding="utf-8") as file:
            json.dump(clients, file, indent=4)

        print(f"Client {name} added successfully!")

    def show_clients(self):
        for client in self.load_clients():
            print(client)


if __name__ == "__main__":
    manager = ClientManager()

    manager.add_client(
        "Demo Client",
        "https://example.com",
        "client@example.com"
    )

    manager.show_clients()
