Format of piece data:

Coordinates (coords):
    - Type int. (x,y) order with file (col) first and then rank (row).

Squares random access:
    - board.squares[col*8 + row]

Pieces:
    0 - pawn
    1 - rook   (R)
    2 - knight (N)
    3 - bishop (B)
    4 - queen  (Q)
    5 - king   (K)

Colour:
    0 - white
    1 - black

Move notation:

    - [[x1,y1],[x2,y2],[piece object,captured piece (if any)]]

    - List of 2 coordinates; start then end. If valid, piece at start moved to end.

Move notation (special cases):

    - Castles: Normal king move, but 2 squares, not 1. Rook moves automatically.
    - Pawn promotion: [[x1,y1],[x2,y2],[pawn,captured piece (if any)],promoted piece type]

User input:

    - Starting square, space, end square.
    - Upper or lower case for letter.
    - e.g. 'e2 e4' valid for white's first move.

    - Pawn promotion: piece symbol added after move.
    - e.g. 'e7 e8 Q' to promote to queen.

    -Kingside castles: O-O
    -Queenside castles: O-O-O