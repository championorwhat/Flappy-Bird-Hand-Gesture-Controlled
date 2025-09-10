"""
Configuration file for Hand Gesture Flappy Bird
Contains all game settings and constants
"""

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 150, 255),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'GRAY': (128, 128, 128),
    'SKY_BLUE': (135, 206, 235)
}

# Game Physics
GRAVITY = 0.9
JUMP_STRENGTH = -11
PIPE_SPEED = 3
PIPE_GAP = 180
BIRD_RADIUS = 20

# Bird Settings
BIRD_START_X = 100
BIRD_START_Y = SCREEN_HEIGHT // 2

# Pipe Settings
PIPE_WIDTH = 50
PIPE_SPAWN_DELAY = 120  # frames between pipe spawns
PIPE_MIN_HEIGHT = 100
PIPE_MAX_HEIGHT = SCREEN_HEIGHT - PIPE_GAP - 100

# Camera Settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Hand Gesture Settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
FLAP_COOLDOWN = 300  # milliseconds between flaps
MIN_FINGERS_FOR_FLAP = 2

# Hand landmarks indices (MediaPipe)
HAND_LANDMARKS = {
    'WRIST': 0,
    'THUMB_TIP': 4,
    'INDEX_TIP': 8,
    'MIDDLE_TIP': 12,
    'RING_TIP': 16,
    'PINKY_TIP': 20,
    'THUMB_PIP': 3,
    'INDEX_PIP': 6,
    'MIDDLE_PIP': 10,
    'RING_PIP': 14,
    'PINKY_PIP': 18
}

FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIPS = [3, 6, 10, 14, 18]

# Font Settings
FONT_SIZE = 36
TITLE_FONT_SIZE = 48