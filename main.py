from AIbase import ClassicalAI
from GameState import GameState
from Move import Move

def main():
    state = input()
    gameState = GameState()
    gameState.feed(state)

    ai = ClassicalAI()
    move = ai.makeMove(GameState)
    print(move.get_json())

if __name__ == "__main__":
    main()