from AIbase import ClassicalAI, RandomAI
from GameState import GameState
from Move import Move
import sys

def main(state):
    gameState = GameState()
    gameState.feed(state)

    ai = RandomAI()
    move = ai.makeMove(gameState)
    print(move)

if __name__ == "__main__":
    state = sys.argv[1]
    main(state)