import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Users, Bot, Wifi, WifiOff } from 'lucide-react';

const GameModeSelector = ({ onModeSelect }) => {
  const [joinCode, setJoinCode] = useState('');
  const [playerName, setPlayerName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSinglePlayer = () => {
    onModeSelect('single-player');
  };

  const handleCreateMultiplayer = () => {
    if (!playerName.trim()) {
      alert('Please enter your name first');
      return;
    }
    onModeSelect('create-multiplayer', { playerName: playerName.trim() });
  };

  const handleJoinMultiplayer = () => {
    if (!playerName.trim() || !joinCode.trim()) {
      alert('Please enter both your name and room code');
      return;
    }
    onModeSelect('join-multiplayer', { 
      playerName: playerName.trim(), 
      roomCode: joinCode.trim().toUpperCase() 
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-amber-900 mb-4">Monopoly Classic</h1>
          <p className="text-xl text-amber-700 mb-2">Choose Your Game Mode</p>
          <Badge variant="outline" className="bg-amber-100 text-amber-800 border-amber-400">
            Single Player & Multiplayer Available
          </Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Single Player Mode */}
          <Card className="p-6 bg-gradient-to-br from-amber-50 to-yellow-50 border-amber-300 hover:shadow-lg transition-all duration-200">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-amber-200 rounded-full flex items-center justify-center mx-auto">
                <Bot className="w-8 h-8 text-amber-800" />
              </div>
              
              <h3 className="text-xl font-bold text-amber-900">Single Player</h3>
              <p className="text-amber-700 text-sm">
                Play against 3 AI opponents with different difficulty levels
              </p>
              
              <div className="space-y-2">
                <Badge variant="outline" className="bg-green-100 text-green-800 text-xs">
                  Mentally Slow AI
                </Badge>
                <Badge variant="outline" className="bg-yellow-100 text-yellow-800 text-xs">
                  Medium Rare AI
                </Badge>
                <Badge variant="outline" className="bg-red-100 text-red-800 text-xs">
                  Highly Proficient AI
                </Badge>
              </div>

              <Button 
                onClick={handleSinglePlayer}
                className="w-full bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-700 hover:to-yellow-700 text-white font-semibold"
                disabled={isLoading}
              >
                <Bot className="w-4 h-4 mr-2" />
                Play Solo
              </Button>
            </div>
          </Card>

          {/* Create Multiplayer Room */}
          <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-300 hover:shadow-lg transition-all duration-200">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-blue-200 rounded-full flex items-center justify-center mx-auto">
                <Wifi className="w-8 h-8 text-blue-800" />
              </div>
              
              <h3 className="text-xl font-bold text-blue-900">Create Room</h3>
              <p className="text-blue-700 text-sm">
                Host a game and invite up to 3 friends with a room code
              </p>
              
              <div className="space-y-3">
                <Input
                  placeholder="Enter your name"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  className="border-blue-300 focus:border-blue-500"
                  maxLength={20}
                />
                
                <div className="text-xs text-blue-600 space-y-1">
                  <p>• 2-4 players supported</p>
                  <p>• Host controls game settings</p>
                  <p>• Optional AI bots to fill slots</p>
                </div>
              </div>

              <Button 
                onClick={handleCreateMultiplayer}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold"
                disabled={isLoading || !playerName.trim()}
              >
                <Users className="w-4 h-4 mr-2" />
                Create Room
              </Button>
            </div>
          </Card>

          {/* Join Multiplayer Room */}
          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-green-300 hover:shadow-lg transition-all duration-200">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-green-200 rounded-full flex items-center justify-center mx-auto">
                <WifiOff className="w-8 h-8 text-green-800" />
              </div>
              
              <h3 className="text-xl font-bold text-green-900">Join Room</h3>
              <p className="text-green-700 text-sm">
                Join a friend's game using their room code
              </p>
              
              <div className="space-y-3">
                <Input
                  placeholder="Enter your name"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  className="border-green-300 focus:border-green-500"
                  maxLength={20}
                />
                
                <Input
                  placeholder="Enter room code (e.g., 2FG-8JH)"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                  className="border-green-300 focus:border-green-500 font-mono text-center"
                  maxLength={7}
                />
                
                <div className="text-xs text-green-600">
                  <p>Room codes are 6 characters like: ABC-123</p>
                </div>
              </div>

              <Button 
                onClick={handleJoinMultiplayer}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold"
                disabled={isLoading || !playerName.trim() || !joinCode.trim()}
              >
                <Users className="w-4 h-4 mr-2" />
                Join Room
              </Button>
            </div>
          </Card>
        </div>

        <div className="mt-8 text-center">
          <p className="text-amber-600 text-sm">
            🎲 Classic Monopoly rules • Real-time multiplayer • Cross-platform compatible
          </p>
        </div>
      </div>
    </div>
  );
};

export default GameModeSelector;