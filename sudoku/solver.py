import numpy as np
from collections import defaultdict
from copy import deepcopy as dcopy


def is_valid(p):
    # Count the occurrence of values in every row, column, and box.
    rcounts = [[0 for _ in range(10)] for _ in range(9)]
    ccounts = [[0 for _ in range(10)] for _ in range(9)]
    bcounts = [[0 for _ in range(10)] for _ in range(9)]
    for cell in p.cells:
        (r, c), b = cell.pos, cell.box
        if len(cell.notes) == 0:
            return (False, f"Cell {cell.pos}")
        rcounts[r][cell.val] += 1
        ccounts[c][cell.val] += 1
        bcounts[b][cell.val] += 1

    # Check every row, column, and box for duplicate values.
    for rct, cct, bct in zip(rcounts, ccounts, bcounts):
        for rnum, cnum, bnum in zip(rct[1:], cct[1:], bct[1:]):
            if rnum > 1:
                return (False, f"Row {rnum}")
            if cnum > 1:
                return (False, f"Col {cnum}")
            if bnum > 1:
                return (False, f"Box {bnum}")

    # Return True if the puzzle is valid.
    return True, ""


def std_solve(p):
    if not is_valid(p):
        print("Not a valid puzzle.")

    # fmt:off
    ct = 0
    while ct < 10:
        diffs = ""
        header = f"______________________________________________________________________"
        # Look for increasingly more difficult clues to find.
        diffs += find_naked_general(p, 1)
        diffs += find_hidden_general(p, 1)
        diffs += find_inline(p)
        diffs += find_naked_general(p, 2)
        diffs += find_hidden_general(p, 2)
        diffs += find_naked_general(p, 3)
        diffs += find_hidden_general(p, 3)
        diffs += find_naked_general(p, 4)
        diffs += find_hidden_general(p, 4)
        footer = f"cells unsolved: {p.unsolved}\n______________________________________________________________________\n"
        if not diffs:
            ct += 1
            continue
        else:
            diffs = header + diffs + footer
            print(diffs)

        # Check if the puzzle is solved.
        if not p.unsolved:
            return True
        ct += 1
    # fmt:on
    return False


def nishio(p, n=2):
    # Check if all of the cells have been solved.
    if not p.unsolved:
        return
    for cell in p.cells:
        if not p.unsolved:
            return
        # If there is a naked double in the puzzle, test each value. Call nishio again if solving stalls.
        solved = False
        if len(cell.notes) == n:
            vals = list(cell.notes)
            puzzle_snapshot = dcopy(p)
            try:
                print(
                    "######################## NISHIO - BRANCH 1 ###########################"
                )
                p[cell.pos] = vals[0]
                solved = std_solve(p)
                if solved:
                    return
                else:
                    nishio(p)
            except:
                print(
                    "######################## NISHIO - BRANCH 2 ##########################"
                )
                p.copy(puzzle_snapshot)
                p[cell.pos] = vals[1]
                solved = std_solve(p)
                if solved:
                    return
                else:
                    nishio(p)


def find_naked_general(p, n):
    """
    For a given number (num), if exactly num amount of cells, in a row or column or box, contain exactly num amount of notes and those notes are equal, eliminate those values from the notes of the other cells in the respective row, column, or box.

    Example:
    While checking row 3 with num=2, cells at positions (3,3) and (3,7) are found to have only the 2 notes {4,8}; Notes 4 and 8 will be removed from all other cells in row 3. If the cell at position (3,0) had the notes {1,3,4,7,8}, afterwards it would have the notes {1,3,7}.
    """
    assert n > 0
    if n == 1:
        diffs = ""
        for cell in p.cells:
            if (len(cell.notes) == 1) and (cell.val == 0):
                [note] = cell.notes
                p[cell.pos] = note
                diffs += f"Update Cell: {cell.pos}, {note}\n"
        return "" if not diffs else "\nNAKED n=1\n" + diffs + "\n"

    diffs = ""
    # Row
    for rnum, row in enumerate(p.rows):
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
    for cnum, col in enumerate(p.cols):
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
    for bnum, box in enumerate(p.boxs):
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
    return "" if not diffs else f"\nNAKED n={n}\n" + diffs + "\n"


def find_hidden_general(p, n):
    """
    For a given number (num), if exactly num amount of cells, in a row or column or box, contain more than num amount of notes but share the same num amount of notes, eliminate all but the shared notes in those cells. Eliminate the shared notes from the notes in other cells in the respective row, column, or box.

    Example:
    While checking row 3 with num=2, cells only at positions (3,3) and (3,7) are found to have more than 2 notes, {1,3,4,6,8} and {2,4,7,8}, but share notes 4 and 8; Notes 4 and 8 will be removed from all other notes in the cells of row 3. All notes exluding 4 and 8, for the cells at positions (3,3) and (3,7), will be removed.
    """
    assert n > 0
    if n == 1:
        diffs = ""
        for cell in p.cells:
            if cell.val == 0:
                rnotes, cnotes, bnotes = [], [], []
                (rnum, cnum), bnum = cell.pos, cell.box
                [rnotes.extend(list(rcell.notes)) for rcell in p.rows[rnum]]
                [cnotes.extend(list(ccell.notes)) for ccell in p.cols[cnum]]
                [bnotes.extend(list(bcell.notes)) for bcell in p.boxs[bnum]]
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
        return "" if not diffs else "\nHIDDEN n=1\n" + diffs + "\n"

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
                        if bnum == 1 and n == 2:
                            print()
                        p.checked[n][value].append(key)
                        p.del_notes(val=posns[value], box=[bnum], save=value)
                        diffs1 += f"del notes: box {bnum}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        diffs2 += f"del notes: cells {value}, save {posns[value]}\n"
    return "" if not (diffs1 + diffs2) else f"\nHIDDEN n={n}\n" + diffs1 + diffs2 + "\n"


def find_inline(p):
    diffs = ""
    for box in p.boxs:
        counts = defaultdict(lambda: [])
        for cell in box:
            notes = tuple(sorted(cell.notes))
            for val in notes:
                counts[val].append(cell.pos)
        for key, value in counts.items():
            if len(value) == 2:
                v00, v10 = value[0][0], value[1][0]
                v01, v11 = value[0][1], value[1][1]
                inlinehash1 = (tuple(value), v00, v10, "inline")
                inlinehash2 = (tuple(value), v01, v11, "inline")
                if v00 == v10 and inlinehash1 not in p.checked:
                    p.del_notes(val=[key], row=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                    p.checked[inlinehash1] = True
                elif v01 == v11 and inlinehash2 not in p.checked:
                    p.del_notes(val=[key], col=[v01], save=value)
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
                    p.checked[inlinehash2] = True
            if len(value) == 3:
                v00, v10, v20 = value[0][0], value[1][0], value[2][0]
                v01, v11, v21 = value[0][1], value[1][1], value[2][1]
                inlinehash1 = (tuple(value), v00, v10, v20, "inline")
                inlinehash2 = (tuple(value), v01, v11, v21, "inline")
                if v00 == v10 == v20 and inlinehash1 not in p.checked:
                    p.del_notes(val=[key], row=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                    p.checked[inlinehash1] = True
                elif v01 == v11 == v21 and inlinehash2 not in p.checked:
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
                    p.checked[inlinehash2] = True
    return "" if not diffs else "\nINLINE\n" + diffs + "\n"
