"""
This is deque plus, which is design from 69master.
"""
import functools
import sys
from collections import deque
from tim_sort import tim_sort
from typing import Any

__all__ = ["dqlst"]

method_type = type(type("Cls", (), {"method": lambda: 0}))
__method_append = dict()
option_map = {'append': __method_append}


def _method_map(option, side):
    def mid(method):
        option_map[option].update({side: method})

        @functools.wraps(method)
        def inside(*args, **kws):
            return method(*args, **kws)

        return inside

    return mid


class _Implement(deque):
    """
    Deque plus implement.
    """
    def chain_call(self, option: str, key: str, *args: Any) -> object:
        option_map[option].get(key, self)(self, *args)
        return self

    @_method_map(option="append", side="right")
    def _a_right(self, *objs: Any) -> None:
        """
        right append
        super().append(obj)
        :param obj: any
        :return: self
        """
        for obj in objs:
            super().append(obj)

    @_method_map(option="append", side="left")
    def _a_left(self, *objs: Any) -> None:
        """
        left append
        super().appendleft(obj)
        :param obj: any
        :return: self
        """
        for obj in objs:
            super().appendleft(obj)

    @_method_map(option="append", side="both")
    def _a_both(self, *objs: Any) -> None:
        """
        left and right
        super().append(obj)
        super().appendleft(obj)
        :param obj: any
        :return: self
        """
        for obj in objs:
            super().append(obj)
            super().appendleft(obj)

    def sort(self):
        """
        :return: sorted data
        """
        return tim_sort(self)

    def print(self, *args, sep=' ', end='\n', file=sys.stdout, flush=False):
        print(self, *args, sep=sep, end=end, file=file, flush=flush)
        return self


class DqList(_Implement):
    """
    This class used deque of Python module collections.
    You could used the "chainally calling" of method "chain_call" of this class,
    chain_call could be assigment any amount of args, but not key words.
    DqList().chain_call(self, option -> 'append', side -> 'right', *args -> Any)
    """


dqlst = DqList

if __name__ == '__main__':
    lst = dqlst
    l = lst([1, 5, 4, 6, 2, 4, 3])
    # ll = l.chain_append("both_side", 0, 0, 0, 0, 0).chain_append("right_side", 100).print()
    ll = l.chain_call('append', 'right', 999).print('123')
    print(ll)

