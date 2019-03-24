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
        
        markMoves=[True for n in range(5)]
        #
        if(curScores>=15):
            for markMove in markMoves:
                markMove=False
        #
        if(np.sum(gameState.playerGems[gameState.curPlayer])>7):
            markMoves[0]=False
        #
        if(np.sum(gameState.playerGems[gameState.curPlayer])>8):
            markMoves[1]=False
        #
 
        i = len(gameState.playerReserveCards[gameState.curPlayer])

        if(i==3):
            markMoves[2]=False
        if(i==0):
            markMoves[4]=False
        #
        if(np.sum(gameState.playerGems[gameState.curPlayer])==0 and len(gameState.playerCards[gameState.curPlayer]) == 0):
            markMoves[3]=False
            markMoves[4]=False
        
        #sort the value of the card
        # cards = gameState.cards
        cards = []
        for level in gameState.cards:
            cards.extend(level)
        cards.sort(key=lambda x:x.value)
        #mistake above

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
                #return move.get_json()
                # del gameState.nobles #delete one of the noble card
                break


        #aimCard
        aimColorsNumber=aimCard.costs
        aimColorsNumber=[essentiallyPlayerGems[i]-aimColorsNumber[i] for i in range(5)]
        #if aimColorsNumber's each item bigger than 0, it's ok to purchase
        #if not than collect gems
        isItOKtoPurchase = True
        for n in aimColorsNumber:
            if n < 0:
                aimColors=[colors[aimColorsNumber.index(n)]]
                isItOKtoPurchase=False
                break

        if(isItOKtoPurchase and markMove[3]==True):#reserveCrad not consideration
            move.set_move(3, aimCard)#the return action is in the move function
            return move.get_json()#
        else:
            if(markMoves[4]!=False):
                for playerReserveCards in gameState.playerReserveCards:
                    aimReserveColorsNumber=playerReserveCards.costs
                    aimReserveColorsNumber=essentiallyPlayerGems-aimReserveColorsNumber
                    isItOKPurchaseReverseCard = True
                    for n in aimReserveColorsNumber:
                        if n<0:
                            isItOKPurchaseReverseCard = False
                            break
                    if isItOKPurchaseReverseCard==True:
                        move.set_move(4, playerReserveCards)
                        return move.get_json()

        isItOKtoPurchaseEachCard=True
        if(not isItOKtoPurchase and markMoves[3]==True):
            for card in gameState.cards:
                cardNumber=card.costs
                cardNumber=[essentiallyPlayerGems[i]-cardNumber[i] for i in range(5)]
                for n in cardNumber:
                    if n<0:
                        break
                if n>=0: 
                    targetCard=card 
                    move.set_move(3, targetCard)
                    return move.get_json()

                  
        gems = gameState.gems
        #if above can't act, buy same two gems > 
           
        i=0
        for index, curGems in enumerate(gems):
            if curGems > 4:
                i += 1
                selectIndex = index
        if((i == 1) and (gems[selectIndex] >= 4)) and markMoves[1]:
            move.set_move(1,aimColors) #move to situation2: take two same gems
            return move.get_json()#
        
        #
        if(not isItOKtoPurchase and markMoves[0]==True):#the way to get three gems
            for aimColor in aimColors:
                if gems[colors.index(aimColor)] < 0:
                    del aimColors[aimColors.index(aimColor)]
        
           
            tempColors=cost
            minIndex=0
            # print(cost)
            while len(aimColors) < 3 and not cost[minIndex] == 1000:####
                minIndex=cost.index(min(cost))
                cost[minIndex] = 1000 #define into min
                if ((colors[minIndex] not in aimColors) and (not gameState.gems[minIndex] == 0)):
                    #aimColors[len(aimColors) - 1] = colors[minIndex]
                    aimColors.extend(colors[minIndex])
                # print(cost)
                minIndex=cost.index(min(cost))
                    

            cost=tempColors
            maxIndex=0
            while len(aimColors) > 3 and not cost[maxIndex] == -1:
                maxIndex=cost.index(max(cost))
                if ((colors[maxIndex] in aimColors) and (gameState.gems[maxIndex] != 0)):
                    del(aimColors[maxIndex])
                cost[maxIndex]=-1 #define into max
                maxIndex=cost.index(max(cost))
                        
            cost=tempColors #return present cost list

            move.set_move(0, aimColors)#move to situation1: take different gems 1 or 2 or 3
            return move.get_json()
            # return move
        
        if(markMoves[2]==True):
            move.set_move(2, aimCard)
            return move.get_json()
            # return move
        #if()
        

        #moveIndex

        
        #move.set_move(moveIndex,aimColors)
        #resultIndex=aim color of two same card
        #if((moveIndex==0 and np.sum(jems)+3>10) or (moveIndex==1 and gems[resultIndex]<4) or (moveIndex==2 and playerReserveCard=3)) 


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
