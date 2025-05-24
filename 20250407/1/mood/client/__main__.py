"""Точка входа для запуска клиента MOOD."""
import asyncio
import sys
from mood.client.client import MUDClient


def main():
    """Запустить клиент MOOD."""
    if len(sys.argv) != 2:
        print("Использование: python3 -m mood.client <username>")
        sys.exit(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = MUDClient(sys.argv[1], loop)
    try:
        loop.run_until_complete(client.connect())
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
            loop.run_until_complete(client.writer.wait_closed())
        loop.stop()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
