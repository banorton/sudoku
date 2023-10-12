import numpy as np
from .generic import Positional, Array
from .cell import Cell


class Box(Positional):
    def __init__(
        self,
        pos: tuple = (0, 0),
        puzzle_dim: tuple = (3, 3),
        dim: tuple = (3, 3),
    ):
        self.cells: Array
        self.dim = dim
        self.pos: tuple
        self.num: int
        super().__init__(pos, puzzle_dim)
        self._gen_cells()

    def __str__(self):
        res = "\n"
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                res += str(self.cells[row][col].val) + " "
            res += "\n"
        return res

    def _gen_cells(self):
        arr = [[] for _ in range(self.dim[0])]
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                arr[row].append(Cell((row, col), self.pos, self.dim))
        self.cells = Array(arr)

    def get_vals(self, to_np=False):
        vals = np.zeros(self.dim, int)
        for m, row in enumerate(self.cells):
            for n, cell in enumerate(row):
                vals[m, n] = cell.val
        if to_np:
            return vals
        return list(list(vals))

    def get_notes(self, to_np=False):
        notes = list()
        for row in self.cells:
            for cell in row:
                notes.append(cell.notes)
        if to_np:
            return np.array(notes)
        return notes
