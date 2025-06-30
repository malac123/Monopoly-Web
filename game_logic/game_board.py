class Space:
    def __init__(self, name, space_type, **kwargs):
        self.name = name
        self.type = space_type
        self.owner = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class GameBoard:
    def __init__(self):
        # For demo, use a simple hardcoded board
        self.spaces = [
            Space('Los', 'special', amount=200),
            Space('Badstraße', 'property', cost=60, rent=[2, 10, 30, 90, 160, 250], color_group='brown'),
            Space('Gemeinschaftsfeld', 'special', amount=0),
            Space('Turmstraße', 'property', cost=60, rent=[4, 20, 60, 180, 320, 450], color_group='brown'),
            Space('Einkommensteuer', 'tax', amount=200),
            Space('Südbahnhof', 'station', cost=200, base_rent=25),
            Space('Chausseestraße', 'property', cost=100, rent=[6, 30, 90, 270, 400, 550], color_group='light_blue'),
            Space('Ereignisfeld', 'special', amount=0),
            Space('Elisenstraße', 'property', cost=100, rent=[6, 30, 90, 270, 400, 550], color_group='light_blue'),
            Space('Poststraße', 'property', cost=120, rent=[8, 40, 100, 300, 450, 600], color_group='light_blue'),
            # ... add more spaces as needed ...
        ]

    def get_space(self, position):
        return self.spaces[position % len(self.spaces)] 