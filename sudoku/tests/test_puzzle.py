from sudoku.puzzle import Cell, Puzzle_Backend
from pytest import fixture


# Cell
@fixture
def basic_cell():
    return Cell(pos=(0, 0), box=0)


def testCellNotesChangeAfterSettingValue(basic_cell):
    assert basic_cell.notes == {1, 2, 3, 4, 5, 6, 7, 8, 9}
    basic_cell.val = 1
    assert basic_cell.notes == {1}


def testCellPrivateValueIsChangedAfterSettingValue(basic_cell):
    basic_cell.val = 1
    assert basic_cell._val == 1


def testCellReturnsValueWhenCastToInt(basic_cell):
    assert int(basic_cell.val) == 0


# Puzzle_Backend
@fixture
def empty_puzzle():
    return Puzzle_Backend()


def testPuzzleBackendSetItemChangesCellCorrectly(empty_puzzle):
    empty_puzzle[0, 0] = 1
    assert id(empty_puzzle.rows[0][0]) == id(empty_puzzle[0, 0])
    assert empty_puzzle.rows[0][0].val == empty_puzzle[0, 0].val
    assert empty_puzzle.rows[0][0].notes == empty_puzzle[0, 0].notes
