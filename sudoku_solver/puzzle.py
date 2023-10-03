import numpy as np
from math import ceil
from math import floor


class Sudoku_Board:
    def __init__(self, board_state=np.zeros(81).astype("uint8")):
        self.board_state_history = []
        self.board_state = board_state
        self.update_cell_history()
        self.notes = [[{} for _ in range(9)] for _ in range(9)]
        self.notes_history = (self.notes)
        self.num_unsolved = np.count_nonzero(board_state == 0)


    ##############################################################################################################################
    # GENERIC FUNCTIONS
    def solve(self):
        if not self.check_validity():
            print("Solve ERROR: Not a valid board state.")
            return
        self.fill_notes()
        ct = 1
        print(self.num_unsolved)
        while (self.num_unsolved > 0) and (ct < 11):
            print(ct)
            self.check4_naked_single()
            self.check4_hidden_single()
            self.check4_notes_inline()
            self.check4_hidden_double()
            ct += 1
        self.print_board_state()
        print(self.num_unsolved)


    def cell_to_box(self, pos):
        row, col = pos
        box_row = floor((row)/3)
        box_col = floor((col)/3)
        return (box_row, box_col)
    
    
    def num_to_pos(self, box_num):
        box_row = floor((box_num-1)/3)
        box_col = floor((box_num-1)%3)
        return (box_row, box_col)
    
    
    def pos_to_num(self, box_pos):
        box_row, box_col = box_pos
        box_num = ((box_row) * 3 + box_col) + 1
        return box_num
    
    
    def box_cell_to_cell(self, box_num, rel_pos):
        rel_pos_row, rel_pos_col = rel_pos
        box_row, box_col = self.num_to_pos(box_num)
        cell_row = rel_pos_row + box_row * 3
        cell_col = rel_pos_col + box_col * 3
        return (cell_row, cell_col)
    
    
    def check_validity(self):
        # Check boxs for duplicates.
        for box_num in range(1, 10):
            box = self.get_box_num(box_num).flatten()
            box = np.delete(box, np.where(box == 0)).tolist()
            if len(box) > len(set(box)):
                return 0
            
        # Check rows for duplicates.
        for row_num in range(9):
            row = self.get_row(row_num)
            row = np.delete(row, np.where(row == 0)).tolist()
            if len(row) > len(set(row)):
                return 0
            
        # Check columns for duplicates.
        for col_num in range(9):
            col = self.get_col(col_num).T
            col = np.delete(col, np.where(col == 0)).tolist()
            if len(col) > len(set(col)):
                return 0
        
        # Return 1 if the board state is valid.
        return 1
    
    
    def print_board_state(self):
        for row_num in range(9):
            row = self.get_row(row_num)
            # Print horizontal seperators between boxes.
            if (row_num % 3) == 0:
                print("-------------------------------------------------------------------------------------------------", end="\n")
                print("|\t\t\t\t|\t\t\t\t|\t\t\t\t|", end="\n")
            
            # Print row with vertical seperators between boxes.
            for i in range(3):
                print("|", end="\t")
                print(str(row[i*3]) + "\t" + str(row[i*3+1]), "\t" + str(row[i*3+2]), "\t", end="")
            print("|", end="\n")
            print("|\t\t\t\t|\t\t\t\t|\t\t\t\t|", end="\n")
        print("-------------------------------------------------------------------------------------------------", end="\n")


    ##############################################################################################################################
    # CELL FUNCTIONS
    def get_cell(self, pos):
        row, col = pos
        return self.board_state.reshape(9, 9)[row, col]
    
    
    def get_row(self, i):
        board_state_arr = self.board_state.reshape(9, 9)
        return board_state_arr[i, :]


    def get_col(self, i):
        board_state_arr = self.board_state.reshape(9, 9)
        return board_state_arr[:, i].T
    
    
    def get_box(self, box_pos):
        box_row = box_pos[0] + 1
        box_col = box_pos[1] + 1
        box_arr = self.board_state.reshape(9, 9)[box_row * 3 - 3:box_row * 3, box_col * 3 - 3:box_col * 3]
        return box_arr


    def get_box_num(self, box_num):
        box_row = ceil(box_num / 3)
        box_col = (box_num - 1) % 3 + 1
        return self.get_box((box_row, box_col))
    
    
    def update_cell(self, cell_pos, num):
        cell_row, cell_col = cell_pos
        if (num < 0) or (num > 9):
            print("update cell ERROR: Number outside allowed range (0 - 9).")
        self.board_state[(cell_row)*9 + (cell_col)] = num
        if not self.check_validity():
            print()
            print(cell_pos)
            print(num)
            raise Exception("Stupid")
        # self.notes[cell_row][cell_col] = {num}
        self.replace_note((cell_row, cell_col), {num})
        box_pos = self.cell_to_box((cell_row, cell_col))
        self.discard_notes_row(cell_row, num)
        self.discard_notes_col(cell_col, num)
        self.discard_notes_box(self.cell_to_box((cell_row, cell_col)), num)
        self.num_unsolved -= 1
        self.update_cell_history()
        

    def update_cell_history(self):
        if not self.check_validity():
            print("update cell history ERROR: Not a valid board state.")
            return
        self.board_state_history.append(self.board_state.tolist())


    ##############################################################################################################################
    # NOTES FUNCTIONS
    def get_notes(self, pos):
        row, col = pos
        return self.notes[row][col]


    def discard_note(self, pos, num):
        if pos == (6,6) and num == 4:
            print()
        self.notes[pos[0]][pos[1]].discard(num)
        
        
    def add_note(self, pos, num):
        self.notes[pos[0]][pos[1]].add(num)
        
        
    def replace_note(self, pos, new_set):
        self.notes[pos[0]][pos[1]] = new_set


    def get_notes_row(self, i):
        return self.notes[i]


    def get_notes_col(self, i):
        return [row[i] for row in self.notes]
    
    
    def get_notes_box(self, box_pos):
        box_row = box_pos[0] + 1
        box_col = box_pos[1] + 1
        rows = [self.notes[box_row*3-3], self.notes[box_row*3-2], self.notes[box_row*3-1]]
        box_notes = []
        for row in rows:
            box_notes.append(row[box_col*3-3])
            box_notes.append(row[box_col*3-2])
            box_notes.append(row[box_col*3-1])
        return box_notes


    def get_notes_box_num(self, box_num):
        box_pos = self.num_to_pos(box_num)
        return self.get_notes_box(box_pos)
    
    
    def discard_notes_row(self, row_num, num):
        for col_num in range(9):
            if len(self.notes[row_num][col_num]) != 1:
                # self.notes[row_num][col_num].discard(num)
                self.discard_note((row_num, col_num), num)
    
    
    def discard_notes_col(self, col_num, num):
        for row_num in range(9):
            if len(self.notes[row_num][col_num]) != 1:
                # self.notes[row_num][col_num].discard(num)
                self.discard_note((row_num, col_num), num)


    def discard_notes_box(self, box_pos, num):
        box_row = box_pos[0] + 1
        box_col = box_pos[1] + 1
        row_nums = [box_row*3-3, box_row*3-2, box_row*3-1]
        for row_num in row_nums:
            if len(self.notes[row_num][box_col*3-3]) != 1:
                # self.notes[row_num][box_col*3-3].discard(num)
                self.discard_note((row_num, box_col*3-3), num)
            if len(self.notes[row_num][box_col*3-2]) != 1:
                # self.notes[row_num][box_col*3-2].discard(num)
                self.discard_note((row_num, box_col*3-2), num)
            if len(self.notes[row_num][box_col*3-1]) != 1:
                # self.notes[row_num][box_col*3-1].discard(num)
                self.discard_note((row_num, box_col*3-1), num)


    def fill_notes(self):
        if not self.check_validity():
            print("ERROR: Not a valid board state.")
            return
        
        for row_num in range(9):
            for col_num in range(9):
                if self.board_state[(row_num)*9 + col_num] == 0:
                    impossible_vals = set(self.get_row(row_num)) | set(self.get_col(col_num).T) | set(self.get_box(self.cell_to_box((row_num, col_num))).flatten())
                    impossible_vals.discard(0)
                    possible_vals = set(range(1,10)) - impossible_vals
                    # self.notes[row_num][col_num] = possible_vals
                    self.replace_note((row_num, col_num), possible_vals)
                else:
                    # self.notes[row_num][col_num] = {self.get_cell((row_num, col_num))}
                    self.replace_note((row_num, col_num), {self.get_cell((row_num, col_num))})
    
    
    ##############################################################################################################################
    # LOGIC CHECKS
    def check4_naked_single(self):
        for row_num in range(9):
            for col_num in range(9):
                if (len(self.notes[row_num][col_num]) == 1):
                    if (self.board_state[(row_num)*9 + col_num] == 0):
                        num = self.notes[row_num][col_num].pop()
                        self.update_cell((row_num, col_num), num)
    
    
    def check4_hidden_single(self):
        self.check4_naked_single()
        for row_num in range(9):
            for col_num in range(9):
                curr_set = self.get_notes((row_num, col_num))
                if len(curr_set) == 1:
                    if self.get_cell((row_num, col_num)) == 0:
                        self.update_cell((row_num, col_num), list(curr_set)[0])
                    continue
                box_notes = []
                for note in self.get_notes_box(self.cell_to_box((row_num, col_num))):
                    note.discard(0)
                    box_notes.extend(list(note))
                row_notes = []
                for note in self.get_notes_row(row_num):
                    note.discard(0)
                    row_notes.extend(list(note))      
                col_notes = []
                for note in self.get_notes_col(col_num):
                    note.discard(0)
                    col_notes.extend(list(note))
                for num in list(curr_set):
                    if box_notes.count(num) == 1:
                        self.update_cell((row_num, col_num), num)
                        continue
                    elif row_notes.count(num) == 1:
                        self.update_cell((row_num, col_num), num)
                        continue
                    elif col_notes.count(num) == 1:
                        self.update_cell((row_num, col_num), num)
                        continue
        self.check4_naked_single()
                                    
    
    def check4_notes_inline(self):
        for box_num in range(1, 10):
            box_notes = self.get_notes_box_num(box_num)
            num_positions = [[] for _ in range(10)]
            for cell_num, note in enumerate(box_notes):
                cell_num = cell_num + 1
                note = note.copy()
                note.discard(0)
                rel_pos = self.num_to_pos(cell_num)
                cell_pos = self.box_cell_to_cell(box_num, rel_pos)
                if len(note) == 1:
                    continue
                while note:
                    num = note.pop()
                    num_positions[num].append(cell_pos)
            for num, positions in enumerate(num_positions):
                if len(positions) == 2:
                    # Rows are the same.
                    if positions[0][0] == positions[1][0]:
                        print("2 Inline Row: (" + str(num) + ") in positions " + str(positions[0]) + " and " + str(positions[1]) + " in box " + str(box_num))
                        self.discard_notes_row(positions[0][0], num)
                        print("Discarding " + str(num) + " from row " + str(positions[0][0]), end="\n\n")
                        self.notes[positions[0][0]][positions[0][1]].add(num)
                        self.notes[positions[1][0]][positions[1][1]].add(num)
                    # Columns are the same.
                    elif positions[0][1] == positions[1][1]:
                        print("2 Inline Col: (" + str(num) + ") in positions " + str(positions[0]) + " and " + str(positions[1]) + " in box " + str(box_num))
                        self.discard_notes_col(positions[0][1], num)
                        print("Discarding " + str(num) + " from col " + str(positions[0][1]), end="\n\n")
                        self.notes[positions[0][0]][positions[0][1]].add(num)
                        self.notes[positions[1][0]][positions[1][1]].add(num)
                elif len(positions) == 3:
                    # Rows are the same.
                    if positions[0][0] == positions[1][0] == positions[2][0]:
                        print("3 Inline Row: (" + str(num) + ") in positions " + str(positions[0]) + " and " + str(positions[1]) + " and " + str(positions[2]) + " in box " + str(box_num))
                        self.discard_notes_row(positions[0][0], num)
                        print("Discarding " + str(num) + " from row " + str(positions[0][0]), end="\n\n")
                        self.notes[positions[0][0]][positions[0][1]].add(num)
                        self.notes[positions[1][0]][positions[1][1]].add(num)
                        self.notes[positions[2][0]][positions[2][1]].add(num)
                    # Rows are the same.
                    elif positions[0][1] == positions[1][1] == positions[2][1]:
                        print("3 Inline Col: (" + str(num) + ") in positions " + str(positions[0]) + " and " + str(positions[1]) + " and " + str(positions[2]) + " in box " + str(box_num))
                        self.discard_notes_col(positions[0][1], num)
                        print("Discarding " + str(num) + " from Col " + str(positions[0][1]), end="\n\n")
                        self.notes[positions[0][0]][positions[0][1]].add(num)
                        self.notes[positions[1][0]][positions[1][1]].add(num)
                        self.notes[positions[2][0]][positions[2][1]].add(num)
        self.check4_naked_single()
    
    
    def check4_naked_double(self):
        return
    
        
    def check4_hidden_double(self):
        print("Checking Doubles")
        # CHECK BOXES FOR HIDDEN DOUBLES
        self.check4_naked_single()
        for box_num in range(1, 10):
            box_notes = self.get_notes_box_num(box_num)
            num_positions = [[] for _ in range(10)]
            for cell_num, note in enumerate(box_notes):
                cell_num = cell_num + 1
                note = note.copy()
                note.discard(0)
                rel_pos = self.num_to_pos(cell_num)
                cell_pos = self.box_cell_to_cell(box_num, rel_pos)
                if len(note) == 1:
                    continue
                while note:
                    num = note.pop()
                    num_positions[num].append(cell_pos)
            for num, positions in enumerate(num_positions):
                if len(positions) != 2:
                    num_positions[num] = []
            for num1, positions1 in enumerate(num_positions):
                if not positions1:
                    continue
                positions1 = positions1.copy()
                num_positions[num1] = []
                for num2, positions2 in enumerate(num_positions):
                    if not positions2:
                        continue
                    if positions1 == positions2:
                        # Double found.
                        print("Double Box: (" + str(num1) + ", " + str(num2) + ") in positions " + str(positions1[0]) + " and " + str(positions1[1]) + " in box " + str(box_num))
                        box_pos = self.num_to_pos(box_num)
                        self.discard_notes_box(box_pos, num1)
                        self.discard_notes_box(box_pos, num2)
                        print("Discarding " + str(num1) + " and " + str(num2) + " from box " + str(box_num))
                        # Rows are the same.
                        if positions1[0][0] == positions1[1][0]:
                            self.discard_notes_row(positions1[0][0], num1)
                            self.discard_notes_row(positions1[0][0], num2)
                            print("Discarding " + str(num1) + " and " + str(num2) + " from row " + str(positions1[0][0]))
                        # Columns are the same.
                        elif positions1[0][1] == positions1[1][1]:
                            self.discard_notes_col(positions1[0][1], num1)
                            self.discard_notes_col(positions1[0][1], num2)
                            print("Discarding " + str(num1) + " and " + str(num2) + " from col " + str(positions1[0][1]))
                        self.notes[positions1[0][0]][positions1[0][1]] = {num1, num2}
                        self.notes[positions1[1][0]][positions1[1][1]] = {num1, num2}
                        print()
        # CHECK ROWS FOR HIDDEN DOUBLES
        self.check4_naked_single()
        for row_num in range(9):
            row_notes = self.get_notes_row(row_num)
            num_positions = [[] for _ in range(10)]
            for col_num, note in enumerate(row_notes):
                note = note.copy()
                note.discard(0)
                cell_pos = (row_num, col_num)
                if len(note) == 1:
                    continue
                while note:
                    num = note.pop()
                    num_positions[num].append(cell_pos)
            for num, positions in enumerate(num_positions):
                if len(positions) != 2:
                    num_positions[num] = []
            for num1, positions1 in enumerate(num_positions):
                if not positions1:
                    continue
                positions1 = positions1.copy()
                num_positions[num1] = []
                for num2, positions2 in enumerate(num_positions):
                    if not positions2:
                        continue
                    if positions1 == positions2:
                        # Double found.
                        print("Double Row: (" + str(num1) + ", " + str(num2) + ") in positions " + str(positions1[0]) + " and " + str(positions1[1]))
                        box_pos = self.cell_to_box(positions1[0])
                        self.discard_notes_row(positions1[0][0], num1)
                        self.discard_notes_row(positions1[0][0], num2)
                        print("Discarding " + str(num1) + " and " + str(num2) + " from row " + str(positions1[0][0]))
                        # Boxs are the same.
                        if self.cell_to_box(positions1[0]) == self.cell_to_box(positions1[1]):
                            self.discard_notes_box(box_pos, num1)
                            self.discard_notes_box(box_pos, num2)
                            print("Discarding " + str(num1) + " and " + str(num2) + " from box " + str(self.pos_to_num(self.cell_to_box(positions1[0]))))
                        self.notes[positions1[0][0]][positions1[0][1]] = {num1, num2}
                        self.notes[positions1[1][0]][positions1[1][1]] = {num1, num2}
                        print()
        # CHECK COLS FOR HIDDEN DOUBLES
        self.check4_naked_single()
        for col_num in range(9):
            col_notes = self.get_notes_col(col_num)
            num_positions = [[] for _ in range(10)]
            for row_num, note in enumerate(col_notes):
                note = note.copy()
                note.discard(0)
                cell_pos = (row_num, col_num)
                if len(note) == 1:
                    continue
                while note:
                    num = note.pop()
                    num_positions[num].append(cell_pos)
            for num, positions in enumerate(num_positions):
                if len(positions) != 2:
                    num_positions[num] = []
            for num1, positions1 in enumerate(num_positions):
                if not positions1:
                    continue
                positions1 = positions1.copy()
                num_positions[num1] = []
                for num2, positions2 in enumerate(num_positions):
                    if not positions2:
                        continue
                    if positions1 == positions2:
                        # Double found.
                        print("Double Col: (" + str(num1) + ", " + str(num2) + ") in positions " + str(positions1[0]) + " and " + str(positions1[1]))
                        box_pos = self.cell_to_box(positions1[0])
                        self.discard_notes_col(positions1[0][1], num1)
                        self.discard_notes_col(positions1[0][1], num2)
                        print("Discarding " + str(num1) + " and " + str(num2) + " from col " + str(positions1[0][1]))
                        # Boxs are the same.
                        if self.cell_to_box(positions1[0]) == self.cell_to_box(positions1[1]):
                            self.discard_notes_box(box_pos, num1)
                            self.discard_notes_box(box_pos, num2)
                            print("Discarding " + str(num1) + " and " + str(num2) + " from box " + str(self.pos_to_num(self.cell_to_box(positions1[0]))))
                        self.notes[positions1[0][0]][positions1[0][1]] = {num1, num2}
                        self.notes[positions1[1][0]][positions1[1][1]] = {num1, num2}
                        print()
        self.check4_naked_single()
    
        
    def check4_naked_triple(self):
        return
        
        
    def check4_hidden_triple(self):
        return
    
    
    def check4_naked_quad(self):
        return
        
        
    def check4_hidden_quad(self):
        return
        
        
    def check4_x_wing(self):
        return
    
    
    ##############################################################################################################################
                

