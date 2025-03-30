import socket
import json
import cmd

class MUDClient(cmd.Cmd):
    prompt = "(MUD) "

    def init(self, host="localhost", port=12345):
        super().init()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_command(self, command):
        self.client.send(json.dumps(command).encode())
        return json.loads(self.client.recv(1024).decode())

    def do_move(self, args):
        x, y = map(int, args.split())
        response = self.send_command({"cmd": "move", "x": x, "y": y})
        print(response["status"], response.get("position", ""))

    def do_addmon(self, args):
        parts = args.split()
        name, hp, x, y, hello = parts[0], int(parts[1]), int(parts[2]), int(parts[3]), " ".join(parts[4:])
        response = self.send_command({"cmd": "addmon", "name": name, "hp": hp, "x": x, "y": y, "hello": hello})
        print(response["status"])

    def do_attack(self, args):
        name, damage = args.split()
        response = self.send_command({"cmd": "attack", "name": name, "damage": int(damage)})
        print(response["status"], response.get("remaining_hp", ""))

    def do_exit(self, _):
        print("Goodbye!")
        return True

if name == "main":
    MUDClient().cmdloop()