from __future__ import division#
import json
from Defs import colors

import numpy as np#


class Nobel:
  def __init__(self):
    self.requirements = [0, 0, 0, 0, 0]
  def feed_text(self, text):
    obj = self.obj = json.loads(text)
    # print(text)
    self.score = obj["score"]
    costs = obj["requirements"]
    for c in costs:
        self.requirements[colors.index(c["color"])] = c["count"]

    return self

  def set_attr(self, score, white = 0, blue = 0, green = 0, red = 0, black = 0):
    self.requirements = [white, blue, green, red, black]
    self.score = score
    return self

  def __repr__(self):
        return json.dumps({"score": self.score, "requirements": self.requirements})

class Card:
    def __init__(self):
        pass

    def set_attr(self, level, color, score, white = 0, blue = 0, green = 0, red = 0, black = 0):#add value for rank
        self.level = level
        self.color = colors.index(color)
        self.score = score
        self.costs = [white, blue, green, red, black]
        self.value = np.sum(costs)/scores#
        #mistake above

        return self

    def feed_text(self, text):
        self.text = text

        obj = self.obj = json.loads(text)
        self.costs = [0, 0, 0, 0, 0]
        self.color = -1
        self.level = -1
        
        self.level = obj["level"]
        if "score" in obj:
            self.score = obj["score"]
        else:
            self.score = 0
        self.color = obj["color"]
        self.color_index = colors.index(self.color)

        self.costs = [0, 0, 0, 0, 0]
        costs = obj["costs"]
        for c in costs:
            self.costs[colors.index(c["color"])] = c["count"]

        return self

    def get_json(self):
        return self.text

    def __repr__(self):
        return json.dumps({"score": self.score, "color":self.color, "costs": self.costs, "level": self.level})
    


class GameState:
    def __init__(self):
        self.playerScores = [0, 0, 0]
        self.gems = [0, 0, 0, 0, 0, 0]
        self.cards = [[], [], []]
        self.curPlayer = -1
        self.playerName = []
        self.playerGems = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.playerReserveCards = [[], [], []]
        self.playerCards = [[], [], []]
        self.nobles = [] #贵族卡

    def feed(self, text):
        obj = json.loads(text)
        players = obj["players"]
        for i, p in enumerate(players):
            self.playerName.append(p["name"])
            if "score" in p:
                self.playerScores[i] = p["score"]
            if "gems" in p:
                for gem in p["gems"]:
                    self.playerGems[i][colors.index(gem["color"])] = gem["count"]
            if "reserved_cards" in p:
                for card in p["reserved_cards"]:
                    self.playerReserveCards[i].append(Card().feed_text(json.dumps(card)))
            if "purchased_cards" in p:
                for card in p["purchased_cards"]:
                    self.playerCards[i].append(Card().feed_text(json.dumps(card)))

        gems = obj["table"]["gems"]
        for gem in gems:
            index = colors.index(gem["color"])
            if "count" in gem:
              self.gems[index] = gem["count"]

        # print(obj["table"])
        cards = obj["table"]["cards"]
        for card in cards:
            self.cards[card["level"] - 1].append(Card().feed_text(json.dumps(card)))
        
        nobles = obj["table"]["nobles"]
        for noble in nobles:
            self.nobles.append(Nobel().feed_text(json.dumps(noble)))

        self.curPlayer = self.playerName.index(obj["playerName"])
    
    def debug_print(self):
        print(self.playerScores)
        print(self.gems)
        print(self.cards)
        print(self.curPlayer)
        print(self.playerName)
        print(self.playerGems)
        print(self.nobles)

