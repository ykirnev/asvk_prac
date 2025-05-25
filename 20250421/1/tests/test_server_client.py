"""Тесты для проверки обработки сервером команд от клиента в MOOD."""
import asyncio
import pytest
import multiprocessing
import socket
import psutil
from mood.server.server import start_server
from mood.common.constants import HOST, PORT


@pytest.mark.asyncio
class TestServerClient:
    """Класс для тестирования связки клиент+сервер."""

    @pytest.fixture(autouse=True, scope="function")
    async def setup_teardown(self):
        """Настройка и завершение тестов: запуск сервера и подключение клиента."""
        # Освободить порт, если занят
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((HOST, PORT))
            sock.close()
        except OSError:
            # Порт занят, попытка завершить процесс
            import os
            import signal
            for conn in psutil.net_connections():
                if conn.laddr.port == PORT and conn.status == psutil.CONN_LISTEN:
                    try:
                        os.kill(conn.pid, signal.SIGTERM)
                    except (OSError, psutil.NoSuchProcess):
                        pass

        # Setup: запуск сервера в отдельном процессе
        self.server_process = multiprocessing.Process(
            target=start_server, kwargs={"no_monsters": True}
        )
        self.server_process.start()
        # Даём серверу время на запуск
        await asyncio.sleep(1)

        # Подключение клиента
        try:
            self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
            # Отправка имени пользователя
            username = "test_user"
            self.writer.write(f"{username}\n".encode())
            await self.writer.drain()
            response = await asyncio.wait_for(self.reader.readline(), timeout=2.0)
            assert response.decode().strip() == "Connected to MUD"
            # Очистить буфер
            await self.clear_buffer()
        except (asyncio.TimeoutError, ConnectionRefusedError) as e:
            self.server_process.terminate()
            self.server_process.join()
            pytest.fail(f"Failed to connect to server: {e}")

        yield

        # Teardown: закрытие соединения и остановка сервера
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError):
            pass
        self.server_process.terminate()
        self.server_process.kill()  # Принудительное завершение
        self.server_process.join()

    async def clear_buffer(self):
        """Очистить буфер чтения."""
        while True:
            try:
                response = await asyncio.wait_for(self.reader.read(1024), timeout=0.1)
                if not response:
                    break
                print(f"Debug: Cleared buffer: {response.decode().strip()}")
            except asyncio.TimeoutError:
                break

    async def send_command(self, command: str, expected_lines: int = 1) -> list[str]:
        """Отправить команду на сервер и получить ответы."""
        print(f"Debug: Sending command: {command}")
        await self.clear_buffer()  # Очистить буфер перед отправкой
        self.writer.write(f"{command}\n".encode())
        await self.writer.drain()
        responses = []
        for _ in range(expected_lines):
            try:
                response = await asyncio.wait_for(self.reader.readline(), timeout=2.0)
                response_str = response.decode().strip()
                print(f"Debug: Received response: {response_str}")
                responses.append(response_str)
            except asyncio.TimeoutError:
                print(f"Debug: Timeout waiting for response to {command}")
                break
        return responses

    async def test_addmon(self):
        """Тест: установка монстра недалеко от начального положения (1, 0)."""
        responses = await self.send_command('addmon jgsbat 1 0 "Hi there" 100', expected_lines=2)
        assert responses[0] == "Added monster jgsbat to (1, 0) saying Hi there"
        # Учитываем возможную замену монстра
        assert responses[1] in [
            "test_user added monster jgsbat with 100 hps",
            "Replaced the old monster"
        ]

    async def test_move_to_monster(self):
        """Тест: подход к монстру и получение приветствия."""
        # Устанавливаем монстра
        await self.send_command('addmon jgsbat 1 0 "Hi there" 100', expected_lines=2)

        # Двигаемся к монстру (из (0, 0) в (1, 0))
        responses = await self.send_command("move 1 0", expected_lines=2)
        assert responses[0] == "Moved to (1, 0)"
        assert responses[1] == "monster jgsbat Hi there"

    async def test_attack_monster(self):
        """Тест: атака на монстра."""
        # Устанавливаем монстра
        await self.send_command('addmon jgsbat 1 0 "Hi there" 100', expected_lines=2)

        # Двигаемся к монстру
        await self.send_command("move 1 0", expected_lines=2)

        # Атакуем монстра
        responses = await self.send_command("attack jgsbat 15", expected_lines=3)
        assert responses[0] == "Attacked jgsbat, damage 15 hps"
        assert responses[1] == "jgsbat now has 85 hps"
        assert responses[2] == "test_user attacked jgsbat for 15 hps, 85 left"