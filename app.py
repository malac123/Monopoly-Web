from flask import Flask, render_template, request, redirect, url_for, session
from game_logic.game import Game
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory store for games (for demo; use DB for production)
games = {}

@app.route('/', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        player_names = [name.strip() for name in request.form.getlist('player_names') if name.strip()]
        if 2 <= len(player_names) <= 4:
            game = Game(player_names)
            game_id = str(len(games) + 1)
            games[game_id] = game
            session['game_id'] = game_id
            return redirect(url_for('game_view'))
        else:
            error = 'Bitte 2-4 Spielernamen eingeben.'
            return render_template('setup.html', error=error)
    return render_template('setup.html')

@app.route('/game')
def game_view():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('setup'))
    game = games[game_id]
    return render_template('game.html', game=game)

@app.route('/action', methods=['POST'])
def action():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('setup'))
    game = games[game_id]
    action = request.form.get('action')
    game.handle_action(action)
    return redirect(url_for('game_view'))

if __name__ == '__main__':
    app.run(debug=True)
