from flask import Flask, render_template, request, jsonify
import chess  # Your existing chess logic (unchanged)
from common import ROWS, COLS

app = Flask(__name__)

# Keep track of highlighted square in memory (similar to your game.py)
highlighted_square = None

@app.route("/")
def index():
    """
    Render the main page, which contains the chessboard.
    The board/pieces will be fetched via JavaScript calls.
    """
    return render_template("index.html")

@app.route("/board", methods=["GET"])
def get_board():
    """
    Return the current board state, including piece positions and
    optional highlighted square, in JSON.
    """
    global highlighted_square

    # Build a list (or another structure) describing each piece:
    # e.g. [{"row": 1, "col": 0, "color": "white", "type": "pawn"}, ...]
    pieces = [
        {
            "row": piece.row,
            "col": piece.col,
            "color": piece.color,
            "type": piece.type
        }
        for piece in chess.pieces
    ]

    data = {
        "pieces": pieces,
        "highlighted_square": highlighted_square,
        "winner": chess.winner
    }
    return jsonify(data)

@app.route("/click", methods=["POST"])
def handle_click():
    """
    Handle a click on the board. The frontend (JavaScript) will
    send the row and col in JSON, and we'll update the chess state.
    """
    global highlighted_square

    data = request.get_json()
    row = data.get("row")
    col = data.get("col")

    # Safety check: only handle clicks if in range
    if 0 <= row < ROWS and 0 <= col < COLS:
        chess.board_clicked(row, col)
        
        # If there's a selected piece in chess.py, highlight it:
        if chess.selected is not None:
            highlighted_square = (chess.selected.row, chess.selected.col)
        else:
            highlighted_square = None

    # Return updated board data
    return get_board()

@app.route("/undo", methods=["POST"])
def handle_undo():
    """
    Handle the "undo" event (similar to pressing 'u' in Pygame).
    """
    global highlighted_square
    chess.u_pressed()
    highlighted_square = None
    return get_board()

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
