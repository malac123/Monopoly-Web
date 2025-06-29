from colorama import Fore, init
from random import randint
import os
import sys
import time
from game_logic.game import Game
from game_logic.property import Property
from game_logic.property import display_property_details
from game_logic.player import Player

# Initialisiere Colorama (für Windows-Terminal nötig)
init(autoreset=True)

colors = [Fore.LIGHTBLUE_EX, Fore.RED, Fore.GREEN, Fore.YELLOW]
global_players = []
developer_mode = False

def check_developer_mode():
    global developer_mode
    print(Fore.CYAN + "\nDrücke Enter zum Starten oder 'dev' für Entwicklermodus...")
    choice = input().strip().lower()
    if choice == "dev":
        developer_mode = True
        print(Fore.GREEN + "Entwicklermodus aktiviert! Du kannst jetzt Tests durchführen." + Fore.RESET)
        time.sleep(1)

def main():
    while True:
        clear_term()
        banner()
        check_developer_mode()  # Check for developer mode at start
        start_menu()

def start_menu():
    global developer_mode
    while True:
        print(Fore.BLUE + "\nBitte wählen:")
        print(Fore.YELLOW + "1. Spiel starten")
        print(Fore.YELLOW + "2. Spielregeln")
        if developer_mode:
            print(Fore.YELLOW + "3. Station Tests")
            print(Fore.YELLOW + "4. Beenden" + Fore.RESET)
        else:
            print(Fore.YELLOW + "3. Beenden" + Fore.RESET)
        
        choice = input("\nEingabe (1-4): ").strip()

        if choice == "1":
            setup_game()
        elif choice == "2":
            show_rules()
        elif choice == "3":
            if developer_mode:
                from tests.test_station import test_station_scenarios
                test_station_scenarios()
            else:
                sys.exit(0)
        elif choice == "4" and developer_mode:
            sys.exit(0)
        else:
            print(Fore.RED + "Ungültige Eingabe!")
            time.sleep(1)

def setup_game():
    global colors
    global global_players

    while True:
        try:
            num_players = int(input(Fore.LIGHTBLUE_EX + "Wie viele Spieler möchten mitspielen? "))
            if num_players > 4:
                print(Fore.RED + "Maximal 4 Spieler erlaubt! Wir setzen das Spiel mit 4 Spielern fort.")
                num_players = 4
                time.sleep(3)
            break
        except ValueError:
            print(Fore.RED + "Ungültige Eingabe! Bitte geben Sie eine Ganzzahl ein.")
    clear_term()

    player_names = []
    colors = [Fore.LIGHTBLUE_EX, Fore.RED, Fore.GREEN, Fore.YELLOW]
    for i in range(num_players):
        while True:
            name = input(colors[i] + f"Name des Spielers {i+1}: ").strip()
            if name and " " not in name:                                                    # Lässt den Spieler nicht Leerzeichen im Namen haben :)
                player_names.append(name)
                break
            else:
                print(Fore.RED + "Ungültiger Name! Bitte geben Sie einen Namen ein, der keine Leerzeichen enthält.")

    game = Game(player_names)
    global_players = game.players
    game_loop(game)

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')        # Leert das Terminal, um für sauberkeit und lesbarkeit zu sorgen

def banner():
    print(Fore.CYAN+ " ______                                _       ")   
    print(Fore.CYAN + "|  ___ \                              | |      ")
    print(Fore.CYAN + "| | _ | | ___  ____   ___  ____   ___ | |_   _ ")
    print(Fore.LIGHTBLUE_EX + "| || || |/ _ \|  _ \ / _ \|  _ \ / _ \| | | | |")
    print(Fore.LIGHTBLUE_EX + "| || || | |_| | | | | |_| | | | | |_| | | |_| |")
    print(Fore.BLUE + "|_||_||_|\___/|_| |_|\___/| ||_/ \___/|_|\__  |")
    print(Fore.BLUE + "                          |_|           (____/ ")          # ASCII-Banner (weil warum nicht)
    print(Fore.BLUE + "")

def show_rules():           # Spielregeln
    clear_term()
    print(Fore.YELLOW + "\nMONOPOLY REGELN:")
    print(Fore.CYAN + "- Würfle mit Enter")
    print("- Kaufe Grundstücke (oder auch nicht), wenn du auf ihnen landest")
    print("- Zahle Miete, wenn andere Spieler Eigentümer sind")
    print("- Pass auf, dass du nicht im Gefängnis landest!")
    print("- Ziel: Bankrottiere alle deine Gegner!")
    wait()

