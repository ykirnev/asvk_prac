import asyncio
import multiprocessing
import os
import signal
import socket
import pytest
import psutil
from mood.common.constants import HOST, PORT
from mood.server.server import start_server

@pytest.mark.asyncio
class TestServerClient:
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
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    for conn in proc.net_connections():
                        if conn.laddr.port == PORT:
                            os.kill(proc.pid, signal.SIGTERM)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
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

        # Teardown: завершение сервера и клиента
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except (ConnectionResetError, BrokenPipeError, AttributeError):
            pass
        self.server_process.terminate()
        self.server_process.join()

    async def clear_buffer(self):
        """Очистить входной буфер клиента."""
        while True:
            try:
                await asyncio.wait_for(self.reader.readline(), timeout=0.1)
            except asyncio.TimeoutError:
                break

    async def send_command(self, command: str, expected_lines: int) -> list[str]:
        """Отправить команду серверу и получить ответы."""
        print(f"Debug: Sending command: {command}")
        self.writer.write(f"{command}\n".encode())
        await self.writer.drain()
        responses = []
        for _ in range(expected_lines):
            try:
                response = await asyncio.wait_for(self.reader.readline(), timeout=2.0)
                decoded = response.decode().strip()
                print(f"Debug: Received response: {decoded}")
                responses.append(decoded)
            except asyncio.TimeoutError:
                print("Debug: Timeout waiting for response")
                responses.append("")
        return responses

    async def test_addmon(self):
        """Тест: добавление монстра."""
        responses = await self.send_command('addmon jgsbat 1 0 "Hi there" 100', expected_lines=2)
        assert responses[0] == "Added monster jgsbat to (1, 0) saying Hi there"
        assert responses[1] == "test_user added monster jgsbat with 100 hps"

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