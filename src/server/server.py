import os
from command.cmdmanagement import cmd_map
from threading import Thread
import asyncio
import math
import decimal

##################################################
#                     SERVER                     #
##################################################


class Server:
    def __init_subclass__(cls, **kws):
        # print(kws)
        func = cmd_map(get=kws.get("cmd"))
        cls.name = "kevin"
        cls.result = func
        # print(cls.result())


class Radio:
    def __get__(self, instance, cls):
        return self.clz

    def __set__(self, instance, value):
        instance.msg = value
        cmd = {"cmd": instance.msg}

        class Inside(Server, **cmd):
            """
            For make communication with server.
            """
        self.clz = Inside


class Client:
    radio = Radio()
    msg = 'Hotel_California_1994'


def rock_n_roll():
    msg = input()
    cli.radio = msg
    cli.radio.result()
    return msg


cli = Client()
bytearray

# if __name__ == "__main__":
#     print("=== server start ===")
#     while True:
#         msg = rock_n_roll()
#         if msg == "done": break
