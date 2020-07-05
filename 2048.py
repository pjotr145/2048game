#!/usr/bin/env python

from board2048 import Board

spel = Board()
print(spel)
can_play = True
while spel.check_if_moves_possible():
    getch = input()[0]
#    print("Letter: {}".format(getch))
    if getch == ",":
        spel.move_up()
    elif getch == "o":
        spel.move_down()
    elif getch == "a":
        spel.move_left()
    elif getch == "e":
        spel.move_right()
    else:
        pass
    spel.add_random()
    print(spel)
    can_play = spel.check_if_moves_possible()
