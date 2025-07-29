import React, { useState, useEffect } from 'react';
import GameBoard from "./components/GameBoard";
import GameModeSelector from "./components/GameModeSelector";
import MultiplayerLobby from "./components/MultiplayerLobby";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { 
  createRoom, 
  joinRoom, 
  startGame, 
  updateRoomSettings, 
  MultiplayerWebSocket,
  multiplayerApiCall 
} from './services/multiplayerApi';

function App() {
  const [gameMode, setGameMode] = useState('menu'); // 'menu', 'single-player', 'multiplayer-lobby', 'multiplayer-game'
  const [currentRoom, setCurrentRoom] = useState(null);
  const [currentPlayerId, setCurrentPlayerId] = useState(null);
  const [websocket, setWebsocket] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [error, setError] = useState(null);

  // Handle game mode selection
  const handleModeSelect = async (mode, data) => {
    setError(null);
    
    try {
      if (mode === 'single-player') {
        setGameMode('single-player');
      }
      
      else if (mode === 'create-multiplayer') {
        const response = await multiplayerApiCall(createRoom, data.playerName);
        if (response.success) {
          setCurrentRoom(response.room);
          setCurrentPlayerId(response.room.host_id);
          setGameMode('multiplayer-lobby');
          
          // Connect WebSocket
          connectWebSocket(response.room.id, response.room.host_id);
        } else {
          throw new Error(response.error || 'Failed to create room');
        }
      }
      
      else if (mode === 'join-multiplayer') {
        const response = await multiplayerApiCall(joinRoom, data.roomCode, data.playerName);
        if (response.success) {
          setCurrentRoom(response.room);
          setCurrentPlayerId(response.player_id);
          setGameMode('multiplayer-lobby');
          
          // Connect WebSocket
          connectWebSocket(response.room.id, response.player_id);
        } else {
          throw new Error(response.error || 'Failed to join room');
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // WebSocket connection
  const connectWebSocket = (roomCode, playerId) => {
    if (websocket) {
      websocket.disconnect();
    }

    const ws = new MultiplayerWebSocket(
      roomCode,
      playerId,
      handleWebSocketMessage,
      () => setConnectionStatus('connected'),
      () => setConnectionStatus('disconnected')
    );

    ws.connect();
    setWebsocket(ws);
  };

  // Handle WebSocket messages
  const handleWebSocketMessage = (message) => {
    console.log('WebSocket message:', message);
    
    switch (message.type) {
      case 'player_joined':
      case 'player_left':
      case 'settings_updated':
        setCurrentRoom(message.room);
        break;
        
      case 'game_started':
        setCurrentRoom(message.room);
        setGameMode('multiplayer-game');
        break;
        
      case 'game_update':
        // Handle real-time game updates
        break;
        
      case 'error':
        setError(message.message);
        break;
        
      default:
        console.log('Unknown message type:', message.type);
    }
  };

  // Start multiplayer game
  const handleStartGame = async () => {
    if (!currentRoom || !currentPlayerId) return;
    
    try {
      const response = await multiplayerApiCall(startGame, currentRoom.id, currentPlayerId);
      if (response.success) {
        // WebSocket will handle the game_started message
      } else {
        throw new Error(response.error || 'Failed to start game');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // Update room settings
  const handleUpdateSettings = async (settings) => {
    if (!currentRoom || !currentPlayerId) return;
    
    try {
      await multiplayerApiCall(updateRoomSettings, currentRoom.id, settings, currentPlayerId);
      // WebSocket will handle the settings_updated message
    } catch (err) {
      setError(err.message);
    }
  };

  // Leave room and return to menu
  const handleLeaveRoom = () => {
    if (websocket) {
      websocket.disconnect();
      setWebsocket(null);
    }
    
    setCurrentRoom(null);
    setCurrentPlayerId(null);
    setConnectionStatus('disconnected');
    setGameMode('menu');
    setError(null);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (websocket) {
        websocket.disconnect();
      }
    };
  }, [websocket]);

  // Error display component
  const ErrorMessage = ({ error, onDismiss }) => {
    if (!error) return null;
    
    return (
      <div className="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-lg z-50">
        <div className="flex items-center justify-between">
          <span>{error}</span>
          <button 
            onClick={onDismiss}
            className="ml-4 text-red-500 hover:text-red-700"
          >
            ×
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={
            <>
              <ErrorMessage error={error} onDismiss={() => setError(null)} />
              
              {gameMode === 'menu' && (
                <GameModeSelector onModeSelect={handleModeSelect} />
              )}
              
              {gameMode === 'single-player' && (
                <GameBoard />
              )}
              
              {gameMode === 'multiplayer-lobby' && (
                <MultiplayerLobby
                  room={currentRoom}
                  currentPlayerId={currentPlayerId}
                  onStartGame={handleStartGame}
                  onUpdateSettings={handleUpdateSettings}
                  onLeaveRoom={handleLeaveRoom}
                  isConnected={connectionStatus === 'connected'}
                />
              )}
              
              {gameMode === 'multiplayer-game' && (
                <GameBoard 
                  isMultiplayer={true}
                  room={currentRoom}
                  playerId={currentPlayerId}
                  websocket={websocket}
                />
              )}
            </>
          } />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;