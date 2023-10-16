from .generic import Array
from .helpers import find_puzzle_pos
from itertools import chain
import numpy as np


class Cell:
    def __init__(self, val=0):
        self.val = val
        if val == 0:
            self.notes = set(range(1, 10))
        else:
            self.notes = {val}


class Cell_Array(Array):
    def __init__(self, arr):
        Array.__init__(self, arr)
        self.np = self._get_np(arr)

    def _get_np(self, arr):
        if self.dim[0] == 1:
            return np.array([cell.val for cell in arr])
        np_arr = np.zeros(self.dim, int)
        for m in range(self.dim[0]):
            for n in range(self.dim[1]):
                np_arr[m, n] = arr[m][n].val
        return np_arr

    def get_row(self, row_num):
        return Cell_Array(self.arr[row_num])

    def get_col(self, col_num):
        return Cell_Array(self.T[col_num])

    def flatten(self):
        if self.dim[0] == 1:
            return self
        return Cell_Array(list(chain.from_iterable(self.arr)))

    def to_vals(self) -> list:
        return list(self.np)

    def to_notes(self) -> list:
        if self.dim[0] == 1:
            notes = []
            for cell in self.arr:
                notes.append(cell.notes)
            return notes

        notes = [[] for _ in range(self.dim[0])]
        for m, row in enumerate(self.arr):
            for cell in row:
                notes[m].append(cell.notes)
            return notes

    def del_notes(self, val):
        cells = self.flatten().arr
        for cell in cells:
            if len(cell.notes) > 1:
                cell.notes.discard(val)
