from .generic import Array
from .helpers import find_puzzle_pos
from itertools import chain
import numpy as np


class Cell:
    def __init__(self, val=0, parent=None):
        self.val = val
        if val == 0:
            self.notes = set(range(1, 10))
        else:
            self.notes = {val}
        self.parent = parent


class Cell_Array(Array):
    def __init__(self, arr):
        prep_arr = self._prep_arr(arr)
        Array.__init__(self, prep_arr)
        self.np = self._get_np(prep_arr)

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
        return self.arr

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
                return [Cell(val=arr[i], parent=self) for i in range(len(arr))]
        else:
            if not isinstance(arr[0][0], Cell):
                for row in range(len(arr)):
                    for col in range(len(arr[0])):
                        arr[row][col] = Cell(val=arr[row][col], parent=self)
                return arr
        return arr

    # def update_cell(self, pos: tuple(int, int), val: int):
    #     m, n = pos
    #     self.cells.arr[i][j].val = val
    #     self.cells.arr[i][j].notes = {val}

    #     # Make sure numpy arrays match the lists.
    #     self.cells.np[i, j] = val
    #     self.boxes.arr[a][b].np[m, n] = val

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
