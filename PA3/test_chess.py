# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys

# Uncomment player below to observe behavior
# player1 = MinimaxAI(True, 3)
player1 = AlphaBetaAI(True, 3)
# player1 = IterativeAI(True, 4)
player2 = RandomAI()

# AlphaBeta playing against each other
# player1= AlphaBetaAI(True, 3)
# player2= AlphaBetaAI(False, 3)


game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
