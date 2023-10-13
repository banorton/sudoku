import numpy as np
from .solver import *
from .helpers import puzzle_pos_to_box_pos, num_to_pos
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
            row = self.cells.get_row(row_num).to_list()
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
        box_pos, cell_pos = puzzle_pos_to_box_pos(pos, self.box_dim)
        i, j = pos
        a, b = box_pos
        m, n = cell_pos
        self.cells.arr[i][j].val = val
        self.cells.np[i, j] = val
        self.boxes.arr[a][b].arr[m][n].val = val
        self.boxes.arr[a][b].np[m, n] = val

        if propagate:
            pass

    def get_row(self, row_num: int):
        return self.cells.get_row(row_num)

    def get_col(self, col_num: int):
        return self.cells.get_row(col_num)

    def get_box(self, num: int):
        pos = num_to_pos(num, self.puzzle_dim)
        return self.boxes.arr[pos[0]][pos[1]]

    def del_notes(self, val: int, rows=[], cols=[], boxes=[]):
        for row_num in rows:
            self._del_notes_row(val, row_num)
        for col_num in cols:
            self._del_notes_col(val, col_num)
        for box_num in boxes:
            self._del_notes_box(val, box_num)

    def del_notes_row(self, row_num, num):
        for col_num in range(9):
            if len(self.notes[row_num][col_num]) != 1:
                # self.notes[row_num][col_num].discard(num)
                self.discard_note((row_num, col_num), num)

    def del_notes_col(self, col_num, num):
        for row_num in range(9):
            if len(self.notes[row_num][col_num]) != 1:
                # self.notes[row_num][col_num].discard(num)
                self.discard_note((row_num, col_num), num)

    def del_notes_box(self, box_pos, num):
        box_row = box_pos[0] + 1
        box_col = box_pos[1] + 1
        row_nums = [box_row * 3 - 3, box_row * 3 - 2, box_row * 3 - 1]
        for row_num in row_nums:
            if len(self.notes[row_num][box_col * 3 - 3]) != 1:
                # self.notes[row_num][box_col*3-3].discard(num)
                self.discard_note((row_num, box_col * 3 - 3), num)
            if len(self.notes[row_num][box_col * 3 - 2]) != 1:
                # self.notes[row_num][box_col*3-2].discard(num)
                self.discard_note((row_num, box_col * 3 - 2), num)
            if len(self.notes[row_num][box_col * 3 - 1]) != 1:
                # self.notes[row_num][box_col*3-1].discard(num)
                self.discard_note((row_num, box_col * 3 - 1), num)

    def solve(self):
        if not check_validity(self):
            print("Not a valid puzzle.")

        find_naked_singles(self)
