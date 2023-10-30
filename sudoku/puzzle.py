import numpy as np
from .solver import std_solve, is_valid, nishio
from .helpers import puzzle_pos_to_box_pos
from .box import Box_Array
from .gui.gui import gui
from collections import defaultdict
import tkinter as tk
from math import prod
from .imgproc.imgproc import proc


class Puzzle:
    def __init__(self, vals=None):
        self.puzzle_dim = (3, 3)
        self.box_dim = (3, 3)
        self.cell_dim = (
            self.box_dim[0] * self.puzzle_dim[0],
            self.box_dim[1] * self.puzzle_dim[1],
        )
        self.cells_unsolved = self.cell_dim[0] * self.cell_dim[1]
        self.boxes = Box_Array(self.puzzle_dim, self.box_dim)
        self.cells = self.boxes.to_cell_arr()
        self.checked = defaultdict(lambda: defaultdict(lambda: []))
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

    def _assign_vals(self, vals, force=False):
        if not isinstance(vals, np.ndarray):
            vals = np.array(vals)
        vals = np.reshape(vals, self.cell_dim).tolist()
        for m in range(self.cell_dim[0]):
            for n in range(self.cell_dim[1]):
                self.update_cell((m, n), vals[m][n], force)

    def load(self, vals, force=False):
        self._assign_vals(vals, force)

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

    def update_cell(self, pos: tuple, val: int, force=False, propagate=True):
        if val == 0:
            return
        self.cells_unsolved -= 1
        box_pos, _ = puzzle_pos_to_box_pos(self, pos)
        r, c = pos
        self[r, c].val = val
        self[r, c].notes = {val}

        if not force:
            if not is_valid(self):
                raise Exception("Not valid.")
        elif force:
            if not is_valid(self):
                val = 0
                self[r, c].val = val
                self[r, c].notes = {val}

        if propagate:
            self.del_notes(vals=[val], rows=[r], cols=[c], boxes=[box_pos], save=[pos])

    def del_notes(self, vals=[], rows=[], cols=[], boxes=[], positions=[], save=[]):
        for val in vals:
            for row_num in rows:
                self.del_notes_row(val, row_num)
            for col_num in cols:
                self.del_notes_col(val, col_num)
            for box_pos in boxes:
                self.del_notes_box(val, box_pos)
            if save:
                for pos in save:
                    self.cells[pos[0]][pos[1]].notes.add(val)

    def del_notes_row(self, val, row_num):
        self.cells.get_row(row_num).del_notes(val)

    def del_notes_col(self, val, col_num):
        self.cells.get_col(col_num).del_notes(val)

    def del_notes_box(self, val, box_pos):
        m, n = box_pos
        box = self.boxes[m][n]
        box.del_notes(val)

    def del_notes_cell(self, posns=[], vals=[], save_vals=[]):
        for pos in posns:
            if not vals:
                self[pos].notes = set()
            else:
                for val in vals:
                    self[pos].notes.discard(val)
            for val in save_vals:
                self[pos].notes.add(val)

    def solve(self, prnt=False):
        solved = std_solve(self, prnt)
        if not solved:
            nishio(self, prnt)
        if prnt:
            print("SOLVED")

    def copy(self, p):
        self.cells_unsolved = p.cells_unsolved
        self.boxes = p.boxes
        self.cells = p.cells
        self.checked = p.checked

    def clear(self):
        for row in self:
            for cell in row:
                cell.val = 0
                cell.notes = set(range(1, 10))
        self.cells_unsolved = prod(self.cell_dim)
        self.checked = defaultdict(lambda: defaultdict(lambda: []))


class PuzzleGUI:
    def __init__(self, vals=None):
        self.gui = gui(parent=self)
        self.puzzle = Puzzle()
        if vals:
            self.puzzle.load(vals)
            self.match_GUI_with_Puzzle()
        self.gui.root.mainloop()

    def load(self, vals):
        self.puzzle.load(vals)

    def updateGUI(self, pos, val):
        row, col = pos
        self.gui.entries[row][col].delete(0, tk.END)
        self.gui.entries[row][col].insert(0, str(val))

    def updatePuzzle(self, pos, val):
        return

    def match_GUI_with_Puzzle(self):
        for row in self.puzzle:
            for cell in row:
                if cell.val:
                    self.updateGUI(cell.pos, cell.val)
                else:
                    self.updateGUI(cell.pos, "")

    def match_Puzzle_with_GUI(self):
        self.puzzle.clear()
        for r, row in enumerate(self.gui.entries):
            for c, entry in enumerate(row):
                val = entry.get()
                val = int(val) if val else 0
                self.puzzle.update_cell((r, c), val)

    def solve(self):
        self.match_Puzzle_with_GUI()
        self.puzzle.solve()
        self.match_GUI_with_Puzzle()

    def clear(self):
        self.puzzle.clear()
        self.match_GUI_with_Puzzle()

    def load_image(self):
        nums = proc()
        self.puzzle.clear()
        self.puzzle.load(nums, force=True)
        self.match_GUI_with_Puzzle()
