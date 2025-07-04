from flask import Flask, render_template, request, redirect, url_for, session
from game_logic.game import Game
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Using os.urandom(24) generates a new secret key each time the application starts,
                                #  which will invalidate all existing sessions. This means users will lose their game state on server restart.
                                # For production, use an environment variable or configuration file: os.environ.get('SECRET_KEY')

# In-memory store for games (for demo; use DB for production)
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        player_names = [name.strip() for name in request.form.getlist('player_names') if name.strip()]
        if player_names and player_names[0] == 'Ich hasse Inder':
            player_names[0] = 'Schlechter Mensch'
            return redirect(url_for('inderhasser'))
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
    phase = session.get('phase', 'start')
    can_buy = False
    if phase == 'after_roll':
        space = game.board.get_space(game.current_player.position)
        can_buy = hasattr(space, 'cost') and getattr(space, 'owner', None) is None
    return render_template('game.html', game=game, phase=phase, can_buy=can_buy)

@app.route('/action', methods=['POST'])
def action():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('setup'))
    game = games[game_id]
    action = request.form.get('action')
    phase = session.get('phase', 'start')
    if phase == 'start' and action == 'roll':
        if game.current_player.in_jail:
            game.message = f'{game.current_player.name} ist im Gefängnis und muss eine Runde aussetzen.'
            game.current_player.in_jail = False
            session['phase'] = 'jail_message'
        else:
            game.handle_action('roll')
            space = game.board.get_space(game.current_player.position)
            if hasattr(space, 'cost') and getattr(space, 'owner', None) is None:
                session['phase'] = 'after_roll'
            elif getattr(space, 'type', None) in ['property', 'utility', 'station'] and getattr(space, 'owner', None) and space.owner != game.current_player:
                session['phase'] = 'after_roll'
            else:
                session['phase'] = 'after_roll'
    elif phase == 'jail_message' and action == 'skip':
        game.next_turn()
        session['phase'] = 'start'
    elif phase == 'after_roll':
        if action == 'buy':
            game.handle_action('buy')
        game.handle_action('end_turn')
        session['phase'] = 'start'
    return redirect(url_for('game_view'))
    
@app.route('/inderhasser')
def inderhasser():
    return render_template('inderhasser.html')

if __name__ == '__main__':
    app.run(debug=True)             # Run the app in debug mode // In production disable debug mode:
                                    # debug_mode = os.environ.get('FLASK_ENV') == 'development'
                                    # app.run(debug=debug_mode)
