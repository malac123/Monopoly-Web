from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import random
from datetime import datetime

from models import (
    GameState, GameCreate, Player, Property, DiceRollResponse, 
    PropertyAction, ActionResponse, GameResponse, GameMove
)
from game_logic import (
    PROPERTIES_DATA, create_default_players, roll_dice, move_player,
    calculate_rent, bot_decision_engine, check_win_condition,
    execute_property_purchase, execute_rent_payment
)

router = APIRouter(prefix="/api", tags=["game"])

# In-memory game storage (replace with MongoDB in production)
games_db: Dict[str, GameState] = {}
properties_db: List[Property] = [Property(**prop) for prop in PROPERTIES_DATA]

@router.post("/games", response_model=GameResponse)
async def create_game(game_data: GameCreate):
    """Create a new game session"""
    try:
        # Create new game state
        players = create_default_players()
        if game_data.playerName != "You":
            players[0].name = game_data.playerName
            
        game = GameState(players=players)
        games_db[game.id] = game
        
        return GameResponse(
            success=True,
            game=game,
            message="Game created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")

@router.get("/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: str):
    """Get current game state"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameResponse(
        success=True,
        game=games_db[game_id],
        message="Game retrieved successfully"
    )

@router.get("/properties", response_model=List[Property])
async def get_properties():
    """Get all property definitions"""
    return properties_db

@router.get("/games/{game_id}/properties", response_model=List[Property])
async def get_game_properties(game_id: str):
    """Get properties with current ownership for a game"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Return properties with ownership from game state
    return properties_db

@router.post("/games/{game_id}/roll-dice", response_model=ActionResponse)
async def roll_dice_endpoint(game_id: str):
    """Roll dice for current player"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games_db[game_id]
    current_player = game.players[game.currentPlayerIndex]
    
    if current_player.isBot:
        raise HTTPException(status_code=400, detail="Cannot roll dice for bot player")
    
    try:
        # Roll dice
        dice_result = roll_dice()
        
        # Move player
        old_position = current_player.position
        new_position, passed_go, landed_property = move_player(
            current_player, dice_result.total, properties_db
        )
        
        # Update game state
        game.lastMove = {
            "type": "dice_roll",
            "player": current_player.name,
            "dice": [dice_result.dice1, dice_result.dice2],
            "total": dice_result.total,
            "oldPosition": old_position,
            "newPosition": new_position,
            "passedGO": passed_go,
            "landedProperty": landed_property.name
        }
        
        message = f"{current_player.name} rolled {dice_result.total}"
        if passed_go:
            message += " and passed GO! Collected $200"
        message += f" and landed on {landed_property.name}"
        
        return ActionResponse(
            success=True,
            message=message,
            gameState=game,
            nextAction="handle_property" if landed_property.type != "special" else "end_turn"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to roll dice: {str(e)}")

@router.post("/games/{game_id}/property-action", response_model=ActionResponse)
async def handle_property_action(game_id: str, action: PropertyAction):
    """Handle property buy/decline action"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games_db[game_id]
    player = next(p for p in game.players if p.id == action.playerId)
    property = next(p for p in properties_db if p.id == action.propertyId)
    
    try:
        if action.action == "buy":
            success = execute_property_purchase(player, property, properties_db)
            if success:
                message = f"{player.name} bought {property.name} for ${property.price}"
            else:
                message = f"{player.name} cannot afford {property.name}"
        else:
            message = f"{player.name} declined to buy {property.name}"
        
        return ActionResponse(
            success=True,
            message=message,
            gameState=game,
            nextAction="end_turn"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to handle property action: {str(e)}")

@router.post("/games/{game_id}/end-turn", response_model=ActionResponse)
async def end_turn(game_id: str):
    """End current player's turn and advance to next player"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games_db[game_id]
    
    try:
        # Check win condition
        winner = check_win_condition(game.players)
        if winner:
            game.winner = winner.id
            game.gamePhase = "ended"
            return ActionResponse(
                success=True,
                message=f"{winner.name} wins the game!",
                gameState=game,
                nextAction="game_over"
            )
        
        # Advance to next player
        game.currentPlayerIndex = (game.currentPlayerIndex + 1) % len(game.players)
        next_player = game.players[game.currentPlayerIndex]
        
        return ActionResponse(
            success=True,
            message=f"It's {next_player.name}'s turn",
            gameState=game,
            nextAction="bot_turn" if next_player.isBot else "player_turn"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end turn: {str(e)}")

@router.post("/games/{game_id}/bot-turn", response_model=ActionResponse)
async def execute_bot_turn(game_id: str):
    """Execute a complete bot turn"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games_db[game_id]
    current_player = game.players[game.currentPlayerIndex]
    
    if not current_player.isBot:
        raise HTTPException(status_code=400, detail="Current player is not a bot")
    
    try:
        # Bot rolls dice
        dice_result = roll_dice()
        old_position = current_player.position
        new_position, passed_go, landed_property = move_player(
            current_player, dice_result.total, properties_db
        )
        
        message = f"{current_player.name} rolled {dice_result.total}"
        if passed_go:
            message += " and passed GO! Collected $200"
        
        # Handle property logic
        if landed_property.type == "special":
            message += f" and landed on {landed_property.name}"
        elif landed_property.owner is None:
            # Bot decision for purchasing
            decision = bot_decision_engine(current_player, landed_property)
            if decision.action == "buy" and execute_property_purchase(current_player, landed_property, properties_db):
                message += f" and bought {landed_property.name} for ${landed_property.price}"
            else:
                message += f" and declined to buy {landed_property.name}"
        elif landed_property.owner != current_player.id:
            # Pay rent
            owner = next(p for p in game.players if p.id == landed_property.owner)
            rent = calculate_rent(landed_property, properties_db, owner)
            execute_rent_payment(current_player, owner, rent)
            message += f" and paid ${rent} rent to {owner.name}"
        else:
            message += f" and landed on their own property {landed_property.name}"
        
        # Update game state
        game.lastMove = {
            "type": "bot_turn",
            "player": current_player.name,
            "dice": [dice_result.dice1, dice_result.dice2],
            "total": dice_result.total,
            "action": "completed"
        }
        
        return ActionResponse(
            success=True,
            message=message,
            gameState=game,
            nextAction="end_turn"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute bot turn: {str(e)}")

@router.delete("/games/{game_id}")
async def delete_game(game_id: str):
    """Delete a game session"""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games_db[game_id]
    return {"success": True, "message": "Game deleted successfully"}