import tkinter as tk
from tkinter import ttk
from os import path
from math import floor


class Puzzle_Frontend:
    def __init__(self, parent=None):
        self.parent = parent
        root = tk.Tk()
        self.root = root
        root.geometry("800x600")
        root.resizable(width=False, height=False)
        style = ttk.Style(root)
        root.tk.call("source", path.join(path.dirname(__file__), "forest-light.tcl"))
        root.tk.call("source", path.join(path.dirname(__file__), "forest-dark.tcl"))
        style.theme_use("forest-dark")

        info = ttk.Frame(root)
        solve_btn = ttk.Button(info, text="Solve", command=self.solve)
        solve_btn.pack(fill="x", pady=10)
        clear_btn = ttk.Button(info, text="Clear", command=self.clear)
        clear_btn.pack(fill="x", pady=10)
        # load_image_btn = ttk.Button(info, text="Load Image", command=self.load_image)
        # load_image_btn.pack(fill="x", pady=10)
        info.pack(side="left", padx=10)

        puzzle = ttk.Frame(root)
        puzzle.rowconfigure(tuple(range(3)), weight=1)
        puzzle.columnconfigure(tuple(range(3)), weight=1)
        boxes, cells = self._gen_boxes_and_cells(puzzle)
        self.boxes = boxes
        self.cells = cells
        puzzle.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _gen_boxes_and_cells(self, parent_frame):
        def bpos2cpos(bnum, bpos):
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
        self.parent.solve()

    def clear(self):
        self.parent.clear()

    def update(self, pos, val):
        row, col = pos
        self.cells[row][col].delete(0, tk.END)
        self.cells[row][col].insert(0, str(val))

    # def load_image(self):
    #     self.parent.load_image()
