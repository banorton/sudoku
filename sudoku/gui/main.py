import tkinter as tk
from tkinter import ttk
import os

root = tk.Tk()
root.geometry("800x600")
root.resizable(width=False, height=False)
style = ttk.Style(root)
root.tk.call("source", "sudoku\\gui\\forest-light.tcl")
root.tk.call("source", "sudoku\\gui\\forest-dark.tcl")
style.theme_use("forest-dark")

info = ttk.Frame(root)
solve_btn = ttk.Button(info, text="Solve")
clear_btn = ttk.Button(info, text="Clear")
solve_btn.pack(fill="x", pady=10)
clear_btn.pack(fill="x", pady=10)
info.pack(side="left", padx=10)

puzzle = ttk.Frame(root)
puzzle.rowconfigure(tuple(range(3)), weight=1)
puzzle.columnconfigure(tuple(range(3)), weight=1)
boxes = []
for r in range(3):
    row = []
    for c in range(3):
        pframe = tk.Frame(puzzle, highlightbackground="white", highlightthickness=0.5)
        pframe.rowconfigure(tuple(range(3)), weight=1)
        pframe.columnconfigure(tuple(range(3)), weight=1)
        pframe.grid(column=r, row=c, sticky="news", padx=1, pady=1)
        row.append(pframe)
    boxes.append(row)
entries = []
for row in boxes:
    for box in row:
        for r in range(3):
            for c in range(3):
                new_entry = ttk.Entry(box, font="Helvetica 22 bold", justify="center")
                new_entry.grid(row=r, column=c, sticky="news")
                entries.append(new_entry)
puzzle.pack(side="right", fill="both", expand=True, padx=5, pady=5)

root.mainloop()
