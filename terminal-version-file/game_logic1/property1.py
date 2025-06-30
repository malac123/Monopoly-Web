from colorama import Fore, init
init(autoreset=True)


class Property:
    def __init__(self, name, cost, rent, color_group=None, house_cost=0):
        self.name = name
        self.type = "property" 
        self.cost = cost
        self.rent = rent
        self.color_group = color_group
        self.owner = None
        self.houses = 0
        self.house_cost = house_cost

    def land_on(self, player):
        if self.owner is None:
            return "buy"
        elif self.owner != player:
            return "pay_rent"
        return "owned"


def display_property_details(property):                             # Methode um die Eigenschaften der jeweiligen Properties anzuzeigen / nicht teil von Klasse Property damit man es in terminal_ui importen kann
    print(Fore.LIGHTRED_EX + f"Miete: {property.rent}")

