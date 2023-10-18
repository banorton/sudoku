# TODO: Clean up the array indexing in __getitem__.

from itertools import chain
from .helpers import transpose


class Array:
    def __init__(self, arr):
        self.arr = arr
        if not isinstance(arr[0], list):
            self.T = [[el] for el in arr]
            self.dim = (1, len(arr))
        else:
            self.T = transpose(arr)
            self.dim = (len(arr), len(arr[0]))

    def __getitem__(self, pos):
        res = None
        if isinstance(pos, int):
            res = self.arr[pos]
        elif isinstance(pos, tuple):
            res = self.arr[pos[0]][pos[1]]
        elif pos[0] == slice(None, None, None) and isinstance(pos[1], int):
            res = self.T[pos[1]]
        elif isinstance(pos[0], int) and pos[1] == slice(None, None, None):
            res = self.arr[pos[0]]
        elif isinstance(pos[0], int) and isinstance(pos[1], int):
            res = self.arr[pos[0]][pos[1]]
        return res

    def __iter__(self):
        yield from self.arr

    def flatten(self):
        return list(chain.from_iterable(self))

    def get_row(self, row_num):
        return self[row_num]

    def get_col(self, col_num):
        return self.T[col_num]
