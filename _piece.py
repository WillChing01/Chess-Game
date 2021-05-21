class Piece:
    
    def __init__(self,kind,colour,coords,board,captured=False,attacked=False,atpieces=[],guarded=False,gpieces=[]):
        self.board=board
        
        self.kind=kind
        self.colour=colour
        self.coords=coords
        self.captured=captured
        
        self.attacked=attacked
        self.atpieces=atpieces
        self.guarded=guarded
        self.gpieces=gpieces

        self.atsquares=[]
        self.movelist=[]

        self.hasmoved=False
        self.pinned=False

        #self.value=piecevalue[self.kind]

        if self.kind==5:
            self.incheck=False

    def move(self,coords,reverse=False):
        #assumes that every function call is for a legal move.
        #moves checked in main loop.
        if self.captured==False:

            if reverse==False:

                if self.kind!=0:
                    self.board.sides[self.colour].movehistory.append([self.coords,coords,[self,self.board.squares[coords[1]*8+coords[0]].piece]])
                    self.board.moves.append([self.coords,coords,[self,self.board.squares[coords[1]*8+coords[0]].piece]])
            
                sqr=self.board.squares[coords[1]*8+coords[0]]
                if sqr.occupied==True:
                    if sqr.piece.colour!=self.colour:
                        sqr.piece.captured=True

                if self.kind==0:
                    if coords[0]!=self.coords[0] and self.board.squares[coords[1]*8+coords[0]].occupied==False:
                        #capture by enpassant.
                        sqr=self.board.squares[self.coords[1]*8+coords[0]]
                        if sqr.piece.kind==0:
                            sqr.piece.captured=True
                            self.board.sides[self.colour].movehistory.append([self.coords,coords,[self,sqr.piece]])
                            self.board.moves.append([self.coords,coords,[self,sqr.piece]])
                    else:
                        self.board.sides[self.colour].movehistory.append([self.coords,coords,[self,self.board.squares[coords[1]*8+coords[0]].piece]])
                        self.board.moves.append([self.coords,coords,[self,self.board.squares[coords[1]*8+coords[0]].piece]])
                        

                elif self.kind==5:
                    if abs(coords[0]-self.coords[0])==2:
                        #castles.
                        if coords[0]-self.coords[0]==2:
                            #kingside castles.
                            self.board.sides[self.colour].rooks[1].coords[0]=coords[0]-1
                        elif self.coords[0]-coords[0]==2:
                            #queenside castles.
                            self.board.sides[self.colour].rooks[0].coords[0]=coords[0]+1
                            
                        self.board.sides[self.colour].hascastled=True

                self.coords=coords
                self.hasmoved=True
                
            elif reverse==True:

                if self.kind==5:
                    if abs(coords[0]-self.coords[0])==2:
                        #castles
                        if coords[0]-self.coords[0]==2:
                            #reverse queenside castles
                            self.board.sides[self.colour].rooks[0].coords[0]=0
                        elif self.coords[0]-coords[0]==2:
                            #reverse kingside castles
                            self.board.sides[self.colour].rooks[1].coords[0]=7
                        self.coords=coords
                    else:
                        #no castles.
                        self.coords=coords
                else:
                    self.coords=coords

    def availablemoves(self):
        #does not take into account pins/castling.
        self.movelist=[]
        if self.captured==False:
            if self.kind==5:
                for i in self.atsquares:
                    sqr=self.board.squares[i[1]*8+i[0]]
                    if sqr.occupied==False:
                        if sqr.attacked==True:
                            bad=False
                            for j in sqr.atpieces:
                                if j.colour!=self.colour:
                                    bad=True
                                    break
                            if bad==False:
                                self.movelist.append([self.coords,i,[self,self.board.squares[i[1]*8+i[0]].piece]])
                    elif sqr.occupied==True:
                        if sqr.piece.colour!=self.colour:
                            if sqr.piece.guarded==False:
                                self.movelist.append([self.coords,i,[self,self.board.squares[i[1]*8+i[0]].piece]])
                        
                            
            elif self.kind==0:
                #double step for pawn.
                if self.coords[1]==[1,6][self.colour]:
                    sqr1=self.board.squares[(self.coords[1]+1*((-1)**self.colour))*8+self.coords[0]]
                    sqr2=self.board.squares[(self.coords[1]+2*((-1)**self.colour))*8+self.coords[0]]
                    if sqr1.occupied==False and sqr2.occupied==False:
                        self.movelist.append([self.coords,[self.coords[0],self.coords[1]+((-1)**self.colour)*2],[self,None]])
                #check square in front.
                front=self.board.squares[(self.coords[1]+((-1)**self.colour))*8+self.coords[0]]
                if front.occupied==False:
                    self.movelist.append([self.coords,[self.coords[0],self.coords[1]+(-1)**self.colour],[self,None]])
                #check for capture.
                for i in self.atsquares:
                    sqr=self.board.squares[i[1]*8+i[0]]
                    if sqr.occupied==True and sqr.piece.colour!=self.colour:
                        self.movelist.append([self.coords,i,[self,self.board.squares[i[1]*8+i[0]].piece]])
                #check for en passant.
                if self.coords[1]==4-self.colour:
                    right=[self.coords[0]+1,self.coords[1]]
                    left=[self.coords[0]-1,self.coords[1]]
                    if 0<=right[0]<=7:
                        sqr=self.board.squares[right[1]*8+right[0]]
                        if sqr.occupied==True:
                            if sqr.piece.kind==0 and sqr.piece.colour!=self.colour:
                                history=self.board.sides[(self.colour+1)%2].movehistory
                                lastmove=history[len(history)-1]
                                if lastmove[2][0]==sqr.piece and abs(lastmove[1][1]-lastmove[0][1])==2:
                                    self.movelist.append([self.coords,[right[0],self.coords[1]+(-1)**self.colour],[self,lastmove[2][0]]])
                    if 0<=left[0]<=7:
                        sqr=self.board.squares[left[1]*8+left[0]]
                        if sqr.occupied==True:
                            if sqr.piece.kind==0:
                                history=self.board.sides[(self.colour+1)%2].movehistory
                                lastmove=history[len(history)-1]
                                if lastmove[2][0]==sqr.piece and abs(lastmove[1][1]-lastmove[0][1])==2:
                                    self.movelist.append([self.coords,[left[0],self.coords[1]+(-1)**self.colour],[self,lastmove[2][0]]])

                promomoves=[]
                for move in self.movelist:
                    if move[1][1]==(7+self.colour)%8:
                        #promotion.
                        moves=[move]+[move+[x] for x in range(1,5)]
                        promomoves.append(moves)

                for x in promomoves:
                    self.movelist.remove(x[0])
                    for i in range(1,len(x)):
                        self.movelist.append(x[i])
                
            else:
                for i in self.atsquares:
                    sqr=self.board.squares[i[1]*8+i[0]]
                    if sqr.occupied==False:
                        self.movelist.append([self.coords,i,[self,self.board.squares[i[1]*8+i[0]].piece]])
                    elif sqr.occupied==True and sqr.piece.colour!=self.colour:
                        self.movelist.append([self.coords,i,[self,self.board.squares[i[1]*8+i[0]].piece]])

    def resetstatus(self):
        self.attacked=False
        self.atpieces=[]
        self.guarded=False
        self.gpieces=[]
        self.atsquares=[]
        self.movelist=[]
        self.pinned=False
        if self.kind==5:
            self.incheck=False
