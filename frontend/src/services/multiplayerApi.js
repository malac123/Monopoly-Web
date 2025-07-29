import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/multiplayer`;

// Room Management
export const createRoom = async (hostName) => {
  const response = await axios.post(`${API}/create-room?host_name=${encodeURIComponent(hostName)}`);
  return response.data;
};

export const joinRoom = async (roomCode, playerName) => {
  const response = await axios.post(`${API}/join-room`, {
    room_code: roomCode,
    player_name: playerName
  });
  return response.data;
};

export const getRoom = async (roomCode) => {
  const response = await axios.get(`${API}/room/${roomCode}`);
  return response.data;
};

export const startGame = async (roomCode, hostPlayerId) => {
  const response = await axios.post(`${API}/room/${roomCode}/start-game?host_player_id=${hostPlayerId}`);
  return response.data;
};

export const updateRoomSettings = async (roomCode, settings, hostPlayerId) => {
  const response = await axios.post(`${API}/room/${roomCode}/update-settings?host_player_id=${hostPlayerId}`, settings);
  return response.data;
};

// WebSocket connection class
export class MultiplayerWebSocket {
  constructor(roomCode, playerId, onMessage, onConnect, onDisconnect) {
    this.roomCode = roomCode;
    this.playerId = playerId;
    this.onMessage = onMessage;
    this.onConnect = onConnect;
    this.onDisconnect = onDisconnect;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    try {
      const wsUrl = `${BACKEND_URL.replace('http', 'ws')}/api/multiplayer/ws/${this.roomCode}/${this.playerId}`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        if (this.onConnect) this.onConnect();
        
        // Send ping to establish connection
        this.send({ type: 'ping' });
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (this.onMessage) this.onMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        if (this.onDisconnect) this.onDisconnect();
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      this.attemptReconnect();
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
      return true;
    }
    return false;
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  // Game actions
  rollDice() {
    return this.send({
      type: 'game_action',
      data: { action_type: 'roll_dice' }
    });
  }

  buyProperty(propertyId) {
    return this.send({
      type: 'game_action',
      data: { action_type: 'buy_property', property_id: propertyId }
    });
  }

  declineProperty(propertyId) {
    return this.send({
      type: 'game_action',
      data: { action_type: 'decline_property', property_id: propertyId }
    });
  }

  endTurn() {
    return this.send({
      type: 'game_action',
      data: { action_type: 'end_turn' }
    });
  }
}

// Error handler wrapper
export const multiplayerApiCall = async (apiFunction, ...args) => {
  try {
    return await apiFunction(...args);
  } catch (error) {
    console.error('Multiplayer API call failed:', error);
    throw new Error(error.response?.data?.detail || error.message || 'API call failed');
  }
};