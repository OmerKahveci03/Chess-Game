# moves.py
# used to store game history in the form of previous moves

class Move():
    # secondary_piece stores either the enemy piece that was captured, or pieces involved in special moves, like castling and promotion
    def __init__(self, moved_piece, original_row, original_col, action, secondary_piece=None):
        self.moved_piece = moved_piece
        self.original_row = original_row
        self.original_col = original_col
        self.secondary_piece = secondary_piece
        self.action = action        # actions are one of the following: ['move', 'capture', 'check', 'promotion', 'card']

# pretty self explanitory what this does. Returns true if successful, returns false if not possible
def undo_last_move(move_history, pieces):
    move = None
    if len(move_history) > 0:
        move = move_history.pop()

        # In case of a castle, undo the position of the rook
        castled = False
        if move.moved_piece.type == 'king':
            if move.moved_piece.col == move.original_col + 2:
                move.secondary_piece.col += 2
                castled = True
            elif move.moved_piece.col == move.original_col - 2:
                move.secondary_piece.col -= 3
                castled = True
        
        move.moved_piece.row, move.moved_piece.col = move.original_row, move.original_col
        move.moved_piece.times_moved -= 1
        if move.action == 'promotion':
            move.moved_piece.type = 'pawn'
        
        if move.secondary_piece and not castled:
            pieces.append(move.secondary_piece)
    else:
        return False
    return True