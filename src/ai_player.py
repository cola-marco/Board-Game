import math
from board import Board
from player import Player

def evaluate(board: Board, player: int, extra_turn: bool = False, captured: bool = False) -> int:
    opponent = 3 - player
    
    my_store = board.cells[board.get_store(player)]
    opp_store = board.cells[board.get_store(opponent)]
    
    my_pits_seeds = sum(board.cells[p] for p in board.get_pits(player))
    opp_pits_seeds = sum(board.cells[p] for p in board.get_pits(opponent))
    
    # Dynamic Bonuses
    extra_turn_bonus = 15 if extra_turn else 0
    capture_bonus = 10 if captured else 0

    return (my_store - opp_store) * 20 + (my_pits_seeds - opp_pits_seeds) + extra_turn_bonus + capture_bonus

def minimax(board: Board, depth: int, maximizing: bool, player: int, last_extra: bool = False, last_captured: bool = False) -> tuple[int, int | None]:
    if board.is_terminal():
        b = board.copy()
        b.collect_remaining()
        return evaluate(b, player), None

    if depth == 0:
        return evaluate(board, player, last_extra, last_captured), None

    current_player = player if maximizing else 3 - player
    valid_moves = board.get_valid_moves(current_player)
    
    if not valid_moves:
        return evaluate(board, player, last_extra, last_captured), None

    best_pit = valid_moves[0]
    if maximizing:
        best_score = -math.inf
        for pit in valid_moves:
            nb = board.copy()
            extra, cap = nb.sow(current_player, pit)
            # Recursive call: extra turn means maximizing remains True
            score, _ = minimax(nb, depth - 1, extra, player, extra, cap)
            if score > best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit
    else:
        best_score = math.inf
        for pit in valid_moves:
            nb = board.copy()
            extra, cap = nb.sow(current_player, pit)
            # Recursive call: if opponent gets extra turn, maximizing remains False
            score, _ = minimax(nb, depth - 1, not extra, player, extra, cap)
            if score < best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit

def minimax_ab(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, player: int, last_extra: bool = False, last_captured: bool = False) -> tuple[int, int | None]:
    """Alpha-Beta Pruning. Optimized for speed using the same logic as Minimax."""
    if board.is_terminal():
        b = board.copy()
        b.collect_remaining()
        return evaluate(b, player), None

    if depth == 0:
        return evaluate(board, player, last_extra, last_captured), None

    current_player = player if maximizing else 3 - player
    valid_moves = board.get_valid_moves(current_player)
    
    if not valid_moves:
        return evaluate(board, player, last_extra, last_captured), None

    # Move Ordering: Essential for Alpha-Beta efficiency
    valid_moves.sort(key=lambda m: board.cells[m], reverse=True)

    best_pit = valid_moves[0]
    if maximizing:
        best_score = -math.inf
        for pit in valid_moves:
            nb = board.copy()
            extra, cap = nb.sow(current_player, pit)
            score, _ = minimax_ab(nb, depth - 1, alpha, beta, extra, player, extra, cap)
            if score > best_score:
                best_score = score
                best_pit = pit
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_pit
    else:
        best_score = math.inf
        for pit in valid_moves:
            nb = board.copy()
            extra, cap = nb.sow(current_player, pit)
            score, _ = minimax_ab(nb, depth - 1, alpha, beta, not extra, player, extra, cap)
            if score < best_score:
                best_score = score
                best_pit = pit
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score, best_pit

class AIPlayer(Player):
    def __init__(self, player_id: int, depth: int = 7, use_alpha_beta: bool = True):
        super().__init__(player_id)
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, board: Board) -> int:
        if self.use_alpha_beta:
            _, pit = minimax_ab(board, self.depth, -math.inf, math.inf, True, self.player_id, False, False)
        else:
            _, pit = minimax(board, self.depth, True, self.player_id, False, False)
        return pit

    def __str__(self):
        algo = "Alpha-Beta" if self.use_alpha_beta else "Minimax"
        return f"AI Player {self.player_id} ({algo}, depth={self.depth})"