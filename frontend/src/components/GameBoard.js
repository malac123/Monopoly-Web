import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import PlayerPanel from './PlayerPanel';
import PropertyCard from './PropertyCard';
import DiceRoller from './DiceRoller';
import { Home, Car, Plane, Ship, AlertCircle } from 'lucide-react';
import { createGame, getProperties, rollDice, handlePropertyAction, endTurn, executeBotTurn, apiCall } from '../services/api';

const PLAYER_ICONS = [Home, Car, Plane, Ship];

const GameBoard = () => {
  const [gameState, setGameState] = useState(null);
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [gameMessage, setGameMessage] = useState("Starting new game...");
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  // Initialize game
  useEffect(() => {
    initializeGame();
  }, []);

  const initializeGame = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Create game and load properties
      const [gameResponse, propertiesData] = await Promise.all([
        apiCall(createGame, "You"),
        apiCall(getProperties)
      ]);

      if (gameResponse.success) {
        setGameState(gameResponse.game);
        setProperties(propertiesData);
        setGameMessage("Welcome to Monopoly! Roll the dice to start.");
      } else {
        throw new Error(gameResponse.error || 'Failed to create game');
      }
    } catch (err) {
      setError(err.message);
      setGameMessage("Failed to start game. Please refresh the page.");
    } finally {
      setIsLoading(false);
    }
  };

  const currentPlayer = gameState?.players[gameState.currentPlayerIndex];

  const handleDiceRoll = async () => {
    if (isProcessing || !gameState) return;
    
    try {
      setIsProcessing(true);
      setError(null);

      const response = await apiCall(rollDice, gameState.id);
      
      if (response.success) {
        setGameState(response.gameState);
        setGameMessage(response.message);
        
        // Handle next action
        if (response.nextAction === "handle_property") {
          // Find the property the player landed on
          const currentPlayer = response.gameState.players[response.gameState.currentPlayerIndex];
          const landedProperty = properties.find(p => p.id === currentPlayer.position + 1);
          
          if (landedProperty && landedProperty.type !== 'special' && landedProperty.owner === null) {
            setSelectedProperty(landedProperty);
          } else {
            // Auto end turn for special spaces or owned properties
            setTimeout(() => handleEndTurn(), 2000);
          }
        } else {
          setTimeout(() => handleEndTurn(), 2000);
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePropertyBuy = async () => {
    if (!selectedProperty || !gameState || !currentPlayer) return;
    
    try {
      setIsProcessing(true);
      const response = await apiCall(
        handlePropertyAction, 
        gameState.id, 
        "buy", 
        currentPlayer.id, 
        selectedProperty.id
      );
      
      if (response.success) {
        setGameState(response.gameState);
        setGameMessage(response.message);
        
        // Update property ownership in local state
        setProperties(prev => prev.map(prop => 
          prop.id === selectedProperty.id 
            ? { ...prop, owner: currentPlayer.id }
            : prop
        ));
      }
      
      setSelectedProperty(null);
      setTimeout(() => handleEndTurn(), 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePropertyDecline = async () => {
    if (!selectedProperty || !gameState || !currentPlayer) return;
    
    try {
      setIsProcessing(true);
      const response = await apiCall(
        handlePropertyAction, 
        gameState.id, 
        "decline", 
        currentPlayer.id, 
        selectedProperty.id
      );
      
      if (response.success) {
        setGameState(response.gameState);
        setGameMessage(response.message);
      }
      
      setSelectedProperty(null);
      setTimeout(() => handleEndTurn(), 1500);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleEndTurn = async () => {
    if (!gameState) return;
    
    try {
      const response = await apiCall(endTurn, gameState.id);
      
      if (response.success) {
        setGameState(response.gameState);
        setGameMessage(response.message);
        
        // If next player is a bot, execute bot turn
        if (response.nextAction === "bot_turn") {
          setTimeout(() => handleBotTurn(), 1500);
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleBotTurn = async () => {
    if (!gameState) return;
    
    try {
      setGameMessage(`${currentPlayer?.name} is thinking...`);
      const response = await apiCall(executeBotTurn, gameState.id);
      
      if (response.success) {
        setGameState(response.gameState);
        setGameMessage(response.message);
        
        // Update property ownership if bot bought something
        const updatedProperties = properties.map(prop => {
          const gameProperty = response.gameState.players
            .find(p => p.properties.includes(prop.id));
          return gameProperty ? { ...prop, owner: gameProperty.id } : prop;
        });
        setProperties(updatedProperties);
        
        setTimeout(() => handleEndTurn(), 2000);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const renderBoard = () => {
    if (!properties.length) return null;

    return (
      <div className="relative w-[600px] h-[600px] bg-gradient-to-br from-amber-50 to-yellow-100 border-8 border-amber-900 rounded-lg">
        {/* Center logo area */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-gradient-to-br from-amber-100 to-amber-200 border-4 border-amber-800 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-amber-900 mb-2">MONOPOLY</h2>
            <Badge variant="outline" className="bg-amber-50 text-amber-800 border-amber-600">
              Classic Edition
            </Badge>
          </div>
        </div>

        {/* Properties around the board */}
        {properties.map((property, index) => {
          const angle = (index / properties.length) * 2 * Math.PI;
          const radius = 240;
          const x = Math.cos(angle) * radius + 300;
          const y = Math.sin(angle) * radius + 300;
          
          return (
            <div
              key={property.id}
              className="absolute transform -translate-x-1/2 -translate-y-1/2"
              style={{ left: x, top: y }}
            >
              <Card className={`w-20 h-16 p-1 text-xs border-2 ${
                property.owner ? 'border-green-600 bg-green-50' : 'border-amber-700 bg-amber-50'
              } hover:scale-105 transition-transform cursor-pointer`}
                onClick={() => property.type !== 'special' && setSelectedProperty(property)}
              >
                <div className={`h-2 rounded-t ${property.color} mb-1`}></div>
                <div className="text-center font-semibold text-amber-900 leading-tight">
                  {property.name}
                </div>
                {property.price && (
                  <div className="text-center text-amber-700 text-[10px]">
                    ${property.price}
                  </div>
                )}
              </Card>

              {/* Player pieces on properties */}
              {gameState?.players.map((player, playerIndex) => {
                if (player.position === index) {
                  const PlayerIcon = PLAYER_ICONS[playerIndex];
                  return (
                    <div
                      key={player.id}
                      className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-white border-2 border-amber-800 flex items-center justify-center"
                    >
                      <PlayerIcon className="w-3 h-3 text-amber-800" />
                    </div>
                  );
                }
                return null;
              })}
            </div>
          );
        })}
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center">
        <Card className="p-8 bg-amber-50 border-amber-200">
          <div className="text-center space-y-4">
            <div className="w-8 h-8 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="text-amber-900 font-medium">Starting new Monopoly game...</p>
          </div>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center">
        <Card className="p-8 bg-red-50 border-red-200 max-w-md">
          <div className="text-center space-y-4">
            <AlertCircle className="w-12 h-12 text-red-600 mx-auto" />
            <h3 className="text-lg font-bold text-red-900">Game Error</h3>
            <p className="text-red-700">{error}</p>
            <Button 
              onClick={initializeGame}
              className="bg-red-600 hover:bg-red-700 text-white"
            >
              Try Again
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-amber-900 mb-2">Monopoly Classic</h1>
          <p className="text-amber-700">Single Player vs AI Opponents</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Game Board */}
          <div className="lg:col-span-2 flex justify-center">
            <div className="space-y-4">
              {renderBoard()}
              
              {/* Game Controls */}
              <Card className="p-4 bg-amber-50 border-amber-200">
                <div className="text-center space-y-3">
                  <p className="text-amber-900 font-medium">{gameMessage}</p>
                  
                  {!currentPlayer?.isBot && !isProcessing && !selectedProperty && (
                    <DiceRoller onRoll={handleDiceRoll} disabled={isProcessing} />
                  )}
                  
                  {currentPlayer?.isBot && !selectedProperty && (
                    <Badge variant="outline" className="bg-amber-100 text-amber-800">
                      {currentPlayer.name} is thinking...
                    </Badge>
                  )}

                  {isProcessing && (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
                      <span className="text-amber-700">Processing...</span>
                    </div>
                  )}
                </div>
              </Card>
            </div>
          </div>

          {/* Side Panel */}
          <div className="space-y-4">
            {gameState && (
              <PlayerPanel 
                players={gameState.players} 
                currentPlayerId={currentPlayer?.id}
                properties={properties}
              />
            )}
            
            {selectedProperty && currentPlayer && (
              <PropertyCard
                property={selectedProperty}
                currentPlayer={currentPlayer}
                onBuy={handlePropertyBuy}
                onDecline={handlePropertyDecline}
                disabled={isProcessing}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameBoard;