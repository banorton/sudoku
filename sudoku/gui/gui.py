import tkinter as tk
from tkinter import ttk
from sudoku.box import Box_Array
from sudoku.helpers import box_pos_to_puzzle_pos, transpose
from os import path


class gui:
    def __init__(self, parent=None):
        self.parent = parent
        root = tk.Tk()
        self.root = root
        root.geometry("800x600")
        root.resizable(width=False, height=False)
        style = ttk.Style(root)
        print(__file__)
        root.tk.call("source", path.join(path.dirname(__file__), 'forest-light.tcl'))
        root.tk.call("source", path.join(path.dirname(__file__), 'forest-dark.tcl'))
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
        boxes, entries = self._gen_boxes_and_entries(puzzle)
        self.boxes = boxes
        self.entries = entries
        puzzle.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def _gen_boxes_and_entries(self, parent_frame):
        boxes = []
        for r in range(3):
            row = []
            for c in range(3):
                pframe = tk.Frame(
                    parent_frame, highlightbackground="white", highlightthickness=0.5
                )
                pframe.rowconfigure(tuple(range(3)), weight=1)
                pframe.columnconfigure(tuple(range(3)), weight=1)
                pframe.grid(row=r, column=c, sticky="news", padx=1, pady=1)
                row.append(pframe)
            boxes.append(row)
        entries = [[0 for _ in range(9)] for _ in range(9)]
        for row_num, row in enumerate(boxes):
            for col_num, box in enumerate(row):
                for r in range(3):
                    for c in range(3):
                        new_entry = ttk.Entry(
                            box, font="Helvetica 22 bold", justify="center"
                        )
                        new_entry.grid(row=r, column=c, sticky="news")
                        pos = box_pos_to_puzzle_pos((3, 3), (row_num, col_num), (r, c))
                        entries[pos[0]][pos[1]] = new_entry
        return boxes, entries

    def solve(self):
        self.parent.solve()

    def clear(self):
        self.parent.clear()

    # def load_image(self):
    #     self.parent.load_image()
