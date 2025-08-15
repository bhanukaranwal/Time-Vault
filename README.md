# Time Vault - A Suspenseful Prediction Betting Game

Welcome to **Time Vault**, an original, fully-featured Stake Originals game. This is a suspenseful, time-based prediction betting game with rich interactivity, provably fair mechanics, and engaging social features. Players bet on the exact moment a digital vault will unlock, with dynamic multipliers rewarding precise guesses.

This repository contains the complete source code for the backend, frontend, and deployment configurations.

## Core Concept
Players bet on the exact second (or fraction of a second in advanced modes) when a digital vault will unlock. Each round features a hidden countdown timer between 10 and 180 seconds. Special event rounds include "Quick Burst" (fast unlock with high multipliers) and "Bonus Vault" (flash instant-win windows). The game emphasizes social engagement with live chat, leaderboards, power-ups, and community-driven events.

## Technology Stack

- **Backend:** Python 3.12+ (FastAPI), StakeEngine Math SDK
- **Frontend:** TypeScript, React, TailwindCSS, WebSockets
- **DevOps:** Docker, GitHub Actions

## Repository Structure

```
time-vault/
├── backend/
├── frontend/
├── docker/
├── .github/
├── docs/
├── README.md
└── LICENSE
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js and npm/yarn
- Python 3.12+

### Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bhanukaranwal/time-vault.git
    cd time-vault
    ```

2.  **Run the application using Docker:**
    ```bash
    docker-compose up --build
    ```
    - The frontend will be available at `http://localhost:3000`.
    - The backend API will be available at `http://localhost:8000`.

### Testing

- **Backend (Pytest):**
  ```bash
  docker-compose exec backend pytest
  ```

- **Frontend (Jest):**
  ```bash
  docker-compose exec frontend npm test
  ```

## Documentation

- [API Specification](./docs/API_spec.md)
- [UI Wireframes](./docs/UI_wireframes.md)
- [Event Configuration](./docs/EVENT_config.yaml)
- [Simulation Template](./docs/simulation_template.py)

## Contributing

Please read our contribution guidelines before submitting a pull request. We use a feature-branch workflow.

1.  Create a feature branch (`git checkout -b feature/your-feature-name`).
2.  Commit your changes (`git commit -m 'Add some feature'`).
3.  Push to the branch (`git push origin feature/your-feature-name`).
4.  Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.