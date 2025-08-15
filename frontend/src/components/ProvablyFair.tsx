import React from 'react';

interface ProvablyFairProps {
  result: any;
}

const ProvablyFair: React.FC<ProvablyFairProps> = ({ result }) => {
  if (!result) {
    return (
      <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-2 text-yellow-400">Provably Fair</h3>
        <p className="text-sm text-gray-400">Round results will be shown here.</p>
      </div>
    );
  }

  const { provably_fair_data, unlock_second } = result;

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-2 text-yellow-400">Provably Fair</h3>
      <div className="space-y-1 text-xs break-all">
        <p><strong>Unlock Second:</strong> {unlock_second}</p>
        <p><strong>Server Seed:</strong> <span className="font-mono">{provably_fair_data.server_seed}</span></p>
        <p><strong>Final Hash:</strong> <span className="font-mono">{provably_fair_data.final_hash}</span></p>
      </div>
    </div>
  );
};

export default ProvablyFair;