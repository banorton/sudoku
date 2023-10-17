import numpy as np
from .solver import *
from .helpers import puzzle_pos_to_box_pos, num_to_pos, puzzle_pos_to_box_num
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

    def __getitem__(self, pos):
        return self.cells.__getitem__(pos)

    def __iter__(self):
        yield from self.cells

    def __str__(self):
        puzzle_str = ""
        for row_num in range(self.cell_dim[0]):
            row = self.cells.get_row(row_num).to_vals()
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
        vals = np.reshape(vals, self.cell_dim).tolist()
        for m in range(self.cell_dim[0]):
            for n in range(self.cell_dim[1]):
                self.update_cell((m, n), vals[m][n])

    def load(self, vals):
        self._assign_vals(vals)

    def get_cell(self, pos: tuple):
        row, col = pos
        return self.cells[row][col]

    def get_row(self, row_num: int):
        return self.cells.get_row(row_num)

    def get_col(self, col_num: int):
        return self.cells.get_col(col_num)

    def get_box(self, pos: int):
        row, col = pos
        return self.boxes[row][col]

    def update_cell(self, pos: tuple, val: int, propagate=True):
        if val == 0:
            return
        print(f"UPDATING {pos} : {val}")
        self.cells_unsolved -= 1
        box_pos, _ = puzzle_pos_to_box_pos(self, pos)
        i, j = pos
        self[i, j].val = val
        self[i, j].notes = {val}

        if propagate:
            row, col = pos
            self.del_notes(
                vals=[val], rows=[row], cols=[col], boxes=[box_pos], save=[pos]
            )

        if not is_valid(self):
            raise Exception("Not valid.")

    def del_notes(self, vals=[], rows=[], cols=[], boxes=[], positions=[], save=[]):
        for val in vals:
            for row_num in rows:
                self.del_notes_row(val, row_num)
            for col_num in cols:
                self.del_notes_col(val, col_num)
            for box_pos in boxes:
                self.del_notes_box(val, box_pos)
            for pos in positions:
                self.del_notes_pos(val, pos)
            if save:
                for pos in save:
                    self.cells[pos[0]][pos[1]].notes.add(val)

    def del_notes_row(self, val, row_num):
        self.cells.get_row(row_num).del_notes(val)
        print("del row: ", row_num, " val: ", val)

    def del_notes_col(self, val, col_num):
        self.cells.get_col(col_num).del_notes(val)
        print("del col: ", col_num, " val: ", val)

    def del_notes_box(self, val, box_pos):
        m, n = box_pos
        box = self.boxes[m][n]
        box.del_notes(val)
        print("del box: ", box_pos, " val: ", val)

    def del_notes_pos(self, val, pos):
        pass

    def solve(self):
        if not is_valid(self):
            print("Not a valid puzzle.")

        found = [1]
        while any(found):
            found = []
            print("\nNAKED SINGLES")
            found.append(find_naked_singles(self))

            print("\nHIDDEN SINGLES")
            found.append(find_hidden_singles(self))

            print("\nNAKED DOUBLES")
            found.append(find_naked_doubles(self))

            print("\nHIDDEN DOUBLES")
            found.append(find_hidden_doubles(self))

            if not self.cells_unsolved:
                print("SOLVED!!!!!!!!!")
                break
