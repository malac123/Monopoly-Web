from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict, List, Optional
import uuid
import json
import logging
from datetime import datetime

from multiplayer_models import (
    MultiplayerRoom, PlayerConnection, GameSettings, RoomJoinRequest,
    RoomResponse, JoinRoomResponse, RoomUpdateMessage, WebSocketMessage,
    PlayerAction, GameStateUpdate, generate_room_code
)
from websocket_manager import manager
from game_logic import create_default_players
from models import GameState

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/multiplayer", tags=["multiplayer"])

# In-memory storage for rooms (replace with MongoDB/Redis in production)
rooms_db: Dict[str, MultiplayerRoom] = {}
active_games: Dict[str, GameState] = {}  # room_id -> game_state

@router.post("/create-room", response_model=RoomResponse)
async def create_room(host_name: str = "Host"):
    """Create a new multiplayer room"""
    try:
        room_id = generate_room_code()
        
        # Ensure unique room code
        while room_id in rooms_db:
            room_id = generate_room_code()
        
        host_player = PlayerConnection(
            name=host_name,
            is_host=True,
            avatar_icon=0
        )
        
        room = MultiplayerRoom(
            id=room_id,
            host_id=host_player.id,
            players=[host_player]
        )
        
        rooms_db[room_id] = room
        logger.info(f"Created room {room_id} with host {host_name}")
        
        return RoomResponse(
            success=True,
            room=room,
            message=f"Room {room_id} created successfully"
        )
        
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create room: {str(e)}")

@router.post("/join-room", response_model=JoinRoomResponse)
async def join_room(request: RoomJoinRequest):
    """Join an existing room"""
    try:
        room_code = request.room_code.upper().strip()
        
        if room_code not in rooms_db:
            return JoinRoomResponse(
                success=False,
                error="Room not found",
                message="Invalid room code"
            )
        
        room = rooms_db[room_code]
        
        # Check if room is full
        if len(room.players) >= room.max_players:
            return JoinRoomResponse(
                success=False,
                error="Room is full",
                message=f"Room {room_code} is already full ({room.max_players} players)"
            )
        
        # Check if game already started
        if room.status == "playing":
            return JoinRoomResponse(
                success=False,
                error="Game in progress",
                message="Cannot join - game is already in progress"
            )
        
        # Check for duplicate names
        existing_names = [p.name.lower() for p in room.players]
        if request.player_name.lower() in existing_names:
            return JoinRoomResponse(
                success=False,
                error="Name taken",
                message="Player name already taken in this room"
            )
        
        # Create new player
        new_player = PlayerConnection(
            name=request.player_name,
            is_host=False,
            avatar_icon=len(room.players)  # Simple avatar assignment
        )
        
        room.players.append(new_player)
        rooms_db[room_code] = room
        
        # Broadcast player joined to room
        await manager.broadcast_to_room(
            room_code,
            {
                "type": "player_joined",
                "room": room.dict(),
                "player_name": new_player.name,
                "message": f"{new_player.name} joined the room"
            }
        )
        
        logger.info(f"Player {request.player_name} joined room {room_code}")
        
        return JoinRoomResponse(
            success=True,
            room=room,
            player_id=new_player.id,
            message=f"Successfully joined room {room_code}"
        )
        
    except Exception as e:
        logger.error(f"Error joining room: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to join room: {str(e)}")

@router.get("/room/{room_code}", response_model=RoomResponse)
async def get_room(room_code: str):
    """Get room information"""
    room_code = room_code.upper().strip()
    
    if room_code not in rooms_db:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return RoomResponse(
        success=True,
        room=rooms_db[room_code],
        message="Room retrieved successfully"
    )

@router.post("/room/{room_code}/start-game")
async def start_game(room_code: str, host_player_id: str):
    """Start the game (host only)"""
    try:
        room_code = room_code.upper().strip()
        
        if room_code not in rooms_db:
            raise HTTPException(status_code=404, detail="Room not found")
        
        room = rooms_db[room_code]
        
        # Verify host permissions
        if room.host_id != host_player_id:
            raise HTTPException(status_code=403, detail="Only the host can start the game")
        
        # Check minimum players
        if len(room.players) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 players to start")
        
        # Create game state
        game_players = []
        for i, player in enumerate(room.players):
            game_players.append({
                "id": i + 1,
                "name": player.name,
                "money": room.settings.starting_money,
                "position": 0,
                "properties": [],
                "isBot": False,
                "difficulty": None,
                "multiplayer_id": player.id  # Link to multiplayer player
            })
        
        # Add bots if requested
        if room.settings.include_bots and len(room.players) < 4:
            bots_needed = min(room.settings.bot_count, 4 - len(room.players))
            bot_names = ["AI Player 1", "AI Player 2", "AI Player 3"]
            difficulties = ["Mentally slow", "Medium rare", "Highly proficient"]
            
            for i in range(bots_needed):
                game_players.append({
                    "id": len(game_players) + 1,
                    "name": bot_names[i],
                    "money": room.settings.starting_money,
                    "position": 0,
                    "properties": [],
                    "isBot": True,
                    "difficulty": difficulties[i % 3],
                    "multiplayer_id": None
                })
        
        game_state = GameState(
            id=str(uuid.uuid4()),
            players=game_players,
            currentPlayerIndex=0,
            gamePhase="playing"
        )
        
        # Update room status
        room.status = "playing"
        room.game_id = game_state.id
        rooms_db[room_code] = room
        active_games[room_code] = game_state
        
        # Broadcast game started
        await manager.broadcast_to_room(
            room_code,
            {
                "type": "game_started",
                "room": room.dict(),
                "game_state": game_state.dict(),
                "message": "Game has started!"
            }
        )
        
        logger.info(f"Game started in room {room_code} with {len(game_players)} players")
        
        return {
            "success": True,
            "message": "Game started successfully",
            "game_id": game_state.id
        }
        
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")

@router.post("/room/{room_code}/update-settings")
async def update_room_settings(room_code: str, settings: GameSettings, host_player_id: str):
    """Update room settings (host only)"""
    try:
        room_code = room_code.upper().strip()
        
        if room_code not in rooms_db:
            raise HTTPException(status_code=404, detail="Room not found")
        
        room = rooms_db[room_code]
        
        # Verify host permissions
        if room.host_id != host_player_id:
            raise HTTPException(status_code=403, detail="Only the host can update settings")
        
        # Update settings
        room.settings = settings
        rooms_db[room_code] = room
        
        # Broadcast settings update
        await manager.broadcast_to_room(
            room_code,
            {
                "type": "settings_updated",
                "room": room.dict(),
                "message": "Game settings updated"
            }
        )
        
        return {"success": True, "message": "Settings updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@router.websocket("/ws/{room_code}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    """WebSocket endpoint for real-time communication"""
    room_code = room_code.upper().strip()
    connection_id = str(uuid.uuid4())
    
    try:
        await manager.connect(websocket, connection_id)
        manager.add_to_room(connection_id, room_code)
        manager.map_player_to_connection(player_id, connection_id)
        
        # Update player connection status
        if room_code in rooms_db:
            room = rooms_db[room_code]
            for player in room.players:
                if player.id == player_id:
                    player.is_connected = True
                    player.websocket_id = connection_id
                    break
        
        logger.info(f"Player {player_id} connected to room {room_code}")
        
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await handle_websocket_message(room_code, player_id, message)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error(f"WebSocket message error: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "message": str(e)
                }))
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    
    finally:
        # Clean up on disconnect
        manager.disconnect(connection_id)
        
        # Update player connection status
        if room_code in rooms_db:
            room = rooms_db[room_code]
            for player in room.players:
                if player.id == player_id:
                    player.is_connected = False
                    player.websocket_id = None
                    break
        
        logger.info(f"Player {player_id} disconnected from room {room_code}")

async def handle_websocket_message(room_code: str, player_id: str, message: dict):
    """Handle incoming WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "ping":
        # Respond to ping
        await manager.send_to_player(player_id, {"type": "pong"})
    
    elif message_type == "game_action":
        # Handle game actions (dice roll, property purchase, etc.)
        await handle_game_action(room_code, player_id, message.get("data", {}))
    
    elif message_type == "chat_message":
        # Handle chat messages (low priority - implement later)
        pass
    
    else:
        logger.warning(f"Unknown message type: {message_type}")

async def handle_game_action(room_code: str, player_id: str, action_data: dict):
    """Handle game actions from players"""
    try:
        if room_code not in active_games:
            await manager.send_to_player(player_id, {
                "type": "error",
                "message": "Game not found"
            })
            return
        
        game_state = active_games[room_code]
        action_type = action_data.get("action_type")
        
        # Validate it's the player's turn
        current_player = game_state.players[game_state.currentPlayerIndex]
        if hasattr(current_player, 'multiplayer_id') and current_player.multiplayer_id != player_id:
            await manager.send_to_player(player_id, {
                "type": "error",
                "message": "Not your turn"
            })
            return
        
        # Handle different action types
        if action_type == "roll_dice":
            # Process dice roll (integrate with existing game logic)
            result = {"success": True, "message": "Dice rolled"}
            
        elif action_type == "buy_property":
            # Process property purchase
            result = {"success": True, "message": "Property purchased"}
            
        # Broadcast game update to all players in room
        await manager.broadcast_to_room(room_code, {
            "type": "game_update",
            "game_state": game_state.dict(),
            "action": action_data,
            "player_id": player_id
        })
        
    except Exception as e:
        logger.error(f"Error handling game action: {e}")
        await manager.send_to_player(player_id, {
            "type": "error",
            "message": str(e)
        })