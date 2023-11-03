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

    ct = 0
    while ct < 10:
        diffs = ""
        # Look for increasingly more difficult clues to find.
        diffs += find_naked_general(p, 1)
        diffs += find_hidden_general(p, 1)
        diffs += find_inline(p)
        diffs += find_naked_general(p, 2)
        diffs += find_hidden_general(p, 2)
        diffs += find_hidden_general(p, 3)
        diffs += f"{p.unsolved}\n\n"
        print(diffs[:-1])

        # Check if the puzzle is solved.
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


def find_hidden_general(p, n):
    assert n > 0
    if n == 1:
        diffs = ""
        for cell in p.cells:
            if cell.val == 0:
                rnotes, cnotes, bnotes = [], [], []
                (rnum, cnum), bnum = cell.pos, cell.box
                [rnotes.extend(list(rcell.notes)) for rcell in p.row[rnum]]
                [cnotes.extend(list(ccell.notes)) for ccell in p.col[cnum]]
                [bnotes.extend(list(bcell.notes)) for bcell in p.box[bnum]]
                for val in cell.notes:
                    if bnotes.count(val) == 1:
                        p[cell.pos] = val
                        diffs += f"Update Cell: {cell.pos}, {val}\n"
                    elif rnotes.count(val) == 1:
                        p[cell.pos] = val
                        diffs += f"Update Cell: {cell.pos}, {val}\n"
                    elif cnotes.count(val) == 1:
                        p[cell.pos] = val
                        diffs += f"Update Cell: {cell.pos}, {val}\n"
        return diffs

    diffs1, diffs2 = "", ""
    rcounts = [defaultdict(lambda: []) for _ in range(9)]
    ccounts = [defaultdict(lambda: []) for _ in range(9)]
    bcounts = [defaultdict(lambda: []) for _ in range(9)]
    for cell in p.cells:
        (r, c), b = cell.pos, cell.box
        notes = sorted(cell.notes)
        for val in notes:
            rcounts[r][val].append(cell.pos)
            ccounts[c][val].append(cell.pos)
            bcounts[b][val].append(cell.pos)

    posns = defaultdict(lambda: [])
    for rnum, counts in enumerate(rcounts):
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == n:
                posns[value].append(key)
                if value in posns and len(posns[value]) == n:
                    if not (value in p.checked[n]):
                        p.checked[n][value].append(key)
                        p.del_notes(val=posns[value], row=[rnum], save=value)
                        diffs1 += f"del notes: row {rnum}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        diffs2 += f"del notes: cells {value}, save {posns[value]}\n"
    posns = defaultdict(lambda: [])
    for cnum, counts in enumerate(ccounts):
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == n:
                posns[value].append(key)
                if value in posns and len(posns[value]) == n:
                    if not (value in p.checked[n]):
                        p.checked[n][value].append(key)
                        p.del_notes(val=posns[value], col=[cnum], save=value)
                        diffs1 += f"del notes: col {cnum}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        diffs2 += f"del notes: cells {value}, save {posns[value]}\n"
    posns = defaultdict(lambda: [])
    for bnum, counts in enumerate(bcounts):
        for key, value in counts.items():
            value = tuple(value)
            if len(value) == n:
                posns[value].append(key)
                if value in posns and len(posns[value]) == n:
                    if not (value in p.checked[n]):
                        p.checked[n][value].append(key)
                        p.del_notes(val=posns[value], box=[bnum], save=value)
                        diffs1 += f"del notes: box {bnum}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        diffs2 += f"del notes: cells {value}, save {posns[value]}\n"

    return diffs1 + diffs2


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
                    p.del_notes(val=[key], row=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                elif v01 == v11:
                    p.del_notes(val=[key], col=[v01], save=value)
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
            if len(value) == 3:
                v00, v10, v20 = value[0][0], value[1][0], value[2][0]
                v01, v11, v21 = value[0][1], value[1][1], value[2][1]
                if v00 == v10 == v20:
                    p.del_notes(val=[key], row=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                elif v01 == v11 == v21:
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
    return diffs
