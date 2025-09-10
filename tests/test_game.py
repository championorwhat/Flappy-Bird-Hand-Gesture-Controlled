"""
Simple tests for Hand Gesture Flappy Bird
Run with: python -m pytest tests/
"""

import sys
import os
import pytest
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all modules can be imported"""
    try:
        import config
        import game_objects
        import hand_gesture_detector
        import game_engine
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_config_values():
    """Test configuration values"""
    import config

    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert config.FPS > 0
    assert config.GRAVITY > 0
    assert config.BIRD_RADIUS > 0

def test_bird_creation():
    """Test bird object creation"""
    from game_objects import Bird

    bird = Bird()
    assert bird.x == 100
    assert bird.y == 300  # SCREEN_HEIGHT // 2
    assert bird.velocity == 0
    assert bird.radius == 20

def test_pipe_creation():
    """Test pipe object creation"""
    from game_objects import Pipe

    pipe = Pipe(400)
    assert pipe.x == 400
    assert pipe.width == 50
    assert pipe.gap_start > 0
    assert pipe.gap_end > pipe.gap_start

def test_score_manager():
    """Test score manager functionality"""
    from game_objects import ScoreManager

    score_manager = ScoreManager()
    assert score_manager.score == 0

    score_manager.update_score()
    assert score_manager.score == 1

    score_manager.reset_score()
    assert score_manager.score == 0

def test_finger_tips_config():
    """Test hand landmark configuration"""
    import config

    assert len(config.FINGER_TIPS) == 5
    assert len(config.FINGER_PIPS) == 5
    assert all(tip > pip for tip, pip in zip(config.FINGER_TIPS, config.FINGER_PIPS))

if __name__ == "__main__":
    pytest.main([__file__])