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

The two main solving algorithms are **find_naked_clues** and **find_hidden_clues**. For a given number, n, the **find_naked_clues** function eliminates values from the notes of the other cells in a given row, column, or box if exactly n amount of cells in a row, column or box contain exactly n amount of notes and those notes are equal. An example is given below,

**Example:**
While checking row 3 with n=2, cells at positions (3,3) and (3,7) are found to have only the 2 notes {4,8}; Notes 4 and 8 will be removed from all other cells in row 3. If the cell at position (3,0) had the notes {1,3,4,7,8}, afterwards it would have the notes {1,3,7}.

For the **find_hidden_clues** function, it works slightly differently. If exactly n amount of cells, in a row or column or box, contain more than n amount of notes but share the same n amount of notes, eliminate all but the shared notes in those cells. Also, eliminate the shared notes from the notes in other cells in the given row, column, or box.

**Example:**
While checking row 3 with num=2, cells only at positions (3,3) and (3,7) are found to have more than 2 notes, {1,3,4,6,8} and {2,4,7,8}, but share notes 4 and 8; Notes 4 and 8 will be removed from all other notes in the cells of row 3. All notes exluding 4 and 8, for the cells at positions (3,3) and (3,7), will be removed.


# Lessons Learned
I learned,
- the basics of tkinter to make the GUI.
- more about how to use git and github for development.
- how to make a python package and use __init__ files.
- arguably most importantly that often my eyes are too big for my stomach. I can think of an endless amount of features I want to add at the start of a project, but that can often be a hinderance. If your intentions are too gradiose, it can be hard to know where to begin.


# Interesting Sudoku Facts
There are many more cool facts about Sudoku puzzles in the [wiki](https://en.wikipedia.org/wiki/Mathematics_of_Sudoku).
- If there are fewer than 17 clues in a Sudoku puzzle, there can not be a unique solution.
- There are approximately 49000 unique 17 clue puzzles with a unique solution.
- The largest minimal puzzle with the most amount of clues (found so far) has 40 clues.



# TODOs (in no particular order)
- Implement a solver guide that guides the user in how to solve the puzzle step by step.
- Allow the user to upload an image of a Sudoku puzzle to get the solution.
- Add the ability to generate puzzles of different difficulties.
- Implement a neural network to solve the puzzles.