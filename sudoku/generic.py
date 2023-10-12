from itertools import chain
import numpy as np
from math import floor


class Array:
    def __init__(self, arr):
        self.arr = arr
        self.T = list(map(list, (zip(*arr))))
        self.np = np.ndarray
        self.dim = (len(arr), len(arr[0]))

    def flatten(self, to_np=False):
        if to_np:
            return np.array(list(chain.from_iterable(self.arr)))
        return list(chain.from_iterable(self.arr))

    def get_row(self, row_num, to_np=False):
        if to_np:
            return self.np[row_num]
        return self.arr[row_num]

    def get_col(self, col_num, to_np=False):
        if to_np:
            return self.np[:, col_num]
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
