from game_logic.player import Player
from game_logic.game_board import GameBoard
from game_logic.property import Property
import random

class Game:
    def __init__(self, player_names, board_data_path="assets/board_data.json"):
        self.players = [Player(name) for name in player_names]
        self.board = GameBoard(board_data_path)
        self.current_player_idx = 0
        self.is_active = True

    @property
    def current_player(self):
        return self.players[self.current_player_idx]

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def play_turn(self):
        player = self.current_player
        dice1, dice2 = self.roll_dice()
        steps = dice1 + dice2
        player.move(steps, board_size=len(self.board.spaces))
        current_space = self.board.get_space(player.position)
        action = None
        if isinstance(current_space, Property):
            action = current_space.land_on(player)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return {
            "player": player.name,
            "dice": (dice1, dice2),
            "steps": steps,
            "position": player.position,
            "space": current_space.name,
            "action": action
        } 