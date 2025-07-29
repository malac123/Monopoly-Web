import React from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Building, DollarSign, Home, ShoppingCart, X } from 'lucide-react';

const PropertyCard = ({ property, currentPlayer, onBuy, onDecline, disabled = false }) => {
  const canAfford = currentPlayer.money >= property.price;
  
  const getPropertyTypeIcon = (type) => {
    switch (type) {
      case 'property':
        return <Home className="w-5 h-5" />;
      case 'utility':
        return <Building className="w-5 h-5" />;
      case 'railroad':
        return <ShoppingCart className="w-5 h-5" />;
      default:
        return <Building className="w-5 h-5" />;
    }
  };

  const getPropertyTypeLabel = (type) => {
    switch (type) {
      case 'property':
        return 'Property';
      case 'utility':
        return 'Utility';
      case 'railroad':
        return 'Railroad';
      default:
        return 'Property';
    }
  };

  return (
    <Card className="p-4 bg-gradient-to-br from-amber-50 to-yellow-50 border-amber-300 shadow-lg">
      <div className="space-y-4">
        {/* Property Header */}
        <div className="text-center space-y-2">
          <div className={`h-8 rounded-lg ${property.color} border-2 border-amber-800 flex items-center justify-center`}>
            <span className="text-white font-bold text-sm drop-shadow">
              {property.name}
            </span>
          </div>
          
          <div className="flex items-center justify-center gap-2">
            {getPropertyTypeIcon(property.type)}
            <Badge variant="outline" className="bg-amber-100 text-amber-800 border-amber-400">
              {getPropertyTypeLabel(property.type)}
            </Badge>
          </div>
        </div>

        {/* Property Details */}
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div className="text-center p-3 bg-white rounded-lg border-2 border-amber-200">
              <DollarSign className="w-6 h-6 mx-auto text-green-600 mb-1" />
              <div className="text-lg font-bold text-amber-900">${property.price}</div>
              <div className="text-xs text-amber-700">Purchase Price</div>
            </div>
            
            <div className="text-center p-3 bg-white rounded-lg border-2 border-amber-200">
              <Home className="w-6 h-6 mx-auto text-blue-600 mb-1" />
              <div className="text-lg font-bold text-amber-900">${property.rent}</div>
              <div className="text-xs text-amber-700">Base Rent</div>
            </div>
          </div>

          {/* Property Description */}
          <div className="p-3 bg-white rounded-lg border border-amber-200">
            <div className="text-sm text-amber-800">
              <p className="mb-2">
                <strong>Location:</strong> {property.description || 'Prime real estate location'}
              </p>
              <p>
                <strong>Investment Value:</strong> {
                  property.price <= 100 ? 'Budget-friendly starter property' :
                  property.price <= 200 ? 'Moderate investment opportunity' :
                  'Premium high-value property'
                }
              </p>
            </div>
          </div>

          {/* Player Affordability */}
          <div className={`p-3 rounded-lg border-2 ${
            canAfford 
              ? 'bg-green-50 border-green-300' 
              : 'bg-red-50 border-red-300'
          }`}>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-semibold text-amber-900">
                  Your Cash: ${currentPlayer.money}
                </div>
                <div className="text-xs text-amber-700">
                  After Purchase: ${currentPlayer.money - property.price}
                </div>
              </div>
              
              <Badge 
                variant="outline" 
                className={canAfford 
                  ? 'bg-green-100 text-green-800 border-green-300' 
                  : 'bg-red-100 text-red-800 border-red-300'
                }
              >
                {canAfford ? 'Affordable' : 'Too Expensive'}
              </Badge>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3 pt-2">
          <Button
            onClick={onBuy}
            disabled={!canAfford || currentPlayer.isBot || disabled}
            className={`h-12 ${
              canAfford && !disabled
                ? 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800' 
                : 'bg-gray-400 cursor-not-allowed'
            } text-white font-semibold shadow-lg transition-all duration-200 hover:shadow-xl`}
          >
            {disabled ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Processing...
              </div>
            ) : (
              <>
                <ShoppingCart className="w-4 h-4 mr-2" />
                Buy Property
              </>
            )}
          </Button>
          
          <Button
            onClick={onDecline}
            disabled={currentPlayer.isBot || disabled}
            variant="outline"
            className="h-12 border-2 border-amber-400 text-amber-800 hover:bg-amber-100 font-semibold transition-all duration-200"
          >
            <X className="w-4 h-4 mr-2" />
            Pass
          </Button>
        </div>

        {currentPlayer.isBot && (
          <div className="text-center">
            <Badge variant="outline" className="bg-amber-100 text-amber-800 border-amber-400">
              {currentPlayer.name} is considering this property...
            </Badge>
          </div>
        )}
      </div>
    </Card>
  );
};

export default PropertyCard;