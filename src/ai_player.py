import math
from board import Board
from player import Player

def evaluate(board: Board, player: int) -> int:
    opponent = 3 - player
    
    my_store = board.cells[board.get_store(player)]
    opp_store = board.cells[board.get_store(opponent)]
    
    my_pits_seeds = sum(board.cells[p] for p in board.get_pits(player))
    opp_pits_seeds = sum(board.cells[p] for p in board.get_pits(opponent))
    
    # Store weight = 10, Pits weight = 1
    return (my_store - opp_store) * 10 + (my_pits_seeds - opp_pits_seeds)

def minimax(board: Board, depth: int, maximizing: bool, player: int) -> tuple[int, int | None]:
    if board.is_terminal() or depth == 0:
        b = board.copy()
        if board.is_terminal(): b.collect_remaining()
        return evaluate(b, player), None

    current_player = player if maximizing else 3 - player
    valid_moves = board.get_valid_moves(current_player)
    
    if not valid_moves:
        return evaluate(board, player), None

    best_pit = valid_moves[0]
    if maximizing:
        best_score = -math.inf
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(current_player, pit)
            score, _ = minimax(new_board, depth - 1, extra_turn, player)
            if score > best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit
    else:
        best_score = math.inf
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(current_player, pit)
            score, _ = minimax(new_board, depth - 1, not extra_turn, player)
            if score < best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit

def minimax_ab(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, player: int) -> tuple[int, int | None]:
    if board.is_terminal() or depth == 0:
        b = board.copy()
        if board.is_terminal(): b.collect_remaining()
        return evaluate(b, player), None

    current_player = player if maximizing else 3 - player
    valid_moves = board.get_valid_moves(current_player)
    
    if not valid_moves:
        return evaluate(board, player), None

    # We sort moves to check pits with more seeds first.
    # This increases the chance of early cutoffs in Alpha-Beta.
    valid_moves.sort(key=lambda m: board.cells[m], reverse=True)

    best_pit = valid_moves[0]
    if maximizing:
        best_score = -math.inf
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(current_player, pit)
            score, _ = minimax_ab(new_board, depth - 1, alpha, beta, extra_turn, player)
            
            if score > best_score:
                best_score = score
                best_pit = pit
            
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break # Beta cutoff
        return best_score, best_pit
    else:
        best_score = math.inf
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(current_player, pit)
            score, _ = minimax_ab(new_board, depth - 1, alpha, beta, not extra_turn, player)
            
            if score < best_score:
                best_score = score
                best_pit = pit
                
            beta = min(beta, best_score)
            if alpha >= beta:
                break # Alpha cutoff
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
        return pit

    def __str__(self):
        algo = "Alpha-Beta" if self.use_alpha_beta else "Minimax"
        return f"AI Player {self.player_id} ({algo}, depth={self.depth})"