import React from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Crown, Bot, User, Home, Car, Plane, Ship } from 'lucide-react';

const PLAYER_ICONS = [Home, Car, Plane, Ship];
const DIFFICULTY_COLORS = {
  'Mentally slow': 'bg-green-100 text-green-800 border-green-300',
  'Medium rare': 'bg-yellow-100 text-yellow-800 border-yellow-300',
  'Highly proficient': 'bg-red-100 text-red-800 border-red-300'
};

const PlayerPanel = ({ players, currentPlayerId, properties }) => {
  const getPlayerProperties = (playerId) => {
    return properties.filter(prop => prop.owner === playerId);
  };

  const getNetWorth = (player) => {
    const propertyValue = getPlayerProperties(player.id).reduce((sum, prop) => sum + prop.price, 0);
    return player.money + propertyValue;
  };

  // Sort players by net worth for ranking
  const sortedPlayers = [...players].sort((a, b) => getNetWorth(b) - getNetWorth(a));

  return (
    <div className="space-y-4">
      <Card className="p-4 bg-amber-50 border-amber-200">
        <h3 className="text-lg font-bold text-amber-900 mb-3 flex items-center gap-2">
          <Crown className="w-5 h-5" />
          Player Rankings
        </h3>
        
        <div className="space-y-3">
          {sortedPlayers.map((player, index) => {
            const PlayerIcon = PLAYER_ICONS[players.indexOf(player)];
            const playerProperties = getPlayerProperties(player.id);
            const netWorth = getNetWorth(player);
            const isCurrentPlayer = player.id === currentPlayerId;
            
            return (
              <Card 
                key={player.id} 
                className={`p-3 transition-all ${
                  isCurrentPlayer 
                    ? 'bg-gradient-to-r from-amber-100 to-yellow-100 border-amber-400 shadow-md ring-2 ring-amber-300' 
                    : 'bg-white border-amber-200 hover:border-amber-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="relative">
                      <Avatar className="w-10 h-10 border-2 border-amber-700">
                        <AvatarFallback className="bg-amber-200 text-amber-900">
                          <PlayerIcon className="w-5 h-5" />
                        </AvatarFallback>
                      </Avatar>
                      
                      {index === 0 && (
                        <Crown className="absolute -top-2 -right-2 w-4 h-4 text-yellow-600" />
                      )}
                      
                      {isCurrentPlayer && (
                        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border border-white"></div>
                      )}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-amber-900">{player.name}</span>
                        {player.isBot ? (
                          <Bot className="w-4 h-4 text-amber-600" />
                        ) : (
                          <User className="w-4 h-4 text-amber-600" />
                        )}
                        {index === 0 && (
                          <Badge variant="outline" className="bg-yellow-100 text-yellow-800 border-yellow-400 text-xs">
                            Leader
                          </Badge>
                        )}
                      </div>
                      
                      {player.isBot && (
                        <Badge 
                          variant="outline" 
                          className={`text-xs ${DIFFICULTY_COLORS[player.difficulty] || 'bg-gray-100 text-gray-800'}`}
                        >
                          {player.difficulty}
                        </Badge>
                      )}
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-sm font-semibold text-amber-900">
                      #{index + 1}
                    </div>
                    <div className="text-xs text-amber-700">
                      Rank
                    </div>
                  </div>
                </div>
                
                <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
                  <div className="text-center p-2 bg-amber-100 rounded border border-amber-200">
                    <div className="font-semibold text-amber-900">${player.money}</div>
                    <div className="text-amber-700">Cash</div>
                  </div>
                  
                  <div className="text-center p-2 bg-amber-100 rounded border border-amber-200">
                    <div className="font-semibold text-amber-900">{playerProperties.length}</div>
                    <div className="text-amber-700">Properties</div>
                  </div>
                  
                  <div className="text-center p-2 bg-amber-100 rounded border border-amber-200">
                    <div className="font-semibold text-amber-900">${netWorth}</div>
                    <div className="text-amber-700">Net Worth</div>
                  </div>
                </div>
                
                {playerProperties.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs text-amber-700 mb-1">Owned Properties:</div>
                    <div className="flex flex-wrap gap-1">
                      {playerProperties.slice(0, 3).map(prop => (
                        <Badge 
                          key={prop.id} 
                          variant="outline" 
                          className="text-xs bg-green-50 text-green-800 border-green-300"
                        >
                          {prop.name}
                        </Badge>
                      ))}
                      {playerProperties.length > 3 && (
                        <Badge variant="outline" className="text-xs bg-amber-100 text-amber-800">
                          +{playerProperties.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>
                )}
              </Card>
            );
          })}
        </div>
        
        <div className="mt-4 pt-3 border-t border-amber-200">
          <div className="text-xs text-amber-700 text-center">
            Current Turn: <span className="font-semibold text-amber-900">
              {players.find(p => p.id === currentPlayerId)?.name}
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default PlayerPanel;