if __name__ == "__main__":
    # board_easy = np.array([9,0,0,3,0,2,6,0,0,4,0,7,0,0,8,9,1,3,6,0,3,1,0,0,0,5,4,0,3,0,0,8,0,4,7,0,0,0,8,0,3,0,1,6,0,0,0,4,2,0,0,5,0,0,8,7,1,9,0,6,0,4,5,3,0,0,0,5,0,0,0,0,2,0,0,4,0,0,0,0,1])
    # sb = Sudoku_Board(board_state=board_easy)
    # board_medium = np.array([0,0,6,4,1,0,0,7,0,5,0,0,0,6,3,4,0,0,0,3,0,0,0,0,0,0,0,0,6,4,0,0,1,0,0,0,0,0,3,6,0,2,0,0,0,0,8,2,5,0,9,0,1,3,0,4,0,0,0,0,8,0,0,0,2,0,0,0,0,0,0,0,3,7,0,2,8,4,1,0,0])
    # sb = Sudoku_Board(board_state=board_medium)
    # board_hard = np.array([0,0,0,0,0,7,0,0,6,0,9,4,0,3,0,0,0,0,0,0,0,0,0,1,2,0,0,1,0,0,0,8,0,0,0,0,0,0,0,0,0,2,8,3,1,7,0,0,0,1,0,0,4,9,0,0,0,0,0,0,0,0,5,5,0,1,9,0,0,0,6,3,0,7,0,0,6,0,9,2,8])
    # sb = Sudoku_Board(board_state=board_hard)
    # board_expert = np.array([5,0,0,9,0,0,0,7,0,0,6,0,0,0,0,9,0,4,8,0,0,0,0,0,0,0,5,7,5,1,0,0,0,0,0,8,6,0,0,2,0,0,5,0,0,0,8,0,0,0,0,0,0,1,9,0,0,0,0,0,3,0,0,0,0,0,0,4,0,0,0,0,0,0,0,5,0,1,0,0,0])
    # sb = Sudoku_Board(board_state=board_expert)
    # board_expert2 = np.array([0,7,2,5,0,0,0,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,4,7,3,0,0,0,0,1,5,7,0,0,0,0,0,0,9,0,8,0,0,0,5,0,0,0,0,0,0,0,0,4,2,0,0,0,0,9,0,0,3,7,0])
    # sb = Sudoku_Board(board_state=board_expert2)
    board_evil = np.array([4,0,0,0,1,0,0,0,0,0,9,0,0,0,0,2,0,0,0,0,3,5,0,4,0,6,0,3,0,0,0,0,0,0,0,4,0,0,0,0,0,8,0,0,0,0,0,4,7,0,6,0,5,0,0,0,7,0,8,0,0,0,0,2,0,0,1,0,7,6,0,0,0,0,0,0,3,0,0,1,0])
    sb = Sudoku_Board(board_state=board_evil)
    assert(sb.board_state.size == 81)
    sb.print_board_state()
    sb.solve()
    print("Validity: " + str(sb.check_validity()))
    
    # TODO: WRITE ALL DATA IN CONSTANT LOOKUP TIME LOOKUP ARRAYS
    # TODO: Store all note deletions using a key related to which row col or box and what number was deleted to make sure no deletions are repeated
    # TODO: Add triples    
    # TODO: Add quads
    # TODO: Add GUI