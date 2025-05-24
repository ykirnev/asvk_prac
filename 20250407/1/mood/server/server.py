"""Серверная часть многопользовательской игры MOOD."""
import asyncio
from mood.common.constants import HOST, PORT


class GameState:
    """Управляет состоянием игрового мира MUD."""
    def __init__(self):
        """Инициализировать состояние игры."""
        self.monsters = {}
        self.players = {}
        self.clients = {}


async def handle_client(reader, writer, game_state: GameState):
    """Обработать подключение клиента.

    Args:
        reader: StreamReader для клиента.
        writer: StreamWriter для клиента.
        game_state: Общее состояние игры.
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
            cmd = data.decode().strip().split()
            if not cmd:
                continue
            try:
                if cmd[0] == "move":
                    dx, dy = int(cmd[1]), int(cmd[2])
                    # Перенос строк для соответствия лимиту 79 символов
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
                    name, x, y = cmd[1], int(cmd[2]), int(cmd[3])
                    hello = " ".join(cmd[4:-1])
                    hp = int(cmd[-1])
                    if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                        writer.write(b"Invalid arguments\n")
                        await writer.drain()
                        continue
                    pos = (x, y)
                    replaced = pos in game_state.monsters
                    game_state.monsters[pos] = (name, hello, hp)
                    # Перенос строки
                    writer.write(
                        f"Added monster {name} to {pos} saying {hello}\n".encode()
                    )
                    if replaced:
                        writer.write(b"Replaced the old monster\n")
                    for u, w in game_state.clients.items():
                        # Перенос строки
                        w.write(
                            f"{username} added monster {name} with {hp} hp\n".encode()
                        )
                        await w.drain()
                elif cmd[0] == "attack":
                    monster_name, damage = cmd[1], int(cmd[2])
                    pos = tuple(game_state.players[username])
                    # Перенос строки
                    if (pos not in game_state.monsters or
                            game_state.monsters[pos][0] != monster_name):
                        writer.write(f"No {monster_name} here\n".encode())
                    else:
                        name, hello, hp = game_state.monsters[pos]
                        damage = min(damage, hp)
                        hp -= damage
                        # Перенос строки
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
                                # Перенос строки
                                w.write(
                                    f"{username} attacked {name} for {damage} hp, "
                                    f"{hp} left\n".encode()
                                )
                        await w.drain()
                elif cmd[0] == "sayall":
                    message = " ".join(cmd[1:])
                    for u, w in game_state.clients.items():
                        w.write(f"{username}: {message}\n".encode())
                        await w.drain()
            except (ValueError, IndexError):
                writer.write(b"Invalid command format\n")
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
    """Запустить сервер MOOD."""
    game_state = GameState()
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, game_state), HOST, PORT
    )
    async with server:
        await server.serve_forever()
