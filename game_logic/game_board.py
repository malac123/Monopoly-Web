import json
from game_logic.property import Property

class Space:
    """Base class for all board spaces"""
    def __init__(self, name, space_type, **kwargs):
        self.name = name
        self.type = space_type
        self.owner = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class GameBoard:
    def __init__(self, board_data_path="assets/board_data.json"):
        with open(board_data_path, encoding="utf-8") as f:
            board_data = json.load(f)
            self.spaces = []
            for data in board_data:
                if data["type"] == "property":
                    space = Property(
                        name=data["name"],
                        cost=data["cost"],
                        rent=data["rent"],
                        color_group=data.get("color_group"),
                        house_cost=data.get("house_cost", 0)
                    )
                else:
                    space = Space(
                        name=data["name"],
                        space_type=data["type"],
                        **{k: v for k, v in data.items() if k not in ["name", "type"]}
                    )
                self.spaces.append(space)

    def get_space(self, position):
        return self.spaces[position % len(self.spaces)] 