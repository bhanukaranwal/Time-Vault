"""
test_game.py

Unit tests for the backend game logic using Pytest.
"""
import pytest
from unittest.mock import patch
from backend.game_logic import GameRoundManager, start_new_round, GAME_STATE

@pytest.fixture(autouse=True)
def reset_game_state():
    """Fixture to reset the global game state before each test."""
    GAME_STATE["current_round"] = None
    GAME_STATE["round_history"] = []
    GAME_STATE["leaderboard"] = {}

def test_game_round_manager_initialization():
    """Tests if a GameRoundManager initializes correctly."""
    config = {"min_seconds": 10, "max_seconds": 180}
    round_manager = GameRoundManager(config)
    assert round_manager.status == "pending"
    assert round_manager.config == config
    assert round_manager.round_id.startswith("round_")

def test_start_betting():
    """Tests the transition to the 'betting' state."""
    config = {"bettingWindow": {"end": 5}}
    round_manager = GameRoundManager(config)
    round_manager.start_betting()
    assert round_manager.status == "betting"
    assert round_manager.start_time is not None
    assert round_manager.end_time > round_manager.start_time

def test_place_bet_in_window():
    """Tests placing a bet during the betting window."""
    round_manager = GameRoundManager({})
    round_manager.start_betting()
    assert round_manager.place_bet("player1", 55, 10.0) is True
    assert len(round_manager.bets) == 1
    assert round_manager.bets[0].player_id == "player1"

def test_place_bet_outside_window():
    """Tests that bets cannot be placed when the window is closed."""
    round_manager = GameRoundManager({})
    assert round_manager.place_bet("player1", 55, 10.0) is False
    round_manager.status = "finished"
    assert round_manager.place_bet("player2", 60, 5.0) is False
    assert len(round_manager.bets) == 0

@patch('backend.game_logic.simulate_round')
def test_end_round_logic(mock_simulate_round):
    """Tests the logic for ending a round and processing results."""
    from backend.sdk_integration import GameRoundResult
    
    # Mock the SDK result
    mock_result = GameRoundResult(
        unlock_second=72,
        winners=[{"player_id": "player2", "payout": 150, "multiplier": 3.0}],
        payouts={"player2": 150},
        provably_fair_data={}
    )
    mock_simulate_round.return_value = mock_result
    
    round_manager = start_new_round()
    round_manager.place_bet(player_id="player1", second=45, amount=10)
    round_manager.place_bet(player_id="player2", second=72, amount=50)

    result = round_manager.end_round()

    assert round_manager.status == "finished"
    assert result.unlock_second == 72
    assert len(GAME_STATE["round_history"]) == 1
    assert GAME_STATE["leaderboard"]["player2"] == 150

def test_start_new_round_updates_global_state():
    """Tests if starting a new round correctly updates the global state."""
    assert GAME_STATE["current_round"] is None
    new_round = start_new_round()
    assert GAME_STATE["current_round"] is new_round
    assert new_round.status == "betting"
