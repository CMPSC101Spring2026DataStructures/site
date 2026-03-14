"""
Utility functions for the Space Invaders game.

This module provides helper functions for rendering sprites, collision detection,
and other common operations.
"""

import pygame
from typing import Tuple, List
from sprites import BinaryMatrix
import config


def draw_matrix_sprite(
    surface: pygame.Surface,
    matrix: BinaryMatrix,
    center_x: int,
    center_y: int,
    color: Tuple[int, int, int],
    pixel_size: int = config.PIXEL_SIZE
) -> None:
    """
    Draw a sprite from a binary matrix onto a surface.

    Args:
        surface: The pygame surface to draw on
        matrix: Binary matrix representing the sprite (1 = pixel, 0 = empty)
        center_x: X coordinate of the sprite center
        center_y: Y coordinate of the sprite top
        color: RGB color tuple for the sprite
        pixel_size: Size of each pixel in the matrix
    """
    for row_idx, row in enumerate(matrix):
        for col_idx, pixel in enumerate(row):
            if pixel == 1:
                x = center_x - (len(row) * pixel_size // 2) + col_idx * pixel_size
                y = center_y + row_idx * pixel_size
                pygame.draw.rect(
                    surface,
                    color,
                    (x, y, pixel_size, pixel_size)
                )


def check_collision(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    threshold: int = 25
) -> bool:
    """
    Check if two objects are colliding based on distance threshold.

    Args:
        x1: X coordinate of first object
        y1: Y coordinate of first object
        x2: X coordinate of second object
        y2: Y coordinate of second object
        threshold: Maximum distance for collision

    Returns:
        True if objects are colliding, False otherwise
    """
    return abs(x1 - x2) < threshold and abs(y1 - y2) < threshold


def draw_text(
    surface: pygame.Surface,
    text: str,
    position: Tuple[int, int],
    font: pygame.font.Font,
    color: Tuple[int, int, int] = config.COLOR_TEXT
) -> None:
    """
    Draw text on a surface at a specific position.

    Args:
        surface: The pygame surface to draw on
        text: The text string to render
        position: (x, y) tuple for text position
        font: Pygame font object to use
        color: RGB color tuple for the text
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def draw_centered_text(
    surface: pygame.Surface,
    text: str,
    center: Tuple[int, int],
    font: pygame.font.Font,
    color: Tuple[int, int, int] = config.COLOR_TEXT
) -> None:
    """
    Draw text centered at a specific position.

    Args:
        surface: The pygame surface to draw on
        text: The text string to render
        center: (x, y) tuple for center position
        font: Pygame font object to use
        color: RGB color tuple for the text
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)
