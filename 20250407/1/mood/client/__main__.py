"""Точка входа для запуска клиента MOOD."""
import argparse
import asyncio
import sys
from mood.client.client import MUDClient


def main():
    """Запустить клиент MOOD."""
    parser = argparse.ArgumentParser(description="MOOD Client")
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
            client.shutting_down = True
            if client.receive_task is not None:
                client.receive_task.cancel()
                try:
                    loop.run_until_complete(client.receive_task)
                except asyncio.CancelledError:
                    pass
            if client.writer is not None:
                client.writer.close()
                loop.run_until_complete(client.writer.wait_closed())
        else:
            loop.run_in_executor(None, client.cmdloop)
            loop.run_forever()
    except KeyboardInterrupt:
        print("\nВыход...")
        client.shutting_down = True
        if client.receive_task is not None:
            client.receive_task.cancel()
            try:
                loop.run_until_complete(client.receive_task)
            except asyncio.CancelledError:
                pass
        if client.writer is not None:
            client.writer.close()
            try:
                loop.run_until_complete(client.writer.wait_closed())
            except (ConnectionResetError, BrokenPipeError):
                pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
