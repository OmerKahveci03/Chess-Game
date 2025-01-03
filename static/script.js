const chessboardEl = document.getElementById('chessboard');
const ROWS = 8;
const COLS = 8;

// Dynamically create squares
for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
        const square = document.createElement('div');
        square.classList.add('square');
        // White or black square color
        if ((row + col) % 2 === 0) {
            square.classList.add('white-square');
        } else {
            square.classList.add('black-square');
        }

        // When user clicks a square, send row/col to server
        square.addEventListener('click', () => {
            handleSquareClick(row, col);
        });

        // Unique ID for each square (so we can update in JS easily)
        square.id = `square-${row}-${col}`;
        chessboardEl.appendChild(square);
    }
}

// Fetch the board state from server and render
function updateBoard() {
    fetch('/board')
        .then(response => response.json())
        .then(data => {
            // Clear existing pieces/highlights
            for (let row = 0; row < ROWS; row++) {
                for (let col = 0; col < COLS; col++) {
                    const squareEl = document.getElementById(`square-${row}-${col}`);
                    squareEl.classList.remove('highlighted');
                    // Remove old piece images if any
                    squareEl.innerHTML = '';
                }
            }
            // Place pieces
            data.pieces.forEach(piece => {
                const squareEl = document.getElementById(`square-${piece.row}-${piece.col}`);
                if (squareEl) {
                    const img = document.createElement('img');
                    img.classList.add('piece-img');
                    // e.g. /static/assets/white_pawn.png or /static/assets/black_knight.png
                    img.src = `/static/assets/${piece.color}_${piece.type}.png`;
                    squareEl.appendChild(img);
                }
            });
            // Highlight the selected square if any
            if (data.highlighted_square) {
                const [hRow, hCol] = data.highlighted_square;
                const highlightEl = document.getElementById(`square-${hRow}-${hCol}`);
                if (highlightEl) {
                    highlightEl.classList.add('highlighted');
                }
            }
            // If there's a winner, you can alert or display a message
            if (data.winner) {
                alert(`Winner: ${data.winner}`);
            }
        })
        .catch(err => console.error(err));
}

function handleSquareClick(row, col) {
    fetch('/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col })
    })
    .then(response => response.json())
    .then(data => {
        renderBoardData(data);
    });
}

// After an action, re-render the board
function renderBoardData(data) {
    // Clear old board
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const squareEl = document.getElementById(`square-${row}-${col}`);
            squareEl.classList.remove('highlighted');
            squareEl.innerHTML = '';
        }
    }
    // Place pieces
    data.pieces.forEach(piece => {
        const squareEl = document.getElementById(`square-${piece.row}-${piece.col}`);
        if (squareEl) {
            const img = document.createElement('img');
            img.classList.add('piece-img');
            img.src = `/static/assets/${piece.color}_${piece.type}.png`;
            squareEl.appendChild(img);
        }
    });
    // Highlight selected
    if (data.highlighted_square) {
        const [hRow, hCol] = data.highlighted_square;
        const highlightEl = document.getElementById(`square-${hRow}-${hCol}`);
        if (highlightEl) {
            highlightEl.classList.add('highlighted');
        }
    }
    // If there's a winner, handle that
    if (data.winner) {
        alert(`Winner: ${data.winner}`);
    }
}

function undoMove() {
    fetch('/undo', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        renderBoardData(data);
    });
}

function startGame() {
    fetch('/start', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        renderBoardData(data);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    startGame(); // Automatically call startGame when the page loads
});

// Initial load
updateBoard();
