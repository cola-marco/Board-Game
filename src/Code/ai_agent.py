import math
from board import Board
from player import Player

def evaluate(board: Board, player: int):
    return board.cells[board.get_store(player)] - board.cells[board.get_store(~player)]

def minimax(board: Board, depth: int, maximizing: bool, player: int):
    opponent = ~player

    if board.check_game_end():
        b = board.copy()
        b.collect_remaining()
        return evaluate(b, player), None

    if depth == 0:
        return evaluate(board, player), None

    # get which pits the current player could select
    valid_moves = board.get_valid_moves(player if maximizing else opponent)
    if not valid_moves:
        return evaluate(board, player), None

    if maximizing:
        best_score = -math.inf
        best_pit = valid_moves[0]
        for pit in valid_moves:
            new_board = board.copy()
            extra_turn, _ = new_board.sow(player, pit)
            score, _ = minimax(new_board, depth - 1, extra_turn, player) # if the player have to play again, it should proceed with another step on the tree
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
            score, _ = minimax(new_board, depth - 1, extra_turn, player)
            if score < best_score:
                best_score = score
                best_pit = pit
        return best_score, best_pit

def minimax_ab(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, player: int):
    opponent = ~player

    if board.check_game_end():
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
    def __init__(self, player_id: int, depth: int, ab: bool): # ab is a boolean value which represent the usage of alpha-beta pruning in the minimax algorithm
        super().__init__(player_id)
        self.depth = depth
        self.ab = ab

    def __str__(self):
        algo = "Alpha-Beta" if self.ab else "Minimax"
        return f"AI Player {self.player_id} ({algo}, depth={self.depth})"

    def get_move(self, board: Board):
        if self.use_alpha_beta:
            _, pit = minimax_ab(board, self.depth, -math.inf, math.inf, True, self.player_id)
        else:
            _, pit = minimax(board, self.depth, True, self.player_id)
        if pit != None:
            pit_num = pit + 1 if self.player_id == 1 else pit - 6
            print(f"AI (Player {self.player_id}) plays pit {pit_num}")
        return pit