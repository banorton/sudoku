from itertools import chain
from math import floor


class Array:
    def __init__(self, arr):
        self.arr = arr
        if not isinstance(arr[0], list):
            self.T = [[el] for el in arr]
            self.dim = (1, len(arr))
        else:
            self.T = list(map(list, (zip(*arr))))
            self.dim = (len(arr), len(arr[0]))

    def __getitem__(self, pos):
        if isinstance(pos, tuple):
            if len(pos) == 2:
                return self.arr[pos[0]][pos[1]]
            else:
                raise Exception(
                    f"Index takes only 1 or 2 values. {len(pos)} were given."
                )
        elif isinstance(pos, int):
            return self.arr[pos]
        else:
            raise Exception(f"{pos} is not a valid index.")

    def __iter__(self):
        yield from self.arr

    def flatten(self):
        return list(chain.from_iterable(self))

    def get_row(self, row_num):
        return self[row_num]

    def get_col(self, col_num):
        return self.T[col_num]


class Positional:
    def __init__(self, pos: tuple, super_dim: tuple = (3, 3)):
        self.super_dim = super_dim
        self.pos = pos
        self.num = self._pos_to_num()

    def _pos_to_num(self) -> int:
        row, col = self.pos[0], self.pos[1]
        num = (row * self.super_dim[0]) + (col + 1)
        return num

    def _num_to_pos(self) -> tuple:
        if self.num <= 0:
            raise Exception("Invalid num for the given super_dim.")
        row = floor((self.num - 1) / self.super_dim[1])
        col = floor((self.num - 1) % self.super_dim[1])
        assert col < self.super_dim[1]
        assert row < self.super_dim[0]
        return (row, col)
