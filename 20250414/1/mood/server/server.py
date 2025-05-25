"""Серверная часть многопользовательской игры MOOD."""
import argparse
import asyncio
import random
import shlex
from typing import Dict, List, Tuple
from babel import Locale
from babel.support import Translations
import os

from mood.common.constants import HOST, PORT


class GameState:
    """Управляет состоянием игрового мира MUD."""
    def __init__(self):
        self.monsters: Dict[Tuple[int, int], Tuple[str, str, int]] = {}
        self.players: Dict[str, List[int]] = {}
        self.clients: Dict[str, asyncio.StreamWriter] = {}
        self.monsters_moving: bool = True


async def move_monsters(game_state: GameState):
    """Перемещает случайного монстра каждые 30 секунд, если режим активен."""
    directions = [("right", (1, 0)), ("left", (-1, 0)), ("up", (0, -1)), ("down", (0, 1))]
    print("Debug: Starting move_monsters task")
    while True:
        await asyncio.sleep(30)
        if not game_state.monsters_moving:
            print("Debug: Monster movement disabled")
            continue
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
            for username, writer in game_state.clients.items():
                locale = getattr(writer, 'locale', 'en_US')
                translations = load_translations(locale)
                message = translations.gettext("{name} moved one cell {direction}").format(
                    name=name, direction=direction_name
                )
                writer.write(message.encode() + b"\n")
                await writer.drain()
            for username, pos in game_state.players.items():
                if (pos[0], pos[1]) == new_pos:
                    writer = game_state.clients[username]
                    writer.write(f"monster {name} {hello}\n".encode())
                    await writer.drain()
            break
        if attempts >= max_attempts:
            print("Debug: No valid monster move found")


