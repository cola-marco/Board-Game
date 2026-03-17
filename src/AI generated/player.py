from abc import ABC, abstractmethod
from board import Board


class Player(ABC):
    def __init__(self, player_id: int):
        self.player_id = player_id  # 0 or 1

    @abstractmethod
    def get_move(self, board: Board) -> int:
        """Returns the pit index chosen by this player."""
        pass

    def __str__(self):
        return f"Player {self.player_id}"


class HumanPlayer(Player):
    def get_move(self, board: Board) -> int:
        valid = board.get_valid_moves(self.player_id)
        # Convert internal indices to pit numbers (1-6) for display
        if self.player_id == 1:
            valid_display = [p + 1 for p in valid]          # index 0-5 -> pit 1-6
        else:
            valid_display = [p - 6 for p in valid]          # index 7-12 -> pit 1-6

        while True:
            try:
                pit_num = int(input(f"Player {self.player_id}, choose pit (1-6): "))
                if pit_num not in valid_display:
                    print(f"Invalid move. Choose from: {valid_display}")
                    continue
                # Convert back to internal index
                if self.player_id == 1:
                    return pit_num - 1
                else:
                    return pit_num + 6
            except ValueError:
                print("Please enter a number between 1 and 6.")
