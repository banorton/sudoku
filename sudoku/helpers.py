"""
TODO: Change puzzle_pos_to_box_pos, puzzle_pos_to_box_num, and find_puzzle_pos 
to take puzzle object instead of all the dimensions.
TODO: Find better names for the functions.
"""

from math import floor, ceil
from itertools import chain


def pos_to_num(pos: tuple, super_dim: tuple) -> int:
    row, col = pos[0], pos[1]
    num = (row * super_dim[0]) + (col + 1)
    return num


def num_to_pos(num: int, super_dim: tuple) -> tuple:
    if num <= 0:
        raise Exception("Invalid num for the given super_dim.")
    row = floor((num - 1) / super_dim[1])
    col = floor((num - 1) % super_dim[1])
    assert col < super_dim[1]
    assert row < super_dim[0]
    return (row, col)


def puzzle_pos_to_box_pos(p, puzzle_pos: tuple) -> tuple:
    box_row = ceil((puzzle_pos[0] + 1) / p.box_dim[0]) - 1
    box_col = ceil((puzzle_pos[1] + 1) / p.box_dim[1]) - 1
    cell_row = ((puzzle_pos[0] + 1) % p.box_dim[0]) - 1
    cell_col = ((puzzle_pos[1] + 1) % p.box_dim[1]) - 1
    return ((box_row, box_col), (cell_row, cell_col))


def puzzle_pos_to_box_pos2(puzzle_pos: tuple, box_dim: tuple) -> tuple:
    box_row = ceil((puzzle_pos[0] + 1) / box_dim[0]) - 1
    box_col = ceil((puzzle_pos[1] + 1) / box_dim[1]) - 1
    cell_row = ((puzzle_pos[0] + 1) % box_dim[0]) - 1
    cell_col = ((puzzle_pos[1] + 1) % box_dim[1]) - 1
    return ((box_row, box_col), (cell_row, cell_col))


def puzzle_pos_to_box_num(p, puzzle_pos: tuple) -> tuple:
    box_pos, cell_pos = puzzle_pos_to_box_pos(puzzle_pos, p.box_dim)
    return pos_to_num(box_pos, p.puzzle_dim)


def find_puzzle_pos(box_dim: tuple, box_pos: tuple, cell_pos: tuple) -> tuple:
    cell_row, cell_col = cell_pos
    box_row, box_col = box_pos
    puzzle_row = cell_row + box_row * box_dim[0]
    puzzle_col = cell_col + box_col * box_dim[1]
    return (puzzle_row, puzzle_col)


def transpose(arr):
    if not isinstance(arr[0], list):
        return [[el] for el in arr]
    else:
        return list(map(list, (zip(*arr))))


def flatten(arr):
    return list(chain.from_iterable(arr))
