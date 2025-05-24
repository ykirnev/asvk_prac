"""Серверная часть многопользовательской игры MOOD.

Этот модуль реализует сервер MUD, который управляет игровым миром, обрабатывает
команды клиентов и поддерживает бродячих монстров, перемещающихся каждые 30 секунд.
"""

import asyncio
import random
import shlex
from typing import Dict, List, Tuple

from mood.common.constants import HOST, PORT


class GameState:
    """Управляет состоянием игрового мира MUD.

    Attributes:
        monsters (Dict[Tuple[int, int], Tuple[str, str, int]]): Словарь монстров,
            где ключ — координаты (x, y), значение — (имя, приветственная фраза, hp).
        players (Dict[str, List[int]]): Словарь игроков, где ключ — имя,
            значение — координаты [x, y].
        clients (Dict[str, asyncio.StreamWriter]): Словарь клиентских соединений.
    """

    def __init__(self):
        """Инициализировать состояние игры."""
        self.monsters: Dict[Tuple[int, int], Tuple[str, str, int]] = {}
        self.players: Dict[str, List[int]] = {}
        self.clients: Dict[str, asyncio.StreamWriter] = {}


async def move_monsters(game_state: GameState):
    """Перемещает случайного монстра каждые 30 секунд.

    Каждые 30 секунд выбирается случайный монстр и направление движения.
    Если целевая клетка свободна от других монстров, монстр перемещается,
    и всем игрокам отправляется сообщение. Если монстр попадает на клетку
    с игроками, происходит "энкаунтер".

    Args:
        game_state: Объект состояния игры.
    """
    directions = [
        ("right", (1, 0)),
        ("left", (-1, 0)),
        ("up", (0, -1)),
        ("down", (0, 1)),
    ]
    print("Debug: Starting move_monsters task")
    while True:
        await asyncio.sleep(30)
        if not game_state.monsters:
            print("Debug: No monsters to move")
            continue
        attempts = 0
        max_attempts = len(game_state.monsters) * 4
        while attempts < max_attempts:
            current_pos = random.choice(list(game_state.monsters.keys()))
            name, hello, hp = game_state.monsters[current_pos]
            direction_name, (dx, dy) = random.choice(directions)
            new_x = (current_pos[0] + dx) % 10
            new_y = (current_pos[1] + dy) % 10
            new_pos = (new_x, new_y)
            if new_pos in game_state.monsters:
                attempts += 1
                print(f"Debug: Attempt {attempts}: {new_pos} occupied")
                continue
            print(f"Debug: Moving {name} from {current_pos} to {new_pos} ({direction_name})")
            game_state.monsters[new_pos] = (name, hello, hp)
            del game_state.monsters[current_pos]
            for writer in game_state.clients.values():
                writer.write(
                    f"{name} moved one cell {direction_name}\n".encode()
                )
                await writer.drain()
            for username, pos in game_state.players.items():
                if (pos[0], pos[1]) == new_pos:
                    writer = game_state.clients[username]
                    writer.write(f"monster {name} {hello}\n".encode())
                    await writer.drain()
            break
        if attempts >= max_attempts:
            print("Debug: No valid monster move found")


