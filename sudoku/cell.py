from .generic import Positional, Array
from .helpers import find_puzzle_pos


class Cell:
    def __init__(self, val=0):
        self.val = val
        self.notes = {i for i in range(1, 10)}

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)


class Cell_Array(Array):
    def __init__(self, arr):
        # Array.__init__(self, self.gen_arr(dim))
        Array.__init__(self, arr)
        # self.np = self._init_np()

    def gen_arr(self, dim):
        arr = [[] for _ in range(dim[0])]
        for row in range(dim[0]):
            for col in range(dim[1]):
                arr[row].append(Cell())
        return arr

    def get_row(self, row_num, to_np=False):
        if to_np:
            return self.np[row_num]
        return self.arr[row_num]

    def get_col(self, col_num, to_np=False):
        if to_np:
            return self.np[:, col_num]
        return self.T[col_num]

    # def _gen_notes(self):
    #     arr = [[] for _ in range(self.cell_dim[0])]
    #     for col_num in range(self.puzzle_dim[1]):
    #         for row_num in range(self.puzzle_dim[0]):
    #             curr_box = self.boxes.arr[row_num][col_num]
    #             for i, box_row in enumerate(curr_box.cells.arr):
    #                 offset = row_num * self.box_dim[0]
    #                 for cell in box_row:
    #                     arr[offset + i].append(cell.notes)
    #     self.notes = Array(arr)

    # def _init_np(self):
    #     pass
