import random

def ordermoves(moves):
    random.shuffle(moves)
    return moves

#alpha=-999 beta=+999
def negamax(self,depth,a,b,colour,root=False,display=False):
    if depth==0 or self.White.checkmated==True or self.Black.checkmated==True:
        return self.evaluate(colour)

    self.updatestatus()

    moves=self.sides[colour].movelist

    #moves=ordermoves(moves)

    #board.display()
    #print(board.moves)

    value=-999999999
    if root==True:
        allmoves=[]

    for move in moves:
        if root==True:
            pass
            #print(moves.index(move)+1,"/",len(moves))
        if display==True:
            print(depth,move)
        #if move[0]==[6,7] and move[1]==[4,6]:
            #board.display()
            #print(board.moves)
        self.makemove(move,colour)
##        oldvalue=value
        compare=-(negamax(self,depth-1,-b,-a,(colour+1)%2,display=display))
        value=max(value,compare)
        if root==True:
            allmoves.append([compare,move])
##        if value>oldvalue:
##            topmoves=[move]
##        elif value==oldvalue:
##            topmoves.append(move)
        self.undo(move)
        a=max(a,value)

        if a>=b:
            break
    if root==True:
        return value,allmoves
    else:
        return value

def rootnegamax(self,depth,colour,display=False):
    value,allmoves=negamax(self,depth,-9999999,9999999,colour,root=True,display=display)
    #print("Score:",value)
    topmoves=[x for x in allmoves if x[0]==value]
##    for i in range(len(topmoves)):
##        print(i+1,topmoves[i][1][0],topmoves[i][1][1])
    return [x[1] for x in topmoves]
