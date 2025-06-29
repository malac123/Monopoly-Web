import json
from game_logic.property import Property

class Space:
    """Base class for all board spaces"""
    def __init__(self, name, space_type, **kwargs):     # **kwargs for additional attributes
        self.name = name
        self.type = space_type
        self.owner = None
        # Add all additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

class GameBoard:
    def __init__(self):
        with open("assets/board_data.json", encoding="utf-8") as f:
            board_data = json.load(f)
            self.spaces = []
            
            for data in board_data:
                if data["type"] == "property":
                    space = Property(
                        name=data["name"],
                        cost=data["cost"],
                        rent=data["rent"],
                        color_group=data.get("color_group"),
                        house_cost=data.get("house_cost")
                    )
                else:
                    # Create generic space with all attributes from JSON
                    space = Space(
                        name=data["name"],
                        space_type=data["type"],
                        **{k: v for k, v in data.items() 
                           if k not in ["name", "type"]}
                    )
                self.spaces.append(space)

    def get_space(self, position):
        return self.spaces[position % len(self.spaces)]