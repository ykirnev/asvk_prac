"""Клиентская часть многопользовательской игры MOOD."""
import asyncio
import cmd
import shlex
import sys
from cowsay import cowsay, list_cows

from mood.common.constants import HOST, PORT, JGSBAT_COW


class MUDClient(cmd.Cmd):
    """Клиент многопользовательской игры (MUD) для взаимодействия с сервером
    MOOD."""
    prompt = "MUD> "

    def __init__(self, username: str, loop: asyncio.AbstractEventLoop):
        """Инициализировать клиент MUD.

        Args:
            username: Уникальное имя игрока.
            loop: Цикл событий asyncio для асинхронных операций.
        """
        super().__init__()

        self.username = username
        self.loop = loop
        self.reader = None
        self.writer = None
        self.current_input = ""
        self.receive_task = None
        self.shutting_down = False

    async def connect(self):
        """Подключиться к серверу MOOD и начать получение сообщений."""
        try:
            self.reader, self.writer = await asyncio.open_connection(
                HOST, PORT
            )
            self.writer.write(f"{self.username}\n".encode())
            await self.writer.drain()
            response = await self.reader.readline()
            print(response.decode().strip())
            if "already taken" in response.decode():
                sys.exit(1)
            self.receive_task = asyncio.create_task(self.receive_messages())
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу")
            sys.exit(1)

    async def receive_messages(self):
        """Получать и обрабатывать сообщения от сервера."""
        try:
            while not self.shutting_down:
                data = await self.reader.readline()
                if not data:
                    break
                msg = data.decode().strip()
                if msg.startswith("monster "):
                    _, name, hello = msg.split(" ", 2)
                    if name == "jgsbat":
                        print(cowsay(hello, cowfile=JGSBAT_COW))
                    else:
                        print(cowsay(hello, cow=name))
                else:
                    print(msg)
                if not self.shutting_down:
                    print(self.prompt + self.current_input, end="", flush=True)
        except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
            if not self.shutting_down:
                print("Отключение от сервера")
        finally:
            if not self.shutting_down:
                sys.exit(1)

    async def run_commands_from_file(self, filename: str):
        """Выполнить команды из файла с интервалом 1 секунда.

        Args:
            filename: Путь к файлу с командами (.mood).
        """
        if not filename.endswith(".mood"):
            print("Файл должен иметь расширение .mood")
            sys.exit(1)
        try:
            with open(filename, 'r') as f:
                for line in f:
                    command = line.strip()
                    if command:
                        print(f"{self.prompt}{command}")
                        await self.send_command(command)
                        await asyncio.sleep(1)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            sys.exit(1)

    async def run_cmdloop(self):
        """Асинхронно запустить цикл обработки команд."""
        while not self.shutting_down:
            try:
                line = await self.loop.run_in_executor(None, lambda: self.get_input())
                if not line:
                    break
                await self.process_command(line)
            except KeyboardInterrupt:
                break

    def get_input(self):
        """Получить ввод от пользователя синхронно."""
        try:
            return input(self.prompt)
        except EOFError:
            return ""

    async def process_command(self, line: str):
        """Обработать введённую команду."""
        self.current_input = line
        line = self.precmd(line)
        stop = await self.onecmd(line)
        stop = self.postcmd(stop, line)
        if stop:
            self.shutting_down = True

    async def onecmd(self, line: str):
        """Асинхронно выполнить одну команду."""
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return await self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return await self.default(line)
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            return await self.default(line)
        return await func(arg)

    async def do_up(self, arg: str):
        """Переместить игрока вверх.

        Args:
            arg: Аргументы команды (должны быть пустыми).

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        if arg:
            print("Неверные аргументы")
            return False
        await self.send_command("move 0 -1")
        return False

    async def do_down(self, arg: str):
        """Переместить игрока вниз.

        Args:
            arg: Аргументы команды (должны быть пустыми).

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        if arg:
            print("Неверные аргументы")
            return False
        await self.send_command("move 0 1")
        return False

    async def do_left(self, arg: str):
        """Переместить игрока влево.

        Args:
            arg: Аргументы команды (должны быть пустыми).

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        if arg:
            print("Неверные аргументы")
            return False
        await self.send_command("move -1 0")
        return False

    async def do_right(self, arg: str):
        """Переместить игрока вправо.

        Args:
            arg: Аргументы команды (должны быть пустыми).

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        if arg:
            print("Неверные аргументы")
            return False
        await self.send_command("move 1 0")
        return False

    async def do_addmon(self, arg: str):
        """Добавить монстра в игровой мир.

        Args:
            arg: Аргументы команды в формате:
                 <имя> hello <сообщение> hp <здоровье> coords <x> <y>

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        args = shlex.split(arg)
        print(f"Debug: addmon args: {args}")
        if len(args) != 8 or args[1] != "hello" or args[3] != "hp" or args[5] != "coords":
            print(f"Неверный формат команды, ожидается 8 аргументов: {args}")
            return False
        try:
            name, _, hello, _, hp, _, x, y = args
            x, y, hp = int(x), int(y), int(hp)
            if not (0 <= x <= 9 and 0 <= y <= 9 and hp > 0):
                print("Неверные координаты или здоровье")
                return False
            if name not in list_cows() and name != "jgsbat":
                print("Невозможно добавить неизвестного монстра")
                return False
            command = f'addmon {name} {x} {y} "{hello}" {hp}'
            print(f"Debug: Sending command: {command}")
            await self.send_command(command)
        except (ValueError, IndexError) as e:
            print(f"Ошибка формата: {e}")
        return False

    async def do_attack(self, arg: str):
        """Атаковать монстра оружием.

        Args:
            arg: Аргументы команды в формате:
                 <имя_монстра> [with <оружие>]

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        args = shlex.split(arg)
        print(f"Debug: attack args: {args}")
        if not args:
            print("Неверные аргументы")
            return False
        try:
            monster_name = args[0]
            weapon = "sword"
            if len(args) > 1 and args[1] == "with":
                if len(args) != 3 or args[2] not in ("sword", "spear", "axe"):
                    print("Неизвестное оружие")
                    return False
                weapon = args[2]
            damage = {"sword": 10, "spear": 15, "axe": 20}[weapon]
            command = f"attack {monster_name} {damage}"
            print(f"Debug: Sending command: {command}")
            await self.send_command(command)
        except IndexError as e:
            print(f"Ошибка формата: {e}")
        return False

    async def do_sayall(self, arg: str):
        """Отправить сообщение всем игрокам.

        Args:
            arg: Сообщение для рассылки (одно слово или строка в кавычках).

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        args = shlex.split(arg)
        print(f"Debug: sayall args: {args}")
        if len(args) != 1:
            print("Неверные аргументы")
            return False
        message = args[0]
        command = f"sayall {message}"
        print(f"Debug: Sending command: {command}")
        await self.send_command(command)
        return False

    async def send_command(self, command: str):
        """Отправить команду на сервер.

        Args:
            command: Строка команды для отправки.
        """
        if self.writer is None:
            print("Не подключено к серверу")
            return
        try:
            print(f"Debug: Sending to server: {command}")
            self.writer.write(f"{command}\n".encode())
            await self.writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            if not self.shutting_down:
                print("Отключение от сервера")
            sys.exit(1)

    def complete_attack(self, text: str, line: str, begidx: int, endidx: int):
        """Предоставить автодополнение для команды атаки.

        Args:
            text: Текущий вводимый текст.
            line: Полная строка команды.
            begidx: Начальный индекс текста.
            endidx: Конечный индекс текста.

        Returns:
            Список возможных вариантов автодополнения.
        """
        if line.startswith("attack ") and " with " in line:
            weapons = ["sword", "spear", "axe"]
            return [w for w in weapons if w.startswith(text)]
        cow_names = list_cows() + ["jgsbat"]
        return [name for name in cow_names if name.startswith(text)]

    async def default(self, line: str):
        """Обработать неизвестные команды.

        Args:
            line: Введённая строка команды.

        Returns:
            bool: False, чтобы продолжить цикл команд.
        """
        print("Неверная команда")
        return False

    def postcmd(self, stop: bool, line: str):
        """Обработать команду после выполнения.

        Args:
            stop: Флаг остановки цикла команд.
            line: Введённая строка команды.

        Returns:
            Флаг остановки цикла команд.
        """
        self.current_input = ""
        return stop

    def precmd(self, line: str):
        """Обработать команду перед выполнением.

        Args:
            line: Введённая строка команды.

        Returns:
            Обработанная строка команды.
        """
        self.current_input = line
        return line