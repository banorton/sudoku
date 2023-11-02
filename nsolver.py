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


def find_naked_general(p, n):
    assert n > 0
    if n == 1:
        changes = ""
        for cell in p.cells:
            if (len(cell.notes) == 1) and (cell.val == 0):
                [note] = cell.notes
                p[cell.pos] = note
                changes += f"Update Cell: {cell.pos}, {note}\n"
        return changes

    changes = ""
    # # Row
    # for row_num, row in enumerate(p.cells):
    #     checks = defaultdict(lambda: [])
    #     for cell in row:
    #         notes = tuple(sorted(cell.notes))
    #         if len(notes) == n:
    #             checks[notes].append(cell.pos)
    #             posns = tuple(checks[notes])
    #             if (posns not in p.checked[n]) and (len(posns) == n):
    #                 p.checked[n][posns].extend(notes)
    #                 p.del_notes(vals=notes, rows=[row_num], save=posns)
    #                 changes += f"Del Notes: row {row_num}, vals {notes}, save {posns}\n"
    # # Col
    # for col_num, col in enumerate(p.cells.T):
    #     checks = defaultdict(lambda: [])
    #     for cell in col:
    #         notes = tuple(sorted(cell.notes))
    #         if len(notes) == n:
    #             checks[notes].append(cell.pos)
    #             posns = tuple(checks[notes])
    #             if (posns not in p.checked[n]) and (len(posns) == n):
    #                 p.checked[n][posns].extend(notes)
    #                 p.del_notes(vals=notes, cols=[col_num], save=posns)
    #                 changes += f"Del Notes: col {col_num}, vals {notes}, save {posns}\n"
    # # Box
    # for box in p.boxes.flatten():
    #     checks = defaultdict(lambda: [])
    #     for cell in box.flatten():
    #         notes = tuple(sorted(cell.notes))
    #         if len(notes) == n:
    #             checks[notes].append(cell.pos)
    #             posns = tuple(checks[notes])
    #             if (posns not in p.checked[n]) and (len(posns) == n):
    #                 p.checked[n][posns].extend(notes)
    #                 p.del_notes(vals=notes, boxes=[box.pos], save=posns)
    #                 changes += f"Del Notes: box {box.pos}, vals {notes}, save {posns}\n"
    return changes
