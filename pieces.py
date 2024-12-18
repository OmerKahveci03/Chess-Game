# pieces.py
# This module handles the piece class and stores information on how the different pieces move. 

class Piece():
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color

    # returns a list of coordinates (row, col) that this piece is allowed to move to
    def valid_moves(self, white_pieces, black_pieces):
        move_list = []

        if self.type == 'pawn':
            if self.color == 'black':
                for i in range(-1, 2):
                    move_list.append((self.row + 1, self.col + i))
                if self.row == 1:
                    move_list.append((self.row + 2, self.col))
            else:
                for i in range(-1, 2):
                    move_list.append((self.row - 1, self.col + i))
                if self.row == 6:
                        move_list.append((self.row - 2, self.col))

        elif self.type == 'knight':
            pass

        else:
            # this is just to make sure it is used correctly
            move_list = [(3,3), (3,4), (4,3), (4,4)]
        return move_list