gameState = GameState()
gameState.feed('''{
  "round": 2,
  "playerName": "main1",
  "table": {
    "gems": [{
      "color": "red",
      "count": 5
    }, {
      "color": "gold",
      "count": 5
    }, {
      "color": "green",
      "count": 5
    }, {
      "color": "blue",
      "count": 5
    }, {
      "color": "white",
      "count": 5
    }, {
      "color": "black",
      "count": 5
    }],
    "cards": [{
      "level": 3,
      "score": 3,
      "color": "green",
      "costs": [{
        "color": "white",
        "count": 5
      }, {
        "color": "blue",
        "count": 3
      }, {
        "color": "red",
        "count": 3
      }, {
        "color": "black",
        "count": 3
      }]
    }, {
      "level": 1,
      "score": 1,
      "color": "white",
      "costs": [{
        "color": "green",
        "count": 4
      }]
    }, {
      "level": 1,
      "color": "blue",
      "costs": [{
        "color": "white",
        "count": 1
      }, {
        "color": "green",
        "count": 2
      }, {
        "color": "red",
        "count": 2
      }]
    }, {
      "level": 3,
      "score": 4,
      "color": "blue",
      "costs": [{
        "color": "white",
        "count": 6
      }, {
        "color": "blue",
        "count": 3
      }, {
        "color": "black",
        "count": 3
      }]
    }, {
      "level": 2,
      "score": 2,
      "color": "black",
      "costs": [{
        "color": "blue",
        "count": 1
      }, {
        "color": "green",
        "count": 4
      }, {
        "color": "red",
        "count": 2
      }]
    }, {
      "level": 2,
      "score": 3,
      "color": "white",
      "costs": [{
        "color": "white",
        "count": 6
      }]
    }, {
      "level": 2,
      "score": 3,
      "color": "black",
      "costs": [{
        "color": "black",
        "count": 6
      }]
    }, {
      "level": 1,
      "color": "white",
      "costs": [{
        "color": "blue",
        "count": 1
      }, {
        "color": "green",
        "count": 2
      }, {
        "color": "red",
        "count": 1
      }, {
        "color": "black",
        "count": 1
      }]
    }, {
      "level": 1,
      "color": "white",
      "costs": [{
        "color": "blue",
        "count": 2
      }, {
        "color": "green",
        "count": 2
      }, {
        "color": "black",
        "count": 1
      }]
    }, {
      "level": 2,
      "score": 2,
      "color": "white",
      "costs": [{
        "color": "red",
        "count": 5
      }, {
        "color": "black",
        "count": 3
      }]
    }, {
      "level": 3,
      "score": 4,
      "color": "white",
      "costs": [{
        "color": "black",
        "count": 7
      }]
    }, {
      "level": 3,
      "score": 5,
      "color": "white",
      "costs": [{
        "color": "white",
        "count": 3
      }, {
        "color": "black",
        "count": 7
      }]
    }],
    "nobles": [{
      "score": 3,
      "requirements": [{
        "color": "red",
        "count": 4
      }, {
        "color": "green",
        "count": 4
      }]
    }, {
      "score": 3,
      "requirements": [{
        "color": "black",
        "count": 3
      }, {
        "color": "red",
        "count": 3
      }, {
        "color": "white",
        "count": 3
      }]
    }, {
      "score": 3,
      "requirements": [{
        "color": "green",
        "count": 3
      }, {
        "color": "blue",
        "count": 3
      }, {
        "color": "white",
        "count": 3
      }]
    }, {
      "score": 3,
      "requirements": [{
        "color": "black",
        "count": 3
      }, {
        "color": "blue",
        "count": 3
      }, {
        "color": "white",
        "count": 3
      }]
    }]
  },
  "players": [{
    "name": "main1"
  }, {
    "name": "main2",
    "gems" :   [{
 "color" :   "red" ,
 "count" :   1  },   {
 "color" :   "blue" , "count" :   1  },   {
 "color" :   "white" ,
 "count" :   1  }],
  "purchased_cards" :   [{  "level" :   1 ,  "color" :   "white" ,  "costs" :   [{
 "color" :   "blue" ,
 "count" :   2  },   {
 "color" :   "green" ,
 "count" :   2  },   {
 "color" :   "black" ,
 "count" :   1  }]
 },   {
 "level" :   2 ,  "score" :   3 ,  "color" :   "white" ,  "costs" :   [{
 "color" :   "white" ,
 "count" :   6  }]
 }]
  }, {
    "name": "main3"
  }]
}''')

# gameState.debug_print()
