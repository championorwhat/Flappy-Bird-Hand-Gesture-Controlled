#!/usr/bin/env python3
"""
Hand Gesture Controlled Flappy Bird Game
Main game entry point

Author: AI Assistant
Requirements: Python 3.9+, OpenCV, MediaPipe, Pygame
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game_engine import HandGestureFlappyBird

def main():
    """Main function to start the game"""
    try:
        print("Starting Hand Gesture Flappy Bird...")
        print("Make sure your camera is connected and working!")
        print("Controls:")
        print("  - Raise 2+ fingers to make the bird flap")
        print("  - Keep hand in view of camera")
        print("  - Press Q in camera window to quit")
        print("  - Press SPACE to start game")
        print("  - Press R to restart after game over")
        print("-" * 50)

        game = HandGestureFlappyBird()
        game.run()

    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have installed all requirements:")
        print("pip install -r requirements.txt")
    finally:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()
