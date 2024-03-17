from flask import Flask, render_template, request, jsonify
import chess
import chess.engine
import chess.pgn
import os

app = Flask(__name__)

# Constants
IMAGE_FOLDER_PATH = "static/images"

def get_engines():
    engines = {
        'Stockfish': chess.engine.SimpleEngine.popen_uci("path/to/stockfish"),
    }
    return engines

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/play', methods=['POST'])
def play():
    data = request.get_json()
    fen = data['fen']
    move = data['move']

    board = chess.Board(fen)
    try:
        board.push_uci(move)
        engine = get_engines()['Stockfish']
        result = engine.play(board, chess.engine.Limit(time=0.1))
        engine_move = result.move.uci()
        board.push(result.move)
        return jsonify({'status': 'success', 'fen': board.fen(), 'move': engine_move})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid move'})

if __name__ == "__main__":
    app.run()