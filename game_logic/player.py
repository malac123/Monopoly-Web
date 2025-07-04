class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.position = 0
        self.properties = []
        self.in_jail = False

    def move(self, steps):
        if self.in_jail:
            self.in_jail = False
            return False  # Skip turn if in jail
        self.position = (self.position + steps) % 40
        return True

    def buy_property(self, property):
        if self.money >= property.cost:
            self.money -= property.cost
            self.properties.append(property)
            property.owner = self
            return True
        return False

    def pay_rent(self, property):
        if hasattr(property, 'rent') and hasattr(property, 'owner') and property.owner:
            if isinstance(property.rent, list):
                houses = getattr(property, "houses", 0)
                rent_amount = property.rent[min(houses, len(property.rent) - 1)]            # I think this is correct, but I'm not sure. Amount should be calculated based on number of housese on the property
            else:
                rent_amount = property.rent
            if self.money >= rent_amount:
                self.money -= rent_amount
                property.owner.money += rent_amount
            else:
                self.declare_bankruptcy(property.owner)
        # else: do nothing for non-property fields

    def declare_bankruptcy(self, creditor=None):
        if creditor:
            for prop in self.properties:
                prop.owner = creditor
                creditor.properties.append(prop)
            self.properties.clear()
        self.money = 0

    def go_to_jail(self, board):
        for space in board.spaces:
            if getattr(space, 'type', None) == 'jail':
                self.position = board.spaces.index(space)
                self.in_jail = True

    def release_from_jail(self):
        if self.in_jail:
            self.in_jail = False

    def __str__(self):
        return f"{self.name} | €{self.money} | Position: {self.position}" 