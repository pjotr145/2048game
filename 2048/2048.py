#!/usr/bin/env python

from board2048 import Board
from nn import neuralNetwork
import numpy as np
from random import random, getrandbits
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


montecarlo_width = 5
montecarlo_depth = 5


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
        if direction == 0:
            spel.move_up()
        elif direction == 1:
            spel.move_down()
        elif direction == 2:
            spel.move_left()
        elif direction == 3:
            spel.move_right()
        else:
            pass
        if spel.did_board_change(old_board):
            one_move["board"] = old_board
            one_move["direction"] = direction
            one_move["score"] = spel.move_score
            spel.add_random()
        else:
            count_moves -= 1
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

def play_one_game_with_montecarlo(new_game, mc_width = 100, mc_depth = 20):
    '''
    while moves are possible
        simulate all 4 directions
            each with mc_width games played for mc_depth moves.
        select direction with highest score
        play that direction
    return highest value on board and the played game
    '''
    count_moves = 0
    one_game = {}
    all_directions = [0, 1, 2, 3]       # up, down, left, right
    spel = new_game
    while spel.check_if_moves_possible() and count_moves < max_moves:
        # While moves are possible and total number of moves below limit
        scores = [0, 0, 0, 0]
        for this_move in all_directions:
            # for each of the 4 directions
            this_game = Board()
            this_game.board = spel.board
            this_game.move_in_direction(this_move)
            if this_game.board_changed:
                # Only if that first move does anything
                sim_start_board = this_game.board
                for _ in range(mc_width):
                    # Simulate multiple games to get some sort af average
                    depth_count = 0
                    this_game.board = sim_start_board
                    # start every sim with same start board
                    while this_game.check_if_moves_possible() and \
                    depth_count < mc_depth:
                        this_game.move_in_direction(getrandbits(2))
                        if this_game.board_changed:
                            this_game.add_random()
                            depth_count += 1
                            scores[this_move] += this_game.move_score
        # Needs int() because json can't handle numpy int64.
        direction = int(np.argmax(scores))
        one_move = {}
        one_move["board"] = spel.board
        one_move["direction"] = direction
        spel.move_in_direction(direction)
        one_move["score"] = spel.move_score
        one_game["move_" + str(count_moves)] = one_move
        spel.add_random()
        spel.score += spel.move_score
        count_moves += 1
        print(spel)
        print("Scores: {}".format(scores))
        print(count_moves)
    return max(spel.board), one_game

def find_mc_boards(number_of_boards, min_max_value):
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
            high_game_value, game_steps = play_one_game_with_montecarlo(spel,
                                                           montecarlo_width,
                                                           montecarlo_depth)
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

def play_games(choice):
    if choice == 'C':
        games, counting_total_games = find_boards(nn, 2, 256)
    elif choice == 'M':
        games, counting_total_games = find_mc_boards(500, 512)
    games["counting_games"] = counting_total_games
    print("Total nmr games: {}".format(counting_total_games))
    # Writing to sample.json
    json_object = json.dumps(games, indent=4, sort_keys=False)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

def get_play_choice():
    possible = ["C", "L", "M"]
    getch =[]
    questions = [f'\033[2J' + f'\033[H' + "Create new games json-file : [C]",
                 "Learn from json-file       : [L]",
                 "Use Monte Carlo method     : [M]"]
    while len(getch) < 1 or getch[0].upper() not in possible:
        for i in questions:
            print(i)
        getch = input("Answer: ")
    return getch[0].upper()


if __name__ == "__main__":
    # TODO: refactor main
    # TODO: read variables from config file
    with open("config.json") as f:
        conf = json.load(f)
    # Create instance of neural network
    nn = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    answer = get_play_choice()
    if answer == 'C':
        play_games(answer)
    elif answer == 'L':
        pass
    elif answer == 'M':
        play_games(answer)
    else:
        pass
    print("mc_width: {}".format(conf["montecarlo_width"]))
