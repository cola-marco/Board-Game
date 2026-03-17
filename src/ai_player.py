import math
from board import Board
from player import Player


def evaluate(board: Board, player: int) -> int:
    opponent = 3 - player
    return board.cells[board.get_store(player)] - board.cells[board.get_store(opponent)]


def minimax(board: Board, depth: int, maximizing: bool, player: int) -> tuple[int, int | None]:
    opponent = 3 - player

    if board.check_end():
        b = board.copy()
        b.collect_remaining()
        return evaluate(b, player), None

    if depth == 0:
        return evaluate(board, player), None

    valid_moves = board.get_valid_moves(player if maximizing else opponent)
    if not valid_moves:
        return evaluate(board, player), None

    if maximizing:
        best_score = -math.inf
        best_pit = valid_moves[0]
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(player, pit)
            # extra turn -> still maximizing (same player plays again)
            next_max = True if extra_turn else False
            score, _ = minimax(new_board, depth - 1, next_max, player)
            if score > best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit
    else:
        best_score = math.inf
        best_pit = valid_moves[0]
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(opponent, pit)
            # opponent extra turn -> they play again -> still minimizing
            next_max = extra_turn
            score, _ = minimax(new_board, depth - 1, next_max, player)
            if score < best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit


def minimax_ab(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, player: int) -> tuple[int, int | None]:
    opponent = 3 - player

    if board.check_end():
        b = board.copy()
        b.collect_remaining()
        return evaluate(b, player), None

    if depth == 0:
        return evaluate(board, player), None

    valid_moves = board.get_valid_moves(player if maximizing else opponent)
    if not valid_moves:
        return evaluate(board, player), None

    if maximizing:
        best_score = -math.inf
        best_pit = valid_moves[0]
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(player, pit)
            score, _ = minimax_ab(new_board, depth - 1, alpha, beta, extra_turn, player)
            if score > best_score:
                best_score = score
                best_pit = pit
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break  # beta cutoff
        return best_score, best_pit
    else:
        best_score = math.inf
        best_pit = valid_moves[0]
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(opponent, pit)
            score, _ = minimax_ab(new_board, depth - 1, alpha, beta, extra_turn, player)
            if score < best_score:
                best_score = score
                best_pit = pit
            beta = min(beta, best_score)
            if alpha >= beta:
                break  # alpha cutoff
        return best_score, best_pit


class AIPlayer(Player):
    def __init__(self, player_id: int, depth: int = 7, use_alpha_beta: bool = True):
        super().__init__(player_id)
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, board: Board) -> int:
        if self.use_alpha_beta:
            _, pit = minimax_ab(board, self.depth, -math.inf, math.inf, True, self.player_id)
        else:
            _, pit = minimax(board, self.depth, True, self.player_id)
        pit_num = pit + 1 if self.player_id == 1 else pit - 6
        print(f"AI (Player {self.player_id}) plays pit {pit_num}")
        return pit

    def __str__(self):
        algo = "Alpha-Beta" if self.use_alpha_beta else "Minimax"
        return f"AI Player {self.player_id} ({algo}, depth={self.depth})"