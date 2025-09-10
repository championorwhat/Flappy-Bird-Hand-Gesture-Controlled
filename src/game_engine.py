"""
Main Game Engine
Handles game loop, states, and coordination between components
"""

import pygame
import cv2
import sys
from enum import Enum

from config import *
from hand_gesture_detector import HandGestureDetector
from game_objects import Bird, Pipe, ScoreManager, Background

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class HandGestureFlappyBird:
    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()

        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hand Gesture Flappy Bird")

        # Game timing
        self.clock = pygame.time.Clock()

        # Game state
        self.game_state = GameState.MENU
        self.last_flap_time = 0

        # Game objects
        self.bird = Bird()
        self.pipes = []
        self.score_manager = ScoreManager()
        self.background = Background()

        # Pipe spawning
        self.pipe_spawn_timer = 0

        # Initialize camera and hand detection
        self.setup_camera_and_detection()

        # Fonts
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)

    def setup_camera_and_detection(self):
        """Setup camera and hand gesture detection"""
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

            # Test camera
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Camera not accessible")

            self.hand_detector = HandGestureDetector()
            self.camera_available = True
            print("Camera and hand detection initialized successfully!")

        except Exception as e:
            print(f"Warning: Camera setup failed - {e}")
            print("Game will run without hand gesture control.")
            print("Use SPACE key to play instead.")
            self.camera_available = False
            self.cap = None
            self.hand_detector = None

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.start_game()
                    elif self.game_state == GameState.PLAYING:
                        self.bird.update(should_flap=True)

                elif event.key == pygame.K_r and self.game_state == GameState.GAME_OVER:
                    self.restart_game()

                elif event.key == pygame.K_p and self.game_state == GameState.PLAYING:
                    self.game_state = GameState.PAUSED

                elif event.key == pygame.K_p and self.game_state == GameState.PAUSED:
                    self.game_state = GameState.PLAYING

                elif event.key == pygame.K_q:
                    return False

                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PAUSED:
                        self.game_state = GameState.PLAYING
                    else:
                        self.game_state = GameState.MENU

        return True

    def process_hand_gestures(self):
        """Process camera input for hand gestures"""
        if not self.camera_available or not self.cap:
            return False

        ret, frame = self.cap.read()
        if not ret:
            return False

        # Mirror the frame for natural interaction
        frame = cv2.flip(frame, 1)

        # Detect hand gestures
        gesture_data = self.hand_detector.process_frame(frame)

        # Display camera feed with hand tracking
        cv2.imshow("Hand Tracking - Flappy Bird Control", gesture_data['frame'])

        # Add instructions to camera window
        instructions = [
            "Hand Gesture Controls:",
            "Raise 2+ fingers = Flap",
            "Peace sign = Flap", 
            "Thumbs up = Flap",
            "Press Q = Quit"
        ]

        for i, instruction in enumerate(instructions):
            cv2.putText(
                gesture_data['frame'],
                instruction,
                (10, CAMERA_HEIGHT - 120 + i * 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        # Handle flap with cooldown
        should_flap = False
        if gesture_data['should_flap']:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_flap_time > FLAP_COOLDOWN:
                should_flap = True
                self.last_flap_time = current_time

        return should_flap

    def start_game(self):
        """Start a new game"""
        self.game_state = GameState.PLAYING
        self.bird.reset()
        self.pipes = []
        self.pipe_spawn_timer = 0
        self.score_manager.reset_score()

        # Spawn first pipe
        self.pipes.append(Pipe(SCREEN_WIDTH + 200))

    def restart_game(self):
        """Restart the game"""
        self.start_game()

    def update_game_playing(self, should_flap_gesture):
        """Update game when in playing state"""
        # Update bird
        self.bird.update(should_flap_gesture)

        # Update background
        self.background.update()

        # Update pipes
        for pipe in self.pipes[:]:  # Create copy to avoid modification during iteration
            pipe.update()

            # Check if bird passed pipe (for scoring)
            if pipe.is_bird_passed(self.bird.x):
                pipe.passed = True
                self.score_manager.update_score()

            # Remove off-screen pipes
            if pipe.is_off_screen():
                self.pipes.remove(pipe)

        # Spawn new pipes
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= PIPE_SPAWN_DELAY:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_spawn_timer = 0

        # Check collisions
        self.check_collisions()

    def check_collisions(self):
        """Check for collisions between bird and pipes/ground"""
        bird_rect = self.bird.get_rect()

        # Check ground collision
        if self.bird.y + self.bird.radius >= SCREEN_HEIGHT:
            self.game_state = GameState.GAME_OVER
            return

        # Check pipe collisions
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_collision_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                self.game_state = GameState.GAME_OVER
                return

    def draw_menu(self):
        """Draw menu screen"""
        self.background.draw(self.screen)

        # Title
        title_text = self.title_font.render("Hand Gesture", True, COLORS['WHITE'])
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        )
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.title_font.render("Flappy Bird", True, COLORS['YELLOW'])
        subtitle_rect = subtitle_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

        # Instructions
        instructions = [
            "Controls:",
            "🖐️ Raise 2+ fingers to flap",
            "✌️ Peace sign to flap", 
            "👍 Thumbs up to flap",
            "⌨️ Or use SPACE key",
            "",
            "Press SPACE to start"
        ]

        for i, instruction in enumerate(instructions):
            color = COLORS['WHITE'] if instruction else COLORS['WHITE']
            if "SPACE to start" in instruction:
                color = COLORS['GREEN']

            instruction_text = self.font.render(instruction, True, color)
            instruction_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20 + i * 30)
            )
            self.screen.blit(instruction_text, instruction_rect)

        # Camera status
        camera_status = "📷 Camera: Ready" if self.camera_available else "📷 Camera: Not Available"
        camera_color = COLORS['GREEN'] if self.camera_available else COLORS['RED']
        camera_text = self.font.render(camera_status, True, camera_color)
        self.screen.blit(camera_text, (10, SCREEN_HEIGHT - 30))

    def draw_playing(self):
        """Draw game during play"""
        # Draw background
        self.background.draw(self.screen)

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw bird
        self.bird.draw(self.screen)

        # Draw score
        self.score_manager.draw_score(self.screen)

        # Draw gesture status
        if self.camera_available:
            gesture_text = self.font.render("👋 Gesture Control Active", True, COLORS['GREEN'])
            self.screen.blit(gesture_text, (SCREEN_WIDTH - 250, 10))

    def draw_paused(self):
        """Draw paused screen"""
        self.draw_playing()  # Draw game state

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.title_font.render("PAUSED", True, COLORS['WHITE'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        resume_text = self.font.render("Press P to resume", True, COLORS['WHITE'])
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, resume_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        self.background.draw(self.screen)
        self.score_manager.draw_game_over(self.screen)

    def draw(self):
        """Main drawing function"""
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_playing()
        elif self.game_state == GameState.PAUSED:
            self.draw_paused()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True

        while running:
            # Handle events
            running = self.handle_events()
            if not running:
                break

            # Process hand gestures
            should_flap_gesture = False
            if self.game_state in [GameState.PLAYING, GameState.MENU]:
                should_flap_gesture = self.process_hand_gestures()

                # Start game with gesture if in menu
                if should_flap_gesture and self.game_state == GameState.MENU:
                    self.start_game()

            # Update game state
            if self.game_state == GameState.PLAYING:
                self.update_game_playing(should_flap_gesture)

            # Draw everything
            self.draw()

            # Control frame rate
            self.clock.tick(FPS)

            # Check for camera window close
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        print("Game closed. Thanks for playing!")