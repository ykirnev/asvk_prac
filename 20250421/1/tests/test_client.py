"""Тесты для проверки преобразования клиентом команд в формат протокола."""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from mood.client.client import MUDClient


@pytest.mark.asyncio
async def test_client_commands():
    """Тест преобразования пользовательских команд в формат протокола."""
    loop = asyncio.get_event_loop()
    client = MUDClient("test_user", loop)

    # Мокируем send_command
    client.send_command = AsyncMock()

    # Тест 1: Команда right → move 1 0
    with patch.object(client, 'get_input', return_value="right"):
        await client.process_command("right")
        client.send_command.assert_called_with("move 1 0")

    # Тест 2: Команда down → move 0 1
    client.send_command.reset_mock()
    with patch.object(client, 'get_input', return_value="down"):
        await client.process_command("down")
        client.send_command.assert_called_with("move 0 1")

    # Тест 3: Команда attack jgsbat with spear → attack jgsbat 15
    client.send_command.reset_mock()
    with patch.object(client, 'get_input', return_value="attack jgsbat with spear"):
        await client.process_command("attack jgsbat with spear")
        client.send_command.assert_called_with("attack jgsbat 15")

    # Тест 4: Команда attack jgsbat with axe → attack jgsbat 20
    client.send_command.reset_mock()
    with patch.object(client, 'get_input', return_value="attack jgsbat with axe"):
        await client.process_command("attack jgsbat with axe")
        client.send_command.assert_called_with("attack jgsbat 20")

    # Тест 5: Неверные параметры для attack (неизвестное оружие)
    client.send_command.reset_mock()
    with patch('builtins.print') as mocked_print:
        await client.process_command("attack jgsbat with invalid")
        mocked_print.assert_called_with("Неизвестное оружие")
        client.send_command.assert_not_called()