import cowsay
from io import StringIO
import shlex
from collections import namedtuple

jgsbat = cowsay.read_dot_cow(StringIO( r"""
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

class MUDGame:
    def __init__(self):
        self.player_pos = (0, 0)
        self.monsters = {}

    def move(self, direction):
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
            print("Invalid command")
            return

        self.player_pos = (x, y)
        print(f"Moved to ({x}, {y})")
        self.encounter(x, y)

    def add_monster(self, command):
        tokens = shlex.split(command)

        if tokens[0] != "addmon":
            print("Invalid command")
            return

        monster_data = {}
        i = 1
        while i < len(tokens):
            if tokens[i] == "hello":
                monster_data["hello"] = tokens[i + 1]
                i += 2
            elif tokens[i] == "hp":
                try:
                    monster_data["hp"] = int(tokens[i + 1])
                except ValueError:
                    print("Invalid value for hp")
                    return
                i += 2
            elif tokens[i] == "coords":
                try:
                    monster_data["coords"] = (int(tokens[i + 1]), int(tokens[i + 2]))
                except (ValueError, IndexError):
                    print("Invalid value for coords")
                    return
                i += 3
            else:
                monster_data["name"] = tokens[i]
                i += 1


        name = monster_data["name"]
        hello = monster_data["hello"]
        hp = monster_data["hp"]
        x, y = monster_data["coords"]

        self.monsters[(x, y)] = (name, hello, hp)
        print(f"Added monster {name} to ({x}, {y}) saying {hello} with {hp} HP")

    def encounter(self, x, y):
        if (x, y) in self.monsters:
            name, hello, hp = self.monsters[(x, y)]
            print(cowsay.cow(hello))

def addmon(game, monster_name, x, y, hello):
    if monster_name == "jgsbat":
        game.add_monster("jgsbat", x, y, hello)
    else:
        game.add_monster(monster_name, x, y, hello)


print("<<< Welcome to Python-MUD 0.1 >>>")
game = MUDGame()
game.add_monster('addmon dragon hp 999 coords 6 9 hello "Who goes there?"')
