import chess
from time import sleep
import random

class IterativeAI():
    def __init__(self, max_depth=3):
        self.max_depth = max_depth  # maximum depth
        self.curr_depth = 0         # print out current depth
        self.alphabeta_count = 0       # print out no. of calls

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
        utility += piece_weights["p"] * len(board.pieces(chess.PAWN, chess.WHITE))**2
        utility += piece_weights["n"] * len(board.pieces(chess.KNIGHT, chess.WHITE))**2
        utility += piece_weights["b"] * len(board.pieces(chess.BISHOP, chess.WHITE))**2
        utility += piece_weights["r"] * len(board.pieces(chess.ROOK, chess.WHITE))**2
        utility += piece_weights["q"] * len(board.pieces(chess.QUEEN, chess.WHITE))**2
        utility += piece_weights["k"] * len(board.pieces(chess.KING, chess.WHITE))**2

        # subtract the utility of black pieces
        utility -= piece_weights["p"] * len(board.pieces(chess.PAWN, chess.BLACK))**2
        utility -= piece_weights["n"] * len(board.pieces(chess.KNIGHT, chess.BLACK))**2
        utility -= piece_weights["b"] * len(board.pieces(chess.BISHOP, chess.BLACK))**2
        utility -= piece_weights["r"] * len(board.pieces(chess.ROOK, chess.BLACK))**2
        utility -= piece_weights["q"] * len(board.pieces(chess.QUEEN, chess.BLACK))**2
        utility -= piece_weights["k"] * len(board.pieces(chess.KING, chess.BLACK))**2

        # add randomness to account for utility being same for all moves
        utility += random.random()
        if board.turn == chess.WHITE:
            if board.is_checkmate:
                return (utility - 50)/depth
        else:
            if board.is_checkmate:
                return (utility + 50)/depth
        print("utility: ", utility/depth)
        return utility/depth

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

        if self.initial_max:
            print("max function at depth: ", depth)
            self.initial_max = False

        # if we have reached maximum depth
        if self.cutoff_test(board, depth):
            if self.last_max and self.initial_max:
                print("max function at depth: ", depth)
                self.last_max = False
            # return utility of current state
            return self.utility(board, depth)

        v = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            v = max(v, self.min_value(board, depth + 1, alpha, beta))
            if v >= beta:
                board.pop()
                return v
            alpha = max(alpha, v)
            board.pop()

        return v

    def min_value(self, board, depth, alpha, beta):

        if self.initial_min:
            print("min function at depth: ", depth)
            self.initial_min = False

        # if we have reached maximum depth
        if self.cutoff_test(board, depth):
            if self.last_min and self.initial_min:
                print("min function at depth: ", depth)
                self.last_min = False
            # return utility of current state
            return self.utility(board, depth)

        v = float('inf')
        for move in board.legal_moves:
            board.push(move)
            v = min(v, self.max_value(board, depth + 1, alpha, beta))
            if v <= alpha:
                board.pop()
                return v
            beta = min(beta, v)
            board.pop()

        return v

    def alphabeta(self, board):
        self.alphabeta_count += 1
        print("Number of calls made to alphabeta fn: ", self.alphabeta_count)

        # variables for max utility and corresponding move
        utility_max, best_move = float('-inf'), ""
        self.initial_min = True
        self.initial_max = True
        # alpha, beta for pruning
        alpha, beta = float('-inf'), float('inf')
        for d in range(self.max_depth):

            for move in board.legal_moves:

            ### Iterative Deepening ###

                # make the move
                board.push(move)

                # find out the utility of the move
                utility_move = self.min_value(board, d, alpha, beta)
                # if it is greater than current maximum
                if (utility_move > utility_max):
                    utility_max = utility_move  # store max utility val
                    best_move = move             # store corresponding move
                # undo the move
                board.pop()
                # print the best move
            print("The best move for depth ", d, "is ", move)

        # boolean for printing depth at last min/max
        self.last_min, self.last_max = True, True
        # return the move with max utility
        return best_move

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = self.alphabeta(board)
        sleep(1)   # I'm thinking so hard.
        print("------------------------------------------")
        print("Iterative AI recommending move " + str(move))
        return move