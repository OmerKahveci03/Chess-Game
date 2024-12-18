class Piece():
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color

def initialize_army(pieces, color):
    rows = (0, 1)
    if color == 'white':
        rows = (7, 6)
    types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(0,8):
        pieces.append(Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        pieces.append(Piece(rows[1], i, 'pawn', color))

def piece_exists(pieces, row, col):
    exists = False
    for piece in pieces:
        if piece.row == row and piece.col == col:
            exists = True
            break
    return exists

def print_pieces(pieces):
    for piece in pieces:
        print(f"{piece.color} {piece.type}, ({piece.row}, {piece.col})")
