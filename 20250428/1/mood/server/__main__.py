"""Точка входа для запуска сервера MOOD."""
import asyncio
from mood.server.server import run_server


def main():
    """Запустить сервер MOOD."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
