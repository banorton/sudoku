import numpy as np
from math import (
    floor,
    ceil
)


class Positional_Element:
    def __init__(self, pos: tuple, dim: tuple = (3, 3)):
        self.dim = dim
        self.pos = pos
        self.num = self.pos_to_num(pos)

    def pos_to_num(self, pos: tuple) -> int:
        row, col = pos[0] + 1, pos[1] + 1
        num = (floor(row / self.dim[0]) * 3) + ceil(col / self.dim[0])
        return num


class Puzzle():
    def __init__(self, puzzle_dim: tuple = (3, 3), box_dim: tuple = (3, 3)):
        self.puzzle_dim = puzzle_dim
        self.box_dim = box_dim
        self.box_arr: list[list[int]]
        self.cell_arr: list[list[int]]
        self.cell_arr_np: np.array()
        self._gen_box_arr()
        self._gen_cell_arr()

    class _Cell(Positional_Element):
        def __init__(self, pos: tuple = (0, 0), dim: tuple = (3, 3)):
            self.val = 0
            self.notes = []
            super().__init__(pos, dim)

        def __str__(self):
            return str(self.pos)

    class _Box(Positional_Element):
        def __init__(self, pos: tuple = (0, 0), dim: tuple = (3, 3)):
            self.cell_arr = self._generate_cell_arr()
            super().__init__(pos, dim)

        def _generate_cell_arr(self):
            return 0

        def __str__(self):
            return str(self.pos)

        def __repr__(self):
            return str("Box@" + str(self.pos))

    def _gen_box_arr(self):
        self.box_arr = [[] for _ in range(self.puzzle_dim[0])]
        for row in range(self.puzzle_dim[0]):
            for col in range(self.puzzle_dim[1]):
                self.box_arr[row].append(self._Box((row, col)))

    def _gen_cell_arr(self):
        self.cell_arr_np = np.zeros(
            (self.puzzle_dim[0] * self.box_dim[0], self.puzzle_dim[1] * self.box_dim[1]), int)
        self.cell_arr = [[] for _ in range]
        for box in self.box_arr:
            self.cell_arr

    def __str__(self):
        res = "\n"
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                res += str(self.box_arr[row][col]) + " "
            res += "\n"
        return res
