# Class: COSC 76
# Assignment: PA 3
# Date: Oct 11, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22


import chess
from time import sleep
import random
import collections

class IterativeAI():
    def __init__(self, player, max_depth=3):
        self.player = player
        self.max_depth = max_depth  # maximum depth
        self.curr_depth = 0         # print out current depth
        self.iterative_count = 0       # print out no. of calls

        self.inital_min = True
        self.initial_max = True
        self.last_max = True        # boolean for printing depth at last max
        self.last_min = True        # boolean for printing depth at last min

        self.node_count = 0
        self.utility_calls = 0

    def utility(self, board):

        # material value heuristic for each piece
        piece_weights = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 5, "k": 100000}

        utility = 0

        # check for stalemate
        if board.is_stalemate() or board.is_fivefold_repetition() or board.is_insufficient_material():
            return 0

        # check for fivefold repetition
        if board.is_checkmate():
            if self.player == board.turn:
                return -100000
            else:
                return 100000

        # Add the utility of white pieces
        utility += piece_weights["p"] * len(board.pieces(chess.PAWN, chess.WHITE))
        utility += piece_weights["n"] * len(board.pieces(chess.KNIGHT, chess.WHITE))
        utility += piece_weights["b"] * len(board.pieces(chess.BISHOP, chess.WHITE))
        utility += piece_weights["r"] * len(board.pieces(chess.ROOK, chess.WHITE))
        utility += piece_weights["q"] * len(board.pieces(chess.QUEEN, chess.WHITE))
        utility += piece_weights["k"] * len(board.pieces(chess.KING, chess.WHITE))

        # subtract the utility of black pieces
        utility -= piece_weights["p"] * len(board.pieces(chess.PAWN, chess.BLACK))
        utility -= piece_weights["n"] * len(board.pieces(chess.KNIGHT, chess.BLACK))
        utility -= piece_weights["b"] * len(board.pieces(chess.BISHOP, chess.BLACK))
        utility -= piece_weights["r"] * len(board.pieces(chess.ROOK, chess.BLACK))
        utility -= piece_weights["q"] * len(board.pieces(chess.QUEEN, chess.BLACK))
        utility -= piece_weights["k"] * len(board.pieces(chess.KING, chess.BLACK))


        # add randomness to account for utility being same for all moves
        return utility if self.player else -utility

    def cutoff_test(self, board, depth):
        if depth >= self.max_depth:
            return True
        elif board.is_checkmate():
            return True
        elif board.is_stalemate():
            return True
        else:
            return False

    def max_value(self, board, depth, alpha, beta):

        # Debugging: self.node_count += 1
        # condition for print statements
        if self.initial_max:
            print("max function at depth: ", depth)
            self.initial_max = False

        # check if condition for cutoff is met
        if self.cutoff_test(board, depth):
            # return utility of current state
            return self.utility(board)

        # push move and call min_value fn
        v = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            v = max(v, self.min_value(board, depth + 1, alpha, beta))
            if v >= beta:
                board.pop()        # pop move before returning
                return v
            alpha = max(alpha, v)
            board.pop()

        # return utility value
        return v

    def min_value(self, board, depth, alpha, beta):

        # Debugging: self.node_count += 1

        # condition for print statement
        if self.initial_min:
            print("min function at depth: ", depth)
            self.initial_min = False

        # check if condition for cutoff is met
        if self.cutoff_test(board, depth):
            # return utility of current state
            return self.utility(board)

        # push move and call min_value fn
        v = float('inf')
        for move in board.legal_moves:
            board.push(move)
            v = min(v, self.max_value(board, depth + 1, alpha, beta))
            if v <= alpha:
                board.pop()        # pop move before returning
                return v
            beta = min(beta, v)
            board.pop()
        # return utility
        return v


    def alphabeta(self, board):
        self.iterative_count += 1
        print("Number of calls made to alphabeta fn: ", self.iterative_count)

        # variables for max utility and corresponding move
        utility_max, move_max = float('-inf'), ""
        self.initial_min, self.initial_max = True, True # booleans for printing
        # alpha, beta for pruning
        alpha, beta = float('-inf'), float('inf')

        # turn legal_moves into list to shuffle
        legal_moves = list(board.legal_moves)

        # shuffle the moves to prevent repeated moves
        random.shuffle(legal_moves)

        for d in range(1, self.max_depth+1):

            # for all moves sorted by highest utility
            for move in legal_moves:
                # make the move
                board.push(move)
                # find out the utility of the move
                utility_move = self.min_value(board, d, alpha, beta)
                # if it is greater than current maximum
                if (utility_move > utility_max):
                    utility_max = utility_move  # store max utility val
                    move_max = move             # store corresponding move
                # undo the move
                board.pop()

            print("The best move for depth ", d, "is ", move_max, "with utility of ", utility_max)

        # boolean for printing depth at last min/max
        self.last_min, self.last_max = True, True

        # Debugging (utility of move chosen)
        print("Utility of move selected", utility_max)

        # return the move with max utility
        return move_max

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = self.alphabeta(board)
        #sleep(1)   # I'm thinking so hard.
        print("------------------------------------------")
        print("Iterative AI recommending move " + str(move))
        return move