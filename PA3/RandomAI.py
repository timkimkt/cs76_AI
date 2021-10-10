#import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        #f moves:
        move = random.choice(moves)
        sleep(1)   # I'm thinking so hard.
        print("------------------------------------------")
        print("Random AI recommending move " + str(move))
        return move
