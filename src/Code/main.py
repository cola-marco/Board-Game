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
            return HumanPlayer(), HumanPlayer()

        elif mode == '2':
            print('Choose the depth of the search algorithm of the AI agent (1-7):')
            while(True):
                depth = input().strip()
                if(depth > 0 & depth < 8):
                    return HumanPlayer(), AIagent(depth)
                print('Invalid depth value, try again')

        elif mode == '3':
            print('Choose the depth of the search algorithm of the AI agent 1 (1-7):')
            while(True):
                depth1 = int(input().strip())
                if(depth1 > 0 & depth1 < 8):
                    break
                print('Invalid depth value, try again')
            print('Choose the depth of the search algorithm of the AI agent 2 (1-7):')
            while(True):
                depth2 = int(input().strip())
                if(depth2 > 0 & depth2 < 8):
                    return AIagent(depth1), AIagent(depth2)
                print('Invalid depth value, try again')
        else:
            print('Mode entered not valid, try again')


if __name__ == "__main__":
    p1, p2 = choose_game_mode()
    game = Game(p1, p2)
    game.start()