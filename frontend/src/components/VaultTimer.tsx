import React from 'react';
import Lottie from 'lottie-react';
import vaultAnimation from '../assets/vault.json'; // Placeholder for Lottie animation

interface VaultTimerProps {
  gameState: any;
  result: any;
}

const VaultTimer: React.FC<VaultTimerProps> = ({ gameState, result }) => {
  const getStatusText = () => {
    if (result) {
      return `Vault Unlocked at ${result.unlock_second}s!`;
    }
    if (gameState) {
      switch (gameState.status) {
        case 'betting':
          return 'Betting is Open!';
        case 'running':
          return 'Vault is ticking...';
        default:
          return 'Waiting for next round...';
      }
    }
    return 'Connecting to game...';
  };

  return (
    <div className="w-full bg-gray-800 p-6 rounded-lg shadow-lg text-center mb-4">
      <div className="relative w-64 h-64 mx-auto">
        <Lottie animationData={vaultAnimation} loop={true} />
        {result && (
          <div className="absolute inset-0 flex items-center justify-center text-6xl font-bold text-green-400">
            {result.unlock_second}
          </div>
        )}
      </div>
      <h2 className="text-3xl font-bold mt-4">{getStatusText()}</h2>
      {gameState?.status === 'betting' && (
        <p className="text-yellow-400">Place your bets now!</p>
      )}
    </div>
  );
};

export default VaultTimer;