import cowsay
from io import StringIO
import shlex
import cmd
import readline
from collections import namedtuple

jgsbat = cowsay.read_dot_cow(StringIO(r"""
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     "\\'''--'//"
         (((""  "")))

"""))


class MUDGame(cmd.Cmd):
    prompt = "(MUD) "

    def __init__(self):
        super().__init__()
        self.player_pos = (0, 0)
        self.monsters = {}

    def do_move(self, direction):
        """Move the player in a direction: up, down, left, right."""
        x, y = self.player_pos
        if direction == "up":
            y = (y - 1) % 10
        elif direction == "down":
            y = (y + 1) % 10
        elif direction == "left":
            x = (x - 1) % 10
        elif direction == "right":
            x = (x + 1) % 10
        else:
            print("Invalid direction")
            return

        self.player_pos = (x, y)
        print(f"Moved to ({x}, {y})")
        self.encounter(x, y)

    def do_addmon(self, args):
        """Add a monster with a name, hp, coordinates, and a greeting."""
        tokens = shlex.split(args)
        if not tokens:
            print("Usage: addmon <name> hp <value> coords <x> <y> hello <message>")
            return

        monster_data = {}
        i = 0
        while i < len(tokens):
            if tokens[i] == "hp":
                try:
                    monster_data["hp"] = int(tokens[i + 1])
                except (ValueError, IndexError):
                    print("Invalid value for hp")
                    return
                i += 2
            elif tokens[i] == "coords":
                try:
                    monster_data["coords"] = (int(tokens[i + 1]), int(tokens[i + 2]))
                except (ValueError, IndexError):
                    print("Invalid coordinates")
                    return
                i += 3
            elif tokens[i] == "hello":
                monster_data["hello"] = tokens[i + 1]
                i += 2
            else:
                monster_data["name"] = tokens[i]
                i += 1

        if "name" not in monster_data or "hp" not in monster_data or "coords" not in monster_data:
            print("Invalid monster definition")
            return

        name = monster_data["name"]
        hello = monster_data.get("hello", "Hello!")
        hp = monster_data["hp"]
        x, y = monster_data["coords"]

        self.monsters[(x, y)] = {"name": name, "hello": hello, "hp": hp}
        print(f"Added monster {name} to ({x}, {y}) saying '{hello}' with {hp} HP")

    def encounter(self, x, y):
        if (x, y) in self.monsters:
            monster = self.monsters[(x, y)]
            print(cowsay.cow(monster["hello"]))

    def do_attack(self, args):
        """Attack a monster with specified weapon."""
        args = shlex.split(args)
        weapon = "sword"
        if args:
            weapon = args[1]

        weapon_damage = {
            "sword": 10,
            "spear": 15,
            "axe": 20
        }

        if weapon not in weapon_damage:
            print("Unknown weapon")
            return

        pos = self.player_pos
        if pos not in self.monsters:
            print("No monster here")
            return

        monster = self.monsters[pos]
        damage = weapon_damage[weapon]
        monster["hp"] -= damage
        print(f"Attacked {monster['name']} with {weapon}, damage {damage} hp")

        if monster["hp"] <= 0:
            print(f"{monster['name']} died")
            del self.monsters[pos]
        else:
            print(f"{monster['name']} now has {monster['hp']} hp")

    def complete_attack(self, text, line, begidx, endidx):
        """Auto-complete weapon names for the attack command."""
        weapons = ["sword", "spear", "axe"]
        if text:
            return [w for w in weapons if w.startswith(text)]
        else:
            return weapons


def addmon(game, monster_name, x, y, hello):
    if monster_name == "jgsbat":
        game.add_monster("jgsbat", x, y, hello)
    else:
        game.add_monster(monster_name, x, y, hello)


if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
print("<<< Welcome to Python-MUD 0.2 >>>")
MUDGame().cmdloop()
