from .generic import Positional
from .helpers import find_puzzle_pos


class Cell(Positional):
    def __init__(self, pos: tuple, box_pos: tuple, box_dim: tuple):
        self.val = 0
        self.notes = {i for i in range(1, 10)}
        self.pos: tuple
        self.box_pos = box_pos
        self.num: int
        super().__init__(pos, box_dim)
        self.puzzle_pos = find_puzzle_pos(pos, box_pos, box_dim)

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)
