import asyncio

monsters = {}
players = {}
clients = {}


async def handle_client(reader, writer):
    try:
        username = (await reader.readline()).decode().strip()
        if not username:
            writer.close()
            await writer.wait_closed()
            return
        if username in players:
            writer.write(b"Username already taken\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
        players[username] = [0, 0]
        clients[username] = writer
        writer.write(b"Connected to MUD\n")
        await writer.drain()
        for u, w in clients.items():
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
                    players[username][0] = (players[username][0] + dx) % 10
                    players[username][1] = (players[username][1] + dy) % 10
                    pos = tuple(players[username])
                    writer.write(f"Moved to {pos}\n".encode())
                    if pos in monsters:
                        name, hello, _ = monsters[pos]
                        writer.write(f"monster {name} {hello}\n".encode())
                    await writer.drain()
                elif cmd[0] == "addmon":
                    name, x, y = cmd[1], int(cmd[2]), int(cmd[3])
                    hello = " ".join(cmd[4:-1])  # Collect hello with spaces
                    hp = int(cmd[-1])
                    if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                        writer.write(b"Invalid arguments\n")
                        await writer.drain()
                        continue
                    pos = (x, y)
                    replaced = pos in monsters
                    monsters[pos] = (name, hello, hp)
                    writer.write(f"Added monster {name} to {pos} saying {hello}\n".encode())
                    if replaced:
                        writer.write(b"Replaced the old monster\n")
                    for u, w in clients.items():
                        w.write(f"{username} added monster {name} with {hp} hp\n".encode())
                        await w.drain()
                elif cmd[0] == "attack":
                    monster_name, damage = cmd[1], int(cmd[2])
                    pos = tuple(players[username])
                    if pos not in monsters or monsters[pos][0] != monster_name:
                        writer.write(f"No {monster_name} here\n".encode())
                    else:
                        name, hello, hp = monsters[pos]
                        damage = min(damage, hp)
                        hp -= damage
                        writer.write(f"Attacked {name}, damage {damage} hp\n".encode())
                        if hp == 0:
                            writer.write(f"{name} died\n".encode())
                            del monsters[pos]
                            for u, w in clients.items():
                                w.write(f"{username} killed {name}\n".encode())
                        else:
                            writer.write(f"{name} now has {hp}\n".encode())
                            monsters[pos] = (name, hello, hp)
                            for u, w in clients.items():
                                w.write(f"{username} attacked {name} for {damage} hp, {hp} left\n".encode())
                        await w.drain()
            except (ValueError, IndexError):
                writer.write(b"Invalid command format\n")
                await writer.drain()
    except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
        pass
    finally:
        if username in players:
            del players[username]
            if username in clients:
                del clients[username]
            for u, w in clients.items():
                w.write(f"{username} disconnected\n".encode())
                await w.drain()
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError):
            pass


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())