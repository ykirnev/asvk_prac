"""Точка входа для клиента многопользовательской игры MOOD."""
import argparse
import asyncio
import sys

from mood.client.client import MUDClient


def main():
    """Запустить клиент MUD с поддержкой интерактивного режима или скриптования."""
    parser = argparse.ArgumentParser(description="MOOD MUD Client")
    parser.add_argument("username", help="Имя пользователя для подключения к MUD")
    parser.add_argument(
        "--file",
        help="Путь к файлу с командами (.mood) для автоматического выполнения",
        default=None,
    )
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = MUDClient(args.username, loop)

    try:
        loop.run_until_complete(client.connect())
        if args.file:
            loop.run_until_complete(client.run_commands_from_file(args.file))
        else:
            loop.run_until_complete(client.run_cmdloop())
    except KeyboardInterrupt:
        client.shutting_down = True
        if client.receive_task:
            client.receive_task.cancel()
        if client.writer:
            client.writer.close()
            loop.run_until_complete(client.writer.wait_closed())
    finally:
        loop.close()


if __name__ == "__main__":
    main()