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


def std_solve(p) -> bool:
    if not is_valid(p):
        print("Not a valid puzzle.")
    if not p.cells_unsolved:
        print("SOLVED")
        return True

    ct = 0
    while ct < 10:
        find_naked_singles(p)
        find_hidden_singles(p)
        find_inline(p)
        find_naked_doubles(p)
        find_hidden_doubles(p)
        find_naked_triples(p)
        find_hidden_triples(p)
        find_naked_quadruples(p)
        find_hidden_quadruples(p)
        if not p.cells_unsolved:
            return True
        ct += 1
    return False


def nishio(p):
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
                print(changes)
                solved = std_solve(p)
                if solved:
                    print(
                        "######################################################################"
                    )
                    return
                else:
                    nishio(p)
            except:
                print(f"NISHIO METHOD BRANCH FAIL\n")
                p.copy(puzzle_snapshot)
                p.update_cell(p[cell.pos].pos, vals[1])
                changes = "######################################################################\n"
                changes += f"NISHIO METHOD\nUpdate Cell: {cell.pos}, {vals[1]}\n"
                print(changes)
                solved = std_solve(p)
                if solved:
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
        for row in p.cells:
            for cell in row:
                if cell.val != 0:
                    continue
                col = p.cells.T[cell.pos[1]]
                box = p.get_box(cell.box_pos).flatten()

                row_notes, col_notes, box_notes = (
                    defaultdict(lambda: 0),
                    defaultdict(lambda: 0),
                    defaultdict(lambda: 0),
                )
                for rcell, ccell, bcell in zip(row, col, box):
                    for r in rcell.notes:
                        row_notes[r] += 1
                    for c in ccell.notes:
                        col_notes[c] += 1
                    for b in bcell.notes:
                        box_notes[b] += 1

                for val in cell.notes:
                    if row_notes[val] == 1:
                        p.update_cell(cell.pos, val)
                        changes += f"Update Cell: {cell.pos}, {val}\n"
                    elif col_notes[val] == 1:
                        p.update_cell(cell.pos, val)
                        changes += f"Update Cell: {cell.pos}, {val}\n"
                    elif box_notes[val] == 1:
                        p.update_cell(cell.pos, val)
                        changes += f"Update Cell: {cell.pos}, {val}\n"
        return changes

    changes = ""
    changes_cells = ""
    # Row
    for row_num in range(p.cell_dim[0]):
        row = p.get_row(row_num)
        counts = defaultdict(lambda: [])
        for col_num, cell in enumerate(row):
            notes = tuple(sorted(cell.notes))
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(lambda: [])
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == num:
                poss[value].append(key)
                if value in poss and len(poss[value]) == num:
                    if value in p.checked[num]:
                        continue
                    else:
                        p.checked[num][value].append(key)
                    p.del_notes(vals=poss[value], rows=[row_num], save=value)
                    changes += (
                        f"Del Notes: row {row_num}, vals {poss[value]}, save {value}\n"
                    )
                    p.del_notes_cell(poss=value, save_vals=poss[value])
                    changes_cells += f"Del Notes: cells {value}, save {poss[value]}\n"
    # Col
    for col_num in range(p.cell_dim[1]):
        col = p.get_col(col_num)
        counts = defaultdict(lambda: [])
        for row_num, cell in enumerate(col):
            notes = tuple(sorted(cell.notes))
            for val in notes:
                counts[val].append(cell.pos)
        poss = defaultdict(lambda: [])
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == num:
                poss[value].append(key)
                if value in poss and len(poss[value]) == num:
                    if value in p.checked[num]:
                        continue
                    else:
                        p.checked[num][value].append(key)
                    p.del_notes(vals=poss[value], cols=[col_num], save=value)
                    changes += (
                        f"Del Notes: col {col_num}, vals {poss[value]}, save {value}\n"
                    )
                    p.del_notes_cell(poss=value, save_vals=poss[value])
                    changes_cells += f"Del Notes: cells {value}, save {poss[value]}\n"
    # Box
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(lambda: [])
            for cell in box:
                notes = tuple(sorted(cell.notes))
                for val in notes:
                    counts[val].append(cell.pos)
            poss = defaultdict(lambda: [])
            for key, value in counts.items():
                value = tuple(value)
                if len(value) == num:
                    poss[value].append(key)
                    if value in poss and len(poss[value]) == num:
                        if value in p.checked[num]:
                            continue
                        else:
                            p.checked[num][value].append(key)
                        p.del_notes(vals=poss[value], boxes=[(row, col)], save=value)
                        changes += f"Del Notes: box {(row, col)}, vals {poss[value]}, save {value}\n"
                        p.del_notes_cell(poss=value, save_vals=poss[value])
                        changes_cells += (
                            f"Del Notes: cells {value}, save {poss[value]}\n"
                        )
    return changes + changes_cells


############################################################################
# NAKED
def find_naked_singles(p, prnt=True):
    changes = find_naked_general(p, 1)
    if prnt and changes:
        print("NAKED SINGLES")
        print(changes)
    return changes


def find_naked_doubles(p, prnt=True):
    changes = find_naked_general(p, 2)
    if prnt and changes:
        print("NAKED DOUBLES")
        print(changes)
    return changes


def find_naked_triples(p, prnt=True):
    changes = find_naked_general(p, 3)
    if prnt and changes:
        print("NAKED TRIPLES")
        print(changes)
    return changes


def find_naked_quadruples(p, prnt=True):
    changes = find_naked_general(p, 4)
    if prnt and changes:
        print("NAKED QUADRUPLES")
        print(changes)
    return changes


############################################################################
# HIDDEN
def find_hidden_singles(p, prnt=True):
    changes = find_hidden_general(p, 1)
    if prnt and changes:
        print("HIDDEN SINGLES")
        print(changes)
    return changes


def find_hidden_doubles(p, prnt=True):
    changes = find_hidden_general(p, 2)
    if prnt and changes:
        print("HIDDEN DOUBLES")
        print(changes)
    return changes


def find_hidden_triples(p, prnt=True):
    changes = find_hidden_general(p, 3)
    if prnt and changes:
        print("HIDDEN TRIPLES")
        print(changes)
    return changes


def find_hidden_quadruples(p, prnt=True):
    changes = find_hidden_general(p, 4)
    if prnt and changes:
        print("HIDDEN QUADRUPLES")
        print(changes)
    return changes


############################################################################
# OTHER
def find_inline(p, prnt=True):
    changes = ""
    for row in range(p.puzzle_dim[0]):
        for col in range(p.puzzle_dim[1]):
            box, counts = p.boxes[row, col].flatten(), defaultdict(lambda: [])
            for cell in box:
                notes = tuple(sorted(cell.notes))
                for val in notes:
                    counts[val].append(cell.pos)
            poss = defaultdict(lambda: [])
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
    return changes


def find_xwing(p):
    return
