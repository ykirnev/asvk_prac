"""Точка входа для клиента MOOD."""
import argparse
import asyncio

from mood.client.client import MUDClient


def main():
    """Запустить клиент MUD."""
    parser = argparse.ArgumentParser(description="MOOD MUD Client")
    parser.add_argument("username", help="Имя пользователя")
    parser.add_argument("--file", help="Файл с командами (.mood)")
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
        print("Завершение работы клиента")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
