import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic.game import Game
from ui.terminal_ui import handle_station, show_board, wait
from colorama import Fore
from ui.terminal_ui import clear_term

def test_station_scenarios():
    clear_term()
    """Test different scenarios for landing on stations"""
    print(Fore.BLUE + "\n=== Station Test-Szenarien ===")
    
    # Create test game with 2 players
    test_game = Game(["TestPlayer1", "TestPlayer2"])
    test_player = test_game.players[0]
    other_player = test_game.players[1]
    
    # Find a station
    station = next(space for space in test_game.board.spaces if space.type == "station")
    test_player.position = test_game.board.spaces.index(station)
    
    # Test Scenario 1: Unowned Station
    print(Fore.YELLOW + "\nTest 1: Landen auf unbesetztem Bahnhof")
    station.owner = None
    handle_station(test_player, station, test_game, Fore.LIGHTBLUE_EX)
    wait()
    
    # Test Scenario 2: Owned by Player
    print(Fore.YELLOW + "\nTest 2: Landen auf eigenem Bahnhof")
    station.owner = test_player
    test_player.properties.append(station)
    handle_station(test_player, station, test_game, Fore.LIGHTBLUE_EX)
    wait()
    
    # Test Scenario 3: Owned by Other Player
    print(Fore.YELLOW + "\nTest 3: Landen auf fremdem Bahnhof")
    station.owner = other_player
    other_player.properties.append(station)
    handle_station(test_player, station, test_game, Fore.LIGHTBLUE_EX)
    wait()

if __name__ == "__main__":
    test_station_scenarios() 