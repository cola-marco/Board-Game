"""
benchmark.py — Updated version with preferred output format and expanded tests.
"""
import io
import sys
import random
import time
from game import Game
from ai_player import AIPlayer
from board import Board

def run_games(p1_depth, p2_depth, p1_ab, p2_ab, n_games=50):
    results = {1: 0, 2: 0, 0: 0}
    for _ in range(n_games):
        ai1 = AIPlayer(1, depth=p1_depth, use_alpha_beta=p1_ab)
        ai2 = AIPlayer(2, depth=p2_depth, use_alpha_beta=p2_ab)
        game = Game(ai1, ai2)

        # Force 2 random moves to ensure variety in the 50 games
        for _ in range(2):
            if game.board.is_terminal():
                break
            valid = game.board.get_valid_moves(game.current)
            # We use a temporary sow to keep the game state moving
            extra, _ = game.board.sow(game.current, random.choice(valid))
            if not extra:
                game.switch_player()

        # Suppress game logs
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        winner = game.play()
        sys.stdout = original_stdout
        
        results[winner] += 1
    return results

def fmt(label1, label2, results, n):
    p1 = results[1]
    p2 = results[2]
    d  = results[0]
    return f"  {label1:<25} vs {label2:<25} | P1: {p1:>2}/{n}  P2: {p2:>2}/{n}  Draw: {d:>2}/{n}"

def main():
    N = 50
    print(f"=== KALAH BENCHMARK ({N} games per matchup) ===\n")

    # --- Experiment 1: Alpha-Beta vs Alpha-Beta ---
    print("[ Experiment 1: Alpha-Beta vs Alpha-Beta ]")
    configs = [
        (3, 3), (5, 5), 
        (3, 5), (3, 7), 
        (5, 3), (7, 3)
    ]
    for d1, d2 in configs:
        r = run_games(d1, d2, True, True, N)
        print(fmt(f"AB depth={d1}", f"AB depth={d2}", r, N))

    print("\n[ Experiment 2: Alpha-Beta vs Minimax (Equal Depth) ]")
    # Expanded test cases for Experiment 2
    for d in [3, 4, 5, 6]:
        r = run_games(d, d, True, False, N)
        print(fmt(f"AB depth={d}", f"MM depth={d}", r, N))

    print("\n[ Experiment 3: Speed — average time per move ]")
    # Speed test on a standard board state
    for use_ab, label in [(True, "Alpha-Beta"), (False, "Minimax  ")]:
        for depth in [3, 5, 7]:
            ai = AIPlayer(1, depth=depth, use_alpha_beta=use_ab)
            board = Board()
            times = []
            # Average over 20 calls for stability
            for _ in range(20):
                t0 = time.perf_counter()
                # Dummy call to get_move
                old_out = sys.stdout
                sys.stdout = io.StringIO()
                ai.get_move(board)
                sys.stdout = old_out
                times.append(time.perf_counter() - t0)
            avg = sum(times) / len(times)
            print(f"  {label} depth={depth}: avg {avg:.4f}s per move")

    print("\n=== BENCHMARK DONE ===")

if __name__ == "__main__":
    main()