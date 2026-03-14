
# Add Your Name Here

"""
Game class for Space Invaders.
Manages the game loop and game state.

Students will copy code here following the tutorial instructions.
"""

# COMPLETED-TASK: Add Game class
"""
Game class for Space Invaders.
Manages the game loop and game state.
"""

import pygame
import sys
import config


class Game:
    """
    Main game class that manages the game loop and state.
    """

    def __init__(self) -> None:
        """Initialize the game and all components."""
        pygame.init()
        
        # Display setup
        self.screen: pygame.Surface = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Space Invaders")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Font setup
        self.font: pygame.font.Font = pygame.font.Font(None, config.FONT_SIZE)

        # Player state
        self.player_x: int = config.PLAYER_START_X
        self.player_y: int = config.PLAYER_START_Y

        # Bullet state
        self.bullet_x: int = 0
        self.bullet_y: int = config.PLAYER_START_Y
        self.bullet_fired: bool = False

        # Enemy state - create a list of enemy positions
        self.enemies: list = []
        for i in range(config.NUM_ENEMIES):
            enemy_x = 100 + i * config.ENEMY_SPACING
            enemy_y = config.ENEMY_START_Y
            self.enemies.append([enemy_x, enemy_y, True])  # [x, y, alive]
        
        self.enemy_direction: int = config.ENEMY_SPEED

        # Game state
        self.score: int = 0
        self.running: bool = True

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Shoot bullet
                if event.key == pygame.K_SPACE and not self.bullet_fired:
                    self.bullet_fired = True
                    self.bullet_x = self.player_x

                # Quit game
                if event.key == pygame.K_q:
                    self.running = False

    def handle_input(self) -> None:
        """Process continuous keyboard input for player movement."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= config.PLAYER_SPEED
            # Keep player on screen
            if self.player_x < config.PLAYER_SIZE:
                self.player_x = config.PLAYER_SIZE
                
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += config.PLAYER_SPEED
            # Keep player on screen
            if self.player_x > config.SCREEN_WIDTH - config.PLAYER_SIZE:
                self.player_x = config.SCREEN_WIDTH - config.PLAYER_SIZE

    def update(self) -> None:
        """Update all game entities and check for collisions."""
        # Update bullet position
        if self.bullet_fired:
            self.bullet_y -= config.BULLET_SPEED
            if self.bullet_y < 0:
                self.bullet_fired = False
                self.bullet_y = config.PLAYER_START_Y

        # Update enemy positions
        move_down = False
        
        # Check if any enemy hit the edge
        for enemy in self.enemies:
            if not enemy[2]:  # Skip dead enemies
                continue
            if enemy[0] <= 10 or enemy[0] >= config.SCREEN_WIDTH - 10:
                move_down = True
                break

        # Move enemies down and reverse direction if needed
        if move_down:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                enemy[1] += config.ENEMY_DESCENT

        # Move enemies horizontally
        for enemy in self.enemies:
            if enemy[2]:  # Only move living enemies
                enemy[0] += self.enemy_direction

        # Check for collisions between bullet and enemies
        if self.bullet_fired:
            for enemy in self.enemies:
                if not enemy[2]:  # Skip dead enemies
                    continue
                
                # Simple collision detection (distance check)
                distance = ((self.bullet_x - enemy[0])**2 + 
                          (self.bullet_y - enemy[1])**2)**0.5
                
                if distance < 20:  # If bullet is close enough to enemy
                    enemy[2] = False  # Mark enemy as dead
                    self.bullet_fired = False
                    self.bullet_y = config.PLAYER_START_Y
                    self.score += config.POINTS_PER_ENEMY
                    break

        # Check if all enemies are destroyed - respawn if so
        if all(not enemy[2] for enemy in self.enemies):
            self.respawn_enemies()

    def respawn_enemies(self) -> None:
        """Respawn all enemies when they are all destroyed."""
        for i in range(config.NUM_ENEMIES):
            self.enemies[i] = [
                100 + i * config.ENEMY_SPACING,
                config.ENEMY_START_Y,
                True
            ]
        self.enemy_direction = config.ENEMY_SPEED

    def draw(self) -> None:
        """Render all game elements to the screen."""
        # Clear screen
        self.screen.fill(config.COLOR_BACKGROUND)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, config.COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))

        # Draw player as a triangle (spaceship)
        player_points = [
            (self.player_x, self.player_y - config.PLAYER_SIZE),  # Top point
            (self.player_x - config.PLAYER_SIZE, self.player_y + config.PLAYER_SIZE),  # Bottom left
            (self.player_x + config.PLAYER_SIZE, self.player_y + config.PLAYER_SIZE)   # Bottom right
        ]
        pygame.draw.polygon(self.screen, config.COLOR_PLAYER, player_points)

        # Draw bullet
        if self.bullet_fired:
            pygame.draw.rect(
                self.screen,
                config.COLOR_BULLET,
                (self.bullet_x - config.BULLET_WIDTH // 2, 
                 self.bullet_y, 
                 config.BULLET_WIDTH, 
                 config.BULLET_HEIGHT)
            )

        # Draw enemies as squares
        for enemy in self.enemies:
            if enemy[2]:  # Only draw living enemies
                pygame.draw.rect(
                    self.screen,
                    config.COLOR_ENEMY,
                    (enemy[0] - config.ENEMY_SIZE, 
                     enemy[1] - config.ENEMY_SIZE,
                     config.ENEMY_SIZE * 2, 
                     config.ENEMY_SIZE * 2)
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
