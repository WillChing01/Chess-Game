import sys
import os

sys.path.insert(0,os.getcwd())

#sys.path.insert(0,'C:\\Users\\willi\\OneDrive\\Desktop\\Python\\Chess Game')

from evaluation_constants import *

def evaluate(self,colour):
    #evaluates the current state of the board.

    scores=[0,0]

    if self.White.checkmated==True:
        scores=[-1000000,0]
    elif self.Black.checkmated==True:
        scores=[0,-1000000]

    else:
        #evaluate material.
        for i in range(2):
            for p in self.sides[i].pieces:
                if p.captured==False:

                    #piece value
                    scores[i]+=piecevalue[p.kind]

                    #piece square table
                    if i==0:
                        squarescore=tables[0][p.kind][p.coords[1]+p.coords[0]*8]
                    else:
                        squarescore=tables[0][p.kind][(7-p.coords[1])+(7-p.coords[0])*8]
                    scores[i]+=squarescore
                    
##                    #specific attributes.
##                    if p.kind==1:
##                        #rook
##
##                        #open/semi open file
##                        filescore=20
##                        blocking=[]
##                        for y in range(8):
##                            sqr=self.squares[y*8+p.coords[0]]
##                            if sqr.piece!=None:
##                                if sqr.piece.kind==0:
##                                    filescore-=10
##                        scores[i]+=filescore
##
##                        #7th rank rook only if pawns there or king on 8th.
##                        rankscore=0
##                        if p.coords[1]==6**((p.colour+1)%2):
##                            if self.sides[(p.colour+1)%2].king.coords[1]==(7+p.colour)%8:
##                                rankscore+=10
##                        scores[i]+=rankscore
##
##                        #bonus for xray attack on king.
##                        k=self.sides[(p.colour+1)%2].king
##                        if k.coords[0]==p.coords[0] or k.coords[1]==p.coords[1]:
##                            scores[i]+=5
##
##                        #bonus for defended by friendly rook.
##                        if p.guarded==True:
##                            for x in p.gpieces:
##                                if x.kind==1:
##                                    scores[i]+=10
##
##                        #penalty for undefended.
##                        elif p.guarded==False:
##                            scores[i]-=25
##
##                        #penalty for developing before castles.
##                        if p.hasmoved==True and self.sides[i].hascastled==False:
##                            scores[i]-=25
##                        
##                    elif p.kind==2:
##                        #knight
##
##                        #small bonus if defended by pawn.
##                        defended=False
##                        if p.guarded==True:
##                            for x in p.gpieces:
##                                if x.kind==0:
##                                    scores[i]+=10
##                                    defended=True
##                                    break
##
##                        #bonus for outpost.
##                        #outpost rank(4567-white), defended by pawn. not attackable by enemy pawns.
##                        if defended==True:
##                            if abs(((7+p.colour)%8)-p.coords[1])<=4:
##                                start=p.coords[1]+(-1)**p.colour
##                                end=[6,1][p.colour]
##                                step=(-1)**p.colour
##                                outpost=True
##                                if p.coords[0]<7:
##                                    #right
##                                    for y in range(start,end+step,step):
##                                        sqr=self.squares[y*8+p.coords[0]+1]
##                                        if sqr.occupied==True:
##                                            if sqr.piece.kind==0:
##                                                outpost=False
##                                                break
##                                if p.coords[0]>0 and outpost==True:
##                                    #left
##                                    for y in range(start,end+step,step):
##                                        sqr=self.squares[y*8+p.coords[0]-1]
##                                        if sqr.occupied==True:
##                                            if sqr.piece.kind==0:
##                                                outpost=False
##                                                break
##                                if outpost==True:
##                                    scores[i]+=50
##
##                        #penalty for not developing.
##                        if p.hasmoved==False:
##                            scores[i]-=20
##
##                        #penalty for undefended.
##                        if p.guarded==False:
##                            scores[i]-=20
##                    
##                    elif p.kind==3:
##                        #bishop
##
##                        #bad bishop
##
##                        #penalty for not developing.
##                        if p.hasmoved==False:
##                            scores[i]-=20
##
##                        #penalty for undefended.
##                        if p.guarded==False:
##                            scores[i]-=20
##
##                    elif p.kind==4:
##                        #queen
##
##                        #penalty for early development
##
##                        if p.hasmoved==True and len(self.moves)<10:
##                            scores[i]-=100
##
##                        #penalty for undefended.
##                        if p.guarded==False:
##                            scores[i]-=30
##
##                    elif p.kind==5:
##                        #king
##
##                        #king safety midgame.
##
##                        #king central endgame.
##
##                        #x-ray/pins.
##
##                        #penalty if in check.
##                        if p.incheck==True:
##                            scores[i]-=40
##                        
##                        pass
##
##                    if p.kind!=5:
##                        #trade deals.
##                        #bonus if defended more than attacked.
##                        diff=len(p.atpieces)-len(p.gpieces)
##                        scores[i]-=round(diff*piecevalue[p.kind]/10)
##
##                        if diff>0 and p.guarded==False:
##                            scores[i]-=piecevalue[p.kind]
##
##            #bishop pair.
##
##            if sum([x.captured for x in self.sides[i].bishops])==0:
##                scores[i]+=15
##
##            #pawn structure.
##
##            #midgame/endgame interpolation.
##
##            #mobility of pieces.
##
##            for x in self.sides[i].movelist:
##                if x[2][0].kind<4:
##                    scores[i]+=5
##
##            #centre control.
##            coords=[[3,3],[3,4],[4,3],[4,4]]
##            sqrs=[self.squares[x[1]*8+x[0]] for x in coords]
##            for x in sqrs:
##                if x.occupied==True:
##                    if x.piece.colour==i:
##                        if x.piece.kind==0:
##                            scores[i]+=30
##                            scores[i]+=5*len(x.piece.gpieces)
##                        elif x.piece.kind==2:
##                            scores[i]+=10
##                            scores[i]+=5*len(x.piece.gpieces)
##                for a in x.atpieces:
##                    if a.colour==i:
##                        scores[i]+=5
##
##            #bonus for castles
##            if self.sides[i].hascastled==True:
##                scores[i]+=70

    total=scores[0]-scores[1]

    return total*((-1)**colour)
