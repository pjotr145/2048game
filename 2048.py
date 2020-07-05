#!/usr/bin/env python

from board2048 import Board

spel = Board()
print(spel)

if __name__ == "__main__":
    while spel.check_if_moves_possible():
        getch = input()[0]
        if getch == ",":
            spel.move_up()
            spel.add_random()
        elif getch == "o":
            spel.move_down()
            spel.add_random()
        elif getch == "a":
            spel.move_left()
            spel.add_random()
        elif getch == "e":
            spel.move_right()
            spel.add_random()
        else:
            pass
        print(spel)
        print(spel.normalise_board())
