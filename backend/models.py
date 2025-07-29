from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Property(BaseModel):
    id: int
    name: str
    type: str  # property, railroad, utility, special
    color: str
    price: Optional[int] = None
    rent: Optional[int] = None
    owner: Optional[int] = None
    description: Optional[str] = None

class Player(BaseModel):
    id: int
    name: str
    money: int = 1500
    position: int = 0
    properties: List[int] = []
    isBot: bool = False
    difficulty: Optional[str] = None

class DiceRoll(BaseModel):
    dice1: int = Field(..., ge=1, le=6)
    dice2: int = Field(..., ge=1, le=6)
    total: int = Field(..., ge=2, le=12)

class GameState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    players: List[Player]
    currentPlayerIndex: int = 0
    gamePhase: str = "playing"  # playing, ended
    winner: Optional[int] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastMove: Optional[Dict[str, Any]] = None

class GameCreate(BaseModel):
    playerName: str = "You"

class DiceRollResponse(BaseModel):
    dice1: int
    dice2: int
    total: int
    newPosition: int
    passedGO: bool
    landedProperty: Property

class PropertyAction(BaseModel):
    action: str  # "buy" or "decline"
    playerId: int
    propertyId: int

class BotDecision(BaseModel):
    action: str  # "buy" or "pass"
    reasoning: str
    confidence: float

class GameMove(BaseModel):
    gameId: str
    playerId: int
    moveType: str  # "dice_roll", "buy_property", "pay_rent", etc.
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class GameResponse(BaseModel):
    success: bool
    game: Optional[GameState] = None
    message: str = ""
    error: Optional[str] = None

class ActionResponse(BaseModel):
    success: bool
    message: str
    gameState: Optional[GameState] = None
    nextAction: Optional[str] = None  # For bot turns