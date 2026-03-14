"""
Enemy class for the Space Invaders game.

This module defines the Enemy class representing individual alien invaders
and the EnemyFleet class managing the entire formation.
"""

import pygame
from typing import List, Tuple
import config
from sprites import INVADER_MATRIX, EXPLOSION_MATRIX
from utils import draw_matrix_sprite


class Enemy:
    """
    Represents a single enemy alien invader.

    Attributes:
        x: Current x position
        y: Current y position
        is_hit: Whether the enemy is currently exploding
        explosion_timer: Countdown timer for explosion animation
        destroyed: Whether the enemy is permanently destroyed this wave
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize an enemy at the specified position.

        Args:
            x: Starting x coordinate
            y: Starting y coordinate
        """
        self.x: int = x
        self.y: int = y
        self.is_hit: bool = False
        self.explosion_timer: int = 0
        self.destroyed: bool = False

    def hit(self) -> None:
        """Mark the enemy as hit and start explosion animation."""
        self.is_hit = True
        self.explosion_timer = config.EXPLOSION_DURATION_ENEMY

    def update(self) -> None:
        """Update the enemy state, primarily the explosion timer."""
        if self.is_hit:
            self.explosion_timer -= 1
            if self.explosion_timer <= 0:
                self.destroyed = True
                self.is_hit = False

    def move(self, dx: int, dy: int) -> None:
        """
        Move the enemy by the specified amount.

        Args:
            dx: Change in x position
            dy: Change in y position
        """
        self.x += dx
        self.y += dy

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the enemy or its explosion on the screen.

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
                config.COLOR_EXPLOSION_ENEMY
            )
        elif not self.destroyed:
            # Draw normal invader
            draw_matrix_sprite(
                surface,
                INVADER_MATRIX,
                self.x,
                self.y,
                config.COLOR_ENEMY
            )

    def is_active(self) -> bool:
        """
        Check if the enemy is active (not destroyed and not exploding).

        Returns:
            True if enemy is active, False otherwise
        """
        return not self.destroyed and not self.is_hit

    def get_position(self) -> Tuple[int, int]:
        """
        Get the current position of the enemy.

        Returns:
            Tuple of (x, y) coordinates
        """
        return (self.x, self.y)


class EnemyFleet:
    """
    Manages the fleet of enemy invaders.

    Attributes:
        enemies: List of Enemy objects
        direction: Current movement direction (1 = right, -1 = left)
        speed: Movement speed in pixels per frame
    """

    def __init__(self) -> None:
        """Initialize the enemy fleet at starting positions."""
        self.enemies: List[Enemy] = []
        self.direction: int = 1
        self.speed: int = config.ENEMY_SPEED
        self.reset()

    def reset(self) -> None:
        """Reset all enemies to starting positions for a new wave."""
        self.enemies.clear()
        self.direction = 1
        for i in range(config.NUM_ENEMIES):
            x = 100 + i * config.ENEMY_SPACING
            y = config.ENEMY_START_Y
            self.enemies.append(Enemy(x, y))

    def update(self) -> None:
        """
        Update all enemies in the fleet.

        Handles movement, edge detection, and descent behavior.
        """
        # Update individual enemy states
        for enemy in self.enemies:
            enemy.update()

        # Move active enemies
        should_descend = False
        for enemy in self.enemies:
            if enemy.is_active():
                enemy.move(self.speed * self.direction, 0)
                # Check if any enemy hits the edge
                if enemy.x < 10 or enemy.x > config.SCREEN_WIDTH - 10:
                    should_descend = True

        # If any enemy hit the edge, reverse direction and descend
        if should_descend:
            self.direction *= -1
            for enemy in self.enemies:
                if not enemy.destroyed:
                    enemy.move(0, config.ENEMY_DESCENT)

        # Check if all enemies destroyed - reset for new wave
        if all(enemy.destroyed for enemy in self.enemies):
            self.reset()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all enemies in the fleet.

        Args:
            surface: The pygame surface to draw on
        """
        for enemy in self.enemies:
            enemy.draw(surface)

    def get_active_enemies(self) -> List[Enemy]:
        """
        Get all active (not destroyed, not exploding) enemies.

        Returns:
            List of active Enemy objects
        """
        return [enemy for enemy in self.enemies if enemy.is_active()]

    def get_all_enemies(self) -> List[Enemy]:
        """
        Get all enemies in the fleet.

        Returns:
            List of all Enemy objects
        """
        return self.enemies
