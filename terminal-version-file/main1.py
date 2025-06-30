import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_logic.game import Game
from ui.terminal_ui import main 

if __name__ == "__main__":
    main()