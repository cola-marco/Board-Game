from board import Board
from player import Player


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = {1: player1, 2: player2}
        self.current = 1  # player 1 starts

    def switch_player(self):
        self.current = 3 - self.current

    def play(self) -> int:
        print("\n=== KALAHA ===\n")
        print(self.board)
        print()

        while not self.board.check_end():
            player = self.players[self.current]
            print(f"--- {player}'s turn ---")

            pit = player.get_move(self.board)
            extra_turn, captured = self.board.sow(self.current, pit)

            # Convert pit index to pit number for display
            pit_num = pit + 1 if self.current == 1 else pit - 6
            print(f"Player {self.current} sows from pit {pit_num}")

            if captured:
                print("Capture!")
            if extra_turn:
                print("Extra turn!")

            print()
            print(self.board)
            print()

            if not extra_turn:
                self.switch_player()

        # Game over — collect remaining seeds
        self.board.collect_remaining()
        print("=== GAME OVER ===")
        print(self.board)
        print()

        winner = self.board.get_winner()
        s1 = self.board.cells[self.board.get_store(1)]
        s2 = self.board.cells[self.board.get_store(2)]
        print(f"Player 1 seeds: {s1}")
        print(f"Player 2 seeds: {s2}")

        if winner == 0:
            print("It's a draw!")
        else:
            print(f"Player {winner} wins!")

        return winner
