# chess.py
# This module handles the logic of the chess game. We recieve the moves from game.py as (row, col)

# BASE GAME TO DO:
# 1) Stalemate (Insufficient Material)
# 2) Custom Promoting (need front-end help, can do this later down the line)

from common import ROWS, COLS
from moves import Move, undo_last_move

# global data
turn_color = 'white'
selected = None     # the piece to be highlighted
pieces = []
winner = None
move_history = []

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
        self.times_moved = 0

    def __str__(self):
        s = f"{self.color} {self.type}"
        if self.times_moved == 0:
            s += f" [{self.row}, {self.col}]."
        else:
            s += f" ({self.row}, {self.col})."
        return s

    # kills the piece by removing it from the list. Also returns it in case you'd want to use it
    def kill(self):
        pieces.remove(self)
        return self

    # moves the piece from its initial position to (row, col)
    def move_piece(self, row, col):
        global turn_color
        target_piece = None
        original_row, original_col = self.row, self.col

            # if we are castling, move rook too
        if self.type == 'king' and self.col + 2 == col: 
            target_piece = piece_at(row, col + 1)
            target_piece.col = self.col + 1
        elif self.type == 'king' and self.col - 2 == col:
            target_piece = piece_at(row, col - 2)
            target_piece.col = self.col - 1
            # if we are en passant, target the correct square
        elif self.type == 'pawn' and self.col != col and not piece_at(row, col):
            direction = 1
            if self.color == 'white':
                direction = -1
            target_piece = piece_at(row - direction, col)
            if target_piece:
                target_piece.kill()
            self.row, self.col = row, col
            self.times_moved += 1
        else:   # just a regular move with no special rules
            target_piece = piece_at(row, col)
            if target_piece:
                target_piece.kill()
                
        self.row, self.col = row, col
        self.times_moved += 1

        # promotion checking
        is_promotion = False
        if self.type == 'pawn':
            if (self.color == 'white' and self.row == 0) or (self.color == 'black' and self.row == ROWS - 1):
                self.type = 'queen'
                is_promotion = True

        # change turn
        if turn_color == 'white':
            turn_color = 'black'
        else:
            turn_color = 'white'
        print(f"{turn_color}'s turn.")

        # record move in move_history
        move_history.append(Move(self, original_row, original_col, target_piece, is_promotion))

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

            # attack moves
            if self.is_legal_move(self.row + direction, self.col -1):
                move_list.append((self.row + direction, self.col -1))
            if self.is_legal_move(self.row + direction, self.col + 1):
                move_list.append((self.row + direction, self.col + 1))

            # basic moves (only if no pieces are in the way)
            if not piece_at(self.row + direction, self.col):
                move_list.append((self.row + direction, self.col))
                if self.times_moved == 0 and not piece_at(self.row + 2*direction, self.col):
                    move_list.append((self.row + 2*direction, self.col))

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
            # add castling as a base move if there are no pieces in the way and neither piece has moved
            if short_rook:
                if self.times_moved + short_rook.times_moved != 0 or piece_at(self.row, self.col + 1):
                    moves.remove((0,2))
            if long_rook:
                if self.times_moved + long_rook.times_moved != 0 or piece_at(self.row, self.col - 1) or piece_at(self.row, self.col - 2):
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
#                print(f"The {self.color} {self.type} is delivering check!")
                return True
        return False

# returns true if the piece's king is threatened
    def king_is_threatened(self):
        for piece in pieces:
            if piece.color != self.color and piece.threatens_enemy_king():
                return True
        return False

# returns true if the move leaves the king vulnerable
    def move_leaves_king_vulnerable(self, move):
        original_row, original_col = self.row, self.col
        target_piece = piece_at(move[0], move[1])
        if target_piece:
            pieces.remove(target_piece)
        self.row, self.col = move

        # test all enemy pieces to see if they threaten our king
        in_check = False
        if self.king_is_threatened():
            in_check = True
                
        # undo
        if target_piece:
            pieces.append(target_piece)
        self.row, self.col = original_row, original_col

        return in_check

# returns 0 if not. Returns the direction (-1 or 1) if yes
    def is_en_passant_possible(self):
        if len(move_history) > 0: 
            move = move_history[len(move_history) - 1]

            if move.moved_piece.type == 'pawn':
                if abs(move.original_row - move.moved_piece.row) == 2 and move.moved_piece.row == self.row:
                    return move.moved_piece.col - self.col
        return 0

# gets base moves, then filters out illegal ones caused by check
    def get_valid_moves(self):
        move_list = self.get_base_moves()
        print(f"{self} has base moves: {move_list}")
        valid_moves = []

        # do check testing
        for move in move_list:
            if not self.move_leaves_king_vulnerable(move):
#                print(f"{move} does not result in check for {self}")
                valid_moves.append(move)
            else:
                pass
#                print(f"{move} is illegal, because the king would be under attack")

        # special castling testing. If you are in check or in check in between the castling move, deny the move
        if self.type == 'king':
            if (self.row, self.col + 2) in valid_moves and ((self.row, self.col + 1) not in valid_moves or self.king_is_threatened()):
                valid_moves.remove((self.row, self.col + 2))
            if (self.row, self.col - 2) in valid_moves and ((self.row, self.col - 1) not in valid_moves or self.king_is_threatened()):
                valid_moves.remove((self.row, self.col - 2))

        # special pawn attack testing
        if self.type == 'pawn':
            direction = 1
            if self.color == 'white':
                direction = -1
            if not enemy_piece_at(self.row + direction, self.col + 1) and (self.row + direction, self.col + 1) in valid_moves:
                valid_moves.remove((self.row + direction, self.col + 1))
            if not enemy_piece_at(self.row + direction, self.col - 1) and (self.row + direction, self.col - 1) in valid_moves:
                valid_moves.remove((self.row + direction, self.col - 1))
            
            if self.is_en_passant_possible() != 0:
                print(f"Can en passant {self.is_en_passant_possible()}")
                valid_moves.append((self.row + direction, self.col + self.is_en_passant_possible()))
            
        return valid_moves
    
    def print_valid_moves(self):
        move_list = self.get_valid_moves()
        print(f"{self} has moves: ", end="")
        for move in move_list:
            print(f"({move[0]}, {move[1]})", end=" ")
        print("")

# initializes the list of chess pieces. Can be easily updated to have a dynamic "types" for different types of armies and pieces
def initialize_army(color, types):
    rows = (0, 1)
    if color == 'white':
        rows = (ROWS - 1, ROWS - 2)
    for i in range(0,8):
        pieces.append(Piece(rows[0], i, types[i], color))
    for i in range(0,8):
        pieces.append(Piece(rows[1], i, 'pawn', color))

def initialize_game(white_types, black_types):
    global pieces, move_history, turn_color
    pieces = []
    move_history = []
    turn_color = 'white'
    initialize_army('white', white_types)
    initialize_army('black', black_types)

# search every piece. If any of them can move, it is not checkmate
def is_game_over():
    valid_moves = []
    # check if the turn player can make any moves
    for piece in pieces:
        if piece.color == turn_color:
            valid_moves = piece.get_valid_moves()
            if valid_moves:
                return False
            
    global winner

    # decide if it is checkmate or stalemate
    is_checkmate = False
    for piece in pieces:
        if piece.color != turn_color and piece.threatens_enemy_king():
            is_checkmate = True

    if is_checkmate:
        if turn_color == 'black':
            winner = 'white'
        else:
            winner = 'black'
    else:
        winner = 'stalemate'
    return True

# Either (try to) select a piece, or (try to) move the selected piece
def board_clicked(row, col,):
    if not pieces:
        return None # do nothing if the game hasn't started
    
    global selected
    previously_selected = selected
    target_piece = piece_at(row, col)
    if target_piece and target_piece.color == turn_color:
        if target_piece == previously_selected:
            selected = None
        else:
            selected = target_piece
        return None
    elif previously_selected:
        move_list = previously_selected.get_valid_moves()
        print(f"Attempting to move {previously_selected} to ({row} , {col})")
        if (row, col) in move_list:
            print("\nMove is success!")
            previously_selected.move_piece(row, col)
            if is_game_over():
                if winner == 'stalemate':
                    print("The game is a draw.")
                else:
                    print(f"Checkmate! {winner} has won!")
        else:
            print("\nInvalid Move!")
    selected = None

def u_pressed():
    global turn_color, selected
    selected = None
    if not undo_last_move(move_history, pieces):
        turn_color = 'white'
    else:
        if turn_color == 'white':
            turn_color = 'black'
        else:
            turn_color = 'white'