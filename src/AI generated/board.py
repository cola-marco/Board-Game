SEEDS_PER_PIT = 4
P1_PITS = list(range(0, 6))   # indices 0-5
P1_STORE = 6
P2_PITS = list(range(7, 13))  # indices 7-12
P2_STORE = 13
TOTAL_CELLS = 14


class Board:
    def __init__(self):
        self.cells = [SEEDS_PER_PIT] * TOTAL_CELLS
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

    def copy(self):
        new_board = Board()
        new_board.cells = self.cells[:]
        return new_board

    def get_pits(self, player: int) -> list[int]:
        return P1_PITS if player == 1 else P2_PITS

    def get_store(self, player: int) -> int:
        return P1_STORE if player == 1 else P2_STORE

    def get_opposite_pit(self, pit: int) -> int:
        return 12 - pit

    def get_valid_moves(self, player: int) -> list[int]:
        return [pit for pit in self.get_pits(player) if self.cells[pit] > 0]

    def sow(self, player: int, pit: int) -> tuple[bool, bool]:
        seeds = self.cells[pit]
        if seeds == 0:
            return False, False

        self.cells[pit] = 0
        opponent_store = self.get_store(3 - player)
        pos = pit

        while seeds > 0:
            pos = (pos + 1) % TOTAL_CELLS
            if pos == opponent_store:
                continue  # skip opponent's store
            self.cells[pos] += 1
            seeds -= 1

        # Extra turn: last seed in own store
        own_store = self.get_store(player)
        if pos == own_store:
            return True, False

        # Capture: last seed in an empty own pit on own side
        own_pits = self.get_pits(player)
        if pos in own_pits and self.cells[pos] == 1:
            opposite = self.get_opposite_pit(pos)
            if self.cells[opposite] > 0:
                self.cells[own_store] += 1 + self.cells[opposite]
                self.cells[pos] = 0
                self.cells[opposite] = 0
                return False, True

        return False, False

    def check_end(self) -> bool:
        return (all(self.cells[p] == 0 for p in P1_PITS) or
                all(self.cells[p] == 0 for p in P2_PITS))

    def collect_remaining(self):
        for p in P1_PITS:
            self.cells[P1_STORE] += self.cells[p]
            self.cells[p] = 0
        for p in P2_PITS:
            self.cells[P2_STORE] += self.cells[p]
            self.cells[p] = 0

    def get_winner(self) -> int:
        s1, s2 = self.cells[P1_STORE], self.cells[P2_STORE]
        if s1 > s2:
            return 1
        if s2 > s1:
            return 2
        return 0