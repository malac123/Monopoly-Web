from .player import Player
from .game_board import GameBoard
from .property import Property
import random

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.board = GameBoard()
        self.current_player_idx = 0
        self.is_active = True
        self.last_roll = None
        self.message = ''

    @property
    def current_player(self):
        return self.players[self.current_player_idx]

    def roll_dice(self):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        self.last_roll = d1 + d2
        return self.last_roll

    def move_current_player(self):
        steps = self.last_roll or self.roll_dice()
        player = self.current_player
        player.move(steps)
        return self.board.get_space(player.position)

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.last_roll = None
        self.message = ''

    def buy_property(self):
        player = self.current_player
        space = self.board.get_space(player.position)
        if hasattr(space, 'owner') and space.owner is None and hasattr(space, 'cost'):
            if player.money >= space.cost:
                player.buy_property(space)
                self.message = f'{player.name} hat {space.name} gekauft!'
            else:
                self.message = 'Nicht genug Geld!'
        else:
            self.message = 'Kann nicht gekauft werden.'

    def pay_rent(self):
        player = self.current_player
        space = self.board.get_space(player.position)
        # Only pay rent if this is a property and has an owner
        if hasattr(space, 'rent') and hasattr(space, 'owner') and space.owner and space.owner != player:
            player.pay_rent(space)
            self.message = f'{player.name} hat Miete gezahlt.'
        else:
            self.message = ''

    def handle_action(self, action):
        player = self.current_player
        space = self.board.get_space(player.position)
        if action == 'roll':
            self.roll_dice()
            space = self.move_current_player()
            # Handle special fields
            if getattr(space, 'type', None) == 'property' and getattr(space, 'owner', None) and space.owner != player:
                self.pay_rent()
            elif getattr(space, 'type', None) == 'tax':
                player.money -= getattr(space, 'amount', 0)
                self.message = f'{player.name} zahlt {getattr(space, "amount", 0)}€ Steuern.'
            elif getattr(space, 'type', None) == 'special':
                player.money += getattr(space, 'amount', 0)
                self.message = f'{player.name} erhält {getattr(space, "amount", 0)}€.'
            elif getattr(space, 'type', None) == 'jail':
                player.in_jail = True
                self.message = f'{player.name} ist im Gefängnis und muss eine Runde aussetzen.'
            # Utility and station logic can be added here
        elif action == 'buy':
            self.buy_property()
        elif action == 'end_turn' or action == 'skip':
            self.next_turn() 