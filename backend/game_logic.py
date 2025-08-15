"""
game_logic.py

Handles the core state machine. This version includes critical fixes for race
conditions and adds more robust error handling for event configuration.
"""
import asyncio
import json
import random
import time
import uuid
import yaml
from asyncio import Lock
from datetime import datetime, timezone
from typing import Any, Dict, List

from backend.sdk_integration import Bet, GameRound, simulate_round

# In-memory storage. Use Redis in production for scalability.
GAME_STATE: Dict[str, Any] = {
    "current_round": None,
    "round_history": [],
    "leaderboard": {},
    "active_events": [],
    "player_stats": {},
}
state_lock = Lock()


def log_round_for_audit(round_manager):
    """Appends round data to a log file for provably fair auditing."""
    try:
        with open("provably_fair_audit.log", "a") as f:
            f.write(json.dumps(round_manager.to_dict()) + "\n")
    except IOError as e:
        print(f"Error writing to audit log: {e}")


def load_event_config():
    """Loads and checks for active global events from the YAML file.
    This version is more robust against individual malformed event entries.
    """
    GAME_STATE["active_events"] = []
    try:
        with open("docs/EVENT_config.yaml", 'r') as f:
            config = yaml.safe_load(f)

        now = datetime.now(timezone.utc)
        active_events = []
        for event in config.get("events", []):
            try:
                if event.get("enabled", False):
                    start_time = datetime.fromisoformat(event["start_time"])
                    end_time = datetime.fromisoformat(event["end_time"])
                    if start_time <= now <= end_time:
                        active_events.append(event)
            except (ValueError, TypeError) as e:
                print(f"Skipping malformed event '{event.get('name', 'N/A')}': {e}")
        
        GAME_STATE["active_events"] = active_events
        if active_events:
            print(f"Active global events: {[event['name'] for event in active_events]}")

    except FileNotFoundError:
        print("docs/EVENT_config.yaml not found, running without global events.")
    except Exception as e:
        print(f"Error loading event config: {e}")


class GameRoundManager:
    def __init__(self, config, sio_server):
        self.round_id = f"round_{uuid.uuid4().hex[:8]}"
        self.status = "pending"
        self.sio = sio_server
        self.config = self._apply_event_effects(config)
        self.bets: List[Bet] = []
        self.bet_end_time = None
        self.result = None
        self.sdk_round = GameRound(self.config)
        self.bonus_vault_triggered = False

    def _apply_event_effects(self, config):
        for event in GAME_STATE.get("active_events", []):
            effects = event.get("effects", {})
            config.update(effects)
        return config

    async def start_betting(self):
        self.status = "betting"
        self.bet_end_time = time.time() + self.config.get("bettingWindow", {}).get("end", 5)
        print(f"Round {self.round_id} started. Betting is open.")
        asyncio.create_task(self.bonus_vault_checker())

    async def bonus_vault_checker(self):
        """
        Periodically checks for a Bonus Vault win.
        FIXED: This function now uses the shared lock to prevent race conditions
        when accessing the list of bets.
        """
        while time.time() < self.bet_end_time and not self.bonus_vault_triggered:
            await asyncio.sleep(0.5)
            # Spread the chance over the betting window duration
            if random.random() < self.config.get("bonus_vault_chance", 0.03) / 10:
                async with state_lock:
                    if self.bets and not self.bonus_vault_triggered:
                        self.bonus_vault_triggered = True
                        random_bet = random.choice(self.bets)
                        instant_win_multiplier = 10
                        payout = random_bet.amount * instant_win_multiplier
                        
                        winner_id = random_bet.player_id
                        GAME_STATE["leaderboard"][winner_id] = GAME_STATE["leaderboard"].get(winner_id, 0) + payout
                        
                        win_data = {"player_id": winner_id, "payout": payout}
                        await self.sio.emit("bonus_vault_win", win_data)
                        print(f"Bonus Vault Win! Player {winner_id} won ${payout:.2f}")

    async def place_bet(self, player_id: str, second: int, amount: float, power_up: str | None) -> bool:
        if self.status != "betting": return False
        async with state_lock:
            self.bets.append(Bet(player_id=player_id, second=second, amount=amount, power_up=power_up))
            stats = GAME_STATE["player_stats"].setdefault(player_id, {'wins': 0, 'total_bet': 0, 'total_won': 0})
            stats['total_bet'] += amount
        return True

    async def end_round(self):
        async with state_lock:
            if self.status == "finished": return self.result
            self.status = "finished"
            self.sdk_round.place_bets(self.bets)
            self.result = simulate_round(self.sdk_round)
            
            for winner in self.result.winners:
                player_id = winner['player_id']
                payout = winner['payout']
                GAME_STATE["leaderboard"][player_id] = GAME_STATE["leaderboard"].get(player_id, 0) + payout
                stats = GAME_STATE["player_stats"].setdefault(player_id, {'wins': 0, 'total_bet': 0, 'total_won': 0})
                stats['wins'] += 1
                stats['total_won'] += payout

            GAME_STATE["round_history"].insert(0, self.to_dict())
            if len(GAME_STATE["round_history"]) > 50:
                GAME_STATE["round_history"].pop()
            
            log_round_for_audit(self)
            print(f"Round {self.round_id} finished. Unlock second: {self.result.unlock_second}")
            return self.result

    def get_state(self):
        return {
            "round_id": self.round_id, "status": self.status,
            "bet_end_time": self.bet_end_time, "bets_placed": len(self.bets),
            "result": self.result._asdict() if self.result else None,
            "active_events": [event['name'] for event in GAME_STATE.get("active_events", [])]
        }
        
    def to_dict(self):
        return {
            "round_id": self.round_id, "config": self.config,
            "bets": [bet._asdict() for bet in self.bets],
            "result": self.result._asdict() if self.result else None
        }


async def start_new_round(sio_server):
    async with state_lock:
        load_event_config()
        config = {
            "min_seconds": 10, "max_seconds": 180,
            "quick_burst_chance": 0.05, "bonus_vault_chance": 0.03,
            "house_edge": 0.02, "bettingWindow": {"end": 5}
        }
        new_round = GameRoundManager(config, sio_server)
        GAME_STATE["current_round"] = new_round
        await new_round.start_betting()
        return new_round