def show_board(players, board):
    """Displays the board status with player positions and ownership colors."""
    board_visual = [""] * len(board.spaces)
    owner_colors = {}  # Zum Speichern der Farben nach Eigentümer

    # Mark player positions
    for idx, player in enumerate(players):
        if player.position < len(board_visual):
            player_color = colors[idx % len(colors)]
            board_visual[player.position] += f"{player_color} {player.name[0]}"
            owner_colors[player.name] = player_color

    print(Fore.CYAN + "\nAktueller Spielstand:")

    for idx, space in enumerate(board.spaces):
        # Bestimme Farbe des Feldes
        space_color = Fore.WHITE  # Standardfarbe
        if hasattr(space, 'owner') and space.owner:
            owner_name = space.owner.name
            space_color = owner_colors.get(owner_name, Fore.WHITE)

        # Spieler auf Feld markieren
        player_marker = board_visual[idx]
        abbrev_name = space.name[:3].ljust(3)

        field_str = f"{Fore.WHITE}[{space_color}{abbrev_name}{Fore.RESET}{player_marker:^3}{Fore.WHITE}]"
        print(field_str, end="\n" if (idx + 1) % 10 == 0 else " ")
    print()

def game_loop(game):
    colors = [Fore.LIGHTBLUE_EX, Fore.RED, Fore.GREEN, Fore.YELLOW]


    while True:                                     # Moved while True from setup_game to game_loop because it made no sense to have a game_loop loop in setup_game 
        clear_term()
        banner()
        show_board(game.players, game.board)

        player = game.players[game.current_player_idx]
        player_color = colors[game.current_player_idx % len(colors)]

        if player.money <= 0:
            print(f"{Fore.RED}{player.name} ist bankrott und kann nicht weiterspielen.")
            game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
            wait()
            continue

        # Zeigt den aktuellen Kontostand des Spielers
        print(f"{player_color}{player.name}'s{Fore.RESET} aktueller Kontostand: €{player.money}")

        input(f"{player_color}{player.name}{Fore.RESET}, drücke Enter zum Würfeln...")               # sollte 2 optionen geben, 1. für bereits gekaufte gründstücke anzeigen und 2. zum würfeln
        clear_term()
        show_board(game.players, game.board)
        print(f"{player_color}{player.name}'s{Fore.RESET} aktueller Kontostand: €{player.money}")

        dice_roll = throw_dice(player, game)

        if dice_roll == -1:                                 # Skips if player was in jail
            game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
        else:
            player.move(dice_roll)
            current_space = game.board.get_space(player.position)

            print(Fore.CYAN + f"\nDu landest auf: {Fore.MAGENTA}{current_space.name}")

            if current_space.type == "property":
                if current_space.owner is None:
                    print(Fore.GREEN + "Dieses Grundstück ist zu verkaufen!")
                    display_property_details(current_space)
                    while True:
                        buy_choice = input(f"{player_color}{player.name}{Fore.RESET}, möchtest du {current_space.name} für {current_space.cost}€ kaufen? (y/n): ")
                        if buy_choice.lower() == "y":
                            if player.buy_property(current_space):
                                print(Fore.GREEN + f"{player_color}{player.name}{Fore.RESET} hat {current_space.name} gekauft!")
                                current_space.owner = player
                                wait()
                                break
                            else:
                                print(Fore.RED + "Nicht genug Geld, um dieses Grundstück zu kaufen.")
                                wait()
                                break
                        elif buy_choice.lower() == "n":
                            break
                        else:
                            print(Fore.RED + "Ungültige Eingabe! Bitte geben Sie 'y' oder 'n' ein.")
                else:
                    if current_space.owner is not None and current_space.owner is not player:
                        print(Fore.RED + f"Du musst {current_space.rent}€ Miete für {current_space.name} zahlen. (pro Haus auf dem Grundstück + [1])")
                        player.pay_rent(current_space)
                        print(f"{Fore.LIGHTYELLOW_EX}{player.name}'s aktueller Kontostand: €{player.money}")
                        wait()
                    else:
                        print(Fore.LIGHTMAGENTA_EX + f"Du besitzt bereits {current_space.name}. Willkommen zu deinem Grundstück.")
                        print(f"Aktuell befinden sich {current_space.houses} Häuser auf {current_space.name}")
                        while True:
                            houes_choice = input(f"Möchtest du ein Haus bauen für {current_space.house_cost}€? (y/n): ")
                            if houes_choice.lower() == "y":
                                if player.money >= current_space.house_cost:
                                    current_space.houses += 1
                                    print(Fore.GREEN + f"Du hast ein Haus auf {current_space.name} gebaut!")
                                    player.money -= current_space.house_cost
                                    print(f"Aktueller Kontostand: {Fore.LIGHTYELLOW_EX}€{player.money}")
                                else:
                                    print(Fore.RED + "Nicht genug Geld für ein Haus!")
                                print(f"Jetzt befinden sich {current_space.houses} Häuser auf {current_space.name}")         # Debug line
                                wait()
                                break
                            elif houes_choice.lower() == "n":
                                break
                            else:
                                print(Fore.RED + "Ungültige Eingabe! Bitte geben Sie 'y' oder 'n' ein.")
                    
            elif current_space.type == "jail":
                print(Fore.RED + "Du bist im Gefängnis!")
                player.go_to_jail(game.board)
                game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
                wait()
                continue

            elif current_space.type == "special":
                print(Fore.GREEN + f"Du erhältst {current_space.amount}€!")
                player.money += current_space.amount
                print(f"Aktueller Kontostand: {Fore.LIGHTYELLOW_EX}€{player.money}")
                wait()

            elif current_space.type == "tax":
                if hasattr(current_space, 'amount'):
                    print(Fore.RED + f"Zahle {current_space.amount}€ Steuern!")
                    if player.money >= current_space.amount:
                        player.money -= current_space.amount
                        print(f"Aktueller Kontostand: {Fore.LIGHTYELLOW_EX}€{player.money}")
                        wait()
                    else:
                        print(Fore.RED + "Nicht genug Geld, um Steuern zu zahlen!")
                        print(f"Aktueller Kontostand: {Fore.LIGHTYELLOW_EX}€{player.money}")
                        wait()

            elif current_space.type == "station":
                handle_station(player, current_space, game, player_color)
                wait()


            elif current_space.type == "utility":               # Copilot did this (too lazy to do myself)
                if current_space.owner is None:
                    print(Fore.GREEN + "Dieses Versorgungswerk ist zu verkaufen!")
                    display_property_details(current_space)
                    while True:
                        buy_choice = input(f"{player_color}{player.name}{Fore.RESET}, möchtest du {current_space.name} für {current_space.cost}€ kaufen? (y/n): ")
                        if buy_choice.lower() == "y":
                            if player.buy_property(current_space):
                                print(Fore.GREEN + f"{player_color}{player.name}{Fore.RESET} hat {current_space.name} gekauft!")
                                current_space.owner = player
                                wait()
                                break
                            else:
                                print(Fore.RED + "Nicht genug Geld, um dieses Versorgungswerk zu kaufen.")
                                wait()
                                break
                        elif buy_choice.lower() == "n":
                            break
                        else:
                            print(Fore.RED + "Ungültige Eingabe! Bitte geben Sie 'y' oder 'n' ein.")
                elif current_space.owner is not player:
                    # Count how many utilities the owner has
                    owner_utilities = [
                        prop for prop in current_space.owner.properties
                        if hasattr(prop, "type") and prop.type == "utility"
                    ]
                    # Ask for dice roll (simulate again for rent calculation) (can also pass the old dice roll by just adding dice_sum = dice_roll, but I like this option better)

                    d1, d2 = randint(1, 6), randint(1, 6)
                    dice_sum = d1 + d2

                    print(Fore.CYAN + f"{current_space.owner.name} besitzt {len(owner_utilities)} Versorgungswerk(e).")
                    print(Fore.CYAN + f"Du würfelst für die Miete: {d1} + {d2} = {dice_sum}")
                    if len(owner_utilities) == 2:
                        rent = 10 * dice_sum
                    else:
                        rent = 4 * dice_sum
                    print(Fore.RED + f"Du musst {rent}€ Miete zahlen!")
                    if player.money >= rent:
                        player.money -= rent
                        current_space.owner.money += rent
                        print(Fore.LIGHTYELLOW_EX + f"{player.name}'s aktueller Kontostand: €{player.money}")
                    else:
                        print(Fore.RED + "Nicht genug Geld, um die Miete zu zahlen!")
                        player.declare_bankruptcy(current_space.owner)
                    wait()
                else:
                    print(Fore.LIGHTMAGENTA_EX + f"Du besitzt bereits {current_space.name}. Willkommen zu deinem Versorgungswerk.")
                    wait()
        clear_term()
        game.current_player_idx = (game.current_player_idx + 1) % len(game.players)