async def handle_client(reader: asyncio.StreamReader,
                        writer: asyncio.StreamWriter,
                        game_state: GameState):
    """Обработать подключение клиента.

    Args:
        reader: StreamReader для чтения данных от клиента.
        writer: StreamWriter для отправки данных клиенту.
        game_state: Объект состояния игры.
    """
    username = None
    try:
        username = (await reader.readline()).decode().strip()
        if not username:
            writer.close()
            await writer.wait_closed()
            return
        if username in game_state.players:
            writer.write(b"Username already taken\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
        game_state.players[username] = [0, 0]
        game_state.clients[username] = writer
        writer.write(b"Connected to MUD\n")
        await writer.drain()
        for u, w in game_state.clients.items():
            if u != username:
                w.write(f"{username} joined MUD\n".encode())
                await w.drain()

        while True:
            data = await reader.readline()
            if not data:
                break
            cmd = shlex.split(data.decode().strip())
            print(f"Debug: Received command: {cmd}")
            if not cmd:
                continue
            try:
                if cmd[0] == "move":
                    if len(cmd) != 3:
                        writer.write(b"Invalid move format\n")
                        await writer.drain()
                        continue
                    dx, dy = int(cmd[1]), int(cmd[2])
                    game_state.players[username][0] = (
                        game_state.players[username][0] + dx
                    ) % 10
                    game_state.players[username][1] = (
                        game_state.players[username][1] + dy
                    ) % 10
                    pos = tuple(game_state.players[username])
                    writer.write(f"Moved to {pos}\n".encode())
                    if pos in game_state.monsters:
                        name, hello, _ = game_state.monsters[pos]
                        writer.write(f"monster {name} {hello}\n".encode())
                    await writer.drain()
                elif cmd[0] == "addmon":
                    if len(cmd) != 6:
                        writer.write(b"Invalid addmon format\n")
                        await writer.drain()
                        continue
                    name, x, y, hello, hp = cmd[1:]
                    x, y, hp = int(x), int(y), int(hp)
                    if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                        writer.write(b"Invalid arguments\n")
                        await writer.drain()
                        continue
                    pos = (x, y)
                    replaced = pos in game_state.monsters
                    game_state.monsters[pos] = (name, hello, hp)
                    writer.write(
                        f"Added monster {name} to {pos} saying {hello}\n".encode()
                    )
                    if replaced:
                        writer.write(b"Replaced the old monster\n")
                    for u, w in game_state.clients.items():
                        w.write(
                            f"{username} added monster {name} with {hp} hp\n".encode()
                        )
                        await w.drain()
                elif cmd[0] == "attack":
                    if len(cmd) != 3:
                        writer.write(b"Invalid attack format\n")
                        await writer.drain()
                        continue
                    monster_name, damage = cmd[1], int(cmd[2])
                    pos = tuple(game_state.players[username])
                    if (pos not in game_state.monsters or
                            game_state.monsters[pos][0] != monster_name):
                        writer.write(f"No {monster_name} here\n".encode())
                    else:
                        name, hello, hp = game_state.monsters[pos]
                        damage = min(damage, hp)
                        hp -= damage
                        writer.write(
                            f"Attacked {name}, damage {damage} hp\n".encode()
                        )
                        if hp == 0:
                            writer.write(f"{name} died\n".encode())
                            del game_state.monsters[pos]
                            for u, w in game_state.clients.items():
                                w.write(f"{username} killed {name}\n".encode())
                        else:
                            writer.write(f"{name} now has {hp}\n".encode())
                            game_state.monsters[pos] = (name, hello, hp)
                            for u, w in game_state.clients.items():
                                w.write(
                                    f"{username} attacked {name} for {damage} hp, "
                                    f"{hp} left\n".encode()
                                )
                        await writer.drain()
                elif cmd[0] == "sayall":
                    if len(cmd) < 2:
                        writer.write(b"Invalid sayall format\n")
                        await writer.drain()
                        continue
                    message = " ".join(cmd[1:])
                    for u, w in game_state.clients.items():
                        w.write(f"{username}: {message}\n".encode())
                        await w.drain()
                else:
                    writer.write(b"Unknown command\n")
                    await writer.drain()
            except (ValueError, IndexError) as e:
                writer.write(f"Invalid command format: {str(e)}\n".encode())
                await writer.drain()
    except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
        pass
    finally:
        if username in game_state.players:
            del game_state.players[username]
            if username in game_state.clients:
                del game_state.clients[username]
            for u, w in game_state.clients.items():
                w.write(f"{username} disconnected\n".encode())
                await w.drain()
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError):
            pass


async def run_server():
    """Запустить сервер MOOD.

    Создаёт сервер и запускает фоновую задачу для перемещения монстров.
    """
    game_state = GameState()
    asyncio.create_task(move_monsters(game_state))
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, game_state), HOST, PORT
    )
    async with server:
        await server.serve_forever()