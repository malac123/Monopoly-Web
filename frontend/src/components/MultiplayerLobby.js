import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { 
  Users, Settings, Play, Copy, Check, Crown, 
  DollarSign, Clock, Bot, AlertCircle, Wifi, WifiOff
} from 'lucide-react';

const MultiplayerLobby = ({ 
  room, 
  currentPlayerId, 
  onStartGame, 
  onUpdateSettings, 
  onLeaveRoom,
  isConnected = true 
}) => {
  const [settings, setSettings] = useState(room?.settings || {
    starting_money: 1500,
    max_players: 4,
    include_bots: false,
    bot_count: 0,
    game_speed: "normal",
    property_price_multiplier: 1.0,
    rent_multiplier: 1.0,
    pass_go_bonus: 200
  });
  const [copied, setCopied] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const isHost = room?.host_id === currentPlayerId;
  const connectedPlayers = room?.players?.filter(p => p.is_connected) || [];
  const canStart = connectedPlayers.length >= 2;

  useEffect(() => {
    if (room?.settings) {
      setSettings(room.settings);
    }
  }, [room?.settings]);

  const copyRoomCode = async () => {
    try {
      await navigator.clipboard.writeText(room.id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Fallback for browsers that don't support clipboard API
      const textArea = document.createElement('textarea');
      textArea.value = room.id;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleSettingsChange = (key, value) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    if (isHost && onUpdateSettings) {
      onUpdateSettings(newSettings);
    }
  };

  const handleStartGame = () => {
    if (canStart && onStartGame) {
      onStartGame();
    }
  };

  if (!room) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center">
        <Card className="p-8 bg-red-50 border-red-200">
          <div className="text-center space-y-4">
            <AlertCircle className="w-12 h-12 text-red-600 mx-auto" />
            <h3 className="text-lg font-bold text-red-900">Room Not Found</h3>
            <p className="text-red-700">The room you're looking for doesn't exist or has expired.</p>
            <Button onClick={onLeaveRoom} variant="outline" className="border-red-400 text-red-700">
              Back to Menu
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-amber-900 mb-2">Monopoly Lobby</h1>
          <div className="flex items-center justify-center gap-4">
            <Badge variant="outline" className="bg-amber-100 text-amber-800 border-amber-400">
              Room: {room.id}
            </Badge>
            <Button
              onClick={copyRoomCode}
              variant="outline"
              size="sm"
              className="border-amber-400 text-amber-800 hover:bg-amber-100"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 mr-1" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-1" />
                  Copy Code
                </>
              )}
            </Button>
            <Badge 
              variant="outline" 
              className={isConnected ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}
            >
              {isConnected ? (
                <>
                  <Wifi className="w-3 h-3 mr-1" />
                  Connected
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3 mr-1" />
                  Disconnected
                </>
              )}
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Players Panel */}
          <div className="lg:col-span-2 space-y-4">
            <Card className="p-6 bg-amber-50 border-amber-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-amber-900 flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  Players ({connectedPlayers.length}/{room.max_players})
                </h3>
                {!canStart && (
                  <Badge variant="outline" className="bg-yellow-100 text-yellow-800">
                    Need {2 - connectedPlayers.length} more player(s)
                  </Badge>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {room.players.map((player, index) => (
                  <Card 
                    key={player.id} 
                    className={`p-4 ${
                      player.is_connected 
                        ? 'bg-white border-amber-200' 
                        : 'bg-gray-100 border-gray-300 opacity-60'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-amber-200 rounded-full flex items-center justify-center">
                        <span className="text-amber-800 font-bold">
                          {player.name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-amber-900">
                            {player.name}
                          </span>
                          {player.is_host && (
                            <Crown className="w-4 h-4 text-yellow-600" />
                          )}
                          {player.id === currentPlayerId && (
                            <Badge variant="outline" className="bg-blue-100 text-blue-800 text-xs">
                              You
                            </Badge>
                          )}
                        </div>
                        <div className="text-xs text-amber-700">
                          {player.is_connected ? 'Connected' : 'Disconnected'}
                        </div>
                      </div>
                    </div>
                  </Card>
                ))}

                {/* Empty Slots */}
                {Array.from({ length: room.max_players - room.players.length }, (_, index) => (
                  <Card key={`empty-${index}`} className="p-4 bg-gray-50 border-gray-200 border-dashed">
                    <div className="flex items-center justify-center h-16 text-gray-500">
                      <Users className="w-6 h-6 mr-2" />
                      <span>Waiting for player...</span>
                    </div>
                  </Card>
                ))}
              </div>

              {/* Bot Fill Option */}
              {isHost && room.players.length < 4 && (
                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-blue-900 font-medium">Fill with AI Bots</Label>
                      <p className="text-xs text-blue-700 mt-1">
                        Add AI players to fill remaining slots
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch
                        checked={settings.include_bots}
                        onCheckedChange={(checked) => handleSettingsChange('include_bots', checked)}
                      />
                      <Bot className="w-4 h-4 text-blue-600" />
                    </div>
                  </div>
                  
                  {settings.include_bots && (
                    <div className="mt-3">
                      <Label className="text-sm text-blue-800">Number of Bots:</Label>
                      <Input
                        type="number"
                        min="1"
                        max={4 - room.players.length}
                        value={settings.bot_count}
                        onChange={(e) => handleSettingsChange('bot_count', parseInt(e.target.value) || 0)}
                        className="w-20 mt-1 border-blue-300"
                      />
                    </div>
                  )}
                </div>
              )}
            </Card>

            {/* Game Settings */}
            {isHost && (
              <Card className="p-6 bg-amber-50 border-amber-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-amber-900 flex items-center gap-2">
                    <Settings className="w-5 h-5" />
                    Game Settings
                  </h3>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowSettings(!showSettings)}
                    className="border-amber-400 text-amber-800"
                  >
                    {showSettings ? 'Hide' : 'Show'} Settings
                  </Button>
                </div>

                {showSettings && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label className="text-amber-900 font-medium">Starting Money</Label>
                        <div className="flex items-center space-x-2 mt-1">
                          <DollarSign className="w-4 h-4 text-green-600" />
                          <Input
                            type="number"
                            min="500"
                            max="5000"
                            step="100"
                            value={settings.starting_money}
                            onChange={(e) => handleSettingsChange('starting_money', parseInt(e.target.value) || 1500)}
                            className="border-amber-300"
                          />
                        </div>
                      </div>

                      <div>
                        <Label className="text-amber-900 font-medium">Game Speed</Label>
                        <div className="flex items-center space-x-2 mt-1">
                          <Clock className="w-4 h-4 text-blue-600" />
                          <select
                            value={settings.game_speed}
                            onChange={(e) => handleSettingsChange('game_speed', e.target.value)}
                            className="flex h-10 w-full rounded-md border border-amber-300 bg-background px-3 py-2 text-sm"
                          >
                            <option value="slow">Slow</option>
                            <option value="normal">Normal</option>
                            <option value="fast">Fast</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <Label className="text-amber-900 font-medium">Property Price Multiplier</Label>
                        <Input
                          type="number"
                          min="0.5"
                          max="2.0"
                          step="0.1"
                          value={settings.property_price_multiplier}
                          onChange={(e) => handleSettingsChange('property_price_multiplier', parseFloat(e.target.value) || 1.0)}
                          className="mt-1 border-amber-300"
                        />
                      </div>

                      <div>
                        <Label className="text-amber-900 font-medium">Rent Multiplier</Label>
                        <Input
                          type="number"
                          min="0.5"
                          max="2.0"
                          step="0.1"
                          value={settings.rent_multiplier}
                          onChange={(e) => handleSettingsChange('rent_multiplier', parseFloat(e.target.value) || 1.0)}
                          className="mt-1 border-amber-300"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </Card>
            )}
          </div>

          {/* Actions Panel */}
          <div className="space-y-4">
            {/* Start Game */}
            {isHost && (
              <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-green-300">
                <div className="text-center space-y-4">
                  <h3 className="text-lg font-bold text-green-900">Ready to Start?</h3>
                  
                  {canStart ? (
                    <div className="space-y-3">
                      <p className="text-sm text-green-700">
                        All players connected and ready!
                      </p>
                      <Button
                        onClick={handleStartGame}
                        className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold h-12"
                      >
                        <Play className="w-5 h-5 mr-2" />
                        Start Game
                      </Button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <p className="text-sm text-amber-700">
                        Waiting for more players...
                      </p>
                      <Button
                        disabled
                        className="w-full bg-gray-400 text-white h-12 cursor-not-allowed"
                      >
                        <Users className="w-5 h-5 mr-2" />
                        Need {2 - connectedPlayers.length} More Player(s)
                      </Button>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {/* Share Room Code */}
            <Card className="p-6 bg-amber-50 border-amber-200">
              <div className="text-center space-y-4">
                <h3 className="text-lg font-bold text-amber-900">Invite Friends</h3>
                <div className="p-4 bg-white border-2 border-amber-300 rounded-lg">
                  <p className="text-sm text-amber-700 mb-2">Room Code:</p>
                  <p className="text-2xl font-mono font-bold text-amber-900">{room.id}</p>
                </div>
                <Button
                  onClick={copyRoomCode}
                  variant="outline"
                  className="w-full border-amber-400 text-amber-800 hover:bg-amber-100"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4 mr-2" />
                      Copied to Clipboard!
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4 mr-2" />
                      Copy Room Code
                    </>
                  )}
                </Button>
              </div>
            </Card>

            {/* Leave Room */}
            <Card className="p-6 bg-red-50 border-red-200">
              <div className="text-center space-y-4">
                <h3 className="text-lg font-bold text-red-900">Leave Room</h3>
                <p className="text-sm text-red-700">
                  Exit this lobby and return to main menu
                </p>
                <Button
                  onClick={onLeaveRoom}
                  variant="outline"
                  className="w-full border-red-400 text-red-700 hover:bg-red-100"
                >
                  Leave Room
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MultiplayerLobby;