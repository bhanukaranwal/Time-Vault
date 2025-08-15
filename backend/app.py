"""
app.py

Main FastAPI application using Socket.IO, with full game logic,
player stats endpoints, and robust real-time event handling.
"""
import asyncio
import socketio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.game_logic import GAME_STATE, start_new_round, GameRoundManager, state_lock

# --- Server Setup ---
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI(title="Time Vault API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
app.mount('/socket.io', socketio.ASGIApp(sio))

# --- Background Game Loop ---
async def game_loop():
    """The main game loop that orchestrates rounds."""
    while True:
        current_round = await start_new_round(sio)
        await sio.emit("game_update", current_round.get_state())
        
        await asyncio.sleep(current_round.config.get("bettingWindow", {}).get("end", 5))
        
        result = await current_round.end_round()
        
        await sio.emit("round_result", result._asdict())
        await sio.emit("leaderboard_update", get_leaderboard_data())

@app.on_event("startup")
async def startup_event():
    """Starts the game loop when the server boots."""
    asyncio.create_task(game_loop())

# --- Socket.IO Events ---
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    async with state_lock:
        if GAME_STATE["current_round"]:
            await sio.emit("game_update", GAME_STATE["current_round"].get_state(), to=sid)
        await sio.emit("leaderboard_update", get_leaderboard_data(), to=sid)
        await sio.emit("player_stats_update", GAME_STATE["player_stats"].get(sid, {}), to=sid)

@sio.event
async def place_bet(sid, data):
    """Handles a player placing a bet."""
    player_id = sid
    second = data.get("second")
    amount = data.get("amount")
    power_up = data.get("power_up") # e.g., 'multiplier_boost'

    if not all([player_id, isinstance(second, int), isinstance(amount, (int, float))]):
        return {"status": "error", "message": "Invalid bet information."}
    
    current_round: GameRoundManager = GAME_STATE.get("current_round")
    if not await current_round.place_bet(player_id, second, amount, power_up):
        return {"status": "error", "message": "Betting window is closed."}
    
    await sio.emit("new_bet", {"second": second, "amount": amount})
    # Acknowledge success and provide updated stats
    return {
        "status": "success",
        "message": "Bet placed!",
        "stats": GAME_STATE["player_stats"].get(player_id)
    }

@sio.event
async def send_chat_message(sid, data):
    """Broadcasts a chat message to all clients."""
    await sio.emit("chat_message", {"sender": data.get("sender", sid[:6]), "text": data.get("text", "")})

# --- REST API Endpoints ---
def get_leaderboard_data():
    return dict(sorted(GAME_STATE["leaderboard"].items(), key=lambda item: item[1], reverse=True)[:10])

@app.get("/leaderboard")
async def get_leaderboard():
    async with state_lock:
        return get_leaderboard_data()

@app.get("/game/history")
async def get_game_history():
    async with state_lock:
        return {"history": GAME_STATE["round_history"]}

@app.get("/player/{player_id}/stats")
async def get_player_stats(player_id: str):
    async with state_lock:
        stats = GAME_STATE["player_stats"].get(player_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Player not found.")
        return stats