def throw_dice(player, game) -> int:
    if player.in_jail:
        print("Du bist im Gefängnis für diesen Zug.")
        game.current_player_idx = (game.current_player_idx + 1) % len(game.players)
        wait()
        player.in_jail = False  # Automatically release the player from jail after one turn
        return -1  # Return a value to indicate that the player didn't roll the dice
    else:
        d1, d2 = randint(1, 6), randint(1, 6)
        dice_art = {
            1: Fore.WHITE + "",
            2: Fore.RED + "",
            3: Fore.GREEN + "",
            4: Fore.YELLOW + "",
            5: Fore.LIGHTBLUE_EX + "",
            6: Fore.MAGENTA + ""
        }
        print(Fore.CYAN + "\nWürfel:")
        print(f" {dice_art[d1]} {dice_art[d2]}")
        print(Fore.WHITE + f" Summe: {d1 + d2}")
        return d1 + d2
def wait():
    user_input = input(Fore.CYAN + "\n[Enter] zum Fortfahren... (oder [e] und dann Enter zur Beendung des Spiels) ")
    if user_input.lower() == "e":
        winner = max(global_players, key=lambda player: player.money)           # Findet den Spieler, der am meisten Geld hat // player.money ist die variable, die verglichen wird und player ist der parameter
        print(Fore.GREEN + f"{winner.name} hat das Spiel gewonnen! Mit {winner.money}€"+ Fore.RESET)
        time.sleep(5)
        print(Fore.RED + "Spiel wird beendet..." + Fore.RESET)
        time.sleep(2)
        clear_term()
        os._exit(0)
        
