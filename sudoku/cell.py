# TODO: Clean up the array indexing in __getitem__.

from .generic import Array
from .helpers import transpose
from itertools import chain
import numpy as np


class Cell:
    def __init__(self, val=0, parent=None, pos=None):
        self._val = val
        self.pos = pos
        if val == 0:
            self.notes = set(range(1, 10))
        else:
            self.notes = {val}
        self.parent = parent

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        if self.parent != None:
            i, j = self.pos
            self.parent.np[i, j] = new_val
        self._val = new_val


class Cell_Array(Array):
    def __init__(self, arr):
        prep_arr = self._prep_arr(arr)
        Array.__init__(self, prep_arr)
        self.np = self._get_np(prep_arr)

    # def __getitem__(self, pos):
    #     res = None
    #     if isinstance(pos, int):
    #         res = self.arr[pos]
    #     elif pos[0] == slice(None, None, None) and isinstance(pos[1], int):
    #         res = transpose(self.T[pos[1]])
    #     elif isinstance(pos[0], int) and pos[1] == slice(None, None, None):
    #         res = self.arr[pos[0]]
    #     elif isinstance(pos[0], int) and isinstance(pos[1], slice):
    #         res = self.arr[pos[0]][pos[1]]
    #     elif isinstance(pos[0], slice) and isinstance(pos[1], int):
    #         res = transpose(self.T[pos[1]][pos[0]])
    #     elif isinstance(pos[0], int) and isinstance(pos[1], int):
    #         return self.arr[pos[0]][pos[1]]

    #     if isinstance(res, list):
    #         return Cell_Array(res)
    #     else:
    #         return res

    def _get_np(self, arr):
        if self.dim[0] == 1:
            return np.array([cell.val for cell in arr])
        np_arr = np.zeros(self.dim, int)
        for m in range(self.dim[0]):
            for n in range(self.dim[1]):
                np_arr[m, n] = arr[m][n].val
        return np_arr

    def _prep_arr(self, arr):
        if not isinstance(arr[0], list):
            if not isinstance(arr[0], Cell):
                return [
                    Cell(val=arr[i], parent=self, pos=(0, i)) for i in range(len(arr))
                ]
        else:
            if not isinstance(arr[0][0], Cell):
                for row in range(len(arr)):
                    for col in range(len(arr[0])):
                        arr[row][col] = Cell(
                            val=arr[row][col], parent=self, pos=(row, col)
                        )
            else:
                for row in range(len(arr)):
                    for col in range(len(arr[0])):
                        arr[row][col].parent = self
                        arr[row][col].pos = (row, col)
            return arr
        return arr

    def get_row(self, row_num):
        return Cell_Array(self[row_num])

    def get_col(self, col_num):
        return Cell_Array(self.T[col_num])

    def flatten(self):
        if self.dim[0] == 1:
            return self
        return Cell_Array(list(chain.from_iterable(self)))

    def to_vals(self) -> list:
        return list(self.np)

    def to_notes(self) -> list:
        if self.dim[0] == 1:
            notes = []
            for cell in self:
                notes.append(cell.notes)
            return notes

        notes = [[] for _ in range(self.dim[0])]
        for m, row in enumerate(self):
            for cell in row:
                notes[m].append(cell.notes)
            return notes

    def del_notes(self, val):
        cells = self.flatten()
        for cell in cells:
            if len(cell.notes) > 1:
                cell.notes.discard(val)
