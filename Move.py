import json
class Move:
    def __init__(self):
        self.moves = [self.get_diffrent_gems, self.get_two_gems, self.reserve_card, self.purchase_card, self.purchase_reserved_card]
    
    def set_move(self, index, info):
        self.moves[index](info)

    def get_diffrent_gems(self, colors):
        self.move = "get_different_color_gems"
        self.info = colors

    def get_two_gems(self, color):
        self.move = "get_two_same_color_gems"
        self.info = color

    def reserve_card(self, card_info, rand = 0):
        self.move = "reserve_card"
        if rand == 0:
            self.info = {"card": card_info}
        elif rand == 1:
            self.info = {"level": card_info}
            
    def purchase_card(self, card_info):
        self.move = "purchase_card"
        self.info = card_info

    def purchase_reserved_card(self, card_info):
        self.move = "purchase_reserved_card"
        self.info = card_info

    def get_json(self):
        return json.dumps({self.move: self.info})

move = Move()
move.set_move(1, "red")
print(move.get_json())