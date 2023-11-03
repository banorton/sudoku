import numpy as np
from helpers import p2b
from collections import defaultdict
import tkinter as tk
from math import prod
import nsolver as ns


class Cell:
    def __init__(self, val=0, pos=None, box=None):
        if not isinstance(val, int):
            val = int(val)
        self._val = val
        if val == 0:
            self.notes = set(range(1, 10))
        else:
            self.notes = set((val,))
        self.pos = pos
        self.box = box

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val
        self.notes = set((new_val,))

    def __str__(self):
        return f"{self.val}"

    def __repr__(self):
        return f"Cell@{self.pos}"

    def __int__(self):
        return self.val


class Puzzle:
    def __init__(self, vals=None):
        self.unsolved = 81
        self.cells = []
        self.box = [[] for _ in range(9)]
        self.row = [[] for _ in range(9)]
        self.col = [[] for _ in range(9)]
        self.np = None
        self._init(vals)
        self.checked = defaultdict(lambda: defaultdict(lambda: []))

    def __setitem__(self, pos, new_val):
        cell = self.__getitem__(pos)
        self._update_cell(cell, new_val)

    def __getitem__(self, pos):
        res = None
        if isinstance(pos, int):
            res = self.row[pos]
        elif pos[0] == slice(None, None, None) and isinstance(pos[1], int):
            res = self.col[pos[1]]
        elif isinstance(pos[0], int) and pos[1] == slice(None, None, None):
            res = self.row[pos[0]]
        elif isinstance(pos, tuple):
            res = self.row[pos[0]][pos[1]]
        return res

    def __iter__(self):
        yield from self.row

    def __str__(self):
        pstr = ""
        for r, row in enumerate(self.row):
            # Print horizontal seperators between boxes.
            if (r % 3) == 0:
                pstr += "-------------------------------------------------------------------------------------------------\n"
                pstr += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"
            # Print row with vertical seperators between boxes.
            for i in range(3):
                pstr += f"|\t{row[i * 3]}\t{row[i * 3 + 1]}\t{row[i * 3 + 2]}\t"
            pstr += "|\n"
            pstr += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"
        pstr += "-------------------------------------------------------------------------------------------------\n"
        return pstr

    def _init(self, vals):
        if vals:
            arr = np.reshape(np.array(vals), (9, 9))
        else:
            arr = np.zeros((9, 9), int)
        self.np = arr

        # Initialize the cells.
        for r, row in enumerate(arr):
            for c, val in enumerate(row):
                cell = Cell(pos=(r, c), box=p2b((r, c)))
                self.cells.append(cell)
                self.row[r].append(cell)
                self.col[c].append(cell)
                self.box[cell.box].append(cell)

        # Assign all values after initialization to make sure notes are discarded properly.
        for r, row in enumerate(arr):
            for c, val in enumerate(row):
                if val != 0:
                    self[r, c] = val

    def _update_cell(self, cell, new_val):
        new_val = int(new_val)
        cell.val = new_val
        self.np[cell.pos] = new_val
        self.unsolved -= 1
        valid, reason = ns.is_valid(self)
        if not valid:
            raise Exception(reason)
        r, c = cell.pos
        self.del_notes(val=new_val, row=r, col=c, box=cell.box, save=cell.pos)

    def del_notes(self, val=[], row=[], col=[], box=[], save=[]):
        if isinstance(val, int):
            val = [val]
        if isinstance(row, int):
            row = [row]
        if isinstance(col, int):
            col = [col]
        if isinstance(box, int):
            box = [box]
        if isinstance(save, tuple):
            if isinstance(save[0], int):
                save = [save]
            elif isinstance(save[0], tuple):
                save = list(save)
        for val in val:
            for rnum in row:
                self.del_notes_row(val, rnum)
            for cnum in col:
                self.del_notes_col(val, cnum)
            for bnum in box:
                self.del_notes_box(val, bnum)
            if save:
                for pos in save:
                    self[pos[0]][pos[1]].notes.add(val)

    def del_notes_row(self, val, rnum):
        for cell in self.row[rnum]:
            cell.notes.discard(val)

    def del_notes_col(self, val, cnum):
        for cell in self.col[cnum]:
            cell.notes.discard(val)

    def del_notes_box(self, val, bnum):
        for cell in self.box[bnum]:
            cell.notes.discard(val)

    def del_notes_cell(self, posns=[], vals=[], save_vals=[]):
        for pos in posns:
            if not vals:
                self[pos].notes = set()
            else:
                for val in vals:
                    self[pos].notes.discard(val)
            for val in save_vals:
                self[pos].notes.add(val)

    def copy(self, p):
        self.cells = p.cells
        self.box = p.box
        self.row = p.row
        self.col = p.col
        self.np = p.np
        self.unsolved = p.unsolved
        self.checked = p.checked

    def clear(self):
        for row in self.row:
            for cell in row:
                cell.val = 0
                cell.notes = set(range(1, 10))
        self.checked = defaultdict(lambda: defaultdict(lambda: []))

    def solve(self):
        solved = ns.std_solve(self)
        if not solved:
            ns.nishio(self)
