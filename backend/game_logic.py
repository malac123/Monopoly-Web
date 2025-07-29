import random
from typing import Tuple, Dict, Any, Optional
from models import Player, Property, DiceRoll, BotDecision

# Property definitions - matches frontend mock data
PROPERTIES_DATA = [
    {"id": 1, "name": "GO", "type": "special", "color": "bg-green-600", "price": None, "rent": None, "owner": None},
    {"id": 2, "name": "Baltic Ave", "type": "property", "color": "bg-amber-800", "price": 60, "rent": 4, "owner": None, "description": "Affordable starter property"},
    {"id": 3, "name": "Reading Railroad", "type": "railroad", "color": "bg-gray-700", "price": 200, "rent": 25, "owner": None, "description": "Major transportation hub"},
    {"id": 4, "name": "Oriental Ave", "type": "property", "color": "bg-cyan-500", "price": 100, "rent": 6, "owner": None, "description": "Growing neighborhood"},
    {"id": 5, "name": "Vermont Ave", "type": "property", "color": "bg-cyan-500", "price": 100, "rent": 6, "owner": None, "description": "Quiet residential area"},
    {"id": 6, "name": "Jail", "type": "special", "color": "bg-red-600", "price": None, "rent": None, "owner": None},
    {"id": 7, "name": "St. Charles", "type": "property", "color": "bg-pink-500", "price": 140, "rent": 10, "owner": None, "description": "Historic district"},
    {"id": 8, "name": "Electric Co", "type": "utility", "color": "bg-yellow-500", "price": 150, "rent": 15, "owner": None, "description": "Power utility company"},
    {"id": 9, "name": "States Ave", "type": "property", "color": "bg-pink-500", "price": 140, "rent": 10, "owner": None, "description": "Commercial center"},
    {"id": 10, "name": "Tennessee", "type": "property", "color": "bg-orange-500", "price": 180, "rent": 14, "owner": None, "description": "Popular destination"},
    {"id": 11, "name": "Free Parking", "type": "special", "color": "bg-blue-600", "price": None, "rent": None, "owner": None},
    {"id": 12, "name": "Kentucky Ave", "type": "property", "color": "bg-red-600", "price": 220, "rent": 18, "owner": None, "description": "Prime real estate"},
    {"id": 13, "name": "Indiana Ave", "type": "property", "color": "bg-red-600", "price": 220, "rent": 18, "owner": None, "description": "High-value district"},
    {"id": 14, "name": "Atlantic Ave", "type": "property", "color": "bg-yellow-500", "price": 260, "rent": 22, "owner": None, "description": "Luxury avenue"},
    {"id": 15, "name": "Ventnor Ave", "type": "property", "color": "bg-yellow-500", "price": 260, "rent": 22, "owner": None, "description": "Upscale neighborhood"},
    {"id": 16, "name": "Go to Jail", "type": "special", "color": "bg-red-700", "price": None, "rent": None, "owner": None},
    {"id": 17, "name": "Pacific Ave", "type": "property", "color": "bg-green-600", "price": 300, "rent": 26, "owner": None, "description": "Premium location"},
    {"id": 18, "name": "Water Works", "type": "utility", "color": "bg-blue-500", "price": 150, "rent": 15, "owner": None, "description": "Water utility company"},
    {"id": 19, "name": "Park Place", "type": "property", "color": "bg-blue-900", "price": 350, "rent": 35, "owner": None, "description": "Ultra-luxury property"},
    {"id": 20, "name": "Boardwalk", "type": "property", "color": "bg-blue-900", "price": 400, "rent": 50, "owner": None, "description": "Most prestigious address"}
]

def create_default_players() -> list[Player]:
    """Create default game players"""
    return [
        Player(id=1, name="You", isBot=False),
        Player(id=2, name="Slowpoke Sam", isBot=True, difficulty="Mentally slow"),
        Player(id=3, name="Moderate Mike", isBot=True, difficulty="Medium rare"),
        Player(id=4, name="Strategic Sarah", isBot=True, difficulty="Highly proficient")
    ]

def roll_dice() -> DiceRoll:
    """Roll two dice and return result"""
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return DiceRoll(dice1=dice1, dice2=dice2, total=dice1 + dice2)

def move_player(player: Player, steps: int, properties: list[Property]) -> Tuple[int, bool, Property]:
    """
    Move player and return new position, whether passed GO, and landed property
    """
    old_position = player.position
    new_position = (old_position + steps) % len(properties)
    passed_go = new_position < old_position
    
    # Update player position
    player.position = new_position
    
    # Apply GO bonus
    if passed_go:
        player.money += 200
    
    # Get landed property
    landed_property = next(prop for prop in properties if prop.id == new_position + 1)
    
    return new_position, passed_go, landed_property

def calculate_rent(property: Property, properties: list[Property], owner: Player) -> int:
    """Calculate rent for a property"""
    if property.type == "special" or property.rent is None:
        return 0
    
    base_rent = property.rent
    
    # Railroad bonus - more railroads = higher rent
    if property.type == "railroad":
        owned_railroads = sum(1 for prop in properties 
                            if prop.type == "railroad" and prop.owner == owner.id)
        return base_rent * owned_railroads
    
    # Utility bonus - both utilities = 10x rent
    if property.type == "utility":
        owned_utilities = sum(1 for prop in properties 
                            if prop.type == "utility" and prop.owner == owner.id)
        return base_rent * (2 if owned_utilities == 2 else 1)
    
    return base_rent

def bot_decision_engine(bot: Player, property: Property) -> BotDecision:
    """
    Advanced bot AI decision making based on difficulty level
    """
    if property.type == "special" or property.price is None:
        return BotDecision(action="pass", reasoning="Cannot purchase special spaces", confidence=1.0)
    
    affordability = bot.money / property.price if property.price > 0 else 0
    rent_ratio = property.rent / property.price if property.price > 0 and property.rent else 0
    
    if bot.difficulty == "Mentally slow":
        # Simple decision: buy if affordable and cheap
        if affordability > 3 and property.price < 150:
            return BotDecision(
                action="buy", 
                reasoning="It's cheap and I can afford it", 
                confidence=0.6
            )
        return BotDecision(
            action="pass", 
            reasoning="Too expensive or risky", 
            confidence=0.4
        )
    
    elif bot.difficulty == "Medium rare":
        # Moderate strategy: consider rent ratio and affordability
        if affordability > 2 and rent_ratio > 0.08:
            return BotDecision(
                action="buy", 
                reasoning="Good rent-to-price ratio", 
                confidence=0.75
            )
        if affordability > 4 and property.price < 200:
            return BotDecision(
                action="buy", 
                reasoning="Safe investment", 
                confidence=0.65
            )
        return BotDecision(
            action="pass", 
            reasoning="Not a good value", 
            confidence=0.7
        )
    
    elif bot.difficulty == "Highly proficient":
        # Advanced strategy: complex decision making
        expected_return = rent_ratio * 0.7  # Account for vacancy
        risk_factor = 1.5 if property.price > 250 else 1.0
        portfolio_size = len(bot.properties)
        
        if affordability > 2.5 and expected_return > (0.06 / risk_factor):
            return BotDecision(
                action="buy", 
                reasoning="Strong ROI potential", 
                confidence=0.85
            )
        if portfolio_size < 2 and affordability > 3:
            return BotDecision(
                action="buy", 
                reasoning="Portfolio diversification", 
                confidence=0.8
            )
        if property.type == "railroad" and affordability > 2:
            return BotDecision(
                action="buy", 
                reasoning="Strategic railroad acquisition", 
                confidence=0.75
            )
        return BotDecision(
            action="pass", 
            reasoning="Suboptimal investment opportunity", 
            confidence=0.9
        )
    
    return BotDecision(
        action="pass", 
        reasoning="Unknown strategy", 
        confidence=0.5
    )

def check_win_condition(players: list[Player]) -> Optional[Player]:
    """Check if any player has won (others bankrupt)"""
    active_players = [p for p in players if p.money > 0]
    if len(active_players) == 1:
        return active_players[0]
    return None

def execute_property_purchase(player: Player, property: Property, properties: list[Property]) -> bool:
    """Execute property purchase if valid"""
    if (property.price is None or 
        property.owner is not None or 
        player.money < property.price or 
        property.type == "special"):
        return False
    
    # Deduct money and assign ownership
    player.money -= property.price
    property.owner = player.id
    player.properties.append(property.id)
    
    return True

def execute_rent_payment(payer: Player, receiver: Player, amount: int) -> bool:
    """Execute rent payment between players"""
    if payer.money < amount:
        # Player goes bankrupt
        payer.money = 0
        return False
    
    payer.money -= amount
    receiver.money += amount
    return True