from board import Board
from player import Player


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = {0: player1, 1: player2}
        self.current_player = 1

    def switch_player(self):
        self.current_player = ~self.current_player

    def start(self):
        pass