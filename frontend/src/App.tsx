import React, { useEffect, useState, useCallback } from 'react';
import { getSocket } from './api';
import VaultTimer from './components/VaultTimer';
import BetTimeline from './components/BetTimeline';
import Chat from './components/Chat';
import Leaderboard from './components/Leaderboard';
import BetControls from './components/BetControls';
import PlayerDashboard from './components/PlayerDashboard';
import ProvablyFair from './components/ProvablyFair';

const App: React.FC = () => {
  const [socketId, setSocketId] = useState<string | null>(null);
  const [gameState, setGameState] = useState<any>(null);
  const [roundResult, setRoundResult] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any>({});
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [liveBets, setLiveBets] = useState<any>({});
  const [playerStats, setPlayerStats] = useState<any>({});
  const [bonusWin, setBonusWin] = useState<any>(null);
  
  const [selectedSecond, setSelectedSecond] = useState<number>(60);

  const handlePlayerStatsUpdate = useCallback((newStats: any) => {
    if (newStats && typeof newStats === 'object') {
      setPlayerStats(newStats);
    }
  }, []);

  useEffect(() => {
    const socket = getSocket();
    
    const onConnect = () => setSocketId(socket.id);
    const onGameUpdate = (data: any) => {
      setGameState(data);
      setRoundResult(null);
      setLiveBets({});
    };
    const onRoundResult = (data: any) => {
      setRoundResult(data);
      setGameState((prev: any) => ({ ...prev, status: 'finished' }));
    };
    const onNewBet = (data: any) => {
      setLiveBets((prev: any) => ({
        ...prev,
        [data.second]: (prev[data.second] || 0) + data.amount,
      }));
    };
    const onChatMessage = (data: any) => {
      setChatMessages((prev) => [...prev.slice(-100), data]); // Keep chat history from growing indefinitely
    };
    const onBonusVaultWin = (data: any) => {
      setBonusWin(data);
      setTimeout(() => setBonusWin(null), 5000); // Display for 5 seconds
    };

    // Register event listeners
    socket.on('connect', onConnect);
    socket.on('game_update', onGameUpdate);
    socket.on('round_result', onRoundResult);
    socket.on('leaderboard_update', setLeaderboard);
    socket.on('player_stats_update', handlePlayerStatsUpdate);
    socket.on('new_bet', onNewBet);
    socket.on('chat_message', onChatMessage);
    socket.on('bonus_vault_win', onBonusVaultWin);

    // Clean up listeners on component unmount
    return () => {
      socket.off('connect', onConnect);
      socket.off('game_update', onGameUpdate);
      socket.off('round_result', onRoundResult);
      socket.off('leaderboard_update', setLeaderboard);
      socket.off('player_stats_update', handlePlayerStatsUpdate);
      socket.off('new_bet', onNewBet);
      socket.off('chat_message', onChatMessage);
      socket.off('bonus_vault_win', onBonusVaultWin);
    };
  }, [handlePlayerStatsUpdate]);

  const handleSendMessage = (text: string) => {
    getSocket().emit('send_chat_message', { sender: 'bhanukaranwal', text });
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center p-4 font-sans relative">
      {bonusWin && (
        <div className="absolute top-5 left-1/2 -translate-x-1/2 bg-yellow-400 text-black p-4 rounded-lg shadow-2xl z-50 animate-bounce">
          <h2 className="text-2xl font-bold">BONUS VAULT WIN!</h2>
          <p>{bonusWin.player_id.substring(0, 6)}... won ${bonusWin.payout.toFixed(2)}!</p>
        </div>
      )}
      <header className="w-full text-center mb-4">
        <h1 className="text-5xl font-bold text-yellow-400">Time Vault</h1>
        <p className="text-gray-400 h-6 transition-opacity duration-500">
          {gameState?.active_events?.length > 0
            ? <span className="text-yellow-300 animate-pulse">Event Active: {gameState.active_events.join(', ')}!</span>
            : "Place your bet on when the vault will unlock!"}
        </p>
      </header>

      <div className="w-full max-w-screen-xl grid grid-cols-1 lg:grid-cols-5 gap-4">
        <aside className="lg:col-span-1 flex flex-col gap-4">
          <Leaderboard data={leaderboard} />
          <PlayerDashboard stats={playerStats} />
        </aside>

        <main className="lg:col-span-3 flex flex-col items-center gap-4">
          <VaultTimer gameState={gameState} result={roundResult} />
          <BetTimeline selectedSecond={selectedSecond} onSecondSelect={setSelectedSecond} liveBets={liveBets} />
          <BetControls selectedSecond={selectedSecond} disabled={gameState?.status !== 'betting'} onBetPlaced={handlePlayerStatsUpdate} />
        </main>

        <aside className="lg:col-span-1 flex flex-col gap-4">
          <Chat messages={chatMessages} onSendMessage={handleSendMessage} />
          <ProvablyFair result={roundResult} />
        </aside>
      </div>
    </div>
  );
};

export default App;