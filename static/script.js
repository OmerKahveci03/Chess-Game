const chessboardEl = document.getElementById('chessboard');
const ROWS = 8;
const COLS = 8;
const captureSound = new Audio('/static/assets/capture.mp3');
const moveSound = new Audio('static/assets/move.mp3');
captureSound.preload = 'auto';
moveSound.preload = 'auto';

for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
        const square = document.createElement('div');
        square.classList.add('square');
        if ((row + col) % 2 === 0) {
            square.classList.add('white-square');
        } else {
            square.classList.add('black-square');
        }
        square.addEventListener('click', () => {
            handleSquareClick(row, col);
        });

        square.id = `square-${row}-${col}`;
        chessboardEl.appendChild(square);
    }
}

// Clears existing pieces and highlight classes, places pieces, gives highlight class to correct squares. Occurs once
function updateBoard() {
    fetch('/board').then(response => response.json()).then(data => {
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
            if (data.winner) {
                alert(`Winner: ${data.winner}`);
            }
        })
        .catch(err => console.error(err));
}
// Clear old board, place pieces, highlight squares
function renderBoardData(data) {
    // Clear old board
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const squareEl = document.getElementById(`square-${row}-${col}`);
            squareEl.classList.remove('highlighted');
            squareEl.classList.remove('valid-move');
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

    // Highlight valid moves
    if (data.valid_moves) {
        data.valid_moves.forEach(move => {
            const [moveRow, moveCol] = move;
            const moveEl = document.getElementById(`square-${moveRow}-${moveCol}`);
            if (moveEl) {
                moveEl.classList.add('valid-move');
            }
        });
    }

    // Play the correct sound after the move
    if (data.action == 'move') {
        moveSound.play();
    }else if (data.action == 'capture') {
        captureSound.play();
    }

    // If there's a winner, handle that
    if (data.winner) {
        alert(`Winner: ${data.winner}`);
    }
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