from game_logic.player import Player
from game_logic.game_board import GameBoard
from game_logic.property import Property
import random

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        try:
            self.board = GameBoard()
        except FileNotFoundError:
            raise FileNotFoundError("Board data file not found: assets/board_data.json")  
        self.current_player_idx = 0
        self.is_active = True

    def play_round(self):
        current_player = self.players[self.current_player_idx]
        current_player.move(random.randint(2, 12))
        current_space = self.board.get_space(current_player.position)
        
        # Handle space logic here
        if isinstance(current_space, Property):
            action = current_space.land_on(current_player)
            # Implement buy/pay rent logic
        
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)