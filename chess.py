# chess.py
# This module handles the logic of the chess game. We recieve the moves from game.py as (row, col)

# BASE GAME TO DO:
# 1) Castling
# 2) En Peassant
# 3) Promotion

from common import ROWS, COLS

# global data
turn_color = 'white'
selected = None
pieces = []
winner = None

# returns the piece located at (row, col)
def piece_at(row, col):
    for piece in pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

# returns true if the given (row, col) location has an enemy piece
def enemy_piece_at(row, col):
    target_piece = piece_at(row, col)

    if target_piece is not None:
        if target_piece.color != turn_color:
            return True
    return False

class Piece():
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color
        self.has_moved = False

    # kills the piece by removing it from the list. Also returns it in case you'd want to use it
    def kill(self):
        pieces.remove(self)
        return self

    # moves the piece from its initial position to (row, col)
    def move(self, row, col):
        global turn_color

        # if we are castling (short), move rook too
        if self.type == 'king' and self.col + 2 == col: 
            rook = piece_at(row, col + 1)
            rook.col = self.col + 1
        if self.type == 'king' and self.col - 2 == col:
            rook = piece_at(row, col - 2)
            rook.col = self.col - 1

        target_piece = piece_at(row, col)
        if target_piece:
            target_piece.kill()
        self.row = row
        self.col = col
        self.has_moved = True

        # promotion checking
        if self.type == 'pawn':
            if (self.color == 'white' and self.row == 0) or (self.color == 'black' and self.row == ROWS - 1):
                self.type = 'queen'

        if turn_color == 'white':
            turn_color = 'black'
        else:
            turn_color = 'white'

        print(f"{turn_color}'s turn.")

# returns true if the given move (row, col) doesn't go out of bounds or onto a friendly piece
    def is_legal_move(self, row, col):
        target_piece = piece_at(row, col)
        
        # can't move onto your own piece
        if target_piece is not None:
            if target_piece.color == self.color:
#                print(f"Can't move onto your own piece {(row, col)}")
                return False
        
        # can't move out of bounds
        if 0 > row or row >= ROWS or 0 > col or col >= COLS:
#            print(f"Can't move out of bounds {(row, col)}")
            return False
        return True

    # reusable and dynamic code for pieces that move in a fixed direction (row, col)
    # default length is the entire board, but if we make pieces that can only go a fixed distance, this is helpful
    def directional_moves(self, directions, length=ROWS):
        move_list = []
        for direction in directions:
            i = 1
            while i <= length:
                row = self.row + direction[0] * i
                col = self.col + direction[1] * i
                if not self.is_legal_move(row, col):
                    break  # Stop if the move is out of bounds or occupied by a friendly piece
                move_list.append((row, col))
                if piece_at(row, col):  # Stop if any piece is encountered
                    break
                i += 1
        return move_list


    # returns a list of legal moves (row, col) that this piece can take (ignoring checks))
    def get_base_moves(self):
        move_list = []

        if self.type == 'pawn':
            direction = 1
            if self.color == 'white':
                direction = -1

            if not piece_at(self.row + direction, self.col):
                move_list.append((self.row + direction, self.col))
                if not self.has_moved and not piece_at(self.row + 2*direction, self.col):
                    move_list.append((self.row + 2*direction, self.col))

            if enemy_piece_at(self.row + direction, self.col + 1):
                move_list.append((self.row + direction, self.col + 1))
            if enemy_piece_at(self.row + direction, self.col - 1):
                move_list.append((self.row + direction, self.col - 1))

        elif self.type == 'knight':
            moves = [(2,1), (2,-1), (1,2), (1,-2), (-1,2), (-1,-2), (-2,1), (-2,-1)]
            for move in moves:
                move_list = self.directional_moves(moves, 1)

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
            moves = [(-1,-1), (-1, 0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1), (0,2), (0,-2)]
            short_rook = piece_at(self.row, self.col + 3)
            long_rook = piece_at(self.row, self.col - 4)
            if short_rook:
                if self.has_moved or piece_at(self.row, self.col + 1) or short_rook.has_moved:
                    moves.remove((0,2))
            if long_rook:
                if self.has_moved or piece_at(self.row, self.col - 1) or piece_at(self.row, self.col - 2) or long_rook.has_moved:
                    moves.remove((0,-2))
            move_list = self.directional_moves(moves, 1)

        else:
            # this is just to make sure it is used correctly
            move_list = [(3,3), (3,4), (4,3), (4,4)]

        return move_list
    
