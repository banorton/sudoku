# sudoku
This Python package can solve Sudoku puzzles input by the user as long as the puzzle is valid (i.e. no duplicate values in any row, column, or box).


# System Overview:
This project was written only in Python using **numpy**, and **tkinter** for the GUI. I am also using an OCR from **pytesseract** to read in puzzles from an image, but this feature has not been fully implemented yet.

The system is currently laid out as follows,
- **puzzle.py**: Contains the **Cell** object which holds the value and notes for a cell, the **Puzzle_Backend** object which contains all the information for the puzzle and defines how the puzzle interacts with the solver, and the **Puzzle** object which handles the connection between the front and back end of puzzle.
- **solver.py**: Contains all of the algorithms used to solve the puzzle. I talk more in depth on how I made those algorithms in the [next section](#solving-algorithms).
- **gui/**: Contains the **gui.py** file with the **Puzzle_Backend** object, and the theme files for the tkinter gui. **Puzzle_Backend** defines how the tkinter gui is setup. Currently the gui has a puzzle frame on the right to display the values of each of the cells and an info frame on the left which contains the buttons for solving and clearing the puzzle.
- **examples/**: Stores example puzzles of varying difficulties. The difficulties scale from easy to impossible. 


# Solving Algorithms
All the code used to solve the puzzles is in **solver.py** The code was written to solve Sudoku puzzles similar to the way a human would solve the puzzle. That is by finding the most obvious clues first (naked and hidden singles), and working its way to more complicated clues (naked and hidden doubles, triples, quadruples, etc.). This was done intentionally so that I can eventually implement a mode that guides the user while solving the puzzle. The goal would be to explain each piece of logic one at a time until the puzzle is solved so that even someone who has never played Sudoku before could find, or at least understand, the solution to the puzzle.

When the regular algorithms can't make any further progress on the puzzle, I have implemented an algorithm for the **nishio** method. This method is essentially just guess and check. When the solving comes to a halt, there is usually a naked or hidden double somewhere in the puzzle. This means that there is a cell that can only contain 1 of 2 possible values. The nishio method would involve picking 1 of those 2 values and then to continue trying to solve the puzzle. If, while solving, a contradiction is reached, then the value that was picked must be incorrect. The puzzle is reset back to when the choice was made and the other possible value is used. This method is slightly more complicated because it is implemented as a recursive algorithm so that if the solving comes to a halt again after picking 1 of 2 possible values, the nishio method is called again. However, this method should only be used as a last resort, since calling it without having solved any of the cells would cause so many branch points that the puzzle would likely never get solved.


# Lessons Learned
- I learned the basics of tkinter to make the GUI.
- I learned more about how to use git and github for development.
- I learned about how to make a python package. I learned how to use __init__ files.
- First and foremost, I learned that often my eyes are too big for my stomach. I can think of an endless amount of features I want to add at the start of a project, but that can often be a hinderance. If your intentions are too gradiose, it can be hard to know where to begin. However, if you don't think far enough into the future, a lot of rethinking and rewriting has to be done which takes a lot of time. A balance seems to be required.


# TODOs (in no particular order)
- Implement a solver guide that guides the user in how to solve the puzzle step by step.
- Allow the user to upload an image of a Sudoku puzzle to get the solution.
- Add the ability to generate puzzles of different difficulties.
- Implement a neural network to solve the puzzles.