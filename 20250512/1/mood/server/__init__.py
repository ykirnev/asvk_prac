"""
Python MUD Server Module

Реализация многопользовательского подземелья (MUD) с поддержкой:

- Регистрации игроков

- Передвижения по клеточному полю

- Боя с монстрами

- Бродячих монстров

- Системы сообщений между игроками

"""

import readline
import asyncio
import shlex
from ..common import Game, _
import gettext
import locale
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation("mud", BASE_DIR / "po", ["ru"]),
    ("en_US", "UTF-8"): gettext.NullTranslations()
}
locale.setlocale(locale.LC_ALL,  ("en_US", "UTF-8"))

clients = {}
"""Global dictionary to track connected clients {player_name: asyncio.Queue}"""

clients_lock = asyncio.Lock()
"""Lock for thread-safe access to clients dictionary"""

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

async def MUD(reader, writer, game):
    """
        Main client connection handler

        :param reader: asyncio.StreamReader for incoming data
        :param writer: asyncio.StreamWriter for outgoing data
        :param game: Shared Game instance
        :type game: common.Game

        Handles client lifecycle:

        1. Registration

        2. Command processing

        3. Game event notifications

        4. Cleanup on disconnect

        Supported commands:

        - register <name> - Player registration

        - move <direction> - Move player

        - attack <monster> [with <weapon>] - Attack monster

        - addmon <params> - Add monster

        - s <message> - Send message

        - quit - Disconnect
        """
    me = None
    queue = asyncio.Queue()
    while not reader.at_eof():
        message = None
        skip = False
        if not me:
            data = await reader.readline()
            message = shlex.split(data.decode())
        else:
            done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
            for q in done:
                if q is send:
                    send = asyncio.create_task(reader.readline())
                    message = shlex.split(q.result().decode())
                elif q is receive:
                    receive = asyncio.create_task(clients[me].get())
                    writer.write(f"{q.result()}".encode())
                    await writer.drain()
                    skip = True
            if skip:
                continue
        locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
        match message:
            case['locale', args]:
                locale_name = args.strip()
                response = game.players[me].set_locale(locale_name)
                writer.write(f"{response}\n".encode())
            case ["movemonsters", state]:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                if state not in ("on", "off"):
                    writer.write(_("Invalid argument. Use 'on' or 'off'.\n").encode())
                else:
                    game.move_monsters_enabled = (state == "on")
                    async with clients_lock:
                        current_clients = list(clients.items())
                        for player_name, q in current_clients:
                                locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                                response = _("Moving monsters: {state}").format(state=state)
                                await q.put(f"{response}\n")
            case ["register", name]:
                me = name
                res = game.register_player(name)
                writer.write(f'{res}\n'.encode())
                if res.startswith('You') or res.startswith("Вы"):
                    writer.write(_('"<<< Welcome to Python-MUD 0.1 >>>"\n').format().encode())
                    async with clients_lock:
                        clients[name] = queue
                    send = asyncio.create_task(reader.readline())
                    receive = asyncio.create_task(clients[name].get())
                    async with clients_lock:
                        current_clients = list(clients.items())
                        for player_name, q in current_clients:
                            if player_name != me:
                                locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                                await q.put(_("{me} - is new player").format(me=me))
                else :
                    break
            case ['move', a]:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                res = game.move_player(me, a)
                writer.write(f'{res}\n'.encode())
            case ['attack', *args]:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                res = game.attack_exe(me, args)
                writer.write(f'{res[game.players[me].lang]}\n'.encode())
                async with clients_lock:
                    current_clients = list(clients.items())
                    for player_name, q in current_clients:
                        if player_name != me:
                            locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                            await q.put(_("Player {me}: {res}").format(me=me, res=res[game.players[player_name].lang]))
            case ['addmon', *args]:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                res = game.addmon(args)
                writer.write(f'{res[game.players[me].lang]}\n'.encode())
                async with clients_lock:
                    current_clients = list(clients.items())
                    for player_name, q in current_clients:
                        if player_name != me:
                            locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                            await q.put(_("Player {me}: {res}").format(me=me, res=res[game.players[player_name].lang]))
            case ['s', string]:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                async with clients_lock:
                    current_clients = list(clients.items())
                    for player_name, q in current_clients:
                        if player_name != me:
                            locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                            await q.put(_("{me}: {string}").format(me=me, string=string[1:-1]))
            case ['quit']:
                locale.setlocale(locale.LC_ALL, game.players[me].lang)
                writer.write(_('<<< Good bye! >>>\n').encode())
                game.delplayer(me)
                locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
                async with clients_lock:
                    del clients[me]
                break
        await writer.drain()
    async with clients_lock:
        current_clients = list(clients.items())
        for player_name, q in current_clients:
            if player_name != me:
                locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                await q.put(_("Game over for {me}").format(me=me))
    writer.close()
    await writer.wait_closed()


async def monster_movement_loop(game):
    """
        Background task for periodic monster movement

        :param game: Shared Game instance
        :type game: common.Game

        Every 30 seconds:
        1. Moves random monster
        2. Notifies all players about movement
        3. Handles encounters with players
        """
    while True:
        await asyncio.sleep(30)
        locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
        if not game.move_monsters_enabled:
            continue
        move_result = game.move_random_monster()
        if not move_result:
            continue
        res = {}
        for i in LOCALES:
            locale.setlocale(locale.LC_ALL, i)
            res[i] = _("{n} moved one cell {d}").format(n=move_result['name'],d=move_result['direction'])
            #res[i] += _("{n} moved one cell {d}").format(n=move_result['name'], d=move_result['direction'])
        async with clients_lock:
            current_clients = list(clients.items())
        #print(current_clients)
            for player_name, q in current_clients:
                locale.setlocale(locale.LC_ALL, game.players[player_name].lang)
                await q.put(res[game.players[player_name].lang])
        players = game.field[move_result['new_pos'][0]][move_result['new_pos'][1]]["players"]
        monster = game.field[move_result['new_pos'][0]][move_result['new_pos'][1]]["monster"]
        if monster:
            # print(f"{monster.name}, {players}")
            for player_name in players:
                encounter_msg = f"\n{game.encounter(move_result['new_pos'][0], move_result['new_pos'][1])}"
                # print(encounter_msg)
                async with clients_lock:
                    q = clients.get(player_name)
                if q:
                    await q.put(encounter_msg)


async def main():
    """Main server entry point"""
    game = Game()
    server = await asyncio.start_server(lambda r, w: MUD(r, w, game), '0.0.0.0', 1337)
    asyncio.create_task(monster_movement_loop(game))
    async with server:
        await server.serve_forever()

def run_server():
    asyncio.run(main())
