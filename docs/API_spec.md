# Time Vault - API Specification

This document details the RESTful API and WebSocket events for the Time Vault game.

**Base URL:** `/`
**WebSocket URL:** `/ws/{client_id}`

---

## RESTful API Endpoints

### Game Management

#### `POST /game/start`
Manually starts a new game round. Primarily for testing or admin use, as the game loop runs automatically.

-   **Response (200 OK):**
    ```json
    {
      "message": "New round started",
      "round_id": "round_abc123"
    }
    ```

### Betting

#### `POST /game/bet`
Places a bet for the current active round.

-   **Request Body:**
    ```json
    {
      "player_id": "user_12345",
      "second": 72,
      "amount": 50.5
    }
    ```
-   **Response (200 OK):**
    ```json
    {
      "message": "Bet placed successfully."
    }
    ```
-   **Response (400 Bad Request):**
    ```json
    {
      "detail": "Betting window is closed or no round is active."
    }
    ```

#### `POST /game/bet/cancel`
*Future Implementation: Cancels a bet that has been placed but not yet settled.*

### Game State & History

#### `GET /game/state/{roundId}`
Retrieves the public state of a specific round.

-   **Response (200 OK):**
    ```json
    {
      "round_id": "round_abc123",
      "status": "finished",
      "start_time": 1678886400,
      "end_time": 1678886405,
      "bets_placed": 150,
      "result": {
        "unlock_second": 72,
        "winners": [{"player_id": "user_xyz", "payout": 150, "multiplier": 3.0}],
        "payouts": {"user_xyz": 150}
      }
    }
    ```

#### `GET /leaderboard`
Fetches the current leaderboard, sorted by total winnings.

-   **Response (200 OK):**
    ```json
    {
      "playerX": 5000,
      "playerY": 4300,
      "playerZ": 2100
    }
    ```

#### `GET /game/history`
Fetches a list of the last 50 completed rounds.

-   **Response (200 OK):**
    ```json
    {
      "history": [
        { "round_id": "round_abc123", "result": { ... } },
        { "round_id": "round_def456", "result": { ... } }
      ]
    }
    ```

---

## WebSocket Events

The WebSocket is used for broadcasting real-time updates from the server to all connected clients.

### Server-to-Client Events

#### `game_update`
Sent when a new round starts or the game state changes.
-   **Payload:** The same object as `GET /game/state/{roundId}`.

#### `new_bet`
Broadcasts when a new bet is successfully placed.
-   **Payload:** The bet data that was submitted to `POST /game/bet`.

#### `round_result`
Announces the result of a completed round.
-   **Payload:** The `result` object from the round state, including unlock second and winner details.

#### `leaderboard_update`
Sent after a round result to update the leaderboard.
-   **Payload:** The same object as `GET /leaderboard`.

#### `chat_message`
Broadcasts a message sent by a user.
-   **Payload:**
    ```json
    {
      "sender": "user_12345",
      "text": "Good luck everyone!"
    }
    ```

### Client-to-Server Events

#### `chat_message`
A client sends this event to post a message to the chat.
-   **Payload:**
    ```json
    {
        "type": "chat_message",
        "data": { "text": "This is my message" }
    }
    ```