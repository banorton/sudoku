from sudoku.puzzle import Cell


def testCellNotesChangeAfterSettingValue():
    c = Cell(pos=(0, 0), box=0)
    assert c.notes == {1, 2, 3, 4, 5, 6, 7, 8, 9}
    c.val = 1
    assert c.notes == {1}


def testCellPrivateValueIsChangedAfterSettingValue():
    c = Cell(pos=(0, 0), box=0)
    c.val = 1
    assert c._val == 1


def testCellReturnsValueWhenCastToInt():
    c = Cell(pos=(0, 0), box=0)
    assert int(c.val) == 0
