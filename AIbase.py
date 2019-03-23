import json
from Defs import moves, colors
from Move import Move
import random

triples = [('black', 'blue', 'white'),
           ('black', 'green', 'blue'),
           ('black', 'green', 'white'),
           ('black', 'red', 'blue'),
           ('black', 'red', 'green'),
           ('black', 'red', 'white'),
           ('green', 'blue', 'white'),
           ('red', 'blue', 'white'),
           ('red', 'green', 'blue'),
           ('red', 'green', 'white')]
pairs = [('black', 'red'),
         ('black', 'blue'),
         ('black', 'white'),
         ('black', 'green'),
         ('red', 'blue'),
         ('red', 'white'),
         ('red', 'green'),
         ('blue', 'white'),
         ('blue', 'green'),
         ('green', 'white')]

class AI:
    def __init__(self):
        pass

    def makeMove(self, GameState):
        pass

    def validate(self, move):
        pass

class ClassicalAI(AI):
    def __init__(self):
        pass

    def makeMove(self, GameState):
        return Move()

class RandomAI(AI):
    def __init__(self):
        pass

    def makeMove(self, GameState):
        move = Move()
        cards = GameState.cards
        for i in (2, 1, 0):
            level_card = cards[i]
            for card in level_card:
                if move.validate(3, GameState, card):
                    move.set_move(3, card)
                    return move.get_json()
        
        triple = list(triples[random.randint(0, 5)])
        if move.valid_different_gems(GameState, triple):
            move.set_move(0, triple)
            return move.get_json()
        
        color = random.randint(0, 4)
        if move.valid_two_gems(GameState, colors[color]):
            move.set_move(1, colors[color])
            return move.get_json()
        return move.get_json()
