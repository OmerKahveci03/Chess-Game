# The point of this file is to prevent circular imports
ROWS, COLS = 8, 8
turn_color = 'white'
selected = None     # the piece to be highlighted
pieces = []
winner = None
move_history = [] 
action = None       # only has a value right after a click results in a move happening (moving a piece or playing a card)   [None, 'move', 'capture', 'check', 'promotion', 'card']