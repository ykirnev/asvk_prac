import readline
import sys
import socket
import cmd
import shlex
import threading
import time
import webbrowser
from pathlib import Path

import cowsay
FIELD_SIZE = 10

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
def spam(cmd, s):
    try:
        while msg := s.recv(8192):
            msg_received = msg.rstrip().decode()
            print(f'\n{msg_received}')
            print(f'{cmd.prompt}{readline.get_line_buffer()}',
                  end='', flush=True)
    except:
        return


def attack_exe(args):
    """Execute attack command."""
    if not args or args[0] == 'with':
        named = False
    else:
        named = True
        name = args[0]
        if name not in cowsay.list_cows() and name != 'jgsbat':
            return "Cannot attack unknown monster"
    match args[1:] if named else args:
        case ['with', weapon] if weapon in ['sword', 'spear', 'axe']:
            return f"attack {name if named else '.'} {weapon}"
        case []:
            return f"attack {name if named else '.'} sword"
        case _:
            return ("Unknown weapon")


def addmon_exe(args):
    """Execute addmon command."""
    try:
        name = args[0]
        hp = args[args.index('hp') + 1] if 'hp' in args else 999
        hello = args[args.index('hello') + 1] if 'hello' in args else "HELLo"
        coords = (int(args[args.index('coords') + 1]), int(args[args.index('coords') + 2])) if 'coords' in args else (
            0, 0)
        x = coords[0]
        y = coords[1]
        if not (0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE):
            return "Invalid arguments"
        if name not in cowsay.list_cows() and name != 'jgsbat':
            return "Cannot add unknown monster"
    except Exception:
        return "Invalid arguments"
    return f"addmon {name} {hello} {hp} {x} {y}"


def sayall_exe(args):
    """Execute sayall command."""
    match len(args):
        case 1:
            return True
        case _:
            return False


class MUDCmd(cmd.Cmd):
    prompt = "MUD> "
    def __init__(self, s, name):
        super().__init__()
        self.socket = s
        self.socket.sendall(f"register {name}\n".encode())

    def do_up(self, arg):
        """Move player up."""
        self.socket.sendall(f"move up\n".encode())

    def do_down(self, arg):
        """Move player down."""
        self.socket.sendall(f"move down\n".encode())

    def do_left(self, arg):
        """Move player left."""
        self.socket.sendall(f"move left\n".encode())

    def do_right(self, arg):
        """Move player right."""
        self.socket.sendall(f"move right\n".encode())

    def do_addmon(self, arg):
        """Add a monster to the field."""
        args = shlex.split(arg)
        result = addmon_exe(args)
        if result.startswith('addmon'):
            self.socket.sendall(f"{result}\n".encode())
        else:
            print(result)

    def do_sayall(self, args):
        res = sayall_exe(shlex.split(args))
        if res:
            self.socket.sendall(f"s {shlex.split(args)}\n".encode())
        else:
            print("invalid arguments")

    def do_attack(self, args):
        """Attack a monster on the field."""
        result = attack_exe(shlex.split(args))
        if result.startswith('attack'):
            self.socket.sendall(f"{result}\n".encode())
        else:
            print(result)

    def complete_attack(self, text, line, begidx, endidx):
        weapons = ['sword', 'spear', 'axe']
        monsters = [m for m in cowsay.list_cows()] + ['jgsbat']
        args = shlex.split(line[:begidx])
        if len(args) == 1:
            return [w for w in monsters if w.startswith(text)]
        elif len(args) == 2 and args[1] == 'with' or len(args) == 3 and args[2] == 'with':
            return [w for w in weapons if w.startswith(text)]
        return []

    def do_movemonsters(self, args):
        """
        Turning on/off wandering monsters.

        args:str on or off
        """
        self.socket.sendall(f"movemonsters {args}\n".encode())

    def complete_movemonsters(self, text, line, begidx, endidx):
        state = ['on', 'off']
        args = shlex.split(line[:begidx])
        return [w for w in state if w.startswith(text)]



    def do_locale(self, args):
        """Set the locale for messages (e.g. 'ru_RU.UTF-8')."""
        args = shlex.split(args)
        if len(args) != 1 or args[0] not in ['ru_RU.UTF-8', 'en_US.UTF-8']:
            print("Usage: locale ['ru_RU.UTF-8', 'en_US.UTF-8']")
            return
        locale_name = args[0]
        self.socket.sendall(f"locale {locale_name}\n".encode())

    def complete_locale(self, text, line, begidx, endidx):
        state = ['ru_RU.UTF-8', 'en_US.UTF-8']
        args = shlex.split(line[:begidx])
        return [w for w in state if w.startswith(text)]

    def do_quit(self, arg):
        """Quit the game."""
        self.socket.sendall(f"quit\n".encode())
        return True

    def do_documentation(self, args):
        doc_path = Path(__file__).parent.parent.parent / "mood/docs/html/index.html"
        webbrowser.open(f"file://{doc_path.resolve()}")


def main():
    host = "localhost"
    port = 1337
    args = sys.argv[1:]
    file_mode = False
    filename = None
    name = None
    i = 0
    while i < len(args):
        if args[i] == "--file":
            if i + 1 >= len(args):
                print("Missing filename after --file")
                return
            filename = args[i + 1]
            file_mode = True
            i += 2
        else:
            if name is None:
                name = args[i]
                i += 1
            else:
                print("Unexpected argument:", args[i])
                return

    if name is None:
        print("Player name is required")
        return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        cmdline = MUDCmd(s, name)
        server_thread = threading.Thread(target=spam, args=(cmdline, s))
        server_thread.start()
        if not file_mode:
            cmdline.cmdloop()
        else:
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = shlex.split(line)
                        if not parts:
                            continue
                        command = parts[0]
                        args = parts[1:] if len(parts) > 1 else []
                        args_str = ' '.join(args)
                        if hasattr(cmdline, 'do_' + command):
                            getattr(cmdline, 'do_' + command)(args_str)
                            time.sleep(1)
                        else:
                            print(f"Unknown command: {command}")
            except FileNotFoundError:
                print(f"File {filename} not found")
                return
