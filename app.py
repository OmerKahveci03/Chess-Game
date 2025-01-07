from flask import Flask, render_template, request, jsonify
import chess
# from common import *

app = Flask(__name__)

highlighted_square = None

# Renders the main page
@app.route("/")
def index():
    return render_template("index.html")

# Renders the game page
@app.route('/game')
def game():
    return render_template('game.html')

# return current board state in JSON
@app.route("/board", methods=["GET"])
def get_board():
    global highlighted_square
    pieces = [
        {
            "row": piece.row,
            "col": piece.col,
            "color": piece.color,
            "type": piece.type
        }
        for piece in chess.pieces
    ]
    move_list = []
    if chess.selected:
        move_list = chess.selected.get_valid_moves()
    data = {
        "pieces": pieces,
        "highlighted_square": highlighted_square,
        "valid_moves": move_list,
        "winner": chess.winner,
        "action": chess.action
    }
    return jsonify(data)

# Handles click on the board. Recieves (row, col) from frontend
@app.route("/click", methods=["POST"])
def handle_click():
    global highlighted_square

    data = request.get_json()
    row = data.get("row")
    col = data.get("col")
    if 0 <= row < chess.ROWS and 0 <= col < chess.COLS:
        if not chess.winner:
            chess.board_clicked(row, col)
        if chess.selected is not None:
            highlighted_square = (chess.selected.row, chess.selected.col)
        else:
            highlighted_square = None

    return get_board()

# Handles the undo button
@app.route("/undo", methods=["POST"])
def handle_undo():
    global highlighted_square
    chess.u_pressed()
    highlighted_square = None
    return get_board()

# Handles the start button
@app.route("/start", methods=["POST"])
def handle_start():
    types = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    chess.initialize_game(types, types)
    return get_board()

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)