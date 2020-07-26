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
max_moves = 3000
# Max number of games
max_games = 1000


def play_one_game(spel, nn):
    count_moves = 0
    one_game = {}
#    while spel.check_if_moves_possible() and teller < max_moves:
    while spel.check_if_moves_possible() and count_moves < max_moves:
#        inputs = np.asfarray(spel.normalise_board())
#        outputs = nn.query(inputs)
#        direction = np.argmax(outputs)
        direction = random_direction()
        old_board = spel.board
        one_move = {}
        if direction == 0:
            spel.move_up()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 1:
            spel.move_down()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 2:
            spel.move_left()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 3:
            spel.move_right()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                spel.add_random()
            else:
                count_moves -= 1
        else:
            pass
        count_moves += 1
        if spel.did_board_change(old_board):
            one_game[count_moves] = one_move
    return max(spel.board), one_game


def random_direction():
    ''' Simulates a player by chosing randomly in wich direction to move '''
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

if __name__ == "__main__":
    counting_total_games = []
    while len(counting_total_games) < 3:
        nmr_games = 0
        max_val = 0
        while max_val < 512:
            # Create instance of 2048 game
            spel = Board()
            high_game_value, game_steps = play_one_game(spel, nn)
            if high_game_value > max_val:
                max_val = high_game_value
            nmr_games += 1
        print(spel)
        print("Aantal spellen: {}".format(nmr_games))
        counting_total_games += [nmr_games]
        print("Aant keer 512: {}".format(len(counting_total_games)))
        for i in game_steps:
            print("{}: {}".format(i, game_steps[i]))
    print("Total nmr games: {}".format(counting_total_games))
