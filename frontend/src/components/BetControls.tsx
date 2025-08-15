import React, { useState } from 'react';
import { placeBet } from '../api';

interface BetControlsProps {
  selectedSecond: number;
  disabled: boolean;
  onBetPlaced: (newStats: any) => void;
}

const BetControls: React.FC<BetControlsProps> = ({ selectedSecond, disabled, onBetPlaced }) => {
  const [amount, setAmount] = useState(10);
  const [usePowerUp, setUsePowerUp] = useState(false);
  const [isPlacingBet, setIsPlacingBet] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const handlePlaceBet = async () => {
    if (disabled || isPlacingBet) return;
    
    setIsPlacingBet(true);
    setFeedback(null);
    
    try {
      const response: any = await placeBet({
        second: selectedSecond,
        amount,
        ...(usePowerUp && { power_up: 'multiplier_boost' }),
      });
      setFeedback({ type: 'success', message: response.message });
      onBetPlaced(response.stats);
      setUsePowerUp(false);
    } catch (error: any) {
      setFeedback({ type: 'error', message: error.toString() });
    } finally {
      setIsPlacingBet(false);
      setTimeout(() => setFeedback(null), 3000);
    }
  };

  const isButtonDisabled = disabled || isPlacingBet;

  return (
    <div className="w-full bg-gray-800 p-4 rounded-lg shadow-lg mt-4 flex flex-col items-center gap-4">
      <div className="flex items-end justify-center gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300">Amount</label>
          <input type="number" value={amount} onChange={(e) => setAmount(Math.max(0, Number(e.target.value)))} className="bg-gray-700 p-2 rounded w-24 text-center" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300">Selected Second</label>
          <input type="number" value={selectedSecond} readOnly className="bg-gray-600 p-2 rounded w-24 text-center" />
        </div>
        <button
          onClick={() => setUsePowerUp(!usePowerUp)}
          disabled={isButtonDisabled}
          className={`px-4 py-2 font-bold rounded border-2 transition-all ${
            usePowerUp ? 'bg-purple-500 border-purple-300' : 'bg-gray-700 border-gray-600'
          } ${isButtonDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          title="Use 1.5x Multiplier Boost"
        >
          Boost
        </button>
        <button
          onClick={handlePlaceBet}
          disabled={isButtonDisabled}
          className={`px-6 py-2 font-bold rounded w-32 transition-colors ${
            isButtonDisabled ? 'bg-gray-600 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600'
          }`}
        >
          {isPlacingBet ? 'Placing...' : 'Place Bet'}
        </button>
      </div>
      {feedback && <div className={`mt-2 text-sm font-semibold ${feedback.type === 'success' ? 'text-green-400' : 'text-red-400'}`}>{feedback.message}</div>}
    </div>
  );
};

export default BetControls;