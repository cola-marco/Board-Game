"""
Board layout (indices):
    P2 store = index 13
    P2 pits  = indices 7..12  (pit 1..6 for player 2, left to right from P2's perspective)
    P1 store = index 6
    P1 pits  = indices 0..5   (pit 1..6 for player 1, left to right from P1's perspective)

Visual:
            <-- P2
    [13] [12][11][10][9][8][7]
    [ 0][ 1][ 2][3][4][5] [6]
            P1 -->
"""

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
        """Returns pit indices (not pit numbers) with at least 1 seed."""
        return [pit for pit in self.get_pits(player) if self.cells[pit] > 0]

    def sow(self, player: int, pit: int) -> tuple[bool, bool]:
        """
        Sows seeds from the given pit for the given player.
        Returns (extra_turn, captured):
            - extra_turn: True if last seed landed in player's store
            - captured:   True if last seed landed in an empty own pit
                        (capture is already applied inside this method)
        """
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

    def is_terminal(self) -> bool:
        """Game ends when all pits of either player are empty."""
        return (all(self.cells[p] == 0 for p in P1_PITS) or
                all(self.cells[p] == 0 for p in P2_PITS))

    def collect_remaining(self):
        """At end of game, each player collects seeds remaining in their own pits."""
        for p in P1_PITS:
            self.cells[P1_STORE] += self.cells[p]
            self.cells[p] = 0
        for p in P2_PITS:
            self.cells[P2_STORE] += self.cells[p]
            self.cells[p] = 0

    def get_winner(self) -> int:
        """Returns 1, 2, or 0 for draw. Call only after collect_remaining()."""
        s1, s2 = self.cells[P1_STORE], self.cells[P2_STORE]
        if s1 > s2:
            return 1
        if s2 > s1:
            return 2
        return 0

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
