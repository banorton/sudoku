import numpy as np
from .helpers import *
from collections import defaultdict
from copy import deepcopy as dcopy


def is_valid(p) -> bool:
    # Check boxs for duplicates.
    for box in p.boxes.flatten():
        box = box.np.flatten()
        box = np.delete(box, np.where(box == 0))
        if box.size > np.unique(box).size:
            return False

    # Check rows for duplicates.
    for row in p.cells.np:
        row = np.delete(row, np.where(row == 0))
        if row.size > np.unique(row).size:
            return False

    # Check columns for duplicates.
    for col in p.cells.np.T:
        col = np.delete(col, np.where(col == 0))
        if col.size > np.unique(col).size:
            return False

    # Return True if the board state is valid.
    return True


def std_solve(p, prnt=False) -> bool:
    if not is_valid(p):
        print("Not a valid puzzle.")
    if not p.cells_unsolved and prnt:
        print("SOLVED")
        return True

    ct = 0
    while ct < 10:
        find_naked_singles(p, prnt)
        find_hidden_singles(p, prnt)
        find_inline(p, prnt)
        find_naked_doubles(p, prnt)
        find_hidden_doubles(p, prnt)
        find_naked_triples(p, prnt)
        find_hidden_triples(p, prnt)
        find_naked_quadruples(p, prnt)
        find_hidden_quadruples(p, prnt)
        if not p.cells_unsolved:
            return True
        ct += 1
    return False


def nishio(p, prnt=False):
    for cell in p.cells.flatten():
        if not p.cells_unsolved:
            return
        solved = False
        if len(cell.notes) == 2:
            vals = list(cell.notes)
            puzzle_snapshot = dcopy(p)
            try:
                p.update_cell(cell.pos, vals[0])
                changes = "######################################################################\n"
                changes += f"NISHIO METHOD\nUpdate Cell: {cell.pos}, {vals[0]}\n"
                if prnt:
                    print(changes)
                solved = std_solve(p)
                if solved:
                    if prnt:
                        print(
                            "######################################################################"
                        )
                    return
                else:
                    nishio(p)
            except:
                if prnt:
                    print(f"NISHIO METHOD BRANCH FAIL\n")
                p.copy(puzzle_snapshot)
                p.update_cell(p[cell.pos].pos, vals[1])
                changes = "######################################################################\n"
                changes += f"NISHIO METHOD\nUpdate Cell: {cell.pos}, {vals[1]}\n"
                if prnt:
                    print(changes)
                solved = std_solve(p)
                if solved:
                    if prnt:
                        print(
                            "######################################################################"
                        )
                    return
                else:
                    nishio(p)


############################################################################
# GENERALIZED
def find_naked_general(p, num):
    assert num > 0
    if num == 1:
        changes = ""
        for cell in p.cells.flatten():
            if (len(cell.notes) == 1) and (cell.val == 0):
                [note] = cell.notes
                p.update_cell(cell.pos, note)
                changes += f"Update Cell: {cell.pos}, {note}\n"
        return changes

    changes = ""
    # Row
    for row_num, row in enumerate(p.cells):
        checks = defaultdict(lambda: [])
        for cell in row:
            notes = tuple(sorted(cell.notes))
            if len(notes) == num:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[num]) and (len(posns) == num):
                    p.checked[num][posns].extend(notes)
                    p.del_notes(vals=notes, rows=[row_num], save=posns)
                    changes += f"Del Notes: row {row_num}, vals {notes}, save {posns}\n"
    # Col
    for col_num, col in enumerate(p.cells.T):
        checks = defaultdict(lambda: [])
        for cell in col:
            notes = tuple(sorted(cell.notes))
            if len(notes) == num:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[num]) and (len(posns) == num):
                    p.checked[num][posns].extend(notes)
                    p.del_notes(vals=notes, cols=[col_num], save=posns)
                    changes += f"Del Notes: col {col_num}, vals {notes}, save {posns}\n"
    # Box
    for box in p.boxes.flatten():
        checks = defaultdict(lambda: [])
        for cell in box.flatten():
            notes = tuple(sorted(cell.notes))
            if len(notes) == num:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[num]) and (len(posns) == num):
                    p.checked[num][posns].extend(notes)
                    p.del_notes(vals=notes, boxes=[box.pos], save=posns)
                    changes += f"Del Notes: box {box.pos}, vals {notes}, save {posns}\n"
    return changes


def find_hidden_general(p, num):
    assert num > 0
    if num == 1:
        changes = ""
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
                        changes += f"Update Cell: {pos}, {val}\n"
                    elif row_notes.count(val) == 1:
                        p.update_cell(pos, val)
                        changes += f"Update Cell: {pos}, {val}\n"
                    elif col_notes.count(val) == 1:
                        p.update_cell(pos, val)
                        changes += f"Update Cell: {pos}, {val}\n"
        return changes

    changes, changes_cells = "", ""
    # Row
    for row_num, row in enumerate(p.cells):
        counts = defaultdict(lambda: [])
        for cell in row:
            notes = sorted(cell.notes)
            for val in notes:
                counts[val].append(cell.pos)
        posns = defaultdict(lambda: [])
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == num:
                posns[value].append(key)
                if value in posns and len(posns[value]) == num:
                    if value in p.checked[num]:
                        continue
                    else:
                        p.checked[num][value].append(key)
                    p.del_notes(vals=posns[value], rows=[row_num], save=value)
                    changes += (
                        f"Del Notes: row {row_num}, vals {posns[value]}, save {value}\n"
                    )
                    p.del_notes_cell(posns=value, save_vals=posns[value])
                    changes_cells += f"Del Notes: cells {value}, save {posns[value]}\n"
    # Col
    for col_num in range(p.cell_dim[1]):
        col = p.get_col(col_num)
        counts = defaultdict(lambda: [])
        for row_num, cell in enumerate(col):
            notes = tuple(sorted(cell.notes))
            for val in notes:
                counts[val].append(cell.pos)
        posns = defaultdict(lambda: [])
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == num:
                posns[value].append(key)
                if value in posns and len(posns[value]) == num:
                    if value in p.checked[num]:
                        continue
                    else:
                        p.checked[num][value].append(key)
                    p.del_notes(vals=posns[value], cols=[col_num], save=value)
                    changes += (
                        f"Del Notes: col {col_num}, vals {posns[value]}, save {value}\n"
                    )
                    p.del_notes_cell(posns=value, save_vals=posns[value])
                    changes_cells += f"Del Notes: cells {value}, save {posns[value]}\n"
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(lambda: [])
            for cell in box:
                notes = tuple(sorted(cell.notes))
                for val in notes:
                    counts[val].append(cell.pos)
            posns = defaultdict(lambda: [])
            for key, value in counts.items():
                value = tuple(value)
                if len(value) == num:
                    posns[value].append(key)
                    if value in posns and len(posns[value]) == num:
                        if value in p.checked[num]:
                            continue
                        else:
                            p.checked[num][value].append(key)
                        p.del_notes(vals=posns[value], boxes=[(row, col)], save=value)
                        changes += f"Del Notes: box {(row, col)}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        changes_cells += (
                            f"Del Notes: cells {value}, save {posns[value]}\n"
                        )
    return changes + changes_cells


############################################################################
# NAKED
def find_naked_singles(p, prnt=False):
    changes = find_naked_general(p, 1)
    if prnt and changes:
        print("NAKED SINGLES")
        print(changes)
    return changes


def find_naked_doubles(p, prnt=False):
    changes = find_naked_general(p, 2)
    if prnt and changes:
        print("NAKED DOUBLES")
        print(changes)
    return changes


def find_naked_triples(p, prnt=False):
    changes = find_naked_general(p, 3)
    if prnt and changes:
        print("NAKED TRIPLES")
        print(changes)
    return changes


def find_naked_quadruples(p, prnt=False):
    changes = find_naked_general(p, 4)
    if prnt and changes:
        print("NAKED QUADRUPLES")
        print(changes)
    return changes


############################################################################
# HIDDEN
def find_hidden_singles(p, prnt=False):
    changes = find_hidden_general(p, 1)
    if prnt and changes:
        print("HIDDEN SINGLES")
        print(changes)
    return changes


def find_hidden_doubles(p, prnt=False):
    changes = find_hidden_general(p, 2)
    if prnt and changes:
        print("HIDDEN DOUBLES")
        print(changes)
    return changes


def find_hidden_triples(p, prnt=False):
    changes = find_hidden_general(p, 3)
    if prnt and changes:
        print("HIDDEN TRIPLES")
        print(changes)
    return changes


def find_hidden_quadruples(p, prnt=False):
    changes = find_hidden_general(p, 4)
    if prnt and changes:
        print("HIDDEN QUADRUPLES")
        print(changes)
    return changes


############################################################################
# OTHER
def find_inline(p, prnt=False):
    changes = ""
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(lambda: [])
            for cell in box:
                notes = tuple(sorted(cell.notes))
                for val in notes:
                    counts[val].append(cell.pos)
            for key, value in counts.items():
                if len(value) == 2:
                    if value[0][0] == value[1][0]:
                        p.del_notes(vals=[key], rows=[value[0][0]], save=value)
                        changes += (
                            f"Del Notes: row {value[0][0]}, val {[key]}, save {value}\n"
                        )
                    elif value[0][1] == value[1][1]:
                        p.del_notes(vals=[key], cols=[value[0][1]], save=value)
                        changes += (
                            f"Del Notes: col {value[0][1]}, val {[key]}, save {value}\n"
                        )
                if len(value) == 3:
                    if value[0][0] == value[1][0] == value[2][0]:
                        p.del_notes(vals=[key], rows=[value[0][0]], save=value)
                        changes += (
                            f"Del Notes: row {value[0][0]}, val {[key]}, save {value}\n"
                        )
                    elif value[0][1] == value[1][1] == value[2][1]:
                        changes += (
                            f"Del Notes: col {value[0][1]}, val {[key]}, save {value}\n"
                        )
    if prnt and changes:
        print("INLINE")
        print(changes)
    return changes


def find_xwing(p):
    return