# returns true if the piece can attack the king. Move list is all valid moves without check testing
    def threatens_enemy_king(self):
        king_row, king_col = None, None
        for piece in pieces:
            if piece.type == 'king' and piece.color != self.color:
                king_row, king_col = piece.row, piece.col
        
        move_list = self.get_base_moves()
        for move in move_list:
            if move[0] == king_row and move[1] == king_col:
                print(f"The {self.color} {self.type} is delivering check!")
                return True
        return False

# gets base moves, then filters out illegal ones caused by check
    def get_valid_moves(self):
        move_list = self.get_base_moves()
        valid_moves = []

        # do check testing
        # first, simulate move. Then test for check. Then undo
        for move in move_list:
            # simulate move
            original_row, original_col = self.row, self.col
            target_piece = piece_at(move[0], move[1])
            if target_piece:
                pieces.remove(target_piece)
            self.row, self.col = move

            # test all enemy pieces to see if they threaten our king
            in_check = False
            for piece in pieces:
                enemy_piece_moves = piece.get_base_moves()
                if piece.color != self.color and piece.threatens_enemy_king():
                    in_check = True
                    break
                
            # undo
            if target_piece:
                pieces.append(target_piece)
            self.row, self.col = original_row, original_col
            
            if not in_check:
                valid_moves.append(move)

        # special castling testing
        if self.type == 'king':
            if (self.row, self.col + 2) in valid_moves and (self.row, self.col + 1) not in valid_moves:
                valid_moves.remove((self.row, self.col + 2))
            if (self.row, self.col - 2) in valid_moves and (self.row, self.col - 1) not in valid_moves:
                valid_moves.remove((self.row, self.col - 2))
        return valid_moves


# initializes the list of chess pieces. Can be easily updated to have a dynamic "types" for different types of armies and pieces
def initialize_army(color, types):
    rows = (0, 1)
    if color == 'white':
        rows = (7, 6)
    for i in range(0,8):
        pieces.append(Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        pieces.append(Piece(rows[1], i, 'pawn', color))

types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
initialize_army('white', types)
initialize_army('black', types)

# search every piece. If any of them can move, it is not checkmate
def is_checkmate():
    valid_moves = []
    for piece in pieces:
        if piece.color == turn_color:
            valid_moves += piece.get_valid_moves()
            if valid_moves:
                return False
            
    global winner
    if turn_color == 'black':
        winner = 'white'
    else:
        winner = 'black'
    return True

# Either (try to) select a piece, or (try to) move the selected piece
def board_clicked(row, col,):
    global selected, turn_color

    temp = selected
    piece = piece_at(row, col)
    if piece is not None:
#        print(f"There is a {piece.color} {piece.type} on ({piece.row}, {piece.col})")
        if piece.color == turn_color:
            selected = piece

            # print move options
            move_list = piece.get_valid_moves()
            print(f"{piece.color} {piece.type} has moves: ", end="")
            for move in move_list:
                print(f"({move[0]}, {move[1]})", end=" ")
            print("")         

    else:
#        print(f"There's an empty square on ({row}, {col})")
        selected = None
    
    # a piece was previously selected
    if temp is not None:
        for piece in pieces:       # find the previously selected piece in the lists
            if temp is piece:
                move_list = piece.get_valid_moves()
                # try to move, or reject
                if (row, col) in move_list:
                    piece.move(row, col)
                    if is_checkmate():
                        print(f"Checkmate! {winner} has won!")
                else:
                    print("\n\nInvalid Move!\n\n")
                selected = None
                break