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

        # Diverse openings with 1 random moves
        for _ in range(1):  # changed from range(2) random moves to range(1) to have a more similar tree and more stable results
            if game.board.is_terminal():
                break
            valid = game.board.get_valid_moves(game.current)
            extra, _ = game.board.sow(game.current, random.choice(valid))
            if not extra:
                game.switch_player()

        # Silence output
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
    # Spacing regulated to match required output
    return f"  {label1:<25} vs {label2:<25} | P1: {p1:>2}/{n}  P2: {p2:>2}/{n}  Draw: {d:>2}/{n}"

def main():
    N = 200 # increased number of games to have a bigger sample size
    print(f"=== KALAHA BENCHMARK ({N} games per matchup) ===\n")

    # Experiment 1
    print("[Experiment 1: Alpha-Beta vs Alpha-Beta]")
    configs = [(3, 3), (5, 5), (3, 5), (3, 7), (5, 3), (7, 3)]
    for d1, d2 in configs:
        r = run_games(d1, d2, True, True, N)
        print(fmt(f"AB depth={d1}", f"AB depth={d2}", r, N))

    # Experiment 2
    print("\n[Experiment 2: Alpha-Beta vs Minimax (Equal Depth)]")
    depths = [3, 4, 5, 6]
    
    # Part A: AB vs MM
    for d in depths:
        r = run_games(d, d, True, False, N)
        print(fmt(f"AB depth={d}", f"MM depth={d}", r, N))
    
    print("\n -- Swapping P1 and P2 --")
    
    # Part B: MM vs AB (as required)
    for d in depths:
        r = run_games(d, d, False, True, N)
        print(fmt(f"MM depth={d}", f"AB depth={d}", r, N))

    # Experiment 3
    print("\n[Experiment 3: Speed - average time per move]")
    for use_ab, label in [(True, "Alpha-Beta"), (False, "Minimax  ")]:
        for depth in [3, 5, 7]:
            ai = AIPlayer(1, depth=depth, use_alpha_beta=use_ab)
            board = Board()
            times = []
            for _ in range(20):
                t0 = time.perf_counter()
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