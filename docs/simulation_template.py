"""
simulation_template.py

An extendable Python script to simulate multiple rounds of Time Vault
using the mock StakeEngine Math SDK. This is useful for balancing the game,
testing payout distributions, and analyzing the house edge over a large
number of rounds.
"""
import json
from collections import defaultdict
from backend.sdk_integration import GameRound, Bet, simulate_round

def setup_round_from_config(config_path="backend/config/round_schema.json"):
    """Loads round configuration from a JSON file and creates a GameRound."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Adapt the JSON schema to the SDK's expected config format
    sdk_config = {
        "min_seconds": config["vaultTimer"]["minSeconds"],
        "max_seconds": config["vaultTimer"]["maxSeconds"],
        "quick_burst_chance": config["specialEvents"]["quickBurst"]["chance"],
        "bonus_vault_chance": config["specialEvents"]["bonusVault"]["chance"],
        "house_edge": config["houseEdge"]
    }
    return GameRound(sdk_config)

def generate_random_bets(num_bets: int, player_pool_size: int, min_sec: int, max_sec: int) -> list[Bet]:
    """Generates a list of random bets for simulation."""
    bets = []
    for _ in range(num_bets):
        player_id = f"sim_player_{randint(1, player_pool_size)}"
        second = randint(min_sec, max_sec)
        amount = choice([1, 5, 10, 25, 50, 100])
        bets.append(Bet(player_id=player_id, second=second, amount=float(amount)))
    return bets

def run_simulation(num_rounds: int):
    """
    Runs a full simulation for a specified number of rounds and prints a report.
    """
    print(f"--- Starting Time Vault Simulation for {num_rounds} rounds ---")
    
    total_bets_value = 0
    total_payouts_value = 0
    winning_seconds_distribution = defaultdict(int)

    for i in range(num_rounds):
        round_instance = setup_round_from_config()
        
        # Generate some random bets for this round
        # In a more advanced simulation, bet generation could be based on strategies
        bets = generate_random_bets(
            num_bets=randint(50, 200), 
            player_pool_size=50,
            min_sec=round_instance.min_seconds,
            max_sec=round_instance.max_seconds
        )
        round_instance.place_bets(bets)
        
        # Calculate total value of bets for this round
        round_bets_value = sum(bet.amount for bet in bets)
        total_bets_value += round_bets_value

        # Simulate the round
        result = simulate_round(round_instance)
        
        # Tally results
        round_payouts_value = sum(result.payouts.values())
        total_payouts_value += round_payouts_value
        winning_seconds_distribution[result.unlock_second] += 1
        
        print(f"Round {i+1}: Unlocked at {result.unlock_second}s. Pot: ${round_bets_value:.2f}, Payout: ${round_payouts_value:.2f}")

    print("\n--- Simulation Report ---")
    print(f"Total Value of Bets: ${total_bets_value:.2f}")
    print(f"Total Value of Payouts: ${total_payouts_value:.2f}")
    
    if total_bets_value > 0:
        actual_house_edge = (total_bets_value - total_payouts_value) / total_bets_value
        print(f"Actual House Edge: {actual_house_edge:.4%} (Target: {round_instance.house_edge:.2%})")
    
    print("\nTop 10 Winning Seconds:")
    sorted_winning_seconds = sorted(winning_seconds_distribution.items(), key=lambda item: item[1], reverse=True)
    for second, count in sorted_winning_seconds[:10]:
        print(f"  - Second {second}: won {count} times")


if __name__ == "__main__":
    from random import randint, choice
    # You can change the number of rounds to simulate
    run_simulation(num_rounds=100)