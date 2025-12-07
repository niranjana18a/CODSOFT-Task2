from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# ----- Minimax Logic -----
def check_winner(board, player):
    win_cond = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(board[a] == board[b] == board[c] == player for a,b,c in win_cond)

def empty_cells(board):
    return [i for i in range(9) if board[i] == " "]

def minimax(board, is_max):
    if check_winner(board, "X"): return 1
    if check_winner(board, "O"): return -1
    if not empty_cells(board): return 0

    if is_max:
        best = -math.inf
        for index in empty_cells(board):
            board[index] = "X"
            score = minimax(board, False)
            board[index] = " "
            best = max(score, best)
        return best

    else:
        best = math.inf
        for index in empty_cells(board):
            board[index] = "O"
            score = minimax(board, True)
            board[index] = " "
            best = min(score, best)
        return best

def best_move(board):
    best_score = -math.inf
    move = None

    for index in empty_cells(board):
        board[index] = "X"
        score = minimax(board, False)
        board[index] = " "
        if score > best_score:
            best_score = score
            move = index
    return move

# ----- Flask Routes -----
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]

    ai_index = best_move(board)
    board[ai_index] = "X"

    winner = None
    if check_winner(board, "X"):
        winner = "AI"
    elif not empty_cells(board):
        winner = "Draw"

    return jsonify({"board": board, "winner": winner})

if __name__ == "__main__":
    app.run(debug=True)
