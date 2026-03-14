"""
Player class for the Space Invaders game.

This module defines the Player class which handles the player ship's
position, movement, rendering, and state management.
"""

import pygame
from typing import Tuple
import config
from sprites import SHIP_MATRIX, EXPLOSION_MATRIX
from utils import draw_matrix_sprite


class Player:
    """
    Represents the player's ship in the game.

    Attributes:
        x: Current x position of the player
        y: Current y position of the player
        speed: Movement speed in pixels per frame
        is_hit: Whether the player is currently exploding
        explosion_timer: Countdown timer for explosion animation
    """

    def __init__(self) -> None:
        """Initialize the player at the starting position."""
        self.x: int = config.PLAYER_START_X
        self.y: int = config.PLAYER_START_Y
        self.speed: int = config.PLAYER_SPEED
        self.is_hit: bool = False
        self.explosion_timer: int = 0

    def move_left(self) -> None:
        """Move the player left, respecting screen boundaries."""
        if self.x > 10:
            self.x -= self.speed

    def move_right(self) -> None:
        """Move the player right, respecting screen boundaries."""
        if self.x < config.SCREEN_WIDTH - 10:
            self.x += self.speed

    def hit(self) -> None:
        """
        Mark the player as hit and start explosion animation.
        
        This is called when an enemy collides with the player.
        """
        self.is_hit = True
        self.explosion_timer = config.EXPLOSION_DURATION_PLAYER

    def update(self) -> bool:
        """
        Update the player state, primarily the explosion timer.

        Returns:
            True if explosion just finished (life should be lost), False otherwise
        """
        if self.is_hit:
            self.explosion_timer -= 1
            if self.explosion_timer <= 0:
                self.is_hit = False
                return True  # Signal that explosion finished
        return False

    def reset_position(self) -> None:
        """Reset player to starting position (after losing a life)."""
        self.x = config.PLAYER_START_X
        self.y = config.PLAYER_START_Y

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the player ship or explosion on the screen.

        Args:
            surface: The pygame surface to draw on
        """
        if self.is_hit:
            # Draw explosion
            draw_matrix_sprite(
                surface,
                EXPLOSION_MATRIX,
                self.x,
                self.y,
                config.COLOR_EXPLOSION_PLAYER
            )
        else:
            # Draw normal ship
            draw_matrix_sprite(
                surface,
                SHIP_MATRIX,
                self.x,
                self.y,
                config.COLOR_PLAYER
            )

    def get_position(self) -> Tuple[int, int]:
        """
        Get the current position of the player.

        Returns:
            Tuple of (x, y) coordinates
        """
        return (self.x, self.y)
