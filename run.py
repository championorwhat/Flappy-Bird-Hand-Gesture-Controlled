#!/usr/bin/env python3
"""
Quick run script for Hand Gesture Flappy Bird
Alternative to main.py with additional checks
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['pygame', 'cv2', 'mediapipe', 'numpy']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall with: pip install -r requirements.txt")
        return False

    print("✅ All dependencies found!")
    return True

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            print("✅ Camera detected and working!")
            return True
        else:
            print("⚠️  Camera detected but not working properly")
            return False
    except:
        print("⚠️  Camera not available - keyboard controls will be used")
        return False

def main():
    print("🖐️ Hand Gesture Flappy Bird - Quick Run")
    print("=" * 40)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check camera
    camera_ok = check_camera()

    print()
    if camera_ok:
        print("🎮 Starting game with hand gesture control...")
    else:
        print("🎮 Starting game with keyboard control...")
        print("   Use SPACE to flap the bird!")

    print("   Press Q to quit")
    print("=" * 40)

    # Add src to path and run game
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

    try:
        from game_engine import HandGestureFlappyBird
        game = HandGestureFlappyBird()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running game: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check camera permissions")
        print("3. Try running: python main.py")

if __name__ == "__main__":
    main()