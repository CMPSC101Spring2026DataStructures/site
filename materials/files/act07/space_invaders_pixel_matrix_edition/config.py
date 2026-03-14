"""
Configuration constants for Space Invaders game.

This module contains all game configuration parameters including screen dimensions,
colors, gameplay settings, and timing constants.
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
COLOR_EXPLOSION_ENEMY: Tuple[int, int, int] = (255, 165, 0)
COLOR_EXPLOSION_PLAYER: Tuple[int, int, int] = (255, 100, 0)
COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)
COLOR_PAUSE: Tuple[int, int, int] = (255, 255, 0)
COLOR_CONFIRM_BG: Tuple[int, int, int] = (50, 50, 50)

# Player settings
PLAYER_START_X: int = 300
PLAYER_START_Y: int = 360
PLAYER_SPEED: int = 5
PLAYER_LIVES: int = 3

# Bullet settings
BULLET_SPEED: int = 7
BULLET_WIDTH: int = 5
BULLET_HEIGHT: int = 10
BULLET_START_Y: int = 350

# Enemy settings
NUM_ENEMIES: int = 5
ENEMY_SPACING: int = 80
ENEMY_START_Y: int = 50
ENEMY_SPEED: int = 3
ENEMY_DESCENT: int = 20

# Scoring
POINTS_PER_ENEMY: int = 5

# Sprite settings
PIXEL_SIZE: int = 4

# Timing (in frames)
EXPLOSION_DURATION_ENEMY: int = 30  # 0.5 seconds at 60 FPS
EXPLOSION_DURATION_PLAYER: int = 60  # 1.0 second at 60 FPS

# Font settings
FONT_SIZE_NORMAL: int = 36
FONT_SIZE_LARGE: int = 72
FONT_SIZE_CONFIRM: int = 32

# UI positions
SCORE_POS: Tuple[int, int] = (10, 10)
LIVES_POS: Tuple[int, int] = (500, 10)
PAUSE_CENTER: Tuple[int, int] = (300, 200)
CONFIRM_BOX_POS: Tuple[int, int] = (100, 100)
CONFIRM_BOX_SIZE: Tuple[int, int] = (400, 200)
