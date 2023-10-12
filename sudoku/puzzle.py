import numpy as np
from .solver import *
from .helpers import puzzle_pos_to_box_pos
from .box import Box_Array


class Puzzle:
    def __init__(
        self,
        vals=None,
        puzzle_dim: tuple = (3, 3),
        box_dim: tuple = (3, 3),
    ):
        self.puzzle_dim = puzzle_dim
        self.box_dim = box_dim
        self.cell_dim = (
            self.box_dim[0] * self.puzzle_dim[0],
            self.box_dim[1] * self.puzzle_dim[1],
        )
        self.cells_unsolved = self.cell_dim[0] * self.cell_dim[1]
        self.boxes = Box_Array(puzzle_dim, box_dim)
        self.cells = self.boxes.to_cell_arr()
        if not (vals is None):
            self._assign_vals(vals)

    def __str__(self):
        puzzle_str = ""
        for row_num in range(self.cell_dim[0]):
            row = self.cells.get_row(row_num)
            # Print horizontal seperators between boxes.
            if (row_num % self.box_dim[0]) == 0:
                puzzle_str += "-------------------------------------------------------------------------------------------------\n"
                puzzle_str += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"

            # Print row with vertical seperators between boxes.
            for i in range(self.box_dim[1]):
                puzzle_str += "|\t"
                puzzle_str += str(row[i * self.box_dim[1]]) + "\t"
                puzzle_str += str(row[i * self.box_dim[1] + 1]) + "\t"
                puzzle_str += str(row[i * self.box_dim[1] + 2]) + "\t"

            puzzle_str += "|\n"
            puzzle_str += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"

        puzzle_str += "-------------------------------------------------------------------------------------------------\n"
        return puzzle_str

    def _assign_vals(self, vals):
        if not isinstance(vals, np.ndarray):
            vals = np.array(vals)
        vals = np.reshape(vals, self.cell_dim)
        for m in range(self.cell_dim[0]):
            for n in range(self.cell_dim[1]):
                self.update_cell((m, n), vals[m, n])

    def load(self, vals):
        self._assign_vals(vals)

    def update_cell(self, pos: tuple, val: int, propagate=True):
        self.cells.arr[pos[0]][pos[1]].val = val

    def solve(self):
        valid = check_validity(self)
        if valid:
            print("Valid")
        else:
            print("Invalid")
