import matplotlib.pyplot as plt
import time
import io
import sys

from benchmark import run_games
from ai_player import AIPlayer
from board import Board

N = 50  # number of games

def winrate_experiment():
    depths = [3, 5, 7]

    ab_winrates = []
    mm_winrates = []

    print("Running winrate experiment...")

    for d in depths:
        r1 = run_games(d, d, True, False, N)
        r2 = run_games(d, d, False, True, N)

        ab_wins = r1[1] + r2[2]
        mm_wins = r1[2] + r2[1]

        ab_winrates.append(ab_wins / (2 * N))
        mm_winrates.append(mm_wins / (2 * N))

        print(f"Depth {d}: AB={ab_wins:.2f}, MM={mm_wins:.2f}")
        
    # Plot
    plt.figure()
    plt.plot(depths, ab_winrates, marker='o', label='Alpha-Beta')
    plt.plot(depths, mm_winrates, marker='o', label='Minimax')

    plt.xlabel("Depth")
    plt.ylabel("Win Rate")
    plt.title("Win Rate: Alpha-Beta vs Minimax")
    plt.legend()
    plt.grid()

    plt.savefig("winrate_comparison.png")
    plt.show()

def time_experiment():
    depths = [2, 3, 4, 5, 6]

    ab_times = []
    mm_times = []

    print("\nRunning time experiment...")

    for use_ab, label, store in [
        (True, "Alpha-Beta", ab_times),
        (False, "Minimax", mm_times)
    ]:
        for depth in depths:
            ai = AIPlayer(1, depth=depth, use_alpha_beta=use_ab)
            board = Board()

            times = []

            for _ in range(20):
                t0 = time.perf_counter()

                # suppress output
                old_out = sys.stdout
                sys.stdout = io.StringIO()

                ai.get_move(board)

                sys.stdout = old_out

                times.append(time.perf_counter() - t0)

            avg = sum(times) / len(times)
            store.append(avg)

            print(f"{label} depth={depth}: {avg:.4f}s")

    # Plot
    plt.figure()
    plt.plot(depths, ab_times, marker='o', label='Alpha-Beta')
    plt.plot(depths, mm_times, marker='o', label='Minimax')

    plt.xlabel("Depth")
    plt.ylabel("Time per move (seconds)")
    plt.title("Performance: Time vs Depth")
    plt.legend()
    plt.grid()

    plt.savefig("time_comparison.png")
    plt.show()


def main():
    winrate_experiment()
    #time_experiment()


if __name__ == "__main__":
    main()