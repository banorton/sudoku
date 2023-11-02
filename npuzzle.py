import numpy as np
from helpers import p2b


class Cell:
    def __init__(self, val=0, pos=None, box=None, parent=None):
        self._val = val
        if val == 0:
            self.notes = set((1, 2, 3, 4, 5, 6, 7, 8, 9))
        else:
            self.notes = set().add(val)
        self.pos = pos
        self.box = box
        self.parent = parent

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val
        self.notes = set().add(new_val)
        self.parent.np[self.pos] = new_val

    def __str__(self):
        return f"{self.val}"

    def __repr__(self):
        return f"{self.pos}"


class Puzzle:
    def __init__(self, vals=None):
        self.cells = []
        self.box = [[] for _ in range(9)]
        self.row = [[] for _ in range(9)]
        self.col = [[] for _ in range(9)]
        self.np = None
        self._init(vals)

    def __setitem__(self, pos, new_val):
        cell = self.__getitem__(pos)
        cell.val = new_val

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
        for r, row in enumerate(arr):
            for c, val in enumerate(row):
                cell = Cell(val=val, pos=(r, c), box=p2b((r, c)), parent=self)
                self.cells.append(cell)
                self.row[r].append(cell)
                self.col[c].append(cell)
                self.box[cell.box].append(cell)
