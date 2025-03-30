import socket
import json


class MUDServer:
    def init(self, host="localhost", port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(1)
        print(f"Server started on {host}:{port}")
        self.client, _ = self.server.accept()
        print("Client connected")

        self.player_pos = (0, 0)
        self.monsters = {}

    def run(self):
        while True:
            data = self.client.recv(1024).decode()
            if not data:
                break
            response = self.handle_command(json.loads(data))
            self.client.send(json.dumps(response).encode())

    def handle_command(self, command):
        cmd = command.get("cmd")
        if cmd == "move":
            self.player_pos = (command["x"], command["y"])
            return {"status": "moved", "position": self.player_pos}

        elif cmd == "addmon":
            self.monsters[(command["x"], command["y"])] = {
                "name": command["name"], "hp": command["hp"], "hello": command["hello"]
            }
            return {"status": "monster added"}

        elif cmd == "attack":
            pos = self.player_pos
            if pos not in self.monsters:
                return {"status": "no monster"}

            monster = self.monsters[pos]
            if monster["name"] != command["name"]:
                return {"status": "wrong monster"}

            monster["hp"] -= command["damage"]
            if monster["hp"] <= 0:
                del self.monsters[pos]
                return {"status": "monster defeated"}

            return {"status": "hit", "remaining_hp": monster["hp"]}

        return {"status": "unknown command"}


if name == "main":
    MUDServer().run()