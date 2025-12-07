let board = [" "," "," "," "," "," "," "," "," "];
let gameOver = false;

const boardDiv = document.getElementById("board");
const statusText = document.getElementById("status");

function drawBoard() {
    boardDiv.innerHTML = "";
    board.forEach((cell, i) => {
        let box = document.createElement("div");
        box.classList.add("cell");
        box.innerText = cell;
        box.onclick = () => playerMove(i);
        boardDiv.appendChild(box);
    });
}

function playerMove(i) {
    if (board[i] !== " " || gameOver) return;
    board[i] = "O";
    drawBoard();
    checkGameState();

    fetch("/move", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ board })
    })
    .then(response => response.json())
    .then(data => {
        board = data.board;
        drawBoard();
        if (data.winner) {
            gameOver = true;
            statusText.innerText = data.winner === "AI" ? "💀 AI Wins!" : "🤝 Draw!";
        }
    });
}

function checkGameState() {
    statusText.innerText = "🤖 AI is thinking...";
}

function restart() {
    board = [" "," "," "," "," "," "," "," "," "];
    gameOver = false;
    statusText.innerText = "Your turn (O)";
    drawBoard();
}

drawBoard();
