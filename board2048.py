''' class definition for a 2048 board '''

from more_itertools import locate
import random

class Board():
    ''' Class definition of a 2048 board[0, 0, 0]
    '''
    def __init__(self):
        self.len_row = 4
        self.board = [0] * self.len_row * self.len_row
        self.score = 0
        # Start with 2 random values
        self.add_random()
        self.add_random()

#    def __repr__(self):
#        pass

    def __str__(self):
        ''' Make it a pretty sight when printed
        '''
        def esc(code):
            ''' Return full escape code '''
            return f'\033[{code}m'

        def cntr(nmr):
            ''' return nmr centered in string '''
            return str(nmr).center(5, " ")

        def colour(nmr):
            ''' Add some colour to printing the board '''
            colnmrs = {0:0,
                       2:21,
                       4:27,
                       8:46,
                       16:172,
                       32:163,
                       64:160,
                       128:118,
                       256:28,
                       512:35,
                       1024:22,
                       2048:94,
                       4096:88,
                       8192:93}
            if nmr == 0:
                return esc('48;5;0') + esc('38;5;0')
            else:
                return esc(f'48;5;{colnmrs[nmr]}') + esc('38;5;16')

        print_board = f'\033[2J' + f'\033[H'
        for i in range(self.len_row):
            for j in range(self.len_row):
#                print_board += esc('31;43') + cntr(self.board[i * self.len_row + j]) + esc(0)
                print_board += colour(self.board[i * self.len_row + j]) + \
                               cntr(self.board[i * self.len_row + j]) + esc(0)
            print_board += "\n"
        print_board += "\nPoints: {}\n".format(self.score)
        return print_board + esc(0)

    def flatten_board(self):
        ''' Converts list of lists to a 1D list.
            e.g. [[1,2],[3,4]] => [1,2,3,4]
        '''
        self.board = [j for sub in self.board for j in sub]

    def expand_board(self):
        ''' Converts 1D list to 2D list of lists.
            E.g. [1,2,3,4] => [[1,2],[3,4]]
        '''
        self.board = [self.board[i:i + self.len_row] for i in range(0,
                                                                    len(self.board),
                                                                    self.len_row)]

    def move_row(self, row):
        ''' Moves one row according to the rules of the game 2048
            example [0, 2, 0, 2] => [4, 0, 0, 0]
        '''
        # Move all numbers to left. (or remove all 0's)
        all_numbers = list(locate(row))
        row_with_nmrs = [row[i] for i in all_numbers]
        if len(row_with_nmrs) > 1:
            for i in range(len(row_with_nmrs) - 1):
                if row_with_nmrs[i] == row_with_nmrs[i + 1]:
                    row_with_nmrs[i] *= 2
                    self.score += row_with_nmrs[i]
                    row_with_nmrs[i + 1] = 0
        all_numbers = locate(row_with_nmrs)
        row = [row_with_nmrs[i] for i in all_numbers]
        # to add 0's at the end
        new_row = [0, 0, 0, 0]
        new_row[:len(row)] = row
        return new_row

    def move_up(self):
        ''' If possible make all fields on the board move up. '''
        self.expand_board()
        for column in range(self.len_row):
            one_column = []
            for row in range(self.len_row):
                print("board: {}".format(self.board))
                print("row: {} and column: {}".format(row, column))
                one_column += [self.board[row][column]]
            new_column = self.move_row(one_column)
            for row in range(self.len_row):
                self.board[row][column] = new_column[row]
        self.flatten_board()

    def move_down(self):
        ''' If possible make all fields on the board move down. '''
        self.expand_board()
        for column in range(self.len_row):
            one_column = []
            for row in range(self.len_row):
                one_column += [self.board[row][column]]
            new_column = self.move_row(one_column[::-1])
            new_column = new_column[::-1]
            for row in range(self.len_row):
                self.board[row][column] = new_column[row]
        self.flatten_board()

    def move_left(self):
        ''' If possible make all fields on the board move left. '''
        self.expand_board()
#        print(self.board)
        new_board = []
        for row in self.board:
            new_row = self.move_row(row)
            new_board += new_row
        self.board = new_board
#        print(self.board)
#        self.flatten_board()

    def move_right(self):
        ''' If possible make all fields on the board move right. '''
        self.expand_board()
        new_board = []
        for row in self.board:
            new_row = self.move_row(row[::-1])
            new_board += new_row[::-1]
        self.board = new_board
#        self.flatten_board()

    def add_random(self):
        ''' get random empty field en place 2 or 4.
            60% chance on 2 and 40% chance on 4
        '''
#        self.flatten_board()
        all_zeros = [i for i, e in enumerate(self.board) if e == 0]
        if len(all_zeros) > 0:
            select = random.choice(all_zeros)
            criteria = random.random()
            if criteria < 0.6:
                self.board[select] = 2
            else:
                self.board[select] = 4

    def check_if_moves_possible(self):
        ''' If no more moves possible then the game ends '''
        def check_zeros():
            ''' check if there are empty fields on the board '''
            if 0 in self.board:
                return True
            else:
                # if False then next check needs expanded board
                self.expand_board()
                return False

        def check_rows():
            ''' Check if there are the same numbers next to each
                other on a row.
            '''
            for row in self.board:
                for i, j in enumerate(row[:-1]):
                    if j == row[i + 1]:
                        # if True then game needs flattened board
                        self.flatten_board()
                        return True
            return False

        def check_columns():
            ''' Check if there are the same numbers next to each
                other on a column.
            '''
            for j in range(self.len_row):
                column = []
                for row in self.board:
                    column += [row[j]]
                for x, y in enumerate(column[:-1]):
                    if y == column[x + 1]:
                        # if True then game needs flattened board
                        self.flatten_board()
                        return True
            return False

        return (check_zeros() or check_rows() or check_columns())
