import chess
from math import inf


import chess
from time import sleep
import random

class AlphaBetaAI():
    def __init__(self, max_depth=3):
        self.max_depth = max_depth  # maximum depth
        self.curr_depth = 0         # print out current depth
        self.minmax_count = 0       # print out no. of calls

        self.inital_min = True
        self.initial_max = True
        self.last_max = True        # boolean for printing depth at last max
        self.last_min = True        # boolean for printing depth at last min
    #.turn, .ischeckman

    def utility(self, board):
        # material value heuristic for each piece
        piece_weights = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 5, "k": 100000}
        piece_counts_p =  {"p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "k": 0}
        piece_counts_o =  {"p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "k": 0}

        utility = 0
        checkmate, checkmated = True, True

        # scan the board
        for c in "abcdefgh":
            for r in "12345678":
                # find the piece at the board
                piece = board.piece_at(chess.parse_square(str(c)+str(r)))
                if piece:
                    piece = piece.symbol()
                    # add player's surviving pieces
                    if piece.islower():
                        if piece == "k":
                            checkmated = False
                        piece_counts_p[piece] += 1
                        #utility += piece_weights[piece]
                    # subtract opponent's pieces
                    else:
                        #utility -= piece_weights[piece.lower()]
                        if piece == "K":
                            checkmate = False
                        piece_counts_o[piece.lower()] += 1
        # if there are equal number of both pieces, choose random float
        # if utility == 0:
        #     utility = random.random()
        for k, v in piece_counts_p.items():
            utility += piece_weights[k]*(v**2)

        for k, v in piece_counts_o.items():
            utility -= piece_weights[k]*(v**2)
        #
        # if checkmated:
        #     utility = float('-inf')
        #
        # elif checkmate:
        #     utility = float('inf')

        #print("utility val:", utility)
        return (utility + random.random())

    def max_value(self, board, depth):

        if self.initial_max:
            print("max function at depth: ", depth)
            self.initial_max = False

        # if we have reached maximum depth
        if board.is_game_over() or depth >= self.max_depth:
            if self.last_max and self.initial_max:
                print("max function at depth: ", depth)
                self.last_max = False
            # return utility of current state
            return self.utility(board)

        v = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            v = max(v, self.min_value(board, depth + 1))
            board.pop()

        return v

    def min_value(self, board, depth):

        if self.initial_min:
            print("min function at depth: ", depth)
            self.initial_min = False

        if board.is_checkmate():
            print('checkmateD!')
            return -200

        # if we have reached maximum depth
        if board.is_game_over() or depth >= self.max_depth:
            if self.last_min and self.initial_min:
                print("min function at depth: ", depth)
                self.last_min = False
            # return utility of current state
            return self.utility(board)

        v = float('inf')
        for move in board.legal_moves:
            board.push(move)
            v = min(v, self.max_value(board, depth + 1))
            # initial_max = False
            board.pop()

        return v

    def minmax(self, board):
        self.minmax_count += 1
        print("Number of calls made to minmax fn: ", self.minmax_count)

        # variables for max utility and corresponding move
        utility_max, move_max = float('-inf'), ""
        self.initial_min = True
        self.initial_max = True

        for move in board.legal_moves:
            board.push(move)
            # find out the utility of the move
            utility_move = self.min_value(board, 1)
            # self.initial_min = False
            # if it is greater than current maximum
            if (utility_move > utility_max):
                utility_max = utility_move  # store max utility val
                move_max = move             # store corresponding move
            board.pop()

        # boolean for printing depth at last min/max
        self.last_min, self.last_max = True, True
        # return the move with max utility
        return move_max

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = self.minmax(board)
        sleep(1)   # I'm thinking so hard.
        print("------------------------------------------")
        print("Minmax AI recommending move " + str(move))
        return move
