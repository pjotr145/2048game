#!/usr/bin/env python

from board2048 import Board
import copy
#import yaml   "pyyaml"

spel = Board()
print(spel)
rij = spel.move_row([0,2,0,2])
print(rij)

test_rows = [
    [0,2,0,2],
    [4,4,4,4],
    [2,2,2,0],
    [2,0,2,4],
    [0,2,4,4],
    [4,2,2,8]
]
for row in test_rows:
    rij = spel.move_row(row)
    print("{} => {} score: {}".format(row, rij, spel.score))

test_game = [
    [0,2,0,64],
    [0,0,16,64],
    [0,2,2,256],
    [0,2,4,128]
]

#spel.board = copy.deepcopy(test_game)
spel.board = [copy.copy(i) for i in test_game]
for   i in spel.board:
    print(i)
spel.flatten_board()
print("Moving up")
spel.move_up()

for   i in spel.board:
    print(i)
if spel.board == test_game:
    print("the same")
else:
    print("different")
for i in test_game:
        print(i)
spel.board = [copy.copy(i) for i in test_game]
spel.flatten_board()
spel.move_down()
for i in spel.board:
    print(i)
spel.board = test_game

end_games = [[
    [2, 16,  2,  4],
    [4,  2,  4, 32],
    [2, 16, 32, 64],
    [4,  2,  4,  2]
],[
    [2, 16,  2,  4],
    [4,  0,  4, 32],
    [2, 16, 32, 64],
    [4,  2,  4,  2]
],[
    [2, 16,  2,  4],
    [8,  8,  4, 32],
    [2, 16, 32, 64],
    [4,  2,  4,  2]
],[
    [2, 16,  2,  4],
    [4,  2,  4, 32],
    [2,  8, 32, 64],
    [4,  8,  4,  2]
]]

for game in end_games:
    spel.board = game
    spel.flatten_board()
    if (spel.check_if_moves_possible()):
        print("True")
    else:
        print("False")
#print(spel)
