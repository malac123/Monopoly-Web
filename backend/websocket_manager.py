from fastapi import WebSocket
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Active WebSocket connections: {connection_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Room memberships: {room_id: [connection_ids]}
        self.room_connections: Dict[str, List[str]] = {}
        # Player to connection mapping: {player_id: connection_id}
        self.player_connections: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, connection_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        logger.info(f"WebSocket connected: {connection_id}")

    def disconnect(self, connection_id: str):
        """Remove WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove from rooms
        for room_id in list(self.room_connections.keys()):
            if connection_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(connection_id)
                if not self.room_connections[room_id]:
                    del self.room_connections[room_id]
        
        # Remove player mapping
        for player_id, conn_id in list(self.player_connections.items()):
            if conn_id == connection_id:
                del self.player_connections[player_id]
        
        logger.info(f"WebSocket disconnected: {connection_id}")

    def add_to_room(self, connection_id: str, room_id: str):
        """Add connection to a room"""
        if room_id not in self.room_connections:
            self.room_connections[room_id] = []
        
        if connection_id not in self.room_connections[room_id]:
            self.room_connections[room_id].append(connection_id)

    def remove_from_room(self, connection_id: str, room_id: str):
        """Remove connection from a room"""
        if room_id in self.room_connections:
            if connection_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(connection_id)
            
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]

    def map_player_to_connection(self, player_id: str, connection_id: str):
        """Map player ID to connection ID"""
        self.player_connections[player_id] = connection_id

    async def send_to_connection(self, connection_id: str, message: dict):
        """Send message to specific connection"""
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_text(json.dumps(message))
                return True
            except Exception as e:
                logger.error(f"Error sending to connection {connection_id}: {e}")
                self.disconnect(connection_id)
                return False
        return False

    async def send_to_player(self, player_id: str, message: dict):
        """Send message to specific player"""
        connection_id = self.player_connections.get(player_id)
        if connection_id:
            return await self.send_to_connection(connection_id, message)
        return False

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_connection: Optional[str] = None):
        """Broadcast message to all connections in a room"""
        if room_id not in self.room_connections:
            return

        connections = self.room_connections[room_id].copy()
        successful_sends = 0
        
        for connection_id in connections:
            if exclude_connection and connection_id == exclude_connection:
                continue
            
            success = await self.send_to_connection(connection_id, message)
            if success:
                successful_sends += 1

        logger.info(f"Broadcasted to room {room_id}: {successful_sends}/{len(connections)} successful")
        return successful_sends

    async def broadcast_to_all(self, message: dict):
        """Broadcast message to all active connections"""
        successful_sends = 0
        for connection_id in list(self.active_connections.keys()):
            success = await self.send_to_connection(connection_id, message)
            if success:
                successful_sends += 1
        return successful_sends

    def get_room_connections(self, room_id: str) -> List[str]:
        """Get all connection IDs in a room"""
        return self.room_connections.get(room_id, [])

    def get_player_connection(self, player_id: str) -> Optional[str]:
        """Get connection ID for a player"""
        return self.player_connections.get(player_id)

    def is_player_connected(self, player_id: str) -> bool:
        """Check if player is connected"""
        connection_id = self.player_connections.get(player_id)
        return connection_id is not None and connection_id in self.active_connections

    def get_connection_stats(self) -> dict:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "total_rooms": len(self.room_connections),
            "total_players": len(self.player_connections),
            "rooms": {room_id: len(connections) for room_id, connections in self.room_connections.items()}
        }

# Global connection manager instance
manager = ConnectionManager()