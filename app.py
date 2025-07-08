from flask import Flask, request, jsonify, render_template, send_from_directory
from game_logic.game import Game
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

games = {}  # In-memory game storage: {game_id: Game instance}

# --- API Endpoints ---

@app.route('/api/create_game', methods=['POST'])
def create_game():
    data = request.get_json()
    player_names = data.get('player_names')
    forbidden_names = [                                 # List of forbidden names,(for now only the ones offensive to indians) purely an Easter Egg ;)
        'ich hasse inder',                              # TODO: Add more forbidden names    
        'ich mag keine inder',
        'kein inder',
        'absoluter inder',
    ]
    # Normalize and check for forbidden names
    for name in player_names or []:
        normalized = name.strip().lower().replace('  ', ' ')
        if normalized in forbidden_names:
            return jsonify({'redirect': '/inderhasser'}), 403
    if not player_names or not (2 <= len(player_names) <= 8):
        return jsonify({'error': 'player_names must be a list of 2-8 names'}), 400
    game = Game(player_names)
    game_id = str(uuid.uuid4())
    games[game_id] = game
    return jsonify({'game_id': game_id})

@app.route('/api/game_state/<game_id>', methods=['GET'])
def game_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    board_state = []
    for space in game.board.spaces:
        space_info = {
            'name': getattr(space, 'name', ''),
            'type': getattr(space, 'type', ''),
            'owner': getattr(space, 'owner', None).name if getattr(space, 'owner', None) else None,
        }
        if hasattr(space, 'cost'):
            space_info['cost'] = getattr(space, 'cost', None)
        if hasattr(space, 'rent'):
            space_info['rent'] = getattr(space, 'rent', None)
        if hasattr(space, 'color_group'):
            space_info['color_group'] = getattr(space, 'color_group', None)
        if hasattr(space, 'houses'):
            space_info['houses'] = getattr(space, 'houses', 0)
        board_state.append(space_info)
    players_state = []
    for p in game.players:
        players_state.append({
            'name': p.name,
            'money': p.money,
            'position': p.position,
            'properties': [prop.name for prop in p.properties],
            'in_jail': p.in_jail
        })
    return jsonify({
        'players': players_state,
        'current_player': game.current_player.name,
        'board': board_state,
        'current_turn': game.current_player_idx,
        'is_active': game.is_active
    })

@app.route('/api/roll_dice', methods=['POST'])
def roll_dice():
    data = request.get_json()
    game_id = data.get('game_id')
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    result = game.play_turn()
    return jsonify(result)

@app.route('/api/buy_property', methods=['POST'])
def buy_property():
    data = request.get_json()
    game_id = data.get('game_id')
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    player = game.current_player
    space = game.board.get_space(player.position)
    if hasattr(space, 'cost') and getattr(space, 'owner', None) is None:
        success = player.buy_property(space)
        return jsonify({
            'success': success,
            'player_money': player.money,
            'property': space.name
        })
    return jsonify({'success': False, 'reason': 'Cannot buy this property'}), 400

@app.route('/api/end_turn', methods=['POST'])
def end_turn():
    data = request.get_json()
    game_id = data.get('game_id')
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
    return jsonify({'next_player': game.current_player.name})

@app.route('/api/join_game', methods=['POST'])
def join_game():
    data = request.get_json()
    game_id = data.get('game_id')
    player_name = data.get('player_name')
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if any(p.name == player_name for p in game.players):
        return jsonify({'error': 'Player already in game'}), 400
    game.players.append(player_name)
    return jsonify({'success': True})

# --- Special/Legacy Routes ---

@app.route('/inderhasser')
def inderhasser():
    return render_template('inderhasser.html')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/game.html')
def game_html():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
