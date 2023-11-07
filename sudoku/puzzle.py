import numpy as np
from collections import defaultdict
from math import ceil
from sudoku.gui.gui import Puzzle_Frontend
from sudoku.solver import is_valid, std_solve, nishio


class Cell:
    """
    A class to hold the information for each cell in a Sudoku puzzle.

    ...

    Attributes
    ----------
    val : int
        the value of the cell if the cell is solved (0 if unsolved)
    notes : Set[int]
        the possible values for the cell
    pos : str
        the row and column in the puzzle the cell is located at
    box : int
        the number for the box in which the cell is located (0-8)
    """

    def __init__(self, val=0, pos=None, box=None):
        """Constructs a cell which contains the fundamental elements of the sudoku puzzle such as the value and notes.

        Args:
            val (int): The value of the cell if the cell is solved (0 if unsolved). Defaults to 0.
            notes (Set[int]): The possible values for the cell.
            pos (tuple): The row and column in the puzzle the cell is located at. Defaults to None.
            box (int): The number for the box in which the cell is located (0-8). Defaults to None.
        """

        if not isinstance(val, int):
            val = int(val)
        self._val = val
        if val == 0:
            self.notes = set(range(1, 10))
        else:
            self.notes = set((val,))
        self.pos = pos
        self.box = box

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val
        self.notes = set((new_val,))

    def __str__(self):
        """Returns the value of the cell as a string.

        Returns:
            str: The value of the cell.
        """
        return f"{self.val}"

    def __repr__(self):
        """Returns a string indicating this is a Cell object and appends the cell position.

        Returns:
            str: The cell position.
        """
        return f"Cell@{self.pos}"

    def __int__(self):
        """Returns the cell values as an int.

        Returns:
            int: The cell value as an int.
        """
        return self.val


class Puzzle_Backend:
    """
    A class to hold the information for each cell in a Sudoku puzzle.

    ...

    Attributes
    ----------
    unsolved : int
        number of cells unsolved in the puzzle.
    cells : list[Cell]
        list of all the cells in the puzzle
    rows : list[list[Cell]]
        list of all the rows of cells in the puzzle
    cols : list[list[Cell]]
        list of all the columns of cells in the puzzle
    boxs : list[list[Cell]]
        list of all the boxes of cells in the puzzle
    np : numpy.ndarray
        a 2D numpy array with the values of the cells in the puzzle
    checked : defaultdict(lambda: defaultdict(lambda: []))
        a dictionary containing all of the previously checked clues to prevent double checking
    """

    def __init__(self, vals=None):
        """Contructs the backend of the puzzle which contains all the puzzle information and interacts with the solver.

        Args:
            vals (list[int]): The values to initialize each cell of the puzzle with. Defaults to None.
        """
        self.unsolved = 81
        self.cells = []
        self.rows = [[] for _ in range(9)]
        self.cols = [[] for _ in range(9)]
        self.boxs = [[] for _ in range(9)]
        self.np = None
        self.checked = defaultdict(lambda: defaultdict(lambda: []))
        self._init(vals)

    def __setitem__(self, pos, new_val):
        """Gets the cell at position pos, and changes its value to new_val.

        Args:
            pos (tuple): The position of the cell to be modified.
            new_val (int): The new value for the cell.
        """
        cell = self.__getitem__(pos)
        self._update_cell(cell, new_val)

    def __getitem__(self, pos):
        """Returns the cell for a given position.

        Args:
            pos (tuple): The position of the desired cell.

        Returns:
            Cell: The cell at position pos.
        """
        res = None
        if isinstance(pos, int):
            res = self.rows[pos]
        elif pos[0] == slice(None, None, None) and isinstance(pos[1], int):
            res = self.cols[pos[1]]
        elif isinstance(pos[0], int) and pos[1] == slice(None, None, None):
            res = self.rows[pos[0]]
        elif isinstance(pos, tuple):
            res = self.rows[pos[0]][pos[1]]
        return res

    def __iter__(self):
        """Puzzle_Backend iterates from self.rows.

        Yields:
            list[Cell]: A row from the puzzle.
        """
        yield from self.rows

    def __str__(self):
        """Returns string that displays the puzzle.

        Returns:
            str: String that displays the puzzle in terms of its cell's values
        """
        pstr = ""
        for r, row in enumerate(self.rows):
            # Print horizontal seperators between boxes.
            if (r % 3) == 0:
                pstr += "-------------------------------------------------------------------------------------------------\n"
                pstr += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"
            # Print row with vertical seperators between boxes.
            for i in range(3):
                pstr += f"|\t{row[i * 3]}\t{row[i * 3 + 1]}\t{row[i * 3 + 2]}\t"
            pstr += "|\n"
            pstr += "|\t\t\t\t|\t\t\t\t|\t\t\t\t|\n"
        pstr += "-------------------------------------------------------------------------------------------------\n"
        return pstr

    def _init(self, vals):
        """Initializes unsolved, rows, cols, boxs, and np according to the input vals.

        Args:
            vals (list[int]): Values for each cell in the puzzle.
        """
        if vals:
            arr = np.reshape(np.array(vals), (9, 9))
        else:
            arr = np.zeros((9, 9), int)
        self.np = arr

        def p2b(ppos, bdimo=(3, 3), bdimi=(3, 3)):
            brow = ceil((ppos[0] + 1) / bdimi[0]) - 1
            bcol = ceil((ppos[1] + 1) / bdimi[1]) - 1
            return (brow * bdimo[1]) + bcol

        # Initialize the cells.
        for r, row in enumerate(arr):
            for c, val in enumerate(row):
                cell = Cell(pos=(r, c), box=p2b((r, c)))
                self.cells.append(cell)
                self.rows[r].append(cell)
                self.cols[c].append(cell)
                self.boxs[cell.box].append(cell)

        # Assign all values after initialization to make sure notes are discarded properly.
        for r, row in enumerate(arr):
            for c, val in enumerate(row):
                if val != 0:
                    self[r, c] = val

    def _update_cell(self, cell, new_val):
        """Updates all necessary attributes, when a cell is solved, to keep synchronicity.

        Args:
            cell (Cell): The cell that is solved.
            new_val (int): The value of the solved cell.

        Raises:
            Exception: Thrown if the cell is updated with the value 0.
            Exception: Thrown if updating the cell with new_val causes the puzzle to become invalid.
        """
        new_val = int(new_val)
        if new_val == 0:
            raise Exception("Can not assign a value of 0.")
        cell.val = new_val
        self.np[cell.pos] = new_val
        self.unsolved -= 1
        valid, reason = is_valid(self)
        if not valid:
            print(f"\nError: " + reason)
            print(self.np, end="\n\n")
            raise Exception(reason)
        r, c = cell.pos
        self.del_notes(vals=new_val, rows=r, cols=c, boxs=cell.box, save=cell.pos)

    def del_notes(self, vals=[], rows=[], cols=[], boxs=[], save=[]):
        if isinstance(vals, int):
            vals = [vals]
        if isinstance(rows, int):
            rows = [rows]
        if isinstance(cols, int):
            cols = [cols]
        if isinstance(boxs, int):
            boxs = [boxs]
        if isinstance(save, tuple):
            if isinstance(save[0], int):
                save = [save]
            elif isinstance(save[0], tuple):
                save = list(save)
        for val in vals:
            for rnum in rows:
                self.del_notes_row(val, rnum)
            for cnum in cols:
                self.del_notes_col(val, cnum)
            for bnum in boxs:
                self.del_notes_box(val, bnum)
            if save:
                for pos in save:
                    self[pos[0]][pos[1]].notes.add(val)

    def del_notes_row(self, val, rnum):
        for cell in self.rows[rnum]:
            cell.notes.discard(val)

    def del_notes_col(self, val, cnum):
        for cell in self.cols[cnum]:
            cell.notes.discard(val)

    def del_notes_box(self, val, bnum):
        for cell in self.boxs[bnum]:
            cell.notes.discard(val)

    def del_notes_cell(self, posns=[], vals=[], save_vals=[]):
        for pos in posns:
            if not vals:
                self[pos].notes = set()
            else:
                for val in vals:
                    self[pos].notes.discard(val)
            for val in save_vals:
                self[pos].notes.add(val)

    def copy(self, p):
        self.cells = p.cells
        self.boxs = p.boxs
        self.rows = p.rows
        self.cols = p.cols
        self.np = p.np
        self.unsolved = p.unsolved
        self.checked = p.checked

    def clear(self):
        for row in self.rows:
            for cell in row:
                cell.val = 0
                cell.notes = set(range(1, 10))
        self.checked = defaultdict(lambda: defaultdict(lambda: []))
        self.unsolved = 81
        self.np = np.zeros((9, 9), int)

    def load(self, vals):
        self.clear()
        self._init(vals)

    def solve(self):
        # If there are fewer than 17 clues, there can not be a unique solution.
        clue_ct = 0
        for cell in self.cells:
            if cell.val != 0:
                clue_ct += 1
            if clue_ct >= 17:
                break
        if clue_ct < 17:
            raise Exception("Puzzle does not have a unique solution.")
        solved = std_solve(self)
        if not solved:
            nishio(self)


class Puzzle:
    def __init__(self, vals=None, gui=True):
        self.puz = Puzzle_Backend(vals)
        self.gui = Puzzle_Frontend(parent=self) if gui else None
        self.puz2gui()
        self.gui.root.mainloop()

    def load(self, vals):
        self.puz.load(vals)

    def update_gui(self, pos, val):
        self.gui.update(pos, val)

    def update_puz(self, pos, val):
        return

    def puz2gui(self):
        for row in self.puz:
            for cell in row:
                if cell.val != 0:
                    self.update_gui(cell.pos, cell.val)
                else:
                    self.update_gui(cell.pos, "")

    def gui2puz(self):
        self.puz.clear()
        for rnum, row in enumerate(self.gui.cells):
            for cnum, gui_cell in enumerate(row):
                val = gui_cell.get()
                val = int(val) if val else 0
                if val != 0:
                    self.puz[rnum, cnum] = val

    def solve(self):
        self.gui2puz()
        self.puz.solve()
        self.puz2gui()

    def clear(self):
        self.puz.clear()
        self.puz2gui()

    # def load_image(self):
    #     nums = proc()
    #     self.puz.clear()
    #     self.puz.load(nums, force=True)
    #     self.puz2gui()
