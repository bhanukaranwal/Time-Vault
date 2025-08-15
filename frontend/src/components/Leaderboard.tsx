import React from 'react';

interface LeaderboardProps {
  data: { [key: string]: number };
}

const Leaderboard: React.FC<LeaderboardProps> = ({ data }) => {
  const sortedPlayers = Object.entries(data).sort(([, a], [, b]) => b - a);

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4 text-yellow-400">Leaderboard</h3>
      <ul>
        {sortedPlayers.map(([player, score], index) => (
          <li key={player} className="flex justify-between items-center mb-2 p-2 bg-gray-700 rounded">
            <span>{index + 1}. {player}</span>
            <span className="font-bold text-green-400">${score.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;