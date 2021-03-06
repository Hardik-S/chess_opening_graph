# A Graphical Visualization of Chess Openings
# April 2020

# Provides a colorful multi-level pie chart which shows the popularity of openings after moves
# For more info, go to www.github.com/Destaq/opening_analysis

import plotly.graph_objects as go
import chess.pgn, time, random, collections
from collections import Counter


def create_game_list(pgn, depth):
    """ we have one massive pgn that we convert to a list of normal game pgns """
    game_list = []
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:  # continue until exhausted all games
            break
        else:
            if len(list(game.mainline_moves())) > depth - 1:  # for graph visualization
                game_list.append(game)
    return game_list


def parse_individual_games(pgn, depth):
    """ convert each game in the list to SAN format """
    full_list = []
    game_list = create_game_list(pgn, depth)
    for game in game_list:
        small_list = []  # essentially only that game's list
        board = game.board()
        turn = 0
        for move in game.mainline_moves():
            if turn < depth:  # only count moves to needed depth
                turn += 1
                small_list.append(chess.Board.san(board, move=move))
                board.push(move)
            else:
                break
        full_list.append(small_list)

    return full_list


def form_values(depth):
    firstx = [lst[i][:depth]
              for i in
              range(len(lst))]  # probably unneeded but for safety's sake...

    all_level_moves, exclude_first_moves = [], []  # for parent/labels later
    counter = 0
    holder = [firstx[i][0]
              for i in
              range(len(firstx))]
    holder = dict(Counter(holder))

    while counter < depth:
        if counter == 0:
            first_move = list(Counter(
                [tuple(firstx[i][:1])
                 for i in
                 range(len(lst))]).items())  # list of first ply moves based on popularity
            all_level_moves.append(first_move)
            counter += 1

        else:
            counter += 1
            other_move = list(Counter([tuple(firstx[i][:counter])
                                       for i in
                                       range(len(lst))]).items())
            all_level_moves.append(other_move)
            exclude_first_moves.append(other_move)  # obviously excluding first moves (for parent creation)

    pz = []
    true_ids = []  # the ids, that is
    parents = []
    labels = []

    for i in range(len(all_level_moves)):
        labels += [all_level_moves[i][f][0][i]
                   for f in
                   range(len(all_level_moves[i]))]  # similar to hackerrank diagonal

        if i == 0:
            true_ids = [all_level_moves[0][r][0]
                        for r in
                        range(len(all_level_moves[0]))]  # special ids for original parents
            true_ids = [item
                        for sublist in
                        true_ids
                        for item in sublist]  # functions perfectly
            firstcount = len(labels)
        else:
            true_ids += [all_level_moves[i][r][0]
                         for r in
                         range(len(all_level_moves[i]))]
            parents += [all_level_moves[i][r][0][:len(all_level_moves[i][r][0]) - 1]
                        for r in
                        range(len(all_level_moves[i]))]

        pz += [z[0][:i]
               for ply_depth in
               exclude_first_moves
               for z in ply_depth]

    parents = [''] * firstcount + parents  # flattening

    ids = true_ids
    values = [i[1]
              for i in
              first_move] + [i[1]
                             for move in
                             exclude_first_moves
                             for i in move]

    # print(f'\n\nIDS: {ids}\n\nLABELS: {labels}\n\nPARENTS: {parents}\n\nVALUES: {values}')

    return ids, labels, parents, values


def form(ids, labels, parents, values):
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues='total',  # if children exceed parent, graph will crash and not show
        insidetextorientation='horizontal'  # text displays PP
    ))
    return fig


user_input_game_file = input('Which game file should be analyzed? Provide FULL path file. ')
myGame = open(user_input_game_file)
user_input_depth = int(input('To what ply depth should we visualize these games? '))
lst = parse_individual_games(myGame, user_input_depth)  # ask for input here

ids, labels, parents, values = form_values(user_input_depth)

fig = form(ids, labels, parents, values)

fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

fig.show()
