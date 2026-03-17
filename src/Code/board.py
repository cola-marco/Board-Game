from player import Player

NUM_SEEDS_PER_PIT = 4
TOT_CELLS = 14
P1_STORE = 6
P2_STORE = 13
P1_PITS = list(range(0,6))
P2_PITS = list(range(7,13))


class Board:
    def __init__(self):
        self.cells = [NUM_SEEDS_PER_PIT] * TOT_CELLS
        self.cells[P1_STORE] = 0
        self.cells[P2_STORE] = 0

    def __str__(self) -> str:
        c = self.cells
        p2_row = "  ".join(f"{c[i]:2}" for i in range(12, 6, -1))
        p1_row = "  ".join(f"{c[i]:2}" for i in range(0, 6))
        store_p2 = f"{c[P2_STORE]:2}"
        store_p1 = f"{c[P1_STORE]:2}"
        pit_labels_p2 = "  ".join(f" {i}" for i in range(6, 0, -1))
        pit_labels_p1 = "  ".join(f" {i}" for i in range(1, 7))

        lines = [
            f"        P2 <--",
            f"     [{pit_labels_p2}]",
            f"[{store_p2}] [{p2_row}]",
            f"     [{p1_row}] [{store_p1}]",
            f"     [{pit_labels_p1}]",
            f"              --> P1",
        ]
        return "\n".join(lines)
    
    def get_seeds(self, pit: int):
        return self.cells[pit]
    
    def get_opposite_seeds(self, pit: int):
        return self.cells[12 - pit]
    
    def set_opposite_seeds(self, pit: int, value: int):
        self.cells[12 - pit] = value
    
    def get_valid_moves(self, player: Player):
        return [pit for pit in (P1_PITS if player == 0 else P2_PITS) 
                if self.cells[pit] > 0]
    
    def get_winner(self):
        if P1_STORE > P2_STORE:
            return 0
        elif P2_STORE > P1_STORE:
            return 1
        return -1
    
    def collect_remaining(self):
        for pit in P1_PITS:
            self.cells[P1_STORE] += self.cells[pit]
            self.cells[pit] = 0

        for pit in P2_PITS:
            self.cells[P2_STORE] += self.cells[pit]
            self.cells[pit] = 0

    def check_game_end(self):
        return (all(self.cells[p] == 0 for p in P1_PITS) or all(self.cells[p] == 0 for p in P2_PITS))
    
    def get_current_player_store(self, player: int):
        return P1_STORE if player == 0 else P2_STORE
    
    def get_current_player_pits(self, current: Player):
        return P1_PITS if current == 1 else P2_PITS
    
    def saw(self, pit: int, player: int):
        extra_turn, capture = False, False

        seeds = self.cells[pit]
        self.cells[pit] = 0

        pos = pit
        opponent_store = P2_STORE if player == 0 else P1_STORE

        while seeds > 0:
            pos = (pos + 1) % TOT_CELLS

            if pos == opponent_store:
                continue

            self.cells[pos] += 1
            seeds -= 1

        # Extra turn
        if pos == self.get_current_player_store(player):
            extra_turn = True

        # Capture
        if (pos in self.get_current_player_pits(player)
            and self.cells[pos] == 1
            and self.get_opposite_seeds(pos) > 0):

            store = self.get_current_player_store(player)
            opposite = 12 - pos

            self.cells[store] += 1 + self.cells[opposite]
            self.cells[pos] = 0
            self.cells[opposite] = 0
            capture = True

        return extra_turn, capture