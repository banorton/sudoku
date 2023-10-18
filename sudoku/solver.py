# TODO: Optimize the finding algorithms.

import numpy as np
from .helpers import *
from collections import defaultdict


def is_valid(p):
    # Check boxs for duplicates.
    for box_num in range(1, 10):
        box_pos = num_to_pos(box_num, p.puzzle_dim)
        box = p.boxes[box_pos[0]][box_pos[1]]
        box_cells = box.flatten().np
        box_cells = np.delete(box_cells, np.where(box_cells == 0))
        if box_cells.size > np.unique(box_cells).size:
            return 0

    # Check rows for duplicates.
    for row_num in range(9):
        row = p.cells.get_row(row_num).np
        row = np.delete(row, np.where(row == 0))
        if row.size > np.unique(row).size:
            return 0

    # Check columns for duplicates.
    for col_num in range(9):
        col = p.cells.get_col(col_num).np
        col = np.delete(col, np.where(col == 0))
        if col.size > np.unique(col).size:
            return 0

    # Return 1 if the board state is valid.
    return 1


############################################################################
# NAKED
def find_naked_singles(p) -> bool:
    found = False
    for row_num in range(9):
        for col_num in range(9):
            notes = p.cells[row_num][col_num].notes
            if len(notes) == 1:
                if p.cells.np[row_num, col_num] == 0:
                    p.update_cell((row_num, col_num), notes.pop())
                    found = True
    return found


def find_naked_doubles(p) -> bool:
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row, checks = p.get_row(row_num), defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            if len(notes) == 2:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 2:
                    found = True
                    p.del_notes(vals=notes, rows=[row_num], save=checks[notes])
    # Col
    for col_num in range(p.cell_dim[1]):
        col, checks = p.get_col(col_num), defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            if len(notes) == 2:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 2:
                    found = True
                    p.del_notes(vals=notes, cols=[col_num], save=checks[notes])
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, checks = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                if len(notes) == 2:
                    checks[notes].append(cell.pos)
                    if len(checks[notes]) == 2:
                        found = True
                        p.del_notes(vals=notes, boxes=[(row, col)], save=checks[notes])
    return found


def find_naked_triples(p):
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row, checks = p.get_row(row_num), defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            if len(notes) == 3:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 3:
                    found = True
                    p.del_notes(vals=notes, rows=[row_num], save=checks[notes])
    # Col
    for col_num in range(p.cell_dim[1]):
        col, checks = p.get_col(col_num), defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            if len(notes) == 3:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 3:
                    found = True
                    p.del_notes(vals=notes, cols=[col_num], save=checks[notes])
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, checks = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                if len(notes) == 3:
                    checks[notes].append(cell.pos)
                    if len(checks[notes]) == 3:
                        found = True
                        p.del_notes(vals=notes, boxes=[(row, col)], save=checks[notes])
    return found


def find_naked_quadruples(p):
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row, checks = p.get_row(row_num), defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            if len(notes) == 4:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 4:
                    found = True
                    p.del_notes(vals=notes, rows=[row_num], save=checks[notes])
    # Col
    for col_num in range(p.cell_dim[1]):
        col, checks = p.get_col(col_num), defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            if len(notes) == 4:
                checks[notes].append(cell.pos)
                if len(checks[notes]) == 4:
                    found = True
                    p.del_notes(vals=notes, cols=[col_num], save=checks[notes])
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, checks = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                if len(notes) == 4:
                    checks[notes].append(cell.pos)
                    if len(checks[notes]) == 4:
                        found = True
                        p.del_notes(vals=notes, boxes=[(row, col)], save=checks[notes])
    return found


############################################################################
# HIDDEN
def find_hidden_singles(p) -> bool:
    found = False
    for row_num in range(9):
        row = p.get_row(row_num)
        for col_num in range(9):
            pos = (row_num, col_num)
            cell = p.get_cell(pos)
            if cell.val != 0:
                continue
            box_pos, _ = puzzle_pos_to_box_pos(p, pos)
            col, box = p.get_col(col_num), p.get_box(box_pos)

            row_notes = []
            for row_cell in row:
                row_notes.extend(list(row_cell.notes))
            col_notes = []
            for col_cell in col:
                col_notes.extend(list(col_cell.notes))
            box_notes = []
            for box_cell in box.flatten():
                box_notes.extend(list(box_cell.notes))

            for val in list(cell.notes):
                if box_notes.count(val) == 1:
                    p.update_cell(pos, val)
                    found = True
                elif row_notes.count(val) == 1:
                    p.update_cell(pos, val)
                    found = True
                elif col_notes.count(val) == 1:
                    p.update_cell(pos, val)
                    found = True
    return found


def find_hidden_doubles(p):
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row = p.get_row(row_num)
        counts = defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = dict()
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 2:
                if value in poss:
                    found = True
                    p.del_notes(vals=[key, poss[value]], rows=[row_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=[key, poss[value]])
                else:
                    poss[value] = key
    # Col
    for col_num in range(p.cell_dim[1]):
        col = p.get_col(col_num)
        counts = defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = dict()
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 2:
                if value in poss:
                    found = True
                    p.del_notes(vals=[key, poss[value]], cols=[col_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=[key, poss[value]])
                else:
                    poss[value] = key
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                for val in notes:
                    counts[val].append(cell.pos)
            poss = dict()
            for key, value in counts.items():
                value = tuple(value)
                if len(value) == 2:
                    if value in poss:
                        found = True
                        p.del_notes(
                            vals=[key, poss[value]], boxes=[(row, col)], save=value
                        )
                        p.del_notes_cell(poss=value, save_vals=[key, poss[value]])
                    else:
                        poss[value] = key
    return found


def find_hidden_triples(p):
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row = p.get_row(row_num)
        counts = defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(def_val)
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 3:
                poss[value].append(key)
                if value in poss and len(poss[value]) == 3:
                    found = True
                    p.del_notes(vals=poss[value], rows=[row_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=poss[value])
    # Col
    for col_num in range(p.cell_dim[1]):
        col = p.get_col(col_num)
        counts = defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(def_val)
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 3:
                poss[value].append(key)
                if value in poss and len(poss[value]) == 3:
                    found = True
                    p.del_notes(vals=poss[value], cols=[col_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=poss[value])
    # # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                for val in notes:
                    counts[val].append(cell.pos)
            poss = defaultdict(def_val)
            for key, value in counts.items():
                value = tuple(value)
                if len(value) == 3:
                    poss[value].append(key)
                    if value in poss and len(poss[value]) == 3:
                        found = True
                        p.del_notes(vals=poss[value], boxes=[(row, col)], save=value)
                        p.del_notes_cell(poss=value, save_vals=poss[value])
    return found


def find_hidden_quadruples(p):
    def def_val():
        return []

    found = False
    # Row
    for row_num in range(p.cell_dim[0]):
        row = p.get_row(row_num)
        counts = defaultdict(def_val)
        for col_num, cell in enumerate(row):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(def_val)
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 4:
                poss[value].append(key)
                if value in poss and len(poss[value]) == 4:
                    found = True
                    p.del_notes(vals=poss[value], rows=[row_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=poss[value])
    # Col
    for col_num in range(p.cell_dim[1]):
        col = p.get_col(col_num)
        counts = defaultdict(def_val)
        for row_num, cell in enumerate(col):
            notes = tuple(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(def_val)
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == 4:
                poss[value].append(key)
                if value in poss and len(poss[value]) == 4:
                    found = True
                    p.del_notes(vals=poss[value], cols=[col_num], save=value)
                    p.del_notes_cell(poss=value, save_vals=poss[value])
    # # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                for val in notes:
                    counts[val].append(cell.pos)
            poss = defaultdict(def_val)
            for key, value in counts.items():
                value = tuple(value)
                if len(value) == 4:
                    poss[value].append(key)
                    if value in poss and len(poss[value]) == 4:
                        found = True
                        p.del_notes(vals=poss[value], boxes=[(row, col)], save=value)
                        p.del_notes_cell(poss=value, save_vals=poss[value])
    return found


############################################################################
# OTHER
def find_inline(p):
    def def_val():
        return []

    found = False
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(def_val)
            for cell in box:
                notes = tuple(cell.notes)
                for val in notes:
                    counts[val].append(cell.pos)
            poss = defaultdict(def_val)
            for key, value in counts.items():
                if len(value) == 2:
                    if value[0][0] == value[1][0]:
                        found = True
                        p.del_notes(vals=[key], rows=[value[0][0]], save=value)
                    elif value[0][1] == value[1][1]:
                        found = True
                        p.del_notes(vals=[key], cols=[value[0][1]], save=value)
                if len(value) == 3:
                    if value[0][0] == value[1][0] == value[2][0]:
                        found = True
                        p.del_notes(vals=[key], rows=[value[0][0]], save=value)
                    elif value[0][1] == value[1][1] == value[2][1]:
                        found = True
                        p.del_notes(vals=[key], cols=[value[0][1]], save=value)
    return found


def find_xwing(p):
    return


def nishio(p):
    return
