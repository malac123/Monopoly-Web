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