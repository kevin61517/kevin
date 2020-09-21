import functools, sys
from collections import deque
from tim_sort import tim_sort
from typing import Any

__all__ = ["dqlst"]

method_type = type(type("Cls", (), {"method": lambda: 0}))
method_append = dict()
method_pop = dict()


def _append(method_key):
    def mid(method):
        method_append.update({method_key: method})

        @functools.wraps(method)
        def inside(*args, **kws):
            return method(*args, **kws)
        return inside
    return mid


def _pop(method_key):
    def mid(method):
        method_pop.update({method_key: method})

        @functools.wraps(method)
        def inside(*args, **kws):
            return method(*args, **kws)
        return inside
    return mid


class _Implement(deque):
    """
    Deque plus implement.
    """

    def chain_append(self, key: str, *args: Any, **kws: Any) -> object():
        method_append.get(key, self)(self, *args, **kws)
        return self

    def chain_pop(self, key: str, *args: Any, **kws: Any) -> object():
        method_pop.get(key, self)(self, *args, **kws)
        return self

    @_append(method_key="right_side")
    def _a_right(self, *objs: Any) -> None:
        """
        right append
        super().append(obj)
        :param obj: any
        :return: self
        """
        for obj in objs:
            super().append(obj)

    @_append(method_key="left_side")
    def _a_left(self, *objs: Any) -> None:
        """
        left append
        super().appendleft(obj)
        :param obj: any
        :return: self
        """
        for obj in objs:
            super().appendleft(obj)

    @_append(method_key="both_side")
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

    def _p_right(self, *objs: Any):
        ...

    def sort(self):
        """
        :return: sorted data
        """
        return tim_sort(self)

    def print(self, sep=' ', end='\n', file=sys.stdout, flush=False):
        print(self, sep=sep, end=end, file=file, flush=flush)
        return self


class DqList(_Implement):
    """
    This is deque plus, which is design from 69master.
    """
    def __str__(self):
        return """Deque plus"""

    def __repr__(self):
        return \
            """
            This class used deque of Python module collections.
            You could used the "chain calling" of method "chain_append" of this class,
            chain_append could be assigment any amount of args, but not key words args.
            DqList().chain_append()
            """


dqlst = DqList

if __name__ == '__main__':
    lst = dqlst
    l = lst([1, 5, 4, 6, 2, 4, 3])
    ll = l.chain_append("both_side", 0, 0, 0, 0, 0).chain_append("right_side", 100).print()
    print(l)
    print(ll)

