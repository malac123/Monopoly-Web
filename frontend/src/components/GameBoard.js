import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import PlayerPanel from './PlayerPanel';
import PropertyCard from './PropertyCard';
import DiceRoller from './DiceRoller';
import { mockGameData, botDecisionEngine } from '../mock';
import { Home, Car, Plane, Ship } from 'lucide-react';

const PLAYER_ICONS = [Home, Car, Plane, Ship];

const GameBoard = () => {
  const [gameState, setGameState] = useState(mockGameData.initialGameState);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [gameMessage, setGameMessage] = useState("Welcome to Monopoly! Roll the dice to start.");
  const [isRolling, setIsRolling] = useState(false);

  const currentPlayer = gameState.players[gameState.currentPlayerIndex];

  const movePlayer = (playerId, steps) => {
    setGameState(prev => {
      const newState = { ...prev };
      const player = newState.players.find(p => p.id === playerId);
      const newPosition = (player.position + steps) % mockGameData.properties.length;
      
      // Pass GO bonus
      if (newPosition < player.position) {
        player.money += 200;
        setGameMessage(`${player.name} passed GO! Collected $200`);
      }
      
      player.position = newPosition;
      return newState;
    });
  };

  const handleDiceRoll = (diceValue) => {
    if (isRolling) return;
    
    setIsRolling(true);
    movePlayer(currentPlayer.id, diceValue);
    
    setTimeout(() => {
      const property = mockGameData.properties[gameState.players[gameState.currentPlayerIndex].position];
      handleLandOnProperty(property);
      setIsRolling(false);
    }, 1000);
  };

  const handleLandOnProperty = (property) => {
    if (property.type === 'special') {
      setGameMessage(`${currentPlayer.name} landed on ${property.name}`);
      endTurn();
      return;
    }

    if (property.owner === null) {
      setGameMessage(`${currentPlayer.name} can buy ${property.name} for $${property.price}`);
      setSelectedProperty(property);
    } else if (property.owner !== currentPlayer.id) {
      const rent = property.rent;
      payRent(currentPlayer.id, property.owner, rent);
      setGameMessage(`${currentPlayer.name} paid $${rent} rent to ${gameState.players.find(p => p.id === property.owner)?.name}`);
      setTimeout(endTurn, 2000);
    } else {
      setGameMessage(`${currentPlayer.name} owns this property`);
      setTimeout(endTurn, 1500);
    }
  };

  const buyProperty = (propertyId) => {
    setGameState(prev => {
      const newState = { ...prev };
      const property = mockGameData.properties.find(p => p.id === propertyId);
      const player = newState.players.find(p => p.id === currentPlayer.id);
      
      if (player.money >= property.price) {
        player.money -= property.price;
        property.owner = player.id;
        player.properties.push(propertyId);
        setGameMessage(`${player.name} bought ${property.name} for $${property.price}`);
      }
      
      return newState;
    });
    setSelectedProperty(null);
    setTimeout(endTurn, 2000);
  };

  const payRent = (payerId, receiverId, amount) => {
    setGameState(prev => {
      const newState = { ...prev };
      const payer = newState.players.find(p => p.id === payerId);
      const receiver = newState.players.find(p => p.id === receiverId);
      
      payer.money -= amount;
      receiver.money += amount;
      
      return newState;
    });
  };

  const endTurn = () => {
    setGameState(prev => ({
      ...prev,
      currentPlayerIndex: (prev.currentPlayerIndex + 1) % prev.players.length
    }));
    setSelectedProperty(null);
  };

  // Bot AI Turn
  useEffect(() => {
    if (currentPlayer.isBot && !isRolling && !selectedProperty) {
      const timer = setTimeout(() => {
        const diceValue = Math.floor(Math.random() * 6) + Math.floor(Math.random() * 6) + 2;
        handleDiceRoll(diceValue);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [currentPlayer, isRolling, selectedProperty]);

  // Bot property decisions
  useEffect(() => {
    if (currentPlayer.isBot && selectedProperty) {
      const timer = setTimeout(() => {
        const decision = botDecisionEngine(currentPlayer, selectedProperty);
        if (decision.action === 'buy') {
          buyProperty(selectedProperty.id);
        } else {
          setGameMessage(`${currentPlayer.name} declined to buy ${selectedProperty.name}`);
          setSelectedProperty(null);
          setTimeout(endTurn, 1500);
        }
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [currentPlayer, selectedProperty]);

  const renderBoard = () => {
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
        {mockGameData.properties.map((property, index) => {
          const angle = (index / mockGameData.properties.length) * 2 * Math.PI;
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
              {gameState.players.map((player, playerIndex) => {
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
                  
                  {!currentPlayer.isBot && !isRolling && !selectedProperty && (
                    <DiceRoller onRoll={handleDiceRoll} disabled={isRolling} />
                  )}
                  
                  {currentPlayer.isBot && !selectedProperty && (
                    <Badge variant="outline" className="bg-amber-100 text-amber-800">
                      {currentPlayer.name} is thinking...
                    </Badge>
                  )}
                </div>
              </Card>
            </div>
          </div>

          {/* Side Panel */}
          <div className="space-y-4">
            <PlayerPanel 
              players={gameState.players} 
              currentPlayerId={currentPlayer.id}
              properties={mockGameData.properties}
            />
            
            {selectedProperty && (
              <PropertyCard
                property={selectedProperty}
                currentPlayer={currentPlayer}
                onBuy={() => buyProperty(selectedProperty.id)}
                onDecline={() => {
                  setSelectedProperty(null);
                  endTurn();
                }}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameBoard;