#!/usr/bin/env python

from board2048 import Board
from nn import neuralNetwork
import numpy as np
from random import random

# Number of input, hidden and outputnodes
input_nodes = 16
hidden_nodes = 25
output_nodes = 4

# Learning rate
learning_rate = 0.1

# Max number of moves per game
max_moves = 300
# Max number of games
max_games = 1000

def play_one_game(spel, nn):
    teller = 0
#    while spel.check_if_moves_possible() and teller < max_moves:
    while spel.check_if_moves_possible():
#        inputs = np.asfarray(spel.normalise_board())
#        outputs = nn.query(inputs)
#        direction = np.argmax(outputs)
        direction = random_direction()
        if direction == 0:
            spel.move_up()
            spel.add_random()
        elif direction == 1:
            spel.move_down()
            spel.add_random()
        elif direction == 2:
            spel.move_left()
            spel.add_random()
        elif direction == 3:
            spel.move_right()
            spel.add_random()
        else:
            pass
        teller += 1
    return max(spel.board)

def random_direction():
    rand_direction = random()
    if rand_direction < 0.25:
        return 0
    elif rand_direction < 0.5:
        return 1
    elif rand_direction < 0.75:
        return 2
    else:
        return 3


# Create instance of neural network
nn = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
# Create instance of 2048 game
#spel = Board()
#print(spel)
counter = 0
max_val = 0
if __name__ == "__main__":
    while max_val < 512:
        spel = Board()
#        print("New game: {}".format(spel.board))
        teller = 0
#        while spel.check_if_moves_possible() and teller < max_moves:
        while spel.check_if_moves_possible():
#            inputs = np.asfarray(spel.normalise_board())
#            outputs = nn.query(inputs)
#            direction = np.argmax(outputs)
            direction = random_direction()
            if direction == 0:
                spel.move_up()
                spel.add_random()
            elif direction == 1:
                spel.move_down()
                spel.add_random()
            elif direction == 2:
                spel.move_left()
                spel.add_random()
            elif direction == 3:
                spel.move_right()
                spel.add_random()
            else:
                pass
            teller += 1
        if max(spel.board) > max_val:
            max_val = max(spel.board)
        counter +=1
    print(spel)
#    print(spel.board)
    print("Aantal spellen: {}".format(counter))
