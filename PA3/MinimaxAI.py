import chess
from time import sleep
import random

class MinimaxAI():
    def __init__(self, max_depth=3):
        self.max_depth = max_depth  # maximum depth
        self.curr_depth = 0         # print out current depth
        self.minmax_count = 0       # print out no. of calls

        self.inital_min = True
        self.initial_max = True
        self.last_max = True        # boolean for printing depth at last max
        self.last_min = True        # boolean for printing depth at last min
    #.turn, .ischeckman

    def utility(self, board, depth):


        # material value heuristic for each piece
        piece_weights = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 5, "k": 100000}

        utility = 0

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
        utility += random.random()

        print("utility: ", utility)
        return utility

        # piece_counts_p =  {"p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "k": 0}
        # piece_counts_o =  {"p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "k": 0}

        checkmate, checkmated = True, True

        # scan the board
        # for c in "abcdefgh":
        #     for r in "12345678":
        #         # find the piece at the board
        #         piece = board.piece_at(chess.parse_square(str(c)+str(r)))
        #         if piece:
        #             piece = piece.symbol()
        #             # add player's surviving pieces
        #             #if piece.islower():
        #             if piece.isupper():
        #                 if piece == "K":
        #                     checkmated = False
        #                 piece_counts_p[piece.lower()] += 1
        #                 #piece_counts_p[piece] += 1
        #
        #                 #utility += piece_weights[piece]
        #             # subtract opponent's pieces
        #             else:
        #                 #utility -= piece_weights[piece.lower()]
        #                 if piece == "k":
        #                     checkmate = False
        #                 piece_counts_o[piece] += 1
        #                 #piece_counts_o[piece.lower()] += 1
        #
        # for k, v in piece_counts_p.items():
        #     utility += piece_weights[k]*(v**2)
        #
        # for k, v in piece_counts_o.items():
        #     utility -= piece_weights[k]*(v**2)



        # print("utility val:", utility)
        # # if there are equal number of both pieces, choose random float
        # return (utility + random.random())

    def cutoff_test(self, board, depth):
        if depth >= self.max_depth:
            print("max depth")
            return True
        elif board.is_checkmate():
            return True
        elif board.is_stalemate():
            print("stalemate")
            return True
        else:
            return False

    def max_value(self, board, depth):

        # if self.initial_max:
        #     print("max function at depth: ", depth)
        #     self.initial_max = False

        # if we have reached maximum depth
        #if board.is_game_over() or depth >= self.max_depth:
        if self.cutoff_test(board, depth):
            if self.last_max and not self.initial_max:
                #print("max function at depth: ", depth)
                self.last_max = False
            # return utility of current state
            return self.utility(board, depth)

        v = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            v = max(v, self.min_value(board, depth + 1))
            board.pop()

        if self.initial_max:
            print("max function at depth: ", depth)
            self.initial_max = False
        return v

    def min_value(self, board, depth):

        # if self.initial_min:
        #     print("min function at depth: ", depth)
        #     self.initial_min = False

        # if we have reached maximum depth
        #if board.is_game_over() or depth >= self.max_depth:
        if self.cutoff_test(board, depth):
            if self.last_min and not self.initial_min:
                #print("min function at depth: ", depth)
                self.last_min = False
            # return utility of current state
            return self.utility(board, depth)

        v = float('inf')
        for move in board.legal_moves:
            board.push(move)
            v = min(v, self.max_value(board, depth + 1))
            # initial_max = False
            board.pop()
        if self.initial_min:
            print("min function at depth: ", depth)
            self.initial_min = False

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