# chess.py
# This module handles the logic of the chess game. We recieve the moves from game.py as (row, col)

class Piece():
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color

    # returns a list of coordinates (row, col) that this piece is allowed to move to
    def return_valid_moves(self, white_pieces, black_pieces):
        pass

# initializes the list of chess pieces. Can be easily updated to have a dynamic "types" for different types of armies and pieces
def initialize_army(pieces, color):
    rows = (0, 1)
    if color == 'white':
        rows = (7, 6)
    types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(0,8):
        pieces.append(Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        pieces.append(Piece(rows[1], i, 'pawn', color))

# global lists of the pieces
white_pieces = []
black_pieces = []
initialize_army(white_pieces, 'white')
initialize_army(black_pieces, 'black')

def clicked_piece(row, col):
    for piece in white_pieces + black_pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

def print_pieces(pieces):
    for piece in pieces:
        print(f"{piece.color} {piece.type}, ({piece.row}, {piece.col})")

