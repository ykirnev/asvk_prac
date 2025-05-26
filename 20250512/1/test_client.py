import unittest
from io import StringIO

import mood.client as client
import time
from unittest.mock import MagicMock, patch

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.i = 0
        time.sleep(1)

    def setUp(self):
        self.mocker = MagicMock()
        self.cmdline = client.MUDCmd(self.mocker, f'test{self.__class__.i}')
        self.__class__.i += 1

    def test_1(self):
        """Test sayall"""
        self.cmdline.do_sayall("hello")
        self.mocker.sendall.assert_called_with("s ['hello']\n".encode())

    def test_2(self):
        """Test addmon"""
        self.cmdline.do_addmon("dragon hello 'hi' coords 1 1 hp 100")
        self.mocker.sendall.assert_called_with("addmon dragon hi 100 1 1\n".encode())


    def test_3(self):
        """Test incorrect"""
        invalid_cases = [
            "attack unknown_monster with gun",
            "attack cow with"
        ]

        for input_cmd in invalid_cases:
            with self.subTest(input=input_cmd):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    with patch('sys.stdin', StringIO(input_cmd + "\n")):
                        self.cmdline.onecmd(input_cmd)
                        output = mock_stdout.getvalue().strip()
                        self.assertTrue("unknown" in output.lower() or "cannot" in output.lower())
                        self.mocker.sendall.assert_called_with(b'register test2\n')


    def tearDown(self):
        """Очистка после каждого теста"""
        self.mocker.reset_mock()

    @classmethod
    def tearDownClass(cls):
        pass