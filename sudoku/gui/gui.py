import tkinter as tk
from tkinter import ttk
from os import path
from math import floor


class Puzzle_Frontend:
    """Handles all the information and functionality for the gui that the user interacts with."""

    def __init__(self, parent=None):
        """Constructs the gui.

        Args:
            parent (Puzzle): The Puzzle object that allows communication between the front and back end. Defaults to None.
        """

        self.parent = parent
        root = tk.Tk()
        self.root = root
        root.geometry("800x600")
        root.resizable(width=False, height=False)
        style = ttk.Style(root)
        root.tk.call("source", path.join(path.dirname(__file__), "forest-dark.tcl"))
        style.theme_use("forest-dark")

        # Left side of the gui for user input.
        info = ttk.Frame(root)
        solve_btn = ttk.Button(info, text="Solve", command=self.solve)
        solve_btn.pack(fill="x", pady=10)
        clear_btn = ttk.Button(info, text="Clear", command=self.clear)
        clear_btn.pack(fill="x", pady=10)
        # load_image_btn = ttk.Button(info, text="Load Image", command=self.load_image)
        # load_image_btn.pack(fill="x", pady=10)
        info.pack(side="left", padx=10)

        # Right side of the gui to display the values of the cells in the puzzle.
        puzzle = ttk.Frame(root)
        puzzle.rowconfigure(tuple(range(3)), weight=1)
        puzzle.columnconfigure(tuple(range(3)), weight=1)
        boxes, cells = self._gen_boxes_and_cells(puzzle)
        self.boxes = boxes
        self.cells = cells
        puzzle.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _gen_boxes_and_cells(self, parent_frame):
        """Generates the boxes and cells of the gui.

        Args:
            parent (frame): The frame to display the cells in.
        """

        def bpos2cpos(bnum, bpos):
            """Calculates the position of the cell within the 9x9 puzzle from the position of the box and the position of the cell within that box.

            Args:
                bnum (int): Box number.
                bpos (tuple): Box position.

            Returns:
                tuple: Position of cell in the puzzle.
            """
            ppos = (floor(bnum / 3), bnum - (floor(bnum / 3) * 3))
            rnum = (ppos[0] * 3) + bpos[0]
            cnum = (ppos[1] * 3) + bpos[1]
            return (rnum, cnum)

        boxes = []
        for rnum in range(3):
            for cnum in range(3):
                pframe = tk.Frame(
                    parent_frame, highlightbackground="white", highlightthickness=0.5
                )
                pframe.rowconfigure(tuple(range(3)), weight=1)
                pframe.columnconfigure(tuple(range(3)), weight=1)
                pframe.grid(row=rnum, column=cnum, sticky="news", padx=1, pady=1)
                boxes.append(pframe)
        cells = [[0 for _ in range(9)] for _ in range(9)]
        for bnum, box in enumerate(boxes):
            for rnum in range(3):
                for cnum in range(3):
                    new_entry = ttk.Entry(
                        box, font="Helvetica 22 bold", justify="center"
                    )
                    new_entry.grid(row=rnum, column=cnum, sticky="news")
                    pos = bpos2cpos(bnum, (rnum, cnum))
                    cells[pos[0]][pos[1]] = new_entry
        return boxes, cells

    def solve(self):
        """Solves the puzzle in the back-end and then updates the gui."""

        self.parent.solve()

    def clear(self):
        """Clears the puzzle."""

        self.parent.clear()

    def update(self, pos, val):
        """Updates the value of a cell at a particular position in the gui.

        Args:
            pos (tuple): Position of the cell of interest.
            val (int): The new value of the cell.
        """

        row, col = pos
        self.cells[row][col].delete(0, tk.END)
        self.cells[row][col].insert(0, str(val))

    def load_image(self):
        """Loads values in from an image."""

        self.parent.load_image()
