from colorama import Fore, init
init(autoreset=True)

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.position = 0
        self.properties = []
        self.in_jail = False

    def move(self, steps):
        self.position = (self.position + steps) % 40                # Uses modulus Operator to avoid going out of bounds of the board 

    def buy_property(self, property):
        if self.money >= property.cost:
            self.money -= property.cost
            self.properties.append(property)
            property.owner = self
            return True
        return False

    def pay_rent(self, property):
        if property.houses >= len(property.rent):
            rent_amount = property.rent[-1]  # Use highest rent if houses exceed array
        else:
            rent_amount = property.rent[property.houses]
        if self.money >= rent_amount:
            self.money -= rent_amount
            property.owner.money += rent_amount
            print(f"{Fore.RED}{self.name} zahlt {rent_amount}€ Miete an {property.owner.name}.")
        else:
            self.declare_bankruptcy(property.owner)

    def declare_bankruptcy(self, creditor=None):
        """Handle player bankruptcy."""
        print(Fore.RED + f"{self.name} geht bankrott und kann seine Schulden nicht begleichen.")
        if creditor:
            for prop in self.properties:
                prop.owner = creditor
                creditor.properties.append(prop)
            self.properties.clear()
        self.money = 0
    def go_to_jail(self, board):                                        # Spieler geht in den Jail wenn er auf Jail landet... (hat davor gefehlt)
        for space in board.spaces:
            if space.type == "jail":
                self.position = board.spaces.index(space)
                self.in_jail = True
    def release_from_jail(self):
        if self.in_jail:
            self.in_jail = False
            print(Fore.LIGHTGREEN_EX + "Du bischt wieder frei Kollega")
    def __str__(self):
        return f"{self.name} | €{self.money} | Position: {self.position}"
    

