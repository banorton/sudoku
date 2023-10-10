import numpy as np
from math import floor


class Positional_Element:
    def __init__(self, pos: tuple, super_dim: tuple = (3, 3)):
        self.super_dim = super_dim
        self.pos = pos
        self.num = self._pos_to_num()

    def _pos_to_num(self) -> int:
        row, col = self.pos[0], self.pos[1]
        num = (row * self.super_dim[0]) + (col + 1)
        return num

    def _num_to_pos(self) -> tuple:
        if self.num <= 0:
            raise Exception("Invalid num for the given super_dim.")
        row = floor((self.num - 1) / self.super_dim[1])
        col = floor((self.num - 1) % self.super_dim[1])
        assert col < self.super_dim[1]
        assert row < self.super_dim[0]
        return (row, col)

    @staticmethod
    def pos_to_num(pos: tuple, super_dim: tuple) -> int:
        row, col = pos[0], pos[1]
        num = (row * super_dim[0]) + (col + 1)
        return num

    @staticmethod
    def num_to_pos(num: int, super_dim: tuple) -> tuple:
        if num <= 0:
            raise Exception("Invalid num for the given super_dim.")
        row = floor((num - 1) / super_dim[1])
        col = floor((num - 1) % super_dim[1])
        assert col < super_dim[1]
        assert row < super_dim[0]
        return (row, col)

    @staticmethod
    def find_puzzle_pos(cell_pos: tuple, box_pos: tuple, box_dim: tuple) -> tuple:
        cell_row, cell_col = cell_pos
        box_row, box_col = box_pos
        puzzle_row = cell_row + box_row * box_dim[0]
        puzzle_col = cell_col + box_col * box_dim[1]
        return (puzzle_row, puzzle_col)


class Puzzle:
    def __init__(self, puzzle_dim: tuple = (3, 3), box_dim: tuple = (3, 3)):
        self.puzzle_dim = puzzle_dim
        self.dim = box_dim
        self.cell_dim = (
            self.dim[0] * self.puzzle_dim[0],
            self.dim[1] * self.puzzle_dim[1],
        )
        self.box_arr: list[list[Puzzle._Box]]
        self.cell_arr: list[list[int]]
        self.cell_arr_np: np.array()
        self.notes_arr: list[list[set()]]
        self._gen_box_arr()
        self._gen_cell_arr()
        self._gen_notes_arr()

    class _Cell(Positional_Element):
        def __init__(self, pos: tuple, box_pos: tuple, box_dim: tuple):
            self.val = 0
            self.notes = {i for i in range(1, 10)}
            self.pos: tuple
            self.box_pos = box_pos
            self.num: int
            super().__init__(pos, box_dim)
            self.puzzle_pos = self.find_puzzle_pos(pos, box_pos, box_dim)

        def __str__(self):
            return str(self.puzzle_pos)

        def __repr__(self):
            return str(self.puzzle_pos)

    class _Box(Positional_Element):
        def __init__(
            self,
            pos: tuple = (0, 0),
            puzzle_dim: tuple = (3, 3),
            dim: tuple = (3, 3),
        ):
            self.cell_arr: list[list[Puzzle._Cell]]
            self.dim = dim
            self.pos: tuple
            self.num: int
            super().__init__(pos, puzzle_dim)
            self._gen_cell_arr()

        def _gen_cell_arr(self):
            self.cell_arr = [[] for _ in range(self.dim[0])]
            for row in range(self.dim[0]):
                for col in range(self.dim[1]):
                    self.cell_arr[row].append(
                        Puzzle._Cell((row, col), self.pos, self.dim)
                    )

        def __str__(self):
            res = "\n"
            for row in range(self.dim[0]):
                for col in range(self.dim[1]):
                    res += str(self.cell_arr[row][col].val) + " "
                res += "\n"
            return res

    def _gen_box_arr(self):
        self.box_arr = [[] for _ in range(self.puzzle_dim[0])]
        for row in range(self.puzzle_dim[0]):
            for col in range(self.puzzle_dim[1]):
                self.box_arr[row].append(self._Box((row, col)))

    def _gen_cell_arr(self):
        self.cell_arr = [[] for _ in range(self.cell_dim[0])]
        self.cell_arr_np = np.zeros(self.cell_dim, int)
        for col_num in range(self.puzzle_dim[1]):
            for row_num in range(self.puzzle_dim[0]):
                curr_box = self.box_arr[row_num][col_num]
                for i, box_row in enumerate(curr_box.cell_arr):
                    offset = row_num * self.dim[0]
                    for cell in box_row:
                        self.cell_arr[offset + i].append(cell)

    def _gen_notes_arr(self):
        self.notes_arr = [[] for _ in range(self.cell_dim[0])]
        for col_num in range(self.puzzle_dim[1]):
            for row_num in range(self.puzzle_dim[0]):
                curr_box = self.box_arr[row_num][col_num]
                for i, box_row in enumerate(curr_box.cell_arr):
                    offset = row_num * self.dim[0]
                    for cell in box_row:
                        self.notes_arr[offset + i].append(cell.notes)

    def get_row_vals(self, row_num):
        return self.cell_arr_np[row_num - 1]

    def get_col_vals(self, col_num):
        return self.cell_arr_np.T[col_num - 1]

    def get_box_vals(self, box_pos: tuple = None, box_num: int = None):
        if box_num == None and box_pos == None:
            return
        elif box_num != None and box_pos == None:
            box_pos = Positional_Element.num_to_pos(box_num, self.puzzle_dim)
        elif box_num == None and box_pos != None:
            pass
        elif box_num != None and box_pos != None:
            assert box_num == Positional_Element.num_to_pos(box_num, self.puzzle_dim)

        box = self.box_arr[box_pos[0]][box_pos[1]]
        vals = np.zeros(box.dim, int)
        for m, row in enumerate(box.cell_arr):
            for n, cell in enumerate(row):
                vals[m, n] = cell.val
        return vals

    def get_row_notes(self, row_num):
        return self.notes_arr[row_num - 1]

    def get_col_notes(self, col_num):
        transpose = list(map(list, zip(*self.notes_arr)))
        return transpose[col_num - 1]

    def get_box_notes(self, box_num: int = None, box_pos: tuple = None):
        if box_num == None and box_pos == None:
            return
        elif box_num != None and box_pos == None:
            box_pos = Positional_Element.num_to_pos(box_num, self.puzzle_dim)
        elif box_num == None and box_pos != None:
            pass
        elif box_num != None and box_pos != None:
            assert box_num == Positional_Element.num_to_pos(box_num, self.puzzle_dim)

        box = self.box_arr[box_pos[0]][box_pos[1]]
        notes = list()
        for row in box.cell_arr:
            for cell in row:
                notes.append(cell.notes)
        return notes

    def check_validity():
        return

    def __str__(self):
        puzzle_str = ""
        for row_num in range(self.cell_dim[0]):
            row = self.get_row_vals(row_num)
            # Print horizontal seperators between boxes.
            if (row_num % 3) == 0:
                puzzle_str += "-------------------------------------------------------------------------------------------------\n"
                puzzle_str += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"

            # Print row with vertical seperators between boxes.
            for i in range(3):
                puzzle_str += "|\t"
                puzzle_str += str(row[i * 3]) + "\t"
                puzzle_str += str(row[i * 3 + 1]) + "\t"
                puzzle_str += str(row[i * 3 + 2]) + "\t"

            puzzle_str += "|\n"
            puzzle_str += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"

        puzzle_str += "-------------------------------------------------------------------------------------------------\n"
        return puzzle_str