def handle_station(player, current_space, game, player_color):
    stations = [space for space in game.board.spaces if getattr(space, "type", None) == "station"]
    if current_space.owner is None:
        print(Fore.GREEN + "Dieser Bahnhof ist zu verkaufen!")
        print(Fore.LIGHTRED_EX + f"Preis: {current_space.cost}€ | Basis-Miete: {current_space.base_rent}€")
        while True:
            buy_choice = input(f"{player_color}{player.name}{Fore.RESET}, möchtest du {current_space.name} für {current_space.cost}€ kaufen? (y/n): ")
            if buy_choice.lower() == "y":
                if player.money >= current_space.cost:
                    player.money -= current_space.cost
                    player.properties.append(current_space)
                    current_space.owner = player
                    print(Fore.GREEN + f"{player_color}{player.name}{Fore.RESET} hat {current_space.name} gekauft!")
                    break
                else:
                    print(Fore.RED + "Nicht genug Geld, um diesen Bahnhof zu kaufen.")
                    break
            elif buy_choice.lower() == "n":
                break
            else:
                print(Fore.RED + "Ungültige Eingabe! Bitte geben Sie 'y' oder 'n' ein.")
    else:
        show_board(game.players, game.board)
        print(Fore.LIGHTMAGENTA_EX + f"Du bist auf {current_space.name}.")
        other_stations = [s for s in stations if s != current_space]
        if other_stations:
            print(Fore.CYAN + "Möchtest du zu einem anderen Bahnhof teleportieren?")
            for idx, s in enumerate(other_stations):
                print(f"{idx+1}. {s.name} (Besitzer: {s.owner.name if s.owner else 'Unbesetzt'})")
            print("0. Nein, hier bleiben und ggf. Miete zahlen.")
            try:
                choice = int(input("Wähle eine Option: "))
            except ValueError:
                choice = 0
            if choice > 0 and choice <= len(other_stations):
                target_station = other_stations[choice-1]
                payments = []
                # Correctly reference the station names for payment messages
                if current_space.owner != player and current_space.owner is not None:
                    payments.append((current_space.owner, current_space.base_rent * 2, current_space.name))
                if target_station.owner != player and target_station.owner is not None and target_station.owner != current_space.owner:
                    payments.append((target_station.owner, target_station.base_rent * 2, target_station.name))
                for owner, rent, station_name in payments:
                    print(Fore.RED + f"Du musst {rent}€ an {owner.name} zahlen für die Nutzung von {station_name}!")
                    if player.money >= rent:
                        player.money -= rent
                        owner.money += rent
                    else:
                        print(Fore.RED + "Nicht genug Geld für die Bahnhofsnutzung!")
                        player.declare_bankruptcy(owner)