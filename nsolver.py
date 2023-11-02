import numpy as np
from collections import defaultdict
from copy import deepcopy as dcopy


def is_valid(p) -> bool:
    # Check boxs for duplicates.
    for box in p.box:
        box = np.array([int(cell) for cell in box])
        box = np.delete(box, np.where(box == 0))
        if box.size > np.unique(box).size:
            return False

    # Check rows for duplicates.
    for row in p.row:
        row = np.array([int(cell) for cell in row])
        row = np.delete(row, np.where(row == 0))
        if row.size > np.unique(row).size:
            return False

    # Check columns for duplicates.
    for col in p.col:
        col = np.array([int(cell) for cell in col])
        col = np.delete(col, np.where(col == 0))
        if col.size > np.unique(col).size:
            return False

    # Return True if the puzzle is valid.
    return True


def std_solve(p):
    if not is_valid(p):
        print("Not a valid puzzle.")
    if not p.unsolved:
        print("SOLVED")
        return True

    ct = 0
    while ct < 10:
        # Look for increasingly more difficult clues to find.
        print(find_naked_general(p, 1), end="")
        print(find_naked_general(p, 2), end="")
        print(find_naked_general(p, 3), end="")
        print(find_naked_general(p, 4), end="")
        print(p.unsolved, end="\n\n")

        # Check if all of the cells have been solved.
        if not p.unsolved:
            return True
        ct += 1
    return False


def find_naked_general(p, n):
    assert n > 0
    if n == 1:
        diffs = ""
        for cell in p.cells:
            if (len(cell.notes) == 1) and (cell.val == 0):
                [note] = cell.notes
                p[cell.pos] = note
                diffs += f"Update Cell: {cell.pos}, {note}\n"
        return diffs

    diffs = ""
    # Row
    for rnum, row in enumerate(p.row):
        checks = defaultdict(lambda: [])
        for cell in row:
            notes = tuple(sorted(cell.notes))
            if len(notes) == n:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[n]) and (len(posns) == n):
                    p.checked[n][posns].extend(notes)
                    p.del_notes(val=notes, row=rnum, save=posns)
                    diffs += f"del notes: row {rnum}, vals {notes}, save {posns}\n"
    # Col
    for cnum, col in enumerate(p.col):
        checks = defaultdict(lambda: [])
        for cell in col:
            notes = tuple(sorted(cell.notes))
            if len(notes) == n:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[n]) and (len(posns) == n):
                    p.checked[n][posns].extend(notes)
                    p.del_notes(val=notes, col=cnum, save=posns)
                    diffs += f"del notes: col {cnum}, vals {notes}, save {posns}\n"
    # Box
    for bnum, box in enumerate(p.box):
        checks = defaultdict(lambda: [])
        for cell in box:
            notes = tuple(sorted(cell.notes))
            if len(notes) == n:
                checks[notes].append(cell.pos)
                posns = tuple(checks[notes])
                if (posns not in p.checked[n]) and (len(posns) == n):
                    p.checked[n][posns].extend(notes)
                    p.del_notes(val=notes, box=bnum, save=posns)
                    diffs += f"del notes: box {bnum}, vals {notes}, save {posns}\n"
    return diffs


def find_inline(p):
    diffs = ""
    for box in p.box:
        counts = defaultdict(lambda: [])
        for cell in box:
            notes = tuple(sorted(cell.notes))
            for val in notes:
                counts[val].append(cell.pos)
        for key, value in counts.items():
            if len(value) == 2:
                v00, v10 = value[0][0], value[1][0]
                v01, v11 = value[0][1], value[1][1]
                if v00 == v10:
                    p.del_notes(vals=[key], rows=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                elif v01 == v11:
                    p.del_notes(vals=[key], cols=[v01], save=value)
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
            if len(value) == 3:
                v00, v10, v20 = value[0][0], value[1][0], value[2][0]
                v01, v11, v21 = value[0][1], value[1][1], value[2][1]
                if v00 == v10 == v20:
                    p.del_notes(vals=[key], rows=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                elif v01 == v11 == v21:
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
    return diffs
