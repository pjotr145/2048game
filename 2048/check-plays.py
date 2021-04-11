#!/usr/bin/env python

from board2048 import Board
import json
import pickle
import matplotlib.pyplot as plt

# Create instance of 2048 game
spel = Board()
directions = {0:"up",
              1:"down",
              2:"left",
              3:"right"}
games_list = []
moves_list = []
moves_needed = []
max_scores = []
file_list = ["sample.json"]

def remove_moves_after_highest(games):
    ''' After reaching the highest value the game continues until the board
        is not playable anymore. These extra moves can be removed.
    '''
    small_games = {}
    max_scores = []
    for game in games:
        highest = 0
        highest_move = ""
        # find highest value in this game
        for move in games[game]:
            this_max = max(games[game][move]["board"])
            if this_max > highest:
                highest_move = move
                highest = this_max
        max_scores.append(highest)
        small_games[game] = {}
        # find all moves until highests value is reached
        for move in games[game]:
            if max(games[game][move]["board"]) < highest:
                small_games[game][move] = games[game][move]
        small_games[game][highest_move] = games[game][highest_move]
    return small_games, max_scores


if __name__ == "__main__":
    with open("data/sample.json") as f:
        games = json.load(f)
    counting_games = games["counting_games"]
    games.pop("counting_games")
    # Remove unneeded moves and get highest game values
    games, max_scores = remove_moves_after_highest(games)
    moves_needed = []
    # Get number of moves for each game
    for game in games:
        moves_needed.append(len(games[game]))
    json_object = json.dumps(games, indent=4, sort_keys=False)
    with open("data/test.json", "w") as f:
        f.write(json_object)

    print("Number of games needed: {}".format(counting_games))
    print("Number of moves needed: {}".format(moves_needed))
#    print("Highest value reached : {}".format(max_scores))
    # Plot graph. bins = number of collumns in groph.
    plt.style.use('ggplot')
    plt.hist(moves_needed, bins=50)
#    plt.show()
    plt.hist(counting_games, bins=50)
    plt.show()
    print("start")
    for game in games:
        for move in games[game]:
            getch = input()
            if getch == "q":
                break
            else:
                spel.board = games[game][move]["board"]
                print(spel)
                print("Points this move: {}".format([games[game][move]["score"]][0]))
                print("Direction: {}".format(directions[games[game][move]["direction"]]))
                print("Direction: {}".format([games[game][move]["direction"]][0]))
                moves_list.append([games[game][move]["direction"]][0])
                print("Game: {}".format(games[game][move]["board"]))
                games_list.append(games[game][move]["board"])


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
