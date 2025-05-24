import asyncio
import cmd
import shlex
import sys
import io
from cowsay import cowsay, list_cows, read_dot_cow

jgsbat = r"""
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\'--'//__
         (((""`  `"")))
"""

class MUDClient(cmd.Cmd):
    prompt = "MUD> "
    def __init__(self, username, loop):
        super().__init__()
        self.username = username
        self.loop = loop
        self.reader = None
        self.writer = None
        self.current_input = ""
        self.receive_task = None
        self.shutting_down = False

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 8888)
            self.writer.write(f"{self.username}\n".encode())
            await self.writer.drain()
            response = await self.reader.readline()
            print(response.decode().strip())
            if "already taken" in response.decode():
                sys.exit(1)
            self.receive_task = asyncio.create_task(self.receive_messages())
        except ConnectionRefusedError:
            print("Cannot connect to server")
            sys.exit(1)

    async def receive_messages(self):
        try:
            while True:
                data = await self.reader.readline()
                if not data:
                    break
                msg = data.decode().strip()
                if msg.startswith("monster "):
                    _, name, hello = msg.split(" ", 2)
                    if name == "jgsbat":
                        print(cowsay(hello, cowfile=read_dot_cow(io.StringIO(jgsbat))))
                    else:
                        print(cowsay(hello, cow=name))
                else:
                    print(msg)
                print(self.prompt + self.current_input, end="", flush=True)
        except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
            if not self.shutting_down:
                print("Disconnected from server")
            sys.exit(1)

    def do_up(self, arg):
        if arg:
            print("Invalid arguments")
            return
        asyncio.run_coroutine_threadsafe(self.send_command("move 0 -1"), self.loop)

    def do_down(self, arg):
        if arg:
            print("Invalid arguments")
            return
        asyncio.run_coroutine_threadsafe(self.send_command("move 0 1"), self.loop)

    def do_left(self, arg):
        if arg:
            print("Invalid arguments")
            return
        asyncio.run_coroutine_threadsafe(self.send_command("move -1 0"), self.loop)

    def do_right(self, arg):
        if arg:
            print("Invalid arguments")
            return
        asyncio.run_coroutine_threadsafe(self.send_command("move 1 0"), self.loop)

    def do_addmon(self, arg):
        args = shlex.split(arg)
        if len(args) < 6:
            print("Invalid arguments")
            return
        try:
            name = args[0]
            params = {}
            i = 1
            while i < len(args):
                if i + 1 >= len(args):
                    print("Invalid arguments")
                    return
                key = args[i]
                if key not in ("hello", "hp", "coords"):
                    print("Invalid arguments")
                    return
                if key == "coords":
                    if i + 2 >= len(args):
                        print("Invalid arguments")
                        return
                    x, y = args[i + 1], args[i + 2]
                    params[key] = f"{x} {y}"
                    i += 3
                else:
                    params[key] = args[i + 1]
                    i += 2
            if not all(k in params for k in ("hello", "hp", "coords")):
                print("Invalid arguments")
                return
            x, y = map(int, params["coords"].split())
            hp = int(params["hp"])
            if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                print("Invalid arguments")
                return
            if name not in list_cows() and name != "jgsbat":
                print("Cannot add unknown monster")
                return
            hello = params["hello"]
            command = f"addmon {name} {x} {y} {hello} {hp}"
            asyncio.run_coroutine_threadsafe(self.send_command(command), self.loop)
        except (ValueError, IndexError):
            print("Invalid arguments")
            return

    def do_attack(self, arg):
        args = shlex.split(arg)
        if not args:
            print("Invalid arguments")
            return
        monster_name = args[0]
        weapon = "sword"
        if len(args) > 1 and args[1] == "with":
            if len(args) != 3 or args[2] not in ("sword", "spear", "axe"):
                print("Unknown weapon")
                return
            weapon = args[2]
        damage = {"sword": 10, "spear": 15, "axe": 20}[weapon]
        command = f"attack {monster_name} {damage}"
        asyncio.run_coroutine_threadsafe(self.send_command(command), self.loop)

    async def send_command(self, command):
        if self.writer is None:
            print("Not connected to server")
            return
        try:
            self.writer.write(f"{command}\n".encode())
            await self.writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            if not self.shutting_down:
                print("Disconnected from server")
            sys.exit(1)

    def complete_attack(self, text, line, begidx, endidx):
        if line.startswith("attack ") and " with " in line:
            weapons = ["sword", "spear", "axe"]
            return [w for w in weapons if w.startswith(text)]
        return [name for name in list_cows() + ["jgsbat"] if name.startswith(text)]

    def default(self, line):
        print("Invalid command")

    def postcmd(self, stop, line):
        self.current_input = ""
        return stop

    def precmd(self, line):
        self.current_input = line
        return line

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <username>")
        sys.exit(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = MUDClient(sys.argv[1], loop)
    try:
        loop.run_until_complete(client.connect())
        loop.run_in_executor(None, client.cmdloop)
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nExiting...")
        client.shutting_down = True
        # Cancel running tasks
        if client.receive_task is not None:
            client.receive_task.cancel()
            try:
                loop.run_until_complete(client.receive_task)
            except asyncio.CancelledError:
                pass
        if client.writer is not None:
            client.writer.close()
            loop.run_until_complete(client.writer.wait_closed())
        loop.stop()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()