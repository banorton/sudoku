import numpy as np
from .generic import Array
from .cell import Cell, Cell_Array
from .helpers import find_puzzle_pos


class Box(Cell_Array):
    def __init__(self, dim: tuple = (3, 3), pos: tuple = None):
        self.pos = pos
        Cell_Array.__init__(self, self._gen_cell_arr(dim), parent=self)

    def __str__(self):
        res = "\n"
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                res += str(self[row][col].val) + " "
            res += "\n"
        return res

    def _gen_cell_arr(self, dim: tuple):
        arr = [[] for _ in range(dim[0])]
        for row in range(dim[0]):
            for col in range(dim[1]):
                arr[row].append(Cell(pos=(row, col), box_pos=self.pos, parent=self))
        return arr

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


class Box_Array(Array):
    def __init__(self, dim: tuple, box_dim: tuple):
        Array.__init__(self, self._gen_box_arr(dim, box_dim))
        self.dim = dim
        self.box_dim = box_dim
        self.cell_dim = (dim[0] * box_dim[0], dim[1] * box_dim[1])

    def _gen_box_arr(self, dim, box_dim):
        arr = [[] for _ in range(dim[0])]
        for row in range(dim[0]):
            for col in range(dim[1]):
                arr[row].append(Box(box_dim, (row, col)))
        return arr

    def _assign_vals(self, vals):
        if isinstance(vals, np.ndarray):
            vals = np.array(vals)
        vals = np.reshape(vals, self.cell_dim)
        num_row, num_col = self.cell_dim
        for m in range(num_row):
            for n in range(num_col):
                self.update_cell((m, n), vals[m, n])

    def to_cell_arr(self) -> Cell_Array:
        arr = [[] for _ in range(self.cell_dim[0])]
        for col_num in range(self.dim[1]):
            for row_num in range(self.dim[0]):
                curr_box = self[row_num][col_num]
                for i, box_row in enumerate(curr_box):
                    offset = row_num * self.box_dim[0]
                    for cell in box_row:
                        cell.pos = find_puzzle_pos(
                            self.box_dim, (row_num, col_num), cell.pos
                        )
                        arr[offset + i].append(cell)
        return Cell_Array(arr)