def load_translations(locale: str) -> Translations:
    """Загрузить переводы для указанной локали."""
    if locale == 'en_US':
        return Translations()
    try:
        locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
        return Translations.load(locale_dir, [locale], domain='messages')
    except Exception as e:
        print(f"Debug: Failed to load translations for {locale}: {e}")
        return Translations()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, game_state: GameState):
    """Обработать подключение клиента."""
    username = None
    locale = 'en_US'
    writer.locale = locale
    translations = load_translations(locale)
    try:
        print("Debug: Waiting for username")
        username = (await reader.readline()).decode().strip()
        print(f"Debug: Received username: {username}")
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
                w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                message = w_translations.gettext("{username} joined MUD").format(username=username)
                w.write(message.encode() + b"\n")
                await w.drain()

        while True:
            print(f"Debug: Waiting for command from {username}")
            data = await reader.readline()
            if not data:
                print(f"Debug: No data received from {username}, closing connection")
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
                    game_state.players[username][0] = (game_state.players[username][0] + dx) % 10
                    game_state.players[username][1] = (game_state.players[username][1] + dy) % 10
                    pos = tuple(game_state.players[username])
                    writer.write(f"Moved to {pos}\n".encode())
                    if pos in game_state.monsters:
                        name, hello, _ = game_state.monsters[pos]
                        writer.write(f"monster {name} {hello}\n".encode())
                    await writer.drain()
                elif cmd[0] == "addmon":
                    if len(cmd) != 6:
                        writer.write(f"Invalid addmon format, received: {cmd}\n".encode())
                        await writer.drain()
                        continue
                    name, x, y, hello, hp = cmd[1:]
                    try:
                        x, y, hp = int(x), int(y), int(hp)
                    except ValueError as e:
                        writer.write(f"Invalid addmon arguments: {e}\n".encode())
                        await writer.drain()
                        continue
                    if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                        writer.write(b"Invalid coordinates or hp\n")
                        await writer.drain()
                        continue
                    pos = (x, y)
                    replaced = pos in game_state.monsters
                    game_state.monsters[pos] = (name, hello, hp)
                    message = translations.gettext("Added monster {name} to {pos} saying {hello}").format(
                        name=name, pos=pos, hello=hello
                    )
                    writer.write(message.encode() + b"\n")
                    if replaced:
                        writer.write(b"Replaced the old monster\n")
                    for u, w in game_state.clients.items():
                        w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                        message = w_translations.ngettext(
                            "{username} added monster {name} with {hp} hp",
                            "{username} added monster {name} with {hp} hps",
                            hp
                        ).format(username=username, name=name, hp=hp)
                        w.write(message.encode() + b"\n")
                        await w.drain()
                elif cmd[0] == "attack":
                    if len(cmd) != 3:
                        writer.write(f"Invalid attack format, received: {cmd}\n".encode())
                        await writer.drain()
                        continue
                    monster_name, damage = cmd[1], cmd[2]
                    try:
                        damage = int(damage)
                    except ValueError:
                        writer.write(b"Invalid damage value\n")
                        await writer.drain()
                        continue
                    pos = tuple(game_state.players[username])
                    if pos not in game_state.monsters or game_state.monsters[pos][0] != monster_name:
                        message = translations.gettext("No {name} here").format(name=monster_name)
                        writer.write(message.encode() + b"\n")
                    else:
                        name, hello, hp = game_state.monsters[pos]
                        damage = min(damage, hp)
                        hp -= damage
                        try:
                            message = translations.ngettext(
                                "Attacked {name}, damage {damage} hp",
                                "Attacked {name}, damage {damage} hps",
                                damage
                            ).format(name=name, damage=damage)
                            writer.write(message.encode() + b"\n")
                        except KeyError as e:
                            print(f"Debug: Translation error: {e}")
                            message = f"Attacked {name}, damage {damage} hp"
                            writer.write(message.encode() + b"\n")
                        if hp == 0:
                            message = translations.gettext("{name} died").format(name=name)
                            writer.write(message.encode() + b"\n")
                            del game_state.monsters[pos]
                            for u, w in game_state.clients.items():
                                w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                                message = w_translations.gettext("{username} killed {name}").format(
                                    username=username, name=name
                                )
                                w.write(message.encode() + b"\n")
                        else:
                            message = translations.ngettext(
                                "{name} now has {hp} hp",
                                "{name} now has {hp} hps",
                                hp
                            ).format(name=name, hp=hp)
                            writer.write(message.encode() + b"\n")
                            game_state.monsters[pos] = (name, hello, hp)
                            for u, w in game_state.clients.items():
                                w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                                try:
                                    message = w_translations.ngettext(
                                        "{username} attacked {name} for {damage} hp, {hp} left",
                                        "{username} attacked {name} for {damage} hps, {hp} left",
                                        damage
                                    ).format(username=username, name=name, damage=damage, hp=hp)
                                except KeyError as e:
                                    print(f"Debug: Translation error for {u}: {e}")
                                    message = f"{username} attacked {name} for {damage} hp, {hp} left"
                                w.write(message.encode() + b"\n")
                        await writer.drain()
                elif cmd[0] == "sayall":
                    if len(cmd) < 2:
                        writer.write(b"Invalid sayall format\n")
                        await writer.drain()
                        continue
                    message = " ".join(cmd[1:])
                    for u, w in game_state.clients.items():
                        w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                        formatted_message = w_translations.gettext("{username}: {message}").format(
                            username=username, message=message
                        )
                        w.write(formatted_message.encode() + b"\n")
                        await w.drain()
                elif cmd[0] == "movemonsters":
                    if len(cmd) != 2 or cmd[1] not in ("on", "off"):
                        writer.write(b"Invalid movemonsters format: use 'on' or 'off'\n")
                        await writer.drain()
                        continue
                    state = cmd[1] == "on"
                    game_state.monsters_moving = state
                    message = translations.gettext("Moving monsters: {state}").format(state=cmd[1])
                    writer.write(message.encode() + b"\n")
                    await writer.drain()
                elif cmd[0] == "locale":
                    if len(cmd) != 2:
                        writer.write(b"Invalid locale format\n")
                        await writer.drain()
                        continue
                    locale = cmd[1]
                    try:
                        Locale.parse(locale)
                        writer.locale = locale
                        translations = load_translations(locale)
                        message = translations.gettext("Set up locale: {locale}").format(locale=locale)
                        writer.write(message.encode() + b"\n")
                    except Exception as e:
                        writer.write(f"Invalid locale: {str(e)}\n".encode())
                    await writer.drain()
                else:
                    writer.write(f"Unknown command: {cmd[0]}\n".encode())
                    await writer.drain()
            except (ValueError, IndexError) as e:
                writer.write(f"Invalid command format: {str(e)}\n".encode())
                await writer.drain()
    except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError) as e:
        print(f"Debug: Connection error for {username}: {e}")
    finally:
        if username in game_state.players:
            print(f"Debug: Cleaning up for {username}")
            del game_state.players[username]
            if username in game_state.clients:
                del game_state.clients[username]
            for u, w in game_state.clients.items():
                w_translations = load_translations(getattr(w, 'locale', 'en_US'))
                message = w_translations.gettext("{username} disconnected").format(username=username)
                w.write(message.encode() + b"\n")
                await w.drain()
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError):
            pass


async def run_server(no_monsters: bool = False):
    """Запустить сервер MOOD."""
    game_state = GameState()
    if not no_monsters:
        asyncio.create_task(move_monsters(game_state))
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, game_state), HOST, PORT)
    async with server:
        await server.serve_forever()


def main():
    """Запустить сервер MUD."""
    parser = argparse.ArgumentParser(description="MOOD MUD Server")
    parser.add_argument("--no-monsters", action="store_true", help="Отключить перемещение бродячих монстров")
    args = parser.parse_args()
    asyncio.run(run_server(no_monsters=args.no_monsters))


if __name__ == "__main__":
    main()