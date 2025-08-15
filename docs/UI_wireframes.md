# Time Vault - UI Wireframes & UX Notes

This document outlines the visual structure and user experience for the Time Vault game.

## 1. Main Game Screen

The main screen is designed for high engagement and quick access to all critical functions.

```
+--------------------------------------------------------------------------+
|                       TIME VAULT (Logo)                                  |
+--------------------------------------------------------------------------+
|      [Leaderboard]      |      [Main Vault & Timer]      |      [Chat]      |
|                         |                                |                 |
| Top Players:            |      +------------------+      | User1: Hello!   |
| 1. PlayerX - $5000      |      |   [VAULT IMAGE]  |      | User2: Good luck|
| 2. PlayerY - $4300      |      |      15:34s      |      | User3: 🔥       |
| 3. PlayerZ - $2100      |      +------------------+      | ...             |
|                         |                                |                 |
|                         | [Betting Timeline Grid/Slider] | [Message Input] |
+--------------------------------------------------------------------------+
| [Avatar] [XP Bar] |  [Bet Amount] [Place Bet] [Cancel Bet] | [Power-ups]  |
+--------------------------------------------------------------------------+
```

### Components:

-   **Header:** Prominent game logo and title.
-   **Leaderboard (Left Sidebar):** Real-time updates of top winners by total earnings or highest multiplier.
-   **Main Vault (Center):**
    -   Large, visually appealing vault animation (Lottie/SVG).
    -   A clear, digital countdown timer is the focal point.
    -   When the round ends, this area will feature the unlocking animation and reveal the winning second.
-   **Betting Timeline (Center):** An interactive grid or slider representing seconds 10-180. Users can click to select a second to bet on. "Hot" seconds (many bets) can be highlighted with a color intensity scale.
-   **Chat (Right Sidebar):** Live chat feed with support for emojis.
-   **Footer/Controls:**
    -   Player info (avatar, level, XP).
    -   Core betting controls: input for amount, "Place Bet" button.
    -   Power-up buttons (e.g., "Multiplier Boost").

## 2. Result Screen

This screen appears immediately after the vault unlocks.

-   **Animation:** The vault door shakes, clangs open, and emits a burst of light. Confetti and particle effects fill the screen.
-   **Winning Second:** Displayed prominently in the center.
-   **Winner Spotlight:** A podium animation highlights the avatars of the winning players, showing their bet amount and payout multiplier.
-   **Social Sharing:** Buttons to share a screenshot of a big win on social media.

## 3. Support Screens

-   **Tutorial:** An interactive overlay that guides new players through their first bet.
-   **Player Dashboard:** A personal area to view game history, achievements, and detailed statistics.
-   **Event Lobby:** A screen that shows upcoming special events like "Golden Hour" or "Jackpot Cascade," with rules and entry requirements.