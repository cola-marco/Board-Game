"""
benchmark.py — runs multiple AI vs AI games across different depth configurations.

All agents use Alpha-Beta pruning (H-Minimax, slides05), which is the only
algorithm used since it strictly dominates plain Minimax in efficiency while
guaranteeing the same optimal strategy.
"""
import io
import sys
import time
import random
from game import Game
from ai_player import AIPlayer
from board import Board


def run_games(p1_depth, p2_depth, n_games=20, random_opening=True) -> dict:
    results = {1: 0, 2: 0, 0: 0}
    for _ in range(n_games):
        ai1 = AIPlayer(1, depth=p1_depth)
        ai2 = AIPlayer(2, depth=p2_depth)
        game = Game(ai1, ai2)

        # One random opening move to diversify game trees
        if random_opening:
            valid = game.board.get_valid_moves(1)
            pit = random.choice(valid)
            extra, _ = game.board.sow(1, pit)
            if not extra:
                game.current = 2

        sys.stdout = io.StringIO()
        winner = game.play()
        sys.stdout = sys.__stdout__
        results[winner] += 1
    return results


def fmt(label1, label2, results, n):
    p1 = results[1]
    p2 = results[2]
    d  = results[0]
    return (f"  {label1:<20} vs {label2:<20} | "
            f"P1: {p1:>2}/{n}  P2: {p2:>2}/{n}  Draw: {d:>2}/{n}")


def main():
    N = 20
    print(f"=== KALAH BENCHMARK ({N} games per matchup, Alpha-Beta only) ===\n")

    # --- Experiment 1: equal depth ---
    print("[ Experiment 1: Equal depth ]")
    for d in [3, 5, 7]:
        r = run_games(d, d, N)
        print(fmt(f"AB depth={d}", f"AB depth={d}", r, N))
    print()

    # --- Experiment 2: depth advantage ---
    print("[ Experiment 2: Depth advantage ]")
    for d1, d2 in [(3, 5), (3, 7), (5, 7), (5, 3), (7, 3), (7, 5)]:
        r = run_games(d1, d2, N)
        print(fmt(f"AB depth={d1}", f"AB depth={d2}", r, N))
    print()

    # --- Experiment 3: average time per move ---
    print("[ Experiment 3: Average time per move ]")
    for depth in [3, 5, 7, 9]:
        ai = AIPlayer(1, depth=depth)
        board = Board()
        times = []
        for _ in range(10):
            t0 = time.time()
            sys.stdout = io.StringIO()
            ai.get_move(board)
            sys.stdout = sys.__stdout__
            times.append(time.time() - t0)
        avg = sum(times) / len(times)
        print(f"  Alpha-Beta depth={depth}: avg {avg:.3f}s per move")

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()