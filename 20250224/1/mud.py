import random
import cowsay

FIELD_SIZE = 10
field = [[None for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
player_x, player_y = 0, 0

def move_player(direction):
    global player_x, player_y
    if direction == "up":
        player_y = (player_y - 1) % FIELD_SIZE
    elif direction == "down":
        player_y = (player_y + 1) % FIELD_SIZE
    elif direction == "left":
        player_x = (player_x - 1) % FIELD_SIZE
    elif direction == "right":
        player_x = (player_x + 1) % FIELD_SIZE
    else:
        print("Invalid command")
        return
    print(f"Moved to ({player_x}, {player_y})")
    encounter(player_x, player_y)

def encounter(x, y):
    if field[x][y]:
        cowsay.cow(field[x][y])

def add_monster(x, y, hello):
    if field[x][y] is None:
        field[x][y] = hello
        print(f"Added monster to ({x}, {y}) saying {hello}")
    else:
        print(f"Replaced the old monster")
        field[x][y] = hello
        print(f"Added monster to ({x}, {y}) saying {hello}")

def process_command(command):
    parts = command.split()
    if parts[0] == "up" or parts[0] == "down" or parts[0] == "left" or parts[0] == "right":
        move_player(parts[0])
    elif parts[0] == "addmon" and len(parts) == 4:
        try:
            x, y = int(parts[1]), int(parts[2])
            add_monster(x, y, parts[3])
        except ValueError:
            print("Invalid arguments")
    else:
        print("Invalid command")

while True:
    command = input("Enter command: ").strip()
    process_command(command)
