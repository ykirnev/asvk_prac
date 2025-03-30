import asyncio
import json

clients = {}  # {username: writer}
monsters = {}  # {(x, y): {"name": str, "hp": int, "hello": str}}

async def broadcast(message):
    """Отправить сообщение всем подключенным клиентам"""
    for writer in clients.values():
        writer.write((message + "\n").encode())
        await writer.drain()

async def handle_client(reader, writer):
    """Обрабатывает подключение клиента"""
    writer.write("Enter your username: ".encode())
    await writer.drain()
    username = (await reader.readline()).strip().decode()

    if username in clients:
        writer.write("Username already in use! Disconnecting...\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    clients[username] = writer
    await broadcast(f"{username} joined the game!")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            command = json.loads(data.decode().strip())
            response = await process_command(username, command)
            if response:
                writer.write((response + "\n").encode())
                await writer.drain()

    except (asyncio.IncompleteReadError, ConnectionResetError):
        pass

    del clients[username]
    await broadcast(f"{username} left the game.")
    writer.close()
    await writer.wait_closed()

async def process_command(username, command):
    """Обрабатывает команду клиента"""
    cmd = command.get("cmd")

    if cmd == "move":
        x, y = command["x"], command["y"]
        return f"{username} moved to ({x}, {y})"

    elif cmd == "addmon":
        x, y, name, hp, hello = command["x"], command["y"], command["name"], command["hp"], command["hello"]
        monsters[(x, y)] = {"name": name, "hp": hp, "hello": hello}
        await broadcast(f"{username} placed monster {name} ({hp} HP) at ({x}, {y})")

    elif cmd == "attack":
        x, y, name, damage = command["x"], command["y"], command["name"], command["damage"]
        if (x, y) not in monsters or monsters[(x, y)]["name"] != name:
            return f"{username} tried to attack {name}, but it's not here!"

        monster = monsters[(x, y)]
        monster["hp"] -= damage
        if monster["hp"] <= 0:
            del monsters[(x, y)]
            await broadcast(f"{username} killed {name} at ({x}, {y})!")
        else:
            await broadcast(f"{username} hit {name} at ({x}, {y}) for {damage} HP, {monster['hp']} HP remaining")

    return None

async def main():
    server = await asyncio.start_server(handle_client, "localhost", 12345)
    print("Server started on port 12345")
    async with server:
        await server.serve_forever()

asyncio.run(main())