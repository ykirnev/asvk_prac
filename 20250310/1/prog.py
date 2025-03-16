import shlex
import cmd
import readline
import cowsay

class MUDGame(cmd.Cmd):
    prompt = "(MUD) "

    def init(self):
        super().init()
        self.player_pos = (0, 0)
        self.monsters = {}

    def do_addmon(self, args):
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


def do_attack(self, args):
    """Атака монстра по имени с оружием."""
    tokens = shlex.split(args)
    if len(tokens) < 1:
        print("Usage: attack <monster_name> with <weapon>")
        return

    monster_name = tokens[0]
    weapon = tokens[2] if len(tokens) > 2 else "sword"
    damage = 10 if weapon == "sword" else 15 if weapon == "spear" else 20 if weapon == "axe" else 0

    if damage == 0:
        print(f"Unknown weapon {weapon}")
        return

    pos = self.player_pos
    if pos not in self.monsters or self.monsters[pos]["name"] != monster_name:
        print(f"No {monster_name} here")
        return

    monster = self.monsters[pos]
    monster["hp"] -= damage
    print(f"Attacked {monster_name} with {weapon}, damage {damage}")

    if monster["hp"] <= 0:
        print(f"{monster_name} died")
        del self.monsters[pos]
    else:
        print(f"{monster_name} now has {monster['hp']} hp")


def complete_attack(self, text, line, begidx, endidx):
    """Автодополнение для имени монстра и оружия."""
    monsters = [monster["name"] for monster in self.monsters.values() if monster["name"].startswith(text)]
    weapons = ["sword", "spear", "axe"]
    if len(line.split()) == 1:
        return monsters
    elif len(line.split()) == 2:
        return weapons
    return []



if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
print("<<< Welcome to Python-MUD 0.2 >>>")
MUDGame().cmdloop()
