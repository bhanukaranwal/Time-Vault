import React from 'react';

interface PlayerDashboardProps {
  stats: {
    wins?: number;
    total_bet?: number;
    total_won?: number;
  };
}

const PlayerDashboard: React.FC<PlayerDashboardProps> = ({ stats }) => {
  const { wins = 0, total_bet = 0, total_won = 0 } = stats;
  const profit = total_won - total_bet;
  const winRate = total_bet > 0 ? (wins / (total_bet / 10)) * 100 : 0; // Simplified win rate

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4 text-yellow-400">My Stats</h3>
      <ul className="space-y-2 text-sm">
        <li className="flex justify-between"><span>Total Wins:</span> <span className="font-mono">{wins}</span></li>
        <li className="flex justify-between"><span>Total Wagered:</span> <span className="font-mono">${total_bet.toFixed(2)}</span></li>
        <li className="flex justify-between"><span>Total Won:</span> <span className="font-mono">${total_won.toFixed(2)}</span></li>
        <li className="flex justify-between"><span>Profit:</span> <span className={`font-mono ${profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>${profit.toFixed(2)}</span></li>
      </ul>
    </div>
  );
};

export default PlayerDashboard;