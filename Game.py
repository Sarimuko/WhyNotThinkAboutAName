from GameState import GameState
from Move import Move
import AIbase

class Game:
    def __init__(self, max_round):
        self.max_round = max_round
        self.state = GameState()
    
