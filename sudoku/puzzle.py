import numpy as np
from .solver import *
from .generic import Array
from .helpers import puzzle_pos_to_box_pos
from .box import Box


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
        self.boxes: Array
        self.cells: Array
        self.notes: Array
        self._gen_boxes()
        self._gen_cells()
        self._gen_notes()
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

    def _gen_boxes(self):
        arr = [[] for _ in range(self.puzzle_dim[0])]
        for row in range(self.puzzle_dim[0]):
            for col in range(self.puzzle_dim[1]):
                arr[row].append(Box((row, col)))
        self.boxes = Array(arr)

    def _gen_cells(self):
        arr = [[] for _ in range(self.cell_dim[0])]
        for col_num in range(self.puzzle_dim[1]):
            for row_num in range(self.puzzle_dim[0]):
                curr_box = self.boxes.arr[row_num][col_num]
                for i, box_row in enumerate(curr_box.cells.arr):
                    offset = row_num * self.box_dim[0]
                    for cell in box_row:
                        arr[offset + i].append(cell)
        self.cells = Array(arr)

    def _gen_notes(self):
        arr = [[] for _ in range(self.cell_dim[0])]
        for col_num in range(self.puzzle_dim[1]):
            for row_num in range(self.puzzle_dim[0]):
                curr_box = self.boxes.arr[row_num][col_num]
                for i, box_row in enumerate(curr_box.cells.arr):
                    offset = row_num * self.box_dim[0]
                    for cell in box_row:
                        arr[offset + i].append(cell.notes)
        self.notes = Array(arr)

    def _assign_vals(self, vals):
        if isinstance(vals, np.ndarray):
            vals = np.array(vals)

        vals = np.reshape(vals, self.cell_dim)
        num_row, num_col = self.cell_dim
        for m in range(num_row):
            for n in range(num_col):
                self.update_cell((m, n), vals[m, n])

    def update_cell(self, pos: tuple, val: int, propagate=True):
        box_pos, in_box_pos = puzzle_pos_to_box_pos(pos, self.box_dim)
        box = self.boxes.arr[box_pos[0]][box_pos[1]]
        print(box.cells.arr[in_box_pos[0]][in_box_pos[1]].val)
        self.cells.arr[pos[0]][pos[1]].val = val
        self.cells.np[pos[0], pos[1]] = val
        print(box.cells.arr[in_box_pos[0]][in_box_pos[1]].val)
        print()

    def solve(self):
        valid = check_validity(self)
        if valid:
            print("Valid")
        else:
            print("Invalid")
