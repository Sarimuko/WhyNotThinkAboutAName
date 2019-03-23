import json
from Defs import moves
from Move import Move
from Defs import colors

class AI:
    def __init__(self):
        pass

    def makeMove(self, GameState):
        pass

    def validate(self, move):
        pass

class ClassicalAI:
    def __init__(self):
        pass

    def makeMove(self, GameState):
        #judge the situation if we could buy card
        curScores=playerScores[curPlayer]
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
        if(np.sum(playerGems[curPlayer])>7):
            markMoves[0]=False
        #
        if(np.sum(playerGems[curPlayer])>8):
            markMoves[1]=False
        #
        i=0
        for playerReserveCard in playerReserveCards if playerReserveCard:
            i+=1
        if(i==3):
            markMoves[2]=False
        if(i==0):
            markMoves[4]=False
        #
        if(np.sum(playerGems[curPlayer])==0 and not playerCards):
            markMoves[3]=False
            markMoves[4]=False
        
        #sort the value of the card
        cards.sort(key=card.value)

        #calculate the ability of each gems
        #cost is the list of demand gems number
        for card in cards:
            cost+=card.cost
        
        aimIndex=cost.index(max(cost))

        #find aim card
        for card in cards:
            if card.costs[aimIndex]!=0:
                aimCard=card
                break 
        #playerInformation
        for playerCard in playerCards:
            playerCardNum=[0 for n in range(5)]
            playerCardNum[color]=1
            essentiallyPlayerGems+=playerCardNum
        
        #get noble card(free round)
        for m in range(len(GameState.noble)): #noble card circling
            for n in range(5): #five kinds of gems
                if(essentiallyPlayerGems[n] < GameState.noble[m]): #if one kind of gems is less than the noble card's gems
                    break;
            if(n == 5):
                move.set_move(3,GameState.noble[m]) #as same as purchase a card
                del GameState.noble #delete one of the noble card
                break;                
        
        #aimCard
        aimColorsNumber=aimCard.costs
        aimColorsNumber=essentiallyPlayerGems-aimColorsNumber
        #if aimColorsNumber's each item bigger than 0, it's ok to purchase
        #if not than collect gems
        isItOKtoPurchase = True
        for n in aimColorNumber if n<0:
            aimColors=[colors[aimColorNumber.index(n)]]
            isItOKtoPurchase=False
        if(isItOKtoPurchase and markMove[3]==True):#reserveCrad not consideration
            move.set_move(3, aimCard)#the return action is in the move function
            return move#
        else:
            if(markMoves[4]!=False):
                for playerReserveCard in playerReserveCards:
                    aimReserveColorsNumber=playerReserveCard.costs
                    aimReserveColorsNumber=essentiallyPlayerGems-aimReserveColorsNumber
                    isItOKPurchaseReverseCard = True
                    for n in aimReserveColorsNumber if n<0:
                        isItOKPurchaseReverseCard = False
                        break
                    if isItOKPurchaseReverseCard=True:
                        move.set_move(4, playerReserveCard)
                        return move

        
        #if above can't act, buy same two gems > 

        i=0
        for curGems in gems if curGems > 0:
            i += 1
            selectIndex = gems.index(curGems)
        if((i == 1) and (gems[selectIndex] >= 4)):
            move.set_move(1,aimColors) #move to situation2: take two same gems
            return move#


        if(not isItOKtoPurchase and markMove[0]==True):#the way to get three gems
            for aimColor in aimColors:
                if gems[colors.index(aimColor)] < 0:
                    del aimColors[aimColors.index(aimColor)]
            
            tempColors=cost
            while len(aimColors) < 3 or cost[maxIndex] == -1:####
                maxIndex=cost.index(max(cost))
                cost[maxIndex] = -1 #define into min
                if ((colors[maxIndex] not in aimColors) and (GameState.gems[maxIndex] != 0)):
                    aimColors[len(aimColors)] = colors[maxIndex]
                maxIndex=cost.index(max(cost))
                    

            cost=tempColors
            while len(aimColors) > 3 or cost[minIndex] == 1000:
                minIndex=cost.index(min(cost))
                if ((colors[minIndex] in aimColors) and (GameState.gems[minIndex] != 0)):
                    del(aimColors[minIndex])
                cost[minIndex]=1000 #define into max
                minIndex=cost.index(min(cost))
                        
            cost=tempColors #return present cost list

            move.set_move(0, aimColors)#move to situation1: take different gems 1 or 2 or 3
            return move#
        
        if(markMove[2]==True):
            move.set_move(2, aimCard)
            return move

        
        


        

        #moveIndex

        
        #move.set_move(moveIndex,aimColors)
        #resultIndex=aim color of two same card
        #if((moveIndex==0 and np.sum(jems)+3>10) or (moveIndex==1 and gems[resultIndex]<4) or (moveIndex==2 and playerReserveCards=3)) 


        return Move()
