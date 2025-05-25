"""Общие константы для пакета MOOD."""
import io
from cowsay import read_dot_cow

# Параметры подключения к серверу
HOST = "127.0.0.1"
PORT = 8888

# ASCII-арт jgsbat в виде строки
JGSBAT = r"""
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\'--'//__
         (((""`  `"")))
"""

JGSBAT_COW = read_dot_cow(io.StringIO(JGSBAT))
