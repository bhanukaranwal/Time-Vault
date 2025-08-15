"""
sdk_integration.py

This module provides a mock integration for the StakeEngine Math SDK.
This version is refined for clarity and handles dynamic payout calculations
based on various game events and power-ups.
"""
import random
import uuid
from typing import List, Dict, Any, NamedTuple

# --- Mock SDK Data Structures ---

class Bet(NamedTuple):
    """Represents a single player bet, now with an optional power-up field."""
    player_id: str
    second: int
    amount: float
    power_up: str | None = None

class GameRoundResult(NamedTuple):
    """Represents the detailed outcome of a simulated round."""
    unlock_second: int
    winners: List[Dict[str, Any]]
    payouts: Dict[str, float]
    provably_fair_data: Dict[str, str]
    special_event_triggered: str | None

class GameRound:
    """Configures and manages a round's parameters, including event effects."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.min_seconds = config.get("min_seconds", 10)
        self.max_seconds = config.get("max_seconds", 180)
        self.house_edge = config.get("house_edge", 0.02)
        self.bets: List[Bet] = []
        self.server_seed = uuid.uuid4().hex
        self.client_seed = uuid.uuid4().hex # In a real game, this comes from the player
        # Event-driven effects
        self.global_multiplier_boost = config.get("multiplierBoost", 1.0)
        self.quick_burst_chance = config.get("quick_burst_chance", 0.05)

    def place_bets(self, bets: List[Bet]):
        """Adds a list of bets to the current round."""
        self.bets.extend(bets)

    def _generate_unlock_second(self, is_quick_burst=False) -> int:
        """Generates a provably fair unlock second."""
        if is_quick_burst:
            # Quick Burst rounds have a smaller, more volatile range.
            return random.randint(1, 8)
        return random.randint(self.min_seconds, self.max_seconds)

def simulate_round(round_instance: GameRound) -> GameRoundResult:
    """
    Simulates a round, calculating winners and payouts based on its configuration,
    bets, and any active special events.
    """
    total_pot = sum(bet.amount for bet in round_instance.bets)
    payouts = {}
    winners_data = []
    special_event = None

    # 1. Determine if a "Quick Burst" event triggers
    if random.random() < round_instance.quick_burst_chance:
        special_event = "Quick Burst"
        unlock_second = round_instance._generate_unlock_second(is_quick_burst=True)
        winning_bets = [bet for bet in round_instance.bets if bet.second == unlock_second]

        if winning_bets:
            quick_burst_multiplier = random.uniform(50, 150)
            for bet in winning_bets:
                personal_multiplier = 1.5 if bet.power_up == 'multiplier_boost' else 1.0
                final_multiplier = quick_burst_multiplier * round_instance.global_multiplier_boost * personal_multiplier
                payout_amount = bet.amount * final_multiplier
                payouts[bet.player_id] = payouts.get(bet.player_id, 0) + payout_amount
                winners_data.append({
                    "player_id": bet.player_id, "amount": bet.amount, "payout": payout_amount,
                    "multiplier": final_multiplier
                })
    else:
        # 2. Standard Round Logic
        special_event = None
        unlock_second = round_instance._generate_unlock_second()
        winning_bets = [bet for bet in round_instance.bets if bet.second == unlock_second]
        
        if winning_bets:
            total_winner_stake = sum(bet.amount for bet in winning_bets)
            payout_pool = total_pot * (1 - round_instance.house_edge)
            
            for bet in winning_bets:
                proportion = bet.amount / total_winner_stake if total_winner_stake > 0 else 0
                base_payout = payout_pool * proportion
                
                personal_multiplier = 1.5 if bet.power_up == 'multiplier_boost' else 1.0
                final_payout = base_payout * round_instance.global_multiplier_boost * personal_multiplier
                
                payouts[bet.player_id] = payouts.get(bet.player_id, 0) + final_payout
                winners_data.append({
                    "player_id": bet.player_id, "amount": bet.amount, "payout": final_payout,
                    "multiplier": (final_payout / bet.amount if bet.amount > 0 else 0)
                })

    return GameRoundResult(
        unlock_second=unlock_second,
        winners=winners_data,
        payouts=payouts,
        provably_fair_data={
            "server_seed": round_instance.server_seed, "client_seed": round_instance.client_seed,
            "final_hash": uuid.uuid4().hex # Placeholder for the combined hash
        },
        special_event_triggered=special_event
    )