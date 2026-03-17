from game import Game
from player import HumanPlayer
from ai_agent import AIagent

def choose_game_mode():
    print('=== MANCALA GAME STARTED ===')
    print('Choose how you want to play the game:')
    print('1: Human vs Human')
    print('2: Human vs AI agent')
    print('3: Ai agent vs AI agent')
    mode = int(input().strip())

    while(True):
        if mode == '1':
            return HumanPlayer(0), HumanPlayer(1)

        elif mode == '2':
            print('Choose the algorithm of the AI agent:')
            while(True):
                algo = input("AI algorithm - (1) Minimax  (2) Alpha-Beta: ").strip()
                if(algo == 1 or algo == 2):
                    use_ab = (algo != "1")
                    break
                else:
                    print('Value inserted not valid, try again')
            print('Choose the depth of the search algorithm of the AI agent (1-7):')
            while(True):
                depth = int(input().strip())
                if(depth > 0 & depth < 8):
                    return HumanPlayer(0), AIagent(1, depth, use_ab)
                print('Invalid depth value, try again')

        elif mode == '3':
            print('Choose the algorithm of the AI agent 1:')
            while(True):
                algo1 = input("AI algorithm - (1) Minimax  (2) Alpha-Beta: ").strip()
                if(algo1 == 1 or algo1 == 2):
                    use_ab1 = (algo1 != "1")
                    break
                else:
                    print('Value inserted not valid, try again')
            print('Choose the depth of the search algorithm of the AI agent 1 (1-7):')
            while(True):
                depth1 = int(input().strip())
                if(depth1 > 0 & depth1 < 8):
                    break
                print('Invalid depth value, try again')
            print('Choose the algorithm of the AI agent 2:')
            while(True):
                algo2 = input("AI algorithm - (1) Minimax  (2) Alpha-Beta: ").strip()
                if(algo2 == 1 or algo2 == 2):
                    use_ab2 = (algo2 != "1")
                    break
                else:
                    print('Value inserted not valid, try again')
            print('Choose the depth of the search algorithm of the AI agent 2 (1-7):')
            while(True):
                depth2 = int(input().strip())
                if(depth2 > 0 & depth2 < 8):
                    return AIagent(0, depth1, use_ab1), AIagent(1, depth2, use_ab2)
                print('Invalid depth value, try again')
        else:
            print('Mode entered not valid, try again')


if __name__ == "__main__":
    p1, p2 = choose_game_mode()
    game = Game(p1, p2)
    game.start()