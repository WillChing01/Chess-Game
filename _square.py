class Square:
    
    def __init__(self,colour,coords,board,occupied=False,piece=None,attacked=False,atpieces=[]):
        self.board=board
        self.colour=colour
        #across then up with numbers instead of letters. col then row.
        self.coords=coords
        self.occupied=occupied
        self.piece=piece
        self.attacked=attacked
        self.atpieces=atpieces
        self.board.squares.append(self)

    def resetstatus(self):
        self.occupied=False
        self.piece=None
        self.attacked=False
        self.atpieces=[]
