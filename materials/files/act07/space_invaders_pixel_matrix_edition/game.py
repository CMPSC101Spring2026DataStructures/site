"""
Main game class for Space Invaders.

This module contains the Game class which manages the game loop, state,
and all game entities.
"""

import pygame
import sys
from typing import Optional
import config
from player import Player
from enemy import EnemyFleet
from utils import draw_text, draw_centered_text, check_collision


class Game:
    """
    Main game class that manages the game loop and state.

    Attributes:
        screen: Pygame display surface
        clock: Pygame clock for FPS management
        font_normal: Font for regular text
        font_large: Font for large text (pause)
        font_confirm: Font for confirmation dialogs
        player: Player object
        fleet: EnemyFleet object
        bullet_x: Current bullet x position
        bullet_y: Current bullet y position
        bullet_fired: Whether a bullet is currently active
        score: Current game score
        lives: Remaining player lives
        paused: Whether the game is paused
        running: Whether the game is running
    """

    def __init__(self) -> None:
        """Initialize the game and all components."""
        pygame.init()
        
        # Display setup
        self.screen: pygame.Surface = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Space Invaders - Pixel Matrix Edition")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Font setup
        self.font_normal: pygame.font.Font = pygame.font.Font(
            None, config.FONT_SIZE_NORMAL
        )
        self.font_large: pygame.font.Font = pygame.font.Font(
            None, config.FONT_SIZE_LARGE
        )
        self.font_confirm: pygame.font.Font = pygame.font.Font(
            None, config.FONT_SIZE_CONFIRM
        )

        # Game entities
        self.player: Player = Player()
        self.fleet: EnemyFleet = EnemyFleet()

        # Bullet state
        self.bullet_x: int = 0
        self.bullet_y: int = config.BULLET_START_Y
        self.bullet_fired: bool = False

        # Game state
        self.score: int = 0
        self.lives: int = config.PLAYER_LIVES
        self.paused: bool = False
        self.running: bool = True

    def handle_events(self) -> None:
        """Process all pygame events including keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Shoot bullet
                if event.key == pygame.K_SPACE and not self.bullet_fired and not self.paused:
                    self.bullet_fired = True
                    self.bullet_x = self.player.x

                # Toggle pause
                if event.key == pygame.K_p:
                    self.paused = not self.paused

                # Quit with confirmation
                if event.key == pygame.K_q:
                    self._show_quit_confirmation()

    def _show_quit_confirmation(self) -> None:
        """Display quit confirmation dialog and handle response."""
        # Create confirmation box
        confirm_surface = pygame.Surface(config.CONFIRM_BOX_SIZE)
        confirm_surface.fill(config.COLOR_CONFIRM_BG)
        
        # Draw text
        text1 = self.font_confirm.render("Quit Game?", True, config.COLOR_TEXT)
        text2 = self.font_confirm.render(
            "Press Y to quit, N to continue", True, config.COLOR_TEXT
        )
        confirm_surface.blit(text1, (120, 60))
        confirm_surface.blit(text2, (20, 100))
        
        # Display confirmation box
        self.screen.blit(confirm_surface, config.CONFIRM_BOX_POS)
        pygame.display.flip()

        # Wait for response
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.running = False
                        waiting = False
                    elif event.key == pygame.K_n:
                        waiting = False

    def handle_input(self) -> None:
        """Process continuous keyboard input for player movement."""
        if self.paused or self.player.is_hit:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

    def update(self) -> None:
        """Update all game entities and check for collisions."""
        if self.paused:
            return

        # Update player
        if self.player.update():
            # Player explosion finished - lose a life
            self.lives -= 1
            if self.lives > 0:
                self.player.reset_position()
                self.fleet.reset()
                self.bullet_fired = False
                self.bullet_y = config.BULLET_START_Y
            else:
                # Game over
                self.running = False

        # Update bullet
        if self.bullet_fired and not self.player.is_hit:
            self.bullet_y -= config.BULLET_SPEED
            if self.bullet_y < 0:
                self.bullet_fired = False
                self.bullet_y = config.BULLET_START_Y

        # Update enemies
        if not self.player.is_hit:
            self.fleet.update()

        # Check collisions
        self._check_collisions()

    def _check_collisions(self) -> None:
        """Check for bullet-enemy and player-enemy collisions."""
        if self.player.is_hit:
            return

        # Bullet-enemy collisions
        if self.bullet_fired:
            for enemy in self.fleet.get_active_enemies():
                enemy_x, enemy_y = enemy.get_position()
                if check_collision(self.bullet_x, self.bullet_y, enemy_x, enemy_y, 20):
                    enemy.hit()
                    self.bullet_fired = False
                    self.bullet_y = config.BULLET_START_Y
                    self.score += config.POINTS_PER_ENEMY
                    break

        # Player-enemy collisions
        player_x, player_y = self.player.get_position()
        for enemy in self.fleet.get_active_enemies():
            enemy_x, enemy_y = enemy.get_position()
            if check_collision(player_x, player_y, enemy_x, enemy_y, 25):
                self.player.hit()
                break

    def draw(self) -> None:
        """Render all game elements to the screen."""
        # Clear screen
        self.screen.fill(config.COLOR_BACKGROUND)

        # Draw HUD
        draw_text(
            self.screen,
            f"Score: {self.score}",
            config.SCORE_POS,
            self.font_normal
        )
        draw_text(
            self.screen,
            f"Lives: {self.lives}",
            config.LIVES_POS,
            self.font_normal
        )

        # Draw player
        self.player.draw(self.screen)

        # Draw bullet
        if self.bullet_fired:
            pygame.draw.rect(
                self.screen,
                config.COLOR_BULLET,
                (self.bullet_x, self.bullet_y, config.BULLET_WIDTH, config.BULLET_HEIGHT)
            )

        # Draw enemies
        self.fleet.draw(self.screen)

        # Draw pause overlay
        if self.paused:
            draw_centered_text(
                self.screen,
                "PAUSED",
                config.PAUSE_CENTER,
                self.font_large,
                config.COLOR_PAUSE
            )

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)

        pygame.quit()
        sys.exit()
