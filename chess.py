# chess.py
# This module handles the logic of the chess game. We recieve the moves from game.py as (row, col)

import pieces

# initializes the list of chess pieces. Can be easily updated to have a dynamic "types" for different types of armies and pieces
def initialize_army(army, color):
    rows = (0, 1)
    if color == 'white':
        rows = (7, 6)
    types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(0,8):
        army.append(pieces.Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        army.append(pieces.Piece(rows[1], i, 'pawn', color))

# global lists of the pieces
turn_color = 'white'
selected = None
white_pieces = []
black_pieces = []
initialize_army(white_pieces, 'white')
initialize_army(black_pieces, 'black')

def clicked_piece(row, col):
    for piece in white_pieces + black_pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

# if selected is None, select the piece. Otherwise, try moving the piece to the selected spot, and set selected to None
def board_clicked(row, col):
    global selected

    temp = selected
    piece = clicked_piece(row, col)
    if piece is not None:
        print(f"There is a {piece.color} {piece.type} on ({piece.row}, {piece.col})")
        if piece.color == turn_color:
            selected = piece          
    else:
        print(f"There's an empty square on ({row}, {col})")
        selected = None
    
    if temp is not None:
        for piece in white_pieces + black_pieces:
            if temp is piece:
                # try to move, or reject
                if (row, col) in piece.valid_moves(white_pieces, black_pieces):
                    piece.row = row
                    piece.col = col
                else:
                    print("Invalid Move!")
                selected = None
                break
