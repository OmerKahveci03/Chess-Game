const chessboardEl = document.getElementById('chessboard');
const ROWS = 8;
const COLS = 8;
const captureSound = new Audio('/static/assets/capture.mp3');
const moveSound = new Audio('static/assets/move.mp3');
const promotionSound = new Audio('/static/assets/promotion.mp3');
const checkSound = new Audio('static/assets/check.mp3');
captureSound.preload = 'auto';
moveSound.preload = 'auto';
promotionSound.preload = 'auto';
checkSound.preload = 'auto';
let selectedPiece = null;

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

function clearBoard(){
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const squareEl = document.getElementById(`square-${row}-${col}`);
            squareEl.classList.remove('highlighted');
            squareEl.classList.remove('valid-move');
            squareEl.innerHTML = '';
        }
    }
}

function placePieces(data){
    data.pieces.forEach(piece => {
        const squareEl = document.getElementById(`square-${piece.row}-${piece.col}`);
        if (squareEl) {
            const img = document.createElement('img');
            img.classList.add('piece-img');
            img.src = `/static/assets/${piece.color}_${piece.type}.png`;
            squareEl.appendChild(img);
        }
    });
}

function hightlightSquares(data){
    if (data.highlighted_square) {
        const [hRow, hCol] = data.highlighted_square;
        const highlightEl = document.getElementById(`square-${hRow}-${hCol}`);
        if (highlightEl) {
            const pieceEl = highlightEl.querySelector('img');
            highlightEl.classList.add('highlighted');
            pieceEl.classList.add('selected-piece');
//            pieceEl.classList.remove('piece-img');
            selectedPiece = pieceEl
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
}

function playMoveSound(data){
    if (data.action == 'move') {
        moveSound.play();
    }else if (data.action == 'capture') {
        captureSound.play();
    }else if (data.action == 'promotion') {
        promotionSound.play();
    }else if (data.action == 'check') {
        checkSound.play();
    }
}

// Clear old board, place pieces, highlight squares
function renderBoardData(data) {
    clearBoard();
    placePieces(data);
    hightlightSquares(data);    
    playMoveSound(data);

    // If there's a winner, handle that
    if (data.winner) {
        document.getElementById("top_section").textContent = `Winner: ${data.winner}`;
        document.getElementById("chessboard").classList.add("game-over");
    }else{
        document.getElementById("top_section").textContent = `Top Section`;
        document.getElementById("chessboard").classList.remove("game-over");
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

// Initial load
startGame();