import json
from Defs import moves, colors
from Move import Move
import random
import sys
import numpy as np
from GameState import Card, GameState

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

    def makeMove(self, gameState):
        pass

    def validate(self, move):
        pass

class ClassicalAI(AI):
    def __init__(self):
        pass

    def makeMove(self, gameState):
        #judge the situation if we could buy card
        curScores=gameState.playerScores[gameState.curPlayer]
        #if(curScores>=15) 
        #target=15-curScores

        #moves = ["get_different_color_gems", "get_two_same_color_gems", "reserve_card", "purchase_card", "purchase_reserved_card"]
        #colors = ["white", "blue", "green", "red", "black", "gold"]
        move=Move()
        
        # 记录5种操作是否可行
        markMoves=[True for n in range(5)]
        #
        if(curScores>=15):
            for markMove in markMoves:
                markMove=False
        #不能拿3个
        if(np.sum(gameState.playerGems[gameState.curPlayer])>7):
            markMoves[0]=False
        #不能拿两个一样的
        if(np.sum(gameState.playerGems[gameState.curPlayer])>8):
            markMoves[1]=False

        #
        i = len(gameState.playerReserveCards[gameState.curPlayer])

        # 不能保留卡
        if(i==3):
            markMoves[2]=False
        # 不能买自己的保留卡
        if(i==0):
            markMoves[4]=False
        #
        if(np.sum(gameState.playerGems[gameState.curPlayer])==0 and len(gameState.playerCards[gameState.curPlayer]) == 0):
            markMoves[3]=False
            markMoves[4]=False
        
        #sort the value of the card
        # cards = gameState.cards
        cards = []
        # cards.extend(gameState.playerReserveCards[gameState.curPlayer])
        for level in gameState.cards:
            cards.extend(level)
        # cards.extend(gameState.playerReserveCards[gameState.curPlayer])
        cards.sort(key=lambda x:x.value, reverse = True)
        gameState.playerReserveCards[gameState.curPlayer].sort(key=lambda x:x.value, reverse = True)
        
        #mistake above
        for card in gameState.playerReserveCards[gameState.curPlayer]:
            if move.valid_purchase_card(gameState, card):
                move.purchase_card(card)
                return move.get_json()
            elif move.valid_purchase_reserved_card(gameState, card):
                move.purchase_reserved_card(card)
                return move.get_json()
                
        for card in cards:
            if move.valid_purchase_card(gameState, card):
                move.purchase_card(card)
                return move.get_json()
            elif move.valid_purchase_reserved_card(gameState, card):
                move.purchase_reserved_card(card)
                return move.get_json()

        #calculate the ability of each gems
        #cost is the list of demand gems number
        cost=[0, 0, 0, 0, 0]
        for card in cards:
            for i, c in enumerate(card.costs):
                cost[i]+=c
        
        aimIndex=cost.index(min(cost))

        #find aim card
        for card in cards:
            if card.costs[aimIndex]!=0:
                aimCard=card
                break 
        
        # print(aimCard)
        
        # 宝石总数
        essentiallyPlayerGems = gameState.playerGems[gameState.curPlayer]
        #playerInformation
        for playerCard in gameState.playerCards[gameState.curPlayer]:
            essentiallyPlayerGems[playerCard.color]+=1
        
        #get noble card(free round)
        for m in range(len(gameState.nobles)): #noble card circling
            for n in range(5): #five kinds of gems
                if(essentiallyPlayerGems[n] < gameState.nobles[m].requirements[n]): #if one kind of gems is less than the noble card's gems
                    break
            if(n == 5):
                move.set_move(3,gameState.nobles[m]) #as same as purchase a card
                return move.get_json()
                # del gameState.nobles #delete one of the noble card
                break; 


        #aimCard
        # aimcard总共需要的宝石数
        aimColorsNumber=aimCard.costs
        # aimcard需要的宝石是否足够
        aimColorsNumber=[essentiallyPlayerGems[i]-aimColorsNumber[i] for i in range(5)]
        #if aimColorsNumber's each item bigger than 0, it's ok to purchase
        #if not than collect gems
        isItOKtoPurchase = True
        aimColors = []
        for index, n in enumerate(aimColorsNumber):
            if n < 0:
                aimColors.append(index)
                isItOKtoPurchase=False
                # break
        # if(isItOKtoPurchase and markMove[3]==True):#reserveCrad not consideration
        #     move.set_move(3, aimCard)#the return action is in the move function
        #     return move.get_json()#
        # else:
        #     if(markMoves[4]!=False):
        #         for playerReserveCards in gameState.playerReserveCards:
        #             aimReserveColorsNumber=playerReserveCards.costs
        #             aimReserveColorsNumber=essentiallyPlayerGems-aimReserveColorsNumber
        #             isItOKPurchaseReverseCard = True
        #             for n in aimReserveColorsNumber:
        #                 if n<0:
        #                     isItOKPurchaseReverseCard = False
        #                     break
        #             if isItOKPurchaseReverseCard==True:
        #                 move.set_move(4, playerReserveCards)
        #                 return move.get_json()
                      
        gems = gameState.gems
        #if above can't act, buy same two gems > 
           
        # i=0
        # selectIndex = 0
        # for index, curGems in enumerate(gems):
        #     if curGems >= 4:
        #         i += 1
        #         selectIndex = index
        for i in aimColors:
            if(aimColorsNumber[i] >= 2 and  gems[i] >= 4):
                move.set_move(1,colors[i]) #move to situation2: take two same gems
                return move.get_json()#

        if(markMoves[0]==True):#the way to get three gems
            aimColors = [w for w in aimColors if gems[w] >= 0]
            # for aimColor in aimColors:
            #     if gems[aimColor] == 0:
            #         del aimColors[aimColors.index(aimColor)]
            
            # tempColors=cost
            # maxIndex=0
            # print(cost)
            # while len(aimColors) < 3 and not cost[maxIndex] == -1:####
            #     maxIndex=cost.index(max(cost))
            #     cost[maxIndex] = -1 #define into min
            #     if ((colors[maxIndex] not in aimColors) and (not gameState.gems[maxIndex] == 0)):
            #         aimColors[len(aimColors) - 1] = colors[maxIndex]
            #     # print(cost)
            #     maxIndex=cost.index(max(cost))
                    

            # cost=tempColors
            # minIndex=0
            # while len(aimColors) > 3 or cost[minIndex] == 1000:
            #     minIndex=cost.index(min(cost))
            #     if ((colors[minIndex] in aimColors) and (gameState.gems[minIndex] != 0)):
            #         del(aimColors[minIndex])
            #     cost[minIndex]=1000 #define into max
            #     minIndex=cost.index(min(cost))
                        
            # cost=tempColors #return present cost list

            while (len(aimColors) > 3):
                del aimColors[aimColors.index(aimColorsNumber.index(min(aimColorsNumber)))]
            aimColors = [colors[w] for w in aimColors]
            if move.valid_different_gems(gameState, aimColors):
                move.set_move(0, aimColors)#move to situation1: take different gems 1 or 2 or 3
                return move.get_json()
            # return move
        
        if move.valid_reserve_card(gameState, aimCard):
            move.set_move(2, aimCard)
            return move.get_json()

        get_cards = []
        for index, gem in enumerate(gameState.gems):
            if gem > 0:
                get_cards.append(index)
        while (len(get_cards) > 3):
                del get_cards[get_cards.index(aimColorsNumber.index(min(aimColorsNumber)))]
        get_cards = [colors[w] for w in get_cards]
        move.get_diffrent_gems(get_cards)
        return move.get_json()


        return move.get_json()

class RandomAI(AI):
    def __init__(self):
        pass

    def makeMove(self, GameState):
        move = Move()
        move.move = moves[1]
        move.info = "red"
        cards = GameState.cards
        for i in (2, 1, 0):
            level_card = cards[i]
            for card in level_card:
                if move.validate(3, GameState, card):
                    move.set_move(3, card)
                    return move.get_json()
        
        for i in range(12):
            triple = list(triples[random.randint(0, 5)])
            if move.valid_different_gems(GameState, triple):
                sys.stderr.write(str(GameState.gems))
                sys.stderr.write(str(triple))
                sys.stderr.write(str(move.valid_different_gems(GameState, triple)))
                move.set_move(0, triple)
                return move.get_json()
        
        for i in range(5):
            color = random.randint(0, 4)
            if move.valid_two_gems(GameState, colors[color]):
                move.set_move(1, colors[color])
                return move.get_json()
        return move.get_json()
