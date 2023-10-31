# sudoku
This Python package can solve Sudoku puzzles input by the user as long as the puzzle is valid (i.e. no duplicate values in any row, column, or box).


# System Overview:
This project was written completely in Python using **numpy**, and **tkinter** for the GUI. I am also using an OCR from **pytesseract** to read in puzzles from an image, but this feature has not been fully implemented yet.

I originally wrote this project with a very bare-bones framework just to get it working. However, I realized I wanted something more robust so that I could add features in the future that I was interested in like the ability to create puzzles, walk the user through solving a puzzle, etc. I also wanted a project that would help me start thinking about system design and how to plan for the future. I'm still constantly trying to rethink the design to make it make more sense and cut out unnecessary code. The system is currently laid out as follows.

PuzzleGUI
├── GUI
└── Puzzle
    ├── Cell Array (9x9)
    │   └── Cell
    │       ├── Val
    │       └── Note
    └── Box Array
        └── Boxes (3x3)
            └── Box(Cell Array)
Solver
Helpers
Generic

At the top is a **PuzzleGUI** object. This object contains all of the information and objects used for a particular instance of a puzzle. It also acts as the bridge between the backend of the puzzle/puzzle-solver and the front end that displays the puzzle. Each PuzzleGUI has two main objects, a **Gui** object and a **Puzzle** object.

The **Puzzle** object has two main objects, a **Box Array** and a **Cell Array**. These ojects contain the same information but are grouped differently to make certain processes quicker/easier.

The **Cell Array** contains all of the Cells in the puzzle (81 cells). Each **Cell** contains the fundamental elements of the puzzle: the current value of the cell **cell.val** (0 if undetermined) and the notes for the cell **cell.notes** (i.e. the possible values for the cell).

There are 9 boxes in a Sudoku puzzle, each of which contains 9 cells. The **Box Array** object contains 9 **Box** objects in an array with dimensions (3x3). A Box is a Cell Array but with some small changes.

**Solver**: This file contains all the algorithms used to solve a puzzle. It made sense to put them into their own file since it is the bulk of the code and I plan to add more algorithms and methods to solve the puzzle. I intend to make a solver that uses machine learning to solve the puzzles.

**Helpers**: This file contains a miscellany of helpful functions that I use in multiple places.

**Generic**: This file currently contains only a single class, **Array**. This file will likely be expanded as features are added.


# Solving Algorithms
All the code used to solve the puzzles is in **solver.py** The code was written to solve Sudoku puzzles similar to the way a human would solve the puzzle. That is by finding the most obvious clues first (naked and hidden singles), and working its way to more complicated clues (naked and hidden doubles, triples, quadruples, etc.). This was done intentionally so that I can eventually implement a mode that guides the user while solving the puzzle. The goal would be to explain each piece of logic one at a time until the puzzle is solved so that even someone who has never played Sudoku before could find, or at least understand, the solution to the puzzle.

When the regular algorithms can't make any further progress on the puzzle, I have implemented an algorithm for the **nishio** method. This method is essentially just guess and check. When the solving comes to a halt, there is usually a naked or hidden double somewhere in the puzzle. This means that there is a cell that can only contain 1 of 2 possible values. The nishio method would involve picking 1 of those 2 values and then to continue trying to solve the puzzle. If, while solving, a contradiction is reached, then the value that was picked must be incorrect. The puzzle is reset back to when the choice was made and the other possible value is used. This is, slightly more complicated because it is implemented as a recursive algorithm so that if the solving comes to a halt again after picking 1 of 2 possible values, the nishio method is called again. However, this method should only be used as a last resort, since calling it without having solved any of the cells would cause so many branch points that the puzzle would likely never get solved.


# Lessons Learned
I learned many things while making this project. First and foremost is that often my eyes are too big for my stomach. I can think of an endless amount of features I want to add at the start of the project, but that can often be a hinderance. If your intentions are too gradiose, it can be hard to know where to begin. It can make the first step of designing the system feel overwelming. However, if you don't think far enough into the future, a lot of refactoring has to be done which takes a lot of time. There seems to be a balance here. More specifically, I learned a little bit about how to make a python package. I didn't even what __init__ files were before this project. I used this project as a way to get practice using functionalities of python that I wasn't used to using.


# TODOs (in no particular order)
Implement a solver guide that guides the user in how to solve the puzzle step by step.
Implement a neural network to solve the puzzles.
Consolidate and clean up the solving algorithm for hidden clues.
Allow the user to upload an image of a Sudoku puzzle to get the solution.
Let the nishio algorithm split at clues with more than 2 values if necessary.
Use a hashmap to store the counts of notes in rows, cols, and boxes to make algorithms faster.
Implement solving algorithms that are faster but not necessary "user friendly".
Add the ability to generate puzzles of different difficulties.