#!/usr/bin/env python

from board2048 import Board
from nn import neuralNetwork
import numpy as np
from random import random
import json


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
    ''' Plays one game. Still needs manual editing to switch between
        random-player and neural network.
        Returns max value on final board and all boards of current game.
    '''
    count_moves = 0
    one_game = {}
    while spel.check_if_moves_possible() and count_moves < max_moves:
        # TODO: make random/neural player a choice in the game.
#        inputs = np.asfarray(spel.normalise_board())
#        outputs = nn.query(inputs)
#        direction = np.argmax(outputs)
        direction = random_direction()
        old_board = spel.board
        spel.move_score = 0
        one_move = {}
        # TODO: refactor if-loop below. seems too complicated.
        if direction == 0:
            spel.move_up()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                one_move["score"] = spel.move_score
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 1:
            spel.move_down()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                one_move["score"] = spel.move_score
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 2:
            spel.move_left()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                one_move["score"] = spel.move_score
                spel.add_random()
            else:
                count_moves -= 1
        elif direction == 3:
            spel.move_right()
            if spel.did_board_change(old_board):
                one_move["board"] = old_board
                one_move["direction"] = direction
                one_move["score"] = spel.move_score
                spel.add_random()
            else:
                count_moves -= 1
        else:
            pass
        if spel.did_board_change(old_board):
            spel.score += spel.move_score
            one_game["move_" + str(count_moves)] = one_move
        count_moves += 1
        print(spel)
        print("Richting: {}".format(direction))
#        getch=input()
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


def find_boards(nn, number_of_boards, min_max_value):
    ''' Plays game until number_of_boards amount of plays with at least
        min_max_value have been found. E.g 100 games that reached 512.
        Returns list with the boards and direction and a list with the
        number of games needed to play.
    '''
    # for each found game this is the number of games needed to play.
    counting_total_games = []
    games = {}
    while len(counting_total_games) < number_of_boards:
        nmr_games = 0
        max_val = 0
        while max_val < min_max_value:
            # Create instance of 2048 game
            spel = Board()
            high_game_value, game_steps = play_one_game(spel, nn)
            if high_game_value > max_val:
                max_val = high_game_value
            nmr_games += 1
        print(spel)
#        print(game_steps[-1])
        games["game_" + str(len(counting_total_games))] = game_steps
        counting_total_games += [nmr_games]
        # for i in game_steps:
        #     print("{}: {}".format(i, game_steps[i]))
    # TODO: clear games of movements after reaching highest values. Now the
    # game continues after that until board is no longer playable.
    return games, counting_total_games

def remove_moves_after_highest(games):
    ''' After reaching the highest value the game continues until the board
        is not playable anymore. These extra moves can be removed.
    '''
    small_games = {}
    for game in games:
        highest = 0
        # find highest value in this game
        for move in games[game]:
            this_max = max(move[board])
            if this_max > highest:
                highest = this_max
        # add highest value to game as a key
        small_games[game] = {}
        small_games[game][high_value] = highest
        # find all moves until highests value is reached
        for move in games[game]:
            if max(move[board]) < highest:
                small_games[game][move] = move
    return small_games

def get_play_choice():
    possible = ["C", "L", "M"]
    getch =[]
    questions = [f'\033[2J' + f'\033[H' + "Create new games json-file : [C]",
                 "Learn from json-file       : [L]",
                 "Use Markov method          : [M]"]
    while len(getch) < 1 or getch[0].upper() not in possible:
        for i in questions:
            print(i)
        getch = input("Answer: ")
    return getch[0].upper()


if __name__ == "__main__":
    # Create instance of neural network
    nn = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    answer = get_play_choice()
    if answer == 'C':
        games, counting_total_games = find_boards(nn, 2, 256)
        games["counting_games"] = counting_total_games
        print("Total nmr games: {}".format(counting_total_games))
        # Writing to sample.json
        json_object = json.dumps(games, indent=4, sort_keys=False)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
    elif answer == 'L':
        pass
    elif answer == 'M':
        pass
    else:
        pass
