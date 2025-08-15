import React from 'react';

interface BetTimelineProps {
  selectedSecond: number;
  onSecondSelect: (second: number) => void;
  liveBets: { [key: number]: number };
}

const BetTimeline: React.FC<BetTimelineProps> = ({ selectedSecond, onSecondSelect, liveBets }) => {
  const seconds = Array.from({ length: 171 }, (_, i) => i + 10);
  const maxBet = Math.max(1, ...Object.values(liveBets)); // Avoid division by zero

  return (
    <div className="w-full bg-gray-800 p-4 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-2 text-center">Betting Timeline (10s - 180s)</h3>
      <div className="grid grid-cols-10 gap-1">
        {seconds.map((sec) => {
          const betAmount = liveBets[sec] || 0;
          const heat = Math.min(1, betAmount / maxBet); // Normalize heat from 0 to 1
          const bgColor = `rgba(234, 179, 8, ${heat})`; // Yellow with opacity based on heat
          
          return (
            <button
              key={sec}
              onClick={() => onSecondSelect(sec)}
              className={`p-2 rounded text-xs transition-all duration-200 border-2 ${
                selectedSecond === sec ? 'border-green-400' : 'border-transparent'
              }`}
              style={{ backgroundColor: bgColor }}
            >
              {sec}s
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default BetTimeline;