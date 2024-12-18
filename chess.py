# chess.py
# This module handles the logic of the chess game. We recieve the moves from game.py as (row, col)

from common import ROWS, COLS

class Piece():
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color

# returns true if the given (row, col) location has an enemy piece
    def enemy_piece_at(self, row, col):
        the_piece = piece_at(row, col)

        if the_piece is not None:
            if the_piece.color != self.color:
                return True
        return False
    
# returns true if the given (row, col) move is legal for this piece
    def is_valid_move(self, row, col):
        is_legal = True
        the_piece = piece_at(row, col)
        
        if the_piece is not None:
            if the_piece.color == self.color:
                is_legal = False
        
        if 0 > row or row > ROWS or 0 > col or col > COLS:
            is_legal = False

        # if king is left in check, is_legal = False
        return is_legal

    def directional_moves(self, directions):
        move_list = []
        for direction in directions:
                i = 1
                row = self.row + direction[0] * i
                col = self.col + direction[1] * i
                while self.is_valid_move(row, col):
                    move_list.append((row, col))
                    i += 1
                    if self.enemy_piece_at(row, col):
                        break
                    row = self.row + direction[0] * i
                    col = self.col + direction[1] * i
        return move_list

    def move(self, row, col):
        # remove enemy piece if it is here
        if self.enemy_piece_at(row, col):
             pass
        self.row = row
        self.col = col

    # returns a list of coordinates (row, col) that this piece is allowed to move to
    def valid_moves(self):
        move_list = []

        if self.type == 'pawn':
            direction = 1
            start = 1
            if self.color == 'white':
                direction = -1
                start = 6

            if not self.enemy_piece_at(self.row + direction, self.col): # basic move
                move_list.append((self.row + direction, self.col))
                if self.row == start and not self.enemy_piece_at(self.row + direction * 2, self.col):
                    move_list.append((self.row + direction * 2, self.col))
            if self.enemy_piece_at(self.row + direction, self.col + 1): # capture moves
                move_list.append((self.row + direction, self.col + 1))
            if self.enemy_piece_at(self.row + direction, self.col - 1): # capture moves
                move_list.append((self.row + direction, self.col - 1))

            return move_list    # pawns follow unique rules, so I'm returning it before the filter

        elif self.type == 'knight':
            moves = [(2,1), (2,-1), (1,2), (1,-2), (-1,2), (-1,-2), (-2,1), (-2,-1)]
            for move in moves:
                move_list.append((self.row + move[0], self.col + move[1]))

        elif self.type == 'bishop':
            directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
            move_list = self.directional_moves(directions)

        elif self.type == 'rook':
            directions = [(1,0), (0,-1), (0,1), (-1,0)]
            move_list = self.directional_moves(directions)

        elif self.type == 'queen':
            directions = [(1,0), (0,-1), (0,1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            move_list = self.directional_moves(directions)

        elif self.type == 'king':
            moves = [(-1,-1), (-1, 0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,-1)]
            for move in moves:
                move_list.append((self.row + move[0], self.col + move[1]))
        else:
            # this is just to make sure it is used correctly
            move_list = [(3,3), (3,4), (4,3), (4,4)]

        for move in move_list:
            if not self.is_valid_move(*move):
                move_list.remove(move)

        return move_list



# initializes the list of chess pieces. Can be easily updated to have a dynamic "types" for different types of armies and pieces
def initialize_army(army, color):
    rows = (0, 1)
    if color == 'white':
        rows = (7, 6)
    types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for i in range(0,8):
        army.append(Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        army.append(Piece(rows[1], i, 'pawn', color))

# global data
turn_color = 'white'
selected = None

white_pieces = []
black_pieces = []
initialize_army(white_pieces, 'white')
initialize_army(black_pieces, 'black')

# returns the piece located at row, col
def piece_at(row, col):
    for piece in white_pieces + black_pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

# if selected is None, select the piece. Otherwise, try moving the piece to the selected spot, and set selected to None
def board_clicked(row, col,):
    global selected, turn_color

    temp = selected
    piece = piece_at(row, col)
    if piece is not None:
        print(f"There is a {piece.color} {piece.type} on ({piece.row}, {piece.col})")
        if piece.color == turn_color:
            selected = piece          
    else:
        print(f"There's an empty square on ({row}, {col})")
        selected = None
    
    # a piece was previously selected
    if temp is not None:
        for piece in white_pieces + black_pieces:       # find the previously selected piece in the lists
            if temp is piece:
                # try to move, or reject
                if (row, col) in piece.valid_moves():
                    piece.move(row, col, white_pieces, black_pieces)
                    if turn_color == 'white':
                        turn_color = 'black'
                    else:
                        turn_color = 'white'
                    print(f"{turn_color}'s turn.")
                else:
                    print("Invalid Move!")
                selected = None
                break
