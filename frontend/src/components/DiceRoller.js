import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Dice1, Dice2, Dice3, Dice4, Dice5, Dice6, RotateCcw } from 'lucide-react';

const DICE_ICONS = [Dice1, Dice2, Dice3, Dice4, Dice5, Dice6];

const DiceRoller = ({ onRoll, disabled = false }) => {
  const [dice1, setDice1] = useState(1);
  const [dice2, setDice2] = useState(1);
  const [isRolling, setIsRolling] = useState(false);
  const [lastRoll, setLastRoll] = useState(null);

  const rollDice = () => {
    if (disabled || isRolling) return;

    setIsRolling(true);
    
    // Animate dice rolling
    const rollAnimation = setInterval(() => {
      setDice1(Math.floor(Math.random() * 6) + 1);
      setDice2(Math.floor(Math.random() * 6) + 1);
    }, 100);

    // Stop animation and set final values
    setTimeout(() => {
      clearInterval(rollAnimation);
      
      const finalDice1 = Math.floor(Math.random() * 6) + 1;
      const finalDice2 = Math.floor(Math.random() * 6) + 1;
      const total = finalDice1 + finalDice2;
      
      setDice1(finalDice1);
      setDice2(finalDice2);
      setLastRoll({ dice1: finalDice1, dice2: finalDice2, total });
      setIsRolling(false);
      
      onRoll(total);
    }, 1500);
  };

  const Dice1Icon = DICE_ICONS[dice1 - 1];
  const Dice2Icon = DICE_ICONS[dice2 - 1];

  return (
    <div className="space-y-4">
      {/* Dice Display */}
      <Card className="p-6 bg-gradient-to-br from-white to-amber-50 border-2 border-amber-300 shadow-lg">
        <div className="flex items-center justify-center gap-6">
          <div className={`transform transition-transform duration-150 ${
            isRolling ? 'animate-spin' : 'hover:scale-110'
          }`}>
            <div className="w-16 h-16 bg-white border-3 border-amber-800 rounded-lg shadow-lg flex items-center justify-center">
              <Dice1Icon className="w-10 h-10 text-amber-900" />
            </div>
          </div>
          
          <div className="text-3xl font-bold text-amber-900 animate-pulse">
            +
          </div>
          
          <div className={`transform transition-transform duration-150 ${
            isRolling ? 'animate-spin' : 'hover:scale-110'
          }`}>
            <div className="w-16 h-16 bg-white border-3 border-amber-800 rounded-lg shadow-lg flex items-center justify-center">
              <Dice2Icon className="w-10 h-10 text-amber-900" />
            </div>
          </div>
        </div>
        
        {/* Total Display */}
        <div className="text-center mt-4">
          <div className="text-2xl font-bold text-amber-900">
            Total: {dice1 + dice2}
          </div>
          {lastRoll && !isRolling && (
            <div className="text-sm text-amber-700 mt-1">
              Last Roll: {lastRoll.dice1} + {lastRoll.dice2} = {lastRoll.total}
            </div>
          )}
        </div>
      </Card>

      {/* Roll Button */}
      <div className="text-center">
        <Button
          onClick={rollDice}
          disabled={disabled || isRolling}
          className={`h-14 px-8 text-lg font-semibold shadow-lg transition-all duration-200 ${
            isRolling
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-700 hover:to-yellow-700 hover:shadow-xl transform hover:scale-105'
          } text-white`}
        >
          {isRolling ? (
            <div className="flex items-center gap-2">
              <RotateCcw className="w-5 h-5 animate-spin" />
              Rolling...
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Dice1 className="w-5 h-5" />
              Roll Dice
            </div>
          )}
        </Button>
        
        <div className="text-xs text-amber-700 mt-2">
          Click to roll both dice and move your piece
        </div>
      </div>

      {/* Rolling Animation Text */}
      {isRolling && (
        <div className="text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-100 border border-amber-300 rounded-full">
            <div className="w-2 h-2 bg-amber-600 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-amber-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <span className="text-amber-800 font-medium ml-2">Rolling dice...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default DiceRoller;