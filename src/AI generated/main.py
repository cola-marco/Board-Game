from game import Game
from player import HumanPlayer
from ai_player import AIPlayer


def choose_mode():
    print("=== KALAH (MANCALA) ===")
    print("1. Human vs Human")
    print("2. Human vs AI")
    print("3. AI vs AI (benchmark)")
    choice = input("Choose mode (1/2/3): ").strip()

    if choice == "1":
        return HumanPlayer(1), HumanPlayer(2)

    elif choice == "2":
        algo = input("AI algorithm - (1) Minimax  (2) Alpha-Beta [default=2]: ").strip()
        use_ab = (algo != "1")
        depth = input("AI search depth [default=7]: ").strip()
        depth = int(depth) if depth.isdigit() else 7
        return HumanPlayer(1), AIPlayer(2, depth=depth, use_alpha_beta=use_ab)

    elif choice == "3":
        print("\n--- AI 1 ---")
        algo1 = input("Algorithm - (1) Minimax  (2) Alpha-Beta [default=2]: ").strip()
        depth1 = input("Depth [default=7]: ").strip()

        print("\n--- AI 2 ---")
        algo2 = input("Algorithm - (1) Minimax  (2) Alpha-Beta [default=2]: ").strip()
        depth2 = input("Depth [default=5]: ").strip()

        p1 = AIPlayer(1, depth=int(depth1) if depth1.isdigit() else 7, use_alpha_beta=(algo1 != "1"))
        p2 = AIPlayer(2, depth=int(depth2) if depth2.isdigit() else 5, use_alpha_beta=(algo2 != "1"))
        return p1, p2

    else:
        print("Invalid choice, defaulting to Human vs AI.")
        return HumanPlayer(1), AIPlayer(2)


if __name__ == "__main__":
    p1, p2 = choose_mode()
    game = Game(p1, p2)
    game.play()
