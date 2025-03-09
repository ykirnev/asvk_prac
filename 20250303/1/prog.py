import cowsay
from io import StringIO

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

    def add_monster(self, name, x, y, hello):
        if (x, y) in self.monsters:
            print("Replaced the old monster")
        self.monsters[(x, y)] = (name, hello)
        print(f"Added monster {name} to ({x}, {y}) saying {hello}")

    def encounter(self, x, y):
        if (x, y) in self.monsters:
            name, hello = self.monsters[(x, y)]
            print(cowsay.cow(hello))

def addmon(game, monster_name, x, y, hello):
    if monster_name == "jgsbat":
        game.add_monster("jgsbat", x, y, hello)
    else:
        game.add_monster(monster_name, x, y, hello)


print("<<< Welcome to Python-MUD 0.1 >>>")
game = MUDGame()