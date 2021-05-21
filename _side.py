import sys
import os

sys.path.insert(0,os.getcwd())

#sys.path.insert(0,'C:\\Users\\willi\\OneDrive\\Desktop\\Python\\Chess Game')

from _piece import *

class Side:
    
    def __init__(self,colour,board):
        self.board=board
        self.colour=colour
        self.king=Piece(5,colour,[4,(8-colour)%8],self.board)
        self.queen=Piece(4,colour,[3,(8-colour)%8],self.board)
        self.bishops=[Piece(3,colour,[2,(8-colour)%8],self.board),Piece(3,colour,[5,(8-colour)%8],self.board)]
        self.knights=[Piece(2,colour,[1,(8-colour)%8],self.board),Piece(2,colour,[6,(8-colour)%8],self.board)]
        self.rooks=[Piece(1,colour,[0,(8-colour)%8],self.board),Piece(1,colour,[7,(8-colour)%8],self.board)]
        self.pawns=[Piece(0,colour,[x,[1,6][colour]],self.board) for x in range(8)]
        self.pieces=[self.king,self.queen]+self.bishops+self.knights+self.rooks+self.pawns

        self.checkmated=False
        self.stalemated=False
        self.hascastled=False

        self.movehistory=[]
        self.movelist=[]

        self.atsquares=[] #squares attacked by pieces of that colour. form [[[x,y],[object]],[[x2,y2],[object2]]]

    def movepiece(self,moveinfo):
        if moveinfo[2][0].colour==self.colour and moveinfo in self.movelist:
            moveinfo[2][0].move(moveinfo[1])
            if len(moveinfo)==4:
                moveinfo[2][0].kind=moveinfo[3]
                self.board.moves[-1].append(moveinfo[3])
                self.movehistory[-1].append(moveinfo[3])
            return True
        else:
            return False

    def squaresattacked(self):

        self.atsquares=[]

        attacked=[[[x,y],[]] for y in range(8) for x in range(8)]

        for p in self.pieces:
            if p.captured==False:
                if p.kind==5:
                    #king.
                    for x in range(p.coords[0]-1,p.coords[0]+2):
                        for y in range(p.coords[1]-1,p.coords[1]+2):
                            if x>=0 and x<=7 and y>=0 and y<=7:
                                if [x,y]!=p.coords:
                                    attacked[y*8+x][1].append(p)
                                    p.atsquares.append([x,y])

                #queen.
                elif p.kind==4:
                    stop=[False for x in range(8)]
                    for i in range(1,8):
                        
                        points=[[p.coords[0],p.coords[1]+i],
                                [p.coords[0],p.coords[1]-i],
                                [p.coords[0]-i,p.coords[1]],
                                [p.coords[0]+i,p.coords[1]],
                                [p.coords[0]+i,p.coords[1]+i],
                                [p.coords[0]+i,p.coords[1]-i],
                                [p.coords[0]-i,p.coords[1]-i],
                                [p.coords[0]-i,p.coords[1]+i]]

                        for j in range(len(points)):
                            if 0<=points[j][0]<=7 and 0<=points[j][1]<=7 and stop[j]==False:
                                sqr=self.board.squares[points[j][1]*8+points[j][0]]
                                if sqr.piece!=None:
                                    stop[j]=True
                                attacked[points[j][1]*8+points[j][0]][1].append(p)
                                p.atsquares.append(points[j])
                        
                #bishop.
                elif p.kind==3:

                    bstop=[False for x in range(4)]

                    for i in range(1,8):
                        bpoints=[[p.coords[0]+i,p.coords[1]+i],
                                 [p.coords[0]+i,p.coords[1]-i],
                                 [p.coords[0]-i,p.coords[1]-i],
                                 [p.coords[0]-i,p.coords[1]+i]]

                        for j in range(len(bpoints)):
                            if 0<=bpoints[j][0]<=7 and 0<=bpoints[j][1]<=7 and bstop[j]==False and p.captured==False:
                                sqr=self.board.squares[bpoints[j][1]*8+bpoints[j][0]]
                                if sqr.piece!=None:
                                    bstop[j]=True
                                attacked[bpoints[j][1]*8+bpoints[j][0]][1].append(p)
                                p.atsquares.append(bpoints[j])

                #rook.
                elif p.kind==1:
                    
                    rstop=[False for x in range(4)]

                    for i in range(1,8):
                        rpoints=[[p.coords[0],p.coords[1]+i],
                                 [p.coords[0],p.coords[1]-i],
                                 [p.coords[0]-i,p.coords[1]],
                                 [p.coords[0]+i,p.coords[1]]]

                        for j in range(len(rpoints)):
                            if 0<=rpoints[j][0]<=7 and 0<=rpoints[j][1]<=7 and rstop[j]==False and p.captured==False:
                                sqr=self.board.squares[rpoints[j][1]*8+rpoints[j][0]]
                                if sqr.piece!=None:
                                    rstop[j]=True
                                attacked[rpoints[j][1]*8+rpoints[j][0]][1].append(p)
                                p.atsquares.append(rpoints[j])
                
                #knight.
                elif p.kind==2:
                    
                    inc=[1,-1,2,-2]
                    
                    kpoints=[[p.coords[0]+inc[a],p.coords[1]+inc[b]] for a in range(len(inc)) for b in range(len(inc)) if abs(inc[a])!=abs(inc[b])]
                    
                    for j in range(len(kpoints)):
                        if 0<=kpoints[j][0]<=7 and 0<=kpoints[j][1]<=7 and p.captured==False:
                            attacked[kpoints[j][1]*8+kpoints[j][0]][1].append(p)
                            p.atsquares.append(kpoints[j])
        
                #pawn.
                elif p.kind==0:
                    points=[[p.coords[0]+1,p.coords[1]+(-1)**self.colour],
                            [p.coords[0]-1,p.coords[1]+(-1)**self.colour]]
                    for x in points:
                        if 0<=x[0]<=7 and 0<=x[1]<=7 and p.captured==False:
                            attacked[x[1]*8+x[0]][1].append(p)
                            p.atsquares.append(x)

        self.atsquares=attacked

    def availablemoves(self):
        
        self.movelist=[]
        
        if self.king.incheck==True:
            #move king to safety.
            self.king.availablemoves()

            col=False
            row=False
            diag=[]

            for p in self.king.atpieces:
                if p.kind==1:
                    #rook
                    if p.coords[0]==self.king.coords[0]:
                        col=True
                    elif p.coords[1]==self.king.coords[1]:
                        row=True
                elif p.kind==3:
                    #bishop
                    vector=[self.king.coords[0]-p.coords[0],self.king.coords[1]-p.coords[1]]
                    diag.append(vector)
                elif p.kind==4:
                    #queen
                    if p.coords[0]==self.king.coords[0]:
                        col=True
                    elif p.coords[1]==self.king.coords[1]:
                        row=True
                    else:
                        vector=[self.king.coords[0]-p.coords[0],self.king.coords[1]-p.coords[1]]
                        diag.append(vector)

            kingmoves=self.king.movelist[:]
            for x in kingmoves:
                bad=False
                if col==True and x[1][0]==self.king.coords[0] and x[2][1] not in self.king.atpieces:
                    bad=True
                if row==True and x[1][1]==self.king.coords[1] and x[2][1] not in self.king.atpieces:
                    bad=True

                kingv=[x[1][0]-self.king.coords[0],x[1][1]-self.king.coords[1]]

                if kingv[0]!=0 and kingv[1]!=0:
                    for v in diag:
                        if v[0]/kingv[0]==v[1]/kingv[1] and x[2][1] not in self.king.atpieces:
                            bad=True
                            break
                            
                if bad==False:
                    self.movelist.append(x)
                

            if len(self.king.atpieces)==1:
                #can only block/take with single attacker.
                #block check with piece.
                if self.king.atpieces[0].kind==1 or self.king.atpieces[0].kind==3 or self.king.atpieces[0].kind==4:
                    #can only block if rook,bishop,queen attacking.

                    #get vector from attacker to king.
                    vector=[self.king.coords[0]-self.king.atpieces[0].coords[0],self.king.coords[1]-self.king.atpieces[0].coords[1]]
                    distance=max([abs(x) for x in vector])

                    blocksqrs=[]

                    for i in range(1,distance):
                        point=[self.king.atpieces[0].coords[0]+int(vector[0]*(i/distance)),self.king.atpieces[0].coords[1]+int(vector[1]*(i/distance))]
                        blocksqrs.append(point)

                    #################
                    #print(blocksqrs)
                    #################

                        #find pieces which can move to blocksqrs.
                    if len(blocksqrs)>0:
                        if self.queen.captured==False: self.queen.availablemoves()
                        for bishop in self.bishops:
                            if bishop.captured==False: bishop.availablemoves()
                        for rook in self.rooks:
                            if rook.captured==False: rook.availablemoves()
                        for knight in self.knights:
                            if knight.captured==False: knight.availablemoves()
                        for pawn in self.pawns:
                            if pawn.captured==False: pawn.availablemoves()

                        for piece in self.pieces:
                            if piece.captured==False:
                                for x in piece.movelist:
                                    if x[1] in blocksqrs:
                                        self.movelist.append(x)
                        
                                            
                #take attacking piece, with other piece (king done already).
                for p in self.king.atpieces[0].atpieces:
                    if p!=self.king:
                        self.movelist.append([p.coords,self.king.atpieces[0].coords,[p,self.king.atpieces[0]]])
                    
        else:
            #get moves from individual pieces. check for pins.
            if self.queen.captured==False:
                self.queen.availablemoves()
            for bishop in self.bishops:
                if bishop.captured==False:
                    bishop.availablemoves()
            for rook in self.rooks:
                if rook.captured==False:
                    rook.availablemoves()
            for knight in self.knights:
                if knight.captured==False:
                    knight.availablemoves()
            for pawn in self.pawns:
                if pawn.captured==False:
                    pawn.availablemoves()

            pinpieces=[]

            for p in self.board.sides[(self.colour+1)%2].pieces:

                if p.captured==False:

                    if p.kind==1 or p.kind==3 or p.kind==4:

                        vec=[self.king.coords[0]-p.coords[0],self.king.coords[1]-p.coords[1]]
                        distance=max([abs(x) for x in vec])

                        if p.kind==4:
                            if vec[0]==0 or vec[1]==1 or abs(vec[0])==abs(vec[1]):
                                pinpieces.append([p.coords,vec,p])

                        elif p.kind==3:
                            if abs(vec[0])==abs(vec[1]):
                                pinpieces.append([p.coords,vec,p])

                        elif p.kind==1:
                            if vec[0]==0 or vec[1]==0:
                                pinpieces.append([p.coords,vec,p])
                                
            for x in pinpieces:
                distance=max([abs(x) for x in x[1]])
                blocksqrs=[]
                obstruct=False
                for i in range(1,distance):
                    sqr=self.board.squares[(x[0][1]+int(x[1][1]*(i/distance)))*8+(x[0][0]+int(x[1][0]*(i/distance)))]
                    blocksqrs.append(sqr)
                    if sqr.occupied==True:
                        if sqr.piece.colour!=self.colour:
                            obstruct=True
                            break
                if obstruct==False:
                    pinned=[a.piece for a in blocksqrs if a.occupied==True]
                    if len(pinned)==1:
                        pinned[0].movelist=[a for a in pinned[0].movelist if a[2][1]==x[2]]
                        pinned[0].pinned=True

            #check for pins. remove moves which lead to this.

            #add all legal moves.
            self.king.availablemoves()

            for piece in self.pieces:
                if piece.captured==False:
                    for x in piece.movelist:
                        self.movelist.append(x)

            #check for castles.
            if self.king.hasmoved==False:
                kingrooksqr=self.board.squares[((8-self.colour)%8)*8+7]
                queenrooksqr=self.board.squares[((8-self.colour)%8)*8]
                #print(kingrooksqr.coords)
                #print(queenrooksqr.coords)
                if kingrooksqr.occupied==True:
                    if kingrooksqr.piece.kind==1 and kingrooksqr.piece.hasmoved==False:
                        sqrs=[self.board.squares[((8-self.colour)%8)*8+5],self.board.squares[((8-self.colour)%8)*8+6]]
                        if sqrs[0].occupied==False and sqrs[1].occupied==False:
                            cankingside=True
                            for s in sqrs:
                                if s.attacked==True:
                                    for p in s.atpieces:
                                        if p.colour!=self.colour:
                                            cankingside=False
                                            break
                            if cankingside==True:
                                #print("Can kingside castle.")
                                self.movelist.append([self.king.coords,[self.king.coords[0]+2,self.king.coords[1]],[self.king,None]])
                if queenrooksqr.occupied==True:
                    if queenrooksqr.piece.kind==1 and queenrooksqr.piece.hasmoved==False:
                        sqrs=[self.board.squares[((8-self.colour)%8)*8+1],
                              self.board.squares[((8-self.colour)%8)*8+2],
                              self.board.squares[((8-self.colour)%8)*8+3]]
                        if sqrs[0].occupied==False and sqrs[1].occupied==False and sqrs[2].occupied==False:
                            canqueenside=True
                            for s in sqrs:
                                if s.attacked==True and s.coords[0]!=1:
                                    for p in s.atpieces:
                                        if p.colour!=self.colour:
                                            canqueenside=False
                                            break
                            if canqueenside==True:
                                #print("Can queenside castle.")
                                self.movelist.append([self.king.coords,[self.king.coords[0]-2,self.king.coords[1]],[self.king,None]])

        if len(self.movelist)==0 and self.king.incheck==True:
            self.checkmated=True
        elif len(self.movelist)==0 and self.king.incheck==False:
            self.stalemated=True
                    
    def resetstatus(self):
        self.movelist=[]
        self.atsquares=[]
        self.checkmated=False
        self.stalemated=False
