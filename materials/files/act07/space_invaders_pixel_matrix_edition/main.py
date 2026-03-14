"""
Space Invaders - Pixel Matrix Edition

Main entry point for the game.

This is a modern implementation of the classic Space Invaders arcade game,
featuring pixel-art sprites rendered from binary matrices.

Usage:
    python main.py

Controls:
    Arrow Keys/A/D - Move ship left/right
    Spacebar - Fire bullet
    P - Pause/unpause
    Q - Quit (with confirmation)

Author: Educational Project
License: Free to use and modify
"""

from game import Game


def main() -> None:
    """
    Entry point for the Space Invaders game.
    
    Initializes and runs the game loop.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
