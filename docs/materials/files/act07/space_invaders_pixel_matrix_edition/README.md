# Space Invaders - Pixel Matrix Edition

A modern implementation of the classic Space Invaders game using Pygame, featuring pixel-art sprites rendered from binary matrices.

# Table of Contents
- [Space Invaders - Pixel Matrix Edition](#space-invaders---pixel-matrix-edition)
- [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Controls](#controls)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Execution](#execution)
  - [Game Mechanics](#game-mechanics)
    - [Scoring](#scoring)
    - [Lives](#lives)
    - [Alien Behavior](#alien-behavior)
  - [Code Architecture](#code-architecture)
  - [Future Enhancements](#future-enhancements)
  - [License](#license)

## Features

- **AI generated enhancements**: This code was enhanced for extra *funability* using AI (model; Claude Sonnet 4.6)
- **Pixel Art Graphics**: Ships and explosions created from binary matrices (1s and 0s)
- **Classic Gameplay**: Move left/right, shoot aliens, avoid collisions
- **Lives System**: 3 lives per game
- **Score Tracking**: Earn 5 points per destroyed alien
- **Wave System**: New wave spawns when all aliens are destroyed
- **Pause Functionality**: Press 'P' to pause/unpause
- **Quit Confirmation**: Press 'Q' to quit with confirmation dialog

## Controls

- **Arrow Keys / A/D**: Move player ship left and right
- **Spacebar**: Fire bullet
- **P**: Pause/unpause the game
- **Q**: Quit game (with confirmation)

## Installation

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Execution

Note, this project comes with the File `pyproject.toml` for UV. This means that as long as you have UV installed, the code should be able to run after UV build the virtual environment from this configuration file.

To run the code, you should be starting in the directory where you can see the source code files (`*.py`), in addition to the files `pyproject.toml` and `uv.lock` (which both contain information about the versions of the *PyGame* package used in the project.

```bash
uv run main.py
```

## Game Mechanics

### Scoring

- Destroy an alien: **+5 points**
- Score persists across lives

### Lives

- Start with **3 lives**
- Lose a life when an alien touches the player ship
- Game resets (aliens respawn at top) but score is preserved
- Game over when all lives are lost

### Alien Behavior

- Aliens move in formation left to right
- When reaching screen edge, they descend and reverse direction
- Each destroyed alien shows explosion then disappears
- New wave spawns when all aliens are destroyed

## Code Architecture

The game follows object-oriented design principles:

- **Separation of Concerns**: Each class has a single responsibility
- **Configuration Management**: Constants stored in `config.py`
- **Modularity**: Easy to add new features or modify existing ones
- **Documentation**: Comprehensive docstrings and comments
- **Type Hints**: Improved code clarity and IDE support

## Future Enhancements

Potential features for future versions:
- Multiple alien types with different point values
- Player shields
- Alien projectiles
- Sound effects and music
- High score persistence
- Difficulty levels
- Power-ups

## License

Educational project - free to use and modify.
