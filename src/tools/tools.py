from collections import deque
# from .Tim_sort import tim_sort
# from .Tim_sort import tim_sort
# try:
#     from .Tim_sort import tim_sort
# except ImportError as e:
tim_sort = __import__('Tim_sort').tim_sort

method_type = type(type("Cls", (), {"method": lambda: 0}))
method_map = dict()


def key_method(method_key):
    def mid(method):
        method_map.update({method_key: method})

        def inside(*args, **kws):
            return method(*args, **kws)

        return inside

    return mid


class TimSort:
    def binary_search(self, lst, item, start, end):
        if start == end:
            return start if lst[start] > item else start + 1
        if start > end:
            return start

        mid = (start + end) // 2
        if lst[mid] < item:
            return self.binary_search(lst, item, mid + 1, end)
        elif lst[mid] > item:
            return self.binary_search(lst, item, start, mid - 1)
        else:
            return mid

    def insertion_sort(self, lst):
        length = len(lst)

        for index in range(1, length):
            value = lst[index]
            pos = self.binary_search(lst, value, 0, index - 1)
            lst = lst[:pos] + [value] + lst[pos:index] + lst[index + 1:]

        return lst

    def merge(self, left, right):
        if not left:
            return right

        if not right:
            return left

        if left[0] < right[0]:
            return [left[0]] + self.merge(left[1:], right)

        return [right[0]] + self.merge(left, right[1:])

    def tim_sort(self):
        """
        >>> tim_sort("Python")
        ['P', 'h', 'n', 'o', 't', 'y']
        >>> tim_sort((1.1, 1, 0, -1, -1.1))
        [-1.1, -1, 0, 1, 1.1]
        >>> tim_sort(list(reversed(list(range(7)))))
        [0, 1, 2, 3, 4, 5, 6]
        >>> tim_sort([3, 2, 1]) == insertion_sort([3, 2, 1])
        True
        >>> tim_sort([3, 2, 1]) == sorted([3, 2, 1])
        True
        """
        print("== Tim Sort Go ==")
        length = len(self)
        runs, sorted_runs = [], []
        new_run = [self[0]]
        sorted_array = []
        i = 1
        while i < length:
            if self[i] < self[i - 1]:
                runs.append(new_run)
                new_run = [self[i]]
            else:
                new_run.append(self[i])
            i += 1
        runs.append(new_run)

        for run in runs:
            sorted_runs.append(self.insertion_sort(run))
        for run in sorted_runs:
            sorted_array = self.merge(sorted_array, run)

        return sorted_array


class MyList(deque, TimSort):
    def chain_append(self, key, *args, **kws):
        return method_map.get(key)(self, *args, **kws)

    @key_method("right")
    def right(self, obj):
        """
        super().append(obj)
        :param obj:
        :return: self
        """
        super().append(obj)
        return self

    @key_method("left")
    def left(self, obj):
        """
        super().appendleft(obj)
        :param obj:
        :return: self
        """
        super().appendleft(obj)
        return self

    @key_method("width")
    def width_append(self, obj):
        """
        super().append(obj)
        super().appendleft(obj)
        :param obj:
        :return: self
        """
        super().append(obj)
        super().appendleft(obj)
        return self

    def reverse(self):
        super().reverse()
        return self

    def sort(self):
        self.tim_sort()
        return self

    def print(self):
        print(self)
        return self

    # def multiappend(self, *objs):
    #     for obj in objs:
    #         super().append(obj)
    #     return self

    # def sort(self): sort(self); return self


if __name__ == '__main__':
    lst = MyList
    # lst = list
    a = lst([9, 1, 5, 6, 0, 3, 4, 5, 6, 1, 8, 7])
    a.reverse().print()
    # t = __import__('Tim_sort')
    # print(t.tim_sort(a))
