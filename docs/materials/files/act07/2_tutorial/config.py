
# Add Your Name Here

"""
Configuration constants for Space Invaders game.
Contains all game settings and constants.

Students will copy code here following the tutorial instructions.
"""

# COMPLETED-TASK: Add configuration constants here
"""
Configuration constants for Space Invaders game.
"""

from typing import Tuple

# Screen settings
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 400
FPS: int = 60

# Colors (R, G, B)
COLOR_BACKGROUND: Tuple[int, int, int] = (0, 0, 20)
COLOR_PLAYER: Tuple[int, int, int] = (0, 200, 255)
COLOR_ENEMY: Tuple[int, int, int] = (255, 50, 50)
COLOR_BULLET: Tuple[int, int, int] = (255, 255, 0)
COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)

# Player settings
PLAYER_START_X: int = 300
PLAYER_START_Y: int = 360
PLAYER_SPEED: int = 5
PLAYER_SIZE: int = 15

# Bullet settings
BULLET_SPEED: int = 7
BULLET_WIDTH: int = 5
BULLET_HEIGHT: int = 10

# Enemy settings
NUM_ENEMIES: int = 5
ENEMY_SPACING: int = 80
ENEMY_START_Y: int = 50
ENEMY_SPEED: int = 3
ENEMY_DESCENT: int = 20
ENEMY_SIZE: int = 12

# Scoring
POINTS_PER_ENEMY: int = 10

# Font settings
FONT_SIZE: int = 28
