from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import random
import string

class PlayerConnection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    websocket_id: Optional[str] = None
    is_host: bool = False
    is_connected: bool = True
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    avatar_icon: int = 0  # Index for icon selection

class GameSettings(BaseModel):
    starting_money: int = 1500
    max_players: int = 4
    include_bots: bool = False
    bot_count: int = 0
    game_speed: str = "normal"  # slow, normal, fast
    property_price_multiplier: float = 1.0
    rent_multiplier: float = 1.0
    pass_go_bonus: int = 200

class MultiplayerRoom(BaseModel):
    id: str = Field(default_factory=lambda: generate_room_code())
    host_id: str
    players: List[PlayerConnection] = []
    settings: GameSettings = Field(default_factory=GameSettings)
    status: str = "waiting"  # waiting, playing, finished
    game_id: Optional[str] = None  # Links to actual game when started
    created_at: datetime = Field(default_factory=datetime.utcnow)
    max_players: int = 4

class RoomJoinRequest(BaseModel):
    room_code: str
    player_name: str

class RoomUpdateMessage(BaseModel):
    type: str  # "player_joined", "player_left", "settings_updated", "game_started"
    room: MultiplayerRoom
    message: str
    player_name: Optional[str] = None

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    room_id: Optional[str] = None
    player_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class RoomResponse(BaseModel):
    success: bool
    room: Optional[MultiplayerRoom] = None
    message: str = ""
    error: Optional[str] = None

class JoinRoomResponse(BaseModel):
    success: bool
    room: Optional[MultiplayerRoom] = None
    player_id: Optional[str] = None
    message: str = ""
    error: Optional[str] = None

def generate_room_code() -> str:
    """Generate a random room code like '2FG-8JH'"""
    def random_char():
        return random.choice(string.ascii_uppercase + string.digits)
    
    part1 = ''.join(random_char() for _ in range(3))
    part2 = ''.join(random_char() for _ in range(3))
    return f"{part1}-{part2}"

class GameStateUpdate(BaseModel):
    type: str  # "dice_rolled", "property_bought", "turn_changed", etc.
    game_state: Optional[Dict[str, Any]] = None
    player_action: Optional[Dict[str, Any]] = None
    message: str = ""
    next_player_id: Optional[str] = None

class PlayerAction(BaseModel):
    player_id: str
    action_type: str  # "roll_dice", "buy_property", "decline_property", "end_turn"
    data: Dict[str, Any] = {}
    room_id: str