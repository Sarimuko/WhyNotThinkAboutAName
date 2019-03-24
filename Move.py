import json
from Defs import moves, colors
import sys

class Move:
    def __init__(self):
        self.moves = [self.get_diffrent_gems, self.get_two_gems, self.reserve_card, self.purchase_card, self.purchase_reserved_card]
        self.validate_methods = [self.valid_different_gems, self.valid_two_gems, self.valid_reserve_card, self.valid_purchase_card, self.valid_purchase_reserved_card]
    
    def set_move(self, index, info):
        self.moves[index](info)

    def validate(self, index, GameState, info):
        return self.validate_methods[index](GameState, info)

    def get_diffrent_gems(self, colors):
        self.move = "get_different_color_gems"
        self.info = colors

    def valid_different_gems(self, GameState, mcolors):
        gems = GameState.gems
        curPlayer = GameState.curPlayer
        pgems = GameState.playerGems[curPlayer]

        if sum(pgems) + len(mcolors) > 10:
            return False

        for c in mcolors:
            if gems[colors.index(c)] == 0:
                return False

        return True

    def get_two_gems(self, color):
        self.move = "get_two_same_color_gems"
        self.info = color

    def valid_two_gems(self, GameState, color):
        curPlayer = GameState.curPlayer
        pgems = GameState.playerGems[curPlayer]

        if sum(pgems) + 2 > 10:
            return False

        gems = GameState.gems
        if gems[colors.index(color)] < 4:
            return False

        return True

    def reserve_card(self, card_info, rand = 0):
        self.move = "reserve_card"
        if rand == 0:
            self.info = {"card": card_info.obj}
        elif rand == 1:
            self.info = {"level": card_info.obj}

    def valid_reserve_card(self, GameState, card_info):
        curPlayer = GameState.curPlayer
        if len(GameState.playerReserveCards[curPlayer]) == 3:
            return False

        return True

            
    def purchase_card(self, card_info):
        self.move = "purchase_card"
        self.info = card_info.obj

    def valid_purchase_card(self, GameState, card_info):
        gems = GameState.playerGems[GameState.curPlayer]
        cards = GameState.playerCards[GameState.curPlayer]
        for index, card in enumerate(cards):
            gems[card.color] += 1
        costs = card_info.costs
        gold = gems[5]

        need = 0
        for i in range(5):
            if costs[i] > gems[i]:
                need += costs[i] - gems[i]
        if need > gold:
            return False
        return True


    def purchase_reserved_card(self, card_info):
        self.move = "purchase_reserved_card"
        self.info = card_info.obj

    def valid_purchase_reserved_card(self, GameState, card_info):
        if card_info not in GameState.playerReserveCards[GameState.curPlayer]:
            return False
        return self.valid_purchase_card(GameState, card_info)

    def get_json(self):
        sys.stderr.write(json.dumps({self.move: self.info}))
        return json.dumps({self.move: self.info})

# move = Move()
# move.set_move(1, "red")
# print(move.get_json())