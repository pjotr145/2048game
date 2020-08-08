#!/usr/bin/env python

from board2048 import Board
import json

# Create instance of 2048 game
spel = Board()
#print(spel)
directions = {0:"up",
              1:"down",
              2:"left",
              3:"right"}

if __name__ == "__main__":
    with open("sample-256-10000.json") as f:
        games = json.load(f)
    print("start")
    for game in games:
        for move in games[game]:
            getch = input()
            spel.board = games[game][move]["board"]
            print(spel)
            print("Direction: {}".format(directions[games[game][move]["direction"]]))


#    while spel.check_if_moves_possible():
#        getch = input()[0]
#        if getch == ",":
#            spel.move_up()
#            spel.add_random()
#        elif getch == "o":
#            spel.move_down()
#            spel.add_random()
#        elif getch == "a":
#            spel.move_left()
#            spel.add_random()
#        elif getch == "e":
#            spel.move_right()
#            spel.add_random()
#        elif getch == "q":
#            break
#        else:
#            pass
#        print(spel)
