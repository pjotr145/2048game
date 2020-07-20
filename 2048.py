#!/usr/bin/env python

from board2048 import Board

spel = Board()
print(spel)

if __name__ == "__main__":
    while spel.check_if_moves_possible():
        getch = input()[0]
        if getch == ",":
            old_board = spel.board
            spel.move_up()
            if spel.did_board_change(old_board):
                spel.add_random()
        elif getch == "o":
            old_board = spel.board
            spel.move_down()
            if spel.did_board_change(old_board):
                spel.add_random()
        elif getch == "a":
            old_board = spel.board
            spel.move_left()
            if spel.did_board_change(old_board):
                spel.add_random()
        elif getch == "e":
            old_board = spel.board
            spel.move_right()
            if spel.did_board_change(old_board):
                spel.add_random()
        elif getch == "q":
            break
        else:
            pass
        print(spel)
