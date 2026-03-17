from abc import ABC, abstractmethod
from board import Board 

class Player(ABC):
    def __init__(self, player_id: int):
        self.player_id = player_id    # 0 or 1
        
    @abstractmethod
    def get_move(self, board: Board) -> int:
        # returns pit index chosen by player
        pass

    def __str__(self):
        return f"Player {self.player_id}"
    
class HumanPlayer(Player):
    def get_move(self, board: Board) -> int:
        # for valid internal indices (es [0,1,2,3...] or  [7,8,9,...])
        valid_indices = board.get_valid_moves(self.player_id)   # changed from valid to valid_indices

        # Convert once (instead of previous if 1/else 2)
        # to_display: convert internal index -> user-visible number (1-6)
        # to_index: convert user input -> internal index
        if self.player_id == 0:
            to_display = lambda p: p + 1    # index 0-5 -> pit 1-6
            to_index = lambda x: x - 1
        else:
            to_display = lambda p: p - 6    # index 7-12 -> pit 1-6
            to_index = lambda x: x + 6

        # used a set {} instead of a list [] for faster membership check
        valid_display = {to_display(p) for p in valid_indices}

        # loop until user gives valid input
        while True:
            try:
                pit_num = int(input(f"Player {self.player_id}, choose pit (1-6): "))

                if pit_num not in valid_display:
                    print(f"Invalid move. Choose from: {sorted(valid_display)}")
                    continue

                return to_index(pit_num)

            except ValueError:
                print("Please enter a number between 1 and 6.")