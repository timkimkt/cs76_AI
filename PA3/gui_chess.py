# brew install pyqt
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget
import sys
import chess, chess.svg
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame
from HumanPlayer import HumanPlayer
from AlphaBetaAI import AlphaBetaAI
from IterativeAI import IterativeAI

import random
import time

class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)

    def make_move(self):

        print("making move, white turn " + str(self.game.board.turn))
        #print(self.game)
        if not self.game.is_game_over():
            self.game.make_move()
        else:
            print("game result: ", self.game.board.result())
            self.timer.stop()  # Added this line to stop the timer and the call to make_move() so that the print will not be repeated over and over
        self.display_board()

if __name__ == "__main__":

    random.seed(1)

    #player_ronda = RandomAI()

    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    #   with event loop.

    # call Minmax AI with max depth

    # call Alphabeta AI with max depth
    #player1 = AlphaBetaAI(3)

    # call IterativeDeepening with maxdepth
    #player1 = IterativeAI()

    #player1 = MinimaxAI(True, 2)
    player1= AlphaBetaAI(True, 2)
    player2 = RandomAI()

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
    ## Insert example with Minmax AI

