import sys
import random
import os

sys.path.insert(0,os.getcwd())

#sys.path.insert(0,'C:\\Users\\willi\\OneDrive\\Desktop\\Python\\Chess Game')

from _side import *
from _square import *
from evaluation_constants import *
from evaluation import *
from engine import *

class Board:

    def __init__(self,verbose=True):

        setattr(Board,negamax.__name__,negamax)
        setattr(Board,rootnegamax.__name__,rootnegamax)
        setattr(Board,evaluate.__name__,evaluate)
        
        self.squares=[]
        self.White=Side(0,self)
        self.Black=Side(1,self)
        self.sides=[self.White,self.Black]
        self.moves=[]

        for y in range(8):
            for x in range(8):
                Square((x+y+1)%2,[x,y],self)

        self.updatestatus()

        self.turn=0 #White's turn at start.

        self.pc=False #if computer is playing
        self.pcside=1 #computer is black, if playing

        self.verbose=verbose

        if self.verbose: self.display()

    def play(self):
        if self.pc==False:
            #self.sides[self.turn].availablemoves() #get legal moves
            self.display(flip=self.turn) #show board.
            print("__________________________\n")

            if self.sides[self.turn].checkmated==True:
                print("Checkmate!")
                if self.turn==0:
                    print("Black wins!")
                else:
                    print("White wins!")
                return 1
            elif self.sides[self.turn].stalemated==True:
                print("Stalemate!")
                return 0
            
            if self.turn==0:
                usermove=input("White to move: ") #standard chess notation.
            else:
                usermove=input("Black to move: ")
            usermove=self.translate(usermove,self.sides[self.turn].colour) #changes to list used by program.
            if usermove not in self.sides[self.turn].movelist: #no piece in square.
                print("Illegal move.")
                print("Not in movelist.")
                return False
            else:
                move=self.sides[self.turn].movepiece(usermove)
                if move==False:
                    print("Illegal move.")
                    return False
                else:
                    self.turn=(self.turn+1)%2
                    self.updatestatus() #also gets available moves for both sides.

    def playself(self,depth):
        while True:

            if self.turn==0:
                print("White to move: ")
            else:
                print("Black to move: ")
            
            self.display()
            
            for side in self.sides:
                if side.checkmated==True:
                    print("Checkmate!")
                    return None
                elif side.stalemated==True:
                    print("Stalemate!")
                    return None

            length=len(self.sides[self.turn].movelist)

##            if length<17:
##                depth=4
##            else:
##                depth=3

            if length>1:
                bestmoves=self.rootnegamax(depth,self.turn)
                #random.shuffle(bestmoves)
                move=self.sides[self.turn].movepiece(bestmoves[0])
            else:
                move=self.sides[self.turn].movepiece(self.sides[self.turn].movelist[0])
                
            self.turn=(self.turn+1)%2
            self.updatestatus()

            print("Move",len(self.moves))

    def pcmove(self,depth):
        length=len(self.sides[self.turn].movelist)
        out=""
        if length>1:
            bestmoves=self.rootnegamax(depth,self.turn)
            move=self.sides[self.turn].movepiece(bestmoves[0])
            out=bestmoves[0]
        else:
            move=self.sides[self.turn].movepiece(self.sides[self.turn].movelist[0])
            out=self.sides[self.turn].movelist[0]
        self.turn=(self.turn+1)%2
        self.updatestatus()
        return out

    def playpc(self,depth):
        print("-----------------")
        print("Choose your side:")
        print("0 - White")
        print("1 - Black")
        print("-----------------")
        
        try:
            colour=int(input("Side:"))
        except:
            print("Please input an integer.")
            return None

        if colour not in [0,1]:
            print("Please input an integer that is 0 or 1.")
            return None

        while True:
            self.display(flip=colour)
            print("__________________________\n")

            if self.turn==colour:
                if self.sides[colour].checkmated==True:
                    print("Checkmate!")
                    print("You lose!")
                    return None
                elif self.sides[colour].stalemated==True:
                    print("Stalemate!")
                    return None
                print("Your turn.")
                usermove=input("Move: ")
                usermove=self.translate(usermove,colour)
                if usermove not in self.sides[self.turn].movelist:
                    print("Illegal move.")
                    print("Not in movelist.")
                    continue
                else:
                    move=self.sides[self.turn].movepiece(usermove)
                    if move==False:
                        print("Illegal move.")
                        continue
                    else:
                        self.turn=(self.turn+1)%2
                        self.updatestatus()
            else:
                if self.sides[(colour+1)%2].checkmated==True:
                    print("Checkmate!")
                    print("You win!")
                    return None
                elif self.sides[(colour+1)%2].stalemated==True:
                    print("Stalemate!")
                    return None
                print("Computer is thinking...")
                length=len(self.sides[(colour+1)%2].movelist)

                if length>1:
                    bestmoves=self.rootnegamax(depth,self.turn)
                    #random.shuffle(bestmoves)
                    move=self.sides[self.turn].movepiece(bestmoves[0])
                else:
                    move=self.sides[self.turn].movepiece(self.sides[self.turn].movelist[0])

                self.turn=(self.turn+1)%2
                self.updatestatus()

    def translate(self,usermove,colour):
        points=usermove.split()
        points=[x.upper() for x in points]
        if usermove=='O-O' or usermove=='O-O-O':
            #castles.
            if usermove=='O-O':
                #print("Kingside castles input.")
                #kingside castles.
                newmove=[self.sides[colour].king.coords,[self.sides[colour].king.coords[0]+2,self.sides[colour].king.coords[1]],[self.sides[colour].king,None]]
            else:
                #queenside castles.
                newmove=[self.sides[colour].king.coords,[self.sides[colour].king.coords[0]-2,self.sides[colour].king.coords[1]],[self.sides[colour].king,None]]
            return newmove
        elif len(points)==2 or len(points)==3:
            if len(points[0])!=2 or len(points[1])!=2:
                return False
            letters=list('ABCDEFGH')
            if points[0][0] not in letters or points[0][1].isdigit()==False or points[1][0] not in letters or points[1][1].isdigit()==False:
                return False
            start=self.squares[(int(points[0][1])-1)*8+letters.index(points[0][0])]
            end=self.squares[(int(points[1][1])-1)*8+letters.index(points[1][0])]
            pieceletters=['','R','N','B','Q']
            if len(points)==3 and start.piece.kind!=0:
                return False
            elif len(points)==3 and points[2] not in pieceletters:
                return False
            ######### number added should have 1 subtracted from it and be in correct range.
            newmove=[start.coords,end.coords,[start.piece,self.squares[end.coords[1]*8+end.coords[0]].piece]]

            #enpassant exception.
            if newmove[2][0].kind==0:
                if start.coords[0]!=end.coords[0] and newmove[2][1]==None:
                    newmove[2][1]=self.moves[-1][2][0]
            if len(points)==3:
                newmove.append(pieceletters.index(points[2]))

            ###############    
            #print(newmove)
            ###############
            
            return newmove
        else:
            return False

    def display(self,flip=False,graphics=False):
        if graphics==False:
            #text graphics for testing.
            wleft='['
            wright=']'
            bleft='['
            bright=']'
            #bleft='{'
            #bright='}'

            colours=[[wleft,wright],[bleft,bright]]

            squarestyles=['KEYWORD','console']

            piecestyles=['KEYWORD','console']

            pawn='P'
            rook='R'
            knight='N'
            bishop='B'
            queen='Q'
            king='K'

            piecetype=[pawn,rook,knight,bishop,queen,king,' ']
            board=['' for x in range(8)]
            letters='   A  B  C  D  E  F  G  H   '

            for y in range(7,-1,-1):
                if flip==True:
                    y=7-y
                a=sys.stdout.shell.write(str(y+1)+" ","DEFINITION")
                
                for x in range(8):
                    if flip==True:
                        x=7-x
                    s=self.squares[y*8+x]
                    a=sys.stdout.shell.write(colours[s.colour][0],squarestyles[s.colour])
                    if s.piece!=None and s.piece.captured==False:
                        a=sys.stdout.shell.write(piecetype[s.piece.kind],piecestyles[s.piece.colour])
                    else:
                        a=sys.stdout.shell.write(' ')
                    a=sys.stdout.shell.write(colours[s.colour][1],squarestyles[s.colour])
                print('')
            if flip==True:
                print(letters[::-1])
            else:
                print(letters)

    def updatestatus(self):
        #update status on squares occupied.
        self.White.resetstatus()
        self.Black.resetstatus()
        
        for i in self.squares:
            i.resetstatus()
        for p in self.White.pieces:
            if p.captured==False:
                p.resetstatus()
                self.squares[p.coords[1]*8+p.coords[0]].occupied=True
                self.squares[p.coords[1]*8+p.coords[0]].piece=p
        for p in self.Black.pieces:
            if p.captured==False:
                p.resetstatus()
                self.squares[p.coords[1]*8+p.coords[0]].occupied=True
                self.squares[p.coords[1]*8+p.coords[0]].piece=p

        #update status on squares attacked and pieces attacked.

        self.White.squaresattacked()
        self.Black.squaresattacked()

        for i in range(len(self.squares)):
            atpieces=self.White.atsquares[i][1]+self.Black.atsquares[i][1]
            if len(atpieces)>0:
                self.squares[i].attacked=True
                self.squares[i].atpieces=atpieces
                if self.squares[i].occupied==True:
                    for p in atpieces:
                        if p.colour==self.squares[i].piece.colour:
                            self.squares[i].piece.guarded=True
                            self.squares[i].piece.gpieces.append(p)
                        else:
                            self.squares[i].piece.attacked=True
                            self.squares[i].piece.atpieces.append(p)

        #check if kings are in check.
        if self.White.king.attacked==True:
            self.White.king.incheck=True
        elif self.Black.king.attacked==True:
            self.Black.king.incheck=True

        self.White.availablemoves()
        self.Black.availablemoves()

        #remove squares attacked by pinned pieces.
        pinned=[]
        for i in range(2):
            for x in self.sides[i].pieces:
                if x.captured==False:
                    if x.pinned==True:
                        pinned.append(x)

        if len(pinned)>0:
            for i in range(len(self.squares)):
                present=False
                for x in pinned:
                    if x in self.squares[i].atpieces:
                        present=True
                        self.squares[i].atpieces.remove(x)
                if present==True:
                    if len(self.squares[i].atpieces)==0:
                       self.squares[i].attacked=False
                    if self.squares[i].occupied==True:
                        for x in pinned:
                            if x in self.squares[i].piece.atpieces:
                                self.squares[i].piece.atpieces.remove(x)
                            elif x in self.squares[i].piece.gpieces:
                                self.squares[i].piece.gpieces.remove(x)
                            if len(self.squares[i].piece.atpieces)==0:
                                self.squares[i].piece.attacked=False
                            elif len(self.squares[i].piece.gpieces)==0:
                                self.squares[i].guarded=False

    def makemove(self,move,colour):
        result=self.sides[colour].movepiece(move)
        if result==False:
            print("Error in making move:",move)
            self.display()
        else:
            self.turn=(self.turn+1)%2
            self.updatestatus()

    def undo(self,move):
        #reverts the specified move, and all other moves which occurred after it.
        #get last possible index of move.
        try:
            index=max([i for i in range(len(self.moves)) if self.moves[i]==move])
        except:
            print("Error in reversing move:")
            print(move)
            self.display()
            print(self.moves)
        start=len(self.moves)
        for i in range(start-1,index-1,-1):
            m=self.moves[i]
            piece=m[2][0]
            taken=m[2][1]

            #remove from side history.
            #self.sides[piece.colour].movehistory.remove(m)
            del self.sides[piece.colour].movehistory[-1]
            #delete move from history.
            #self.moves.remove(m)
            del self.moves[-1]

            #move piece back.
            piece.move(m[0],reverse=True)

            #respawn captured piece if any.
            if taken!=None:
                taken.captured=False

            #change moved status to False if necessary for pawn or king.

            if piece.kind==5 or piece.kind==1 or piece.kind==4 or piece.kind==2 or piece.kind==3:
                if piece.kind==5 and abs(m[0][0]-m[1][0])==2:
                    #castles.
                    piece.hasmoved=False
                    if m[0][0]-m[1][0]==2:
                        #reverse queenside castles
                        self.sides[piece.colour].rooks[0].hasmoved=False
                    elif m[1][0]-m[0][0]==2:
                        #reverse kingside castles
                        self.sides[piece.colour].rooks[1].hasmoved=False
                    self.sides[piece.colour].hascastled=False
                bad=False
                for x in self.sides[piece.colour].movehistory:
                    if x[2][0]==piece:
                        bad=True
                        break
                if bad==False:
                    piece.hasmoved=False
                if piece.kind==5:
                    if piece not in [x[2][0] for x in self.moves]:
                        if piece.hasmoved==True:
                            print("ERROR!")
                            print(piece.colour)
                            print(m)

            #change piece type back to pawn if necessary.
            if len(move)==4:
                piece.kind=0

        #update which side to move.
        self.turn=len(self.moves)%2

        self.updatestatus()
