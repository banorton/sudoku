from collections import defaultdict
from copy import deepcopy as dcopy


def is_valid(p):
    """Checks if the current state of the puzzle is valid (i.e. no duplicate values in any row, column, or box).

    Args:
        p (Puzzle_Backend): The puzzle that will be checked.

    Returns:
        bool: True if valid, False if invalid.
    """

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
    """This is the "standard solve". It looks for increasingly difficult clues and solves the puzzle in a similiar manner to a human.

    Args:
        p (Puzzle_Backend): The puzzle to be solved.

    Returns:
        bool: True if the puzzle is solved, False if the puzzle is not solved
    """

    if not is_valid(p):
        print("Not a valid puzzle.")

    # fmt:off
    ct = 0
    while ct < 10:
        diffs = ""
        header = f"______________________________________________________________________"
        # Look for increasingly more difficult clues to find.
        diffs += find_naked_clues(p, 1)
        diffs += find_hidden_clues(p, 1)
        diffs += find_inline(p)
        diffs += find_naked_clues(p, 2)
        diffs += find_hidden_clues(p, 2)
        diffs += find_naked_clues(p, 3)
        diffs += find_hidden_clues(p, 3)
        diffs += find_naked_clues(p, 4)
        diffs += find_hidden_clues(p, 4)
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
    """Implementation of the Nishio method for solving a Sudoku puzzle. Essentially guess and check. If a naked clue is found with n values, branch.

    Args:
        p (Puzzle_Backend): The puzzle to be solved.
        n (int): Branch number. Defaults to 2.
    """

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


def find_naked_clues(p, n):
    """Eliminates values from the notes of the other cells in a given row, column, or box if exactly n amount of cells in a row, column or box contain exactly n amount of notes and those notes are equal.

    Args:
        p (Puzzle_Backend): Puzzle in which clues will be looked for.
        n (int): Amount of cells and clues to look for.

    Returns:
        str: A string containing the description of the changes that were made to the puzzle.
    """

    assert n > 0 and n < 9
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
                    p.del_notes(vals=notes, rows=rnum, save=posns)
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
                    p.del_notes(vals=notes, cols=cnum, save=posns)
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
                    p.del_notes(vals=notes, boxs=bnum, save=posns)
                    diffs += f"del notes: box {bnum}, vals {notes}, save {posns}\n"
    return "" if not diffs else f"\nNAKED n={n}\n" + diffs + "\n"


def find_hidden_clues(p, n):
    """If exactly n amount of cells in a row, column, or box contain more than n amount of notes but share the same n amount of notes, eliminate all but the shared notes in those cells. Also, eliminate the shared notes from the notes in other cells in the given row, column, or box.

    Args:
        p (Puzzle_Backend): Puzzle in which clues will be looked for.
        n (int): Amount of cells and clues to look for.

    Returns:
        str: A string containing the description of the changes that were made to the puzzle.
    """

    assert n > 0 and n < 9
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
                        p.del_notes(vals=posns[value], rows=[rnum], save=value)
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
                        p.del_notes(vals=posns[value], cols=[cnum], save=value)
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
                        p.del_notes(vals=posns[value], boxs=[bnum], save=value)
                        diffs1 += f"del notes: box {bnum}, vals {posns[value]}, save {value}\n"
                        p.del_notes_cell(posns=value, save_vals=posns[value])
                        diffs2 += f"del notes: cells {value}, save {posns[value]}\n"
    return "" if not (diffs1 + diffs2) else f"\nHIDDEN n={n}\n" + diffs1 + diffs2 + "\n"


def find_inline(p):
    """Finds cells that share a note that are in the same box and row or box and column. Then the function eliminates that value from the rest of the respective row or column.

    Args:
        p (Puzzle_Backend): Puzzle in which clues will be looked for.

    Returns:
        str: A string containing the description of the changes that were made to the puzzle.
    """

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
                    p.del_notes(vals=[key], rows=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                    p.checked[inlinehash1] = True
                elif v01 == v11 and inlinehash2 not in p.checked:
                    p.del_notes(vals=[key], cols=[v01], save=value)
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
                    p.checked[inlinehash2] = True
            if len(value) == 3:
                v00, v10, v20 = value[0][0], value[1][0], value[2][0]
                v01, v11, v21 = value[0][1], value[1][1], value[2][1]
                inlinehash1 = (tuple(value), v00, v10, v20, "inline")
                inlinehash2 = (tuple(value), v01, v11, v21, "inline")
                if v00 == v10 == v20 and inlinehash1 not in p.checked:
                    p.del_notes(vals=[key], rows=[v00], save=value)
                    diffs += f"del notes: row {v00}, val {[key]}, save {value}\n"
                    p.checked[inlinehash1] = True
                elif v01 == v11 == v21 and inlinehash2 not in p.checked:
                    diffs += f"del notes: col {v01}, val {[key]}, save {value}\n"
                    p.checked[inlinehash2] = True
    return "" if not diffs else "\nINLINE\n" + diffs + "\n"
