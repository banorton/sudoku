from .generic import Array
from .helpers import find_puzzle_pos
from itertools import chain
import numpy as np


class Cell:
    def __init__(self, val=0):
        self.val = val
        self.notes = {i for i in range(1, 10)}

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)


class Cell_Array(Array):
    def __init__(self, arr):
        Array.__init__(self, arr)
        self.np = self._get_np(arr)
        self.notes = self._get_notes(arr)

    def _get_np(self, arr):
        if self.dim[0] == 1:
            return np.array([cell.val for cell in arr])
        np_arr = np.zeros(self.dim, int)
        for m in range(self.dim[0]):
            for n in range(self.dim[1]):
                np_arr[m, n] = arr[m][n].val
        return np_arr

    def _get_notes(self, arr):
        if self.dim[0] == 1:
            return [cell.notes for cell in arr]
        notes = [[] for _ in range(self.dim[0])]
        for m in range(self.dim[0]):
            for n in range(self.dim[1]):
                notes[m].append(arr[m][n].notes)
        return notes

    def get_row(self, row_num):
        return Cell_Array(self.arr[row_num])

    def get_col(self, col_num):
        return Cell_Array(self.arr[col_num])

    def flatten(self):
        return Cell_Array(list(chain.from_iterable(self.arr)))

    def to_list(self):
        return list(self.np)

    # def _gen_notes(self):
    #     arr = [[] for _ in range(self.cell_dim[0])]
    #     for col_num in range(self.puzzle_dim[1]):
    #         for row_num in range(self.puzzle_dim[0]):
    #             curr_box = self.boxes.arr[row_num][col_num]
    #             for i, box_row in enumerate(curr_box.cells.arr):
    #                 offset = row_num * self.box_dim[0]
    #                 for cell in box_row:
    #                     arr[offset + i].append(cell.notes)
    #     self.notes = Array(arr)
