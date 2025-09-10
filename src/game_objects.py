"""
Game Objects Module
Contains Bird and Pipe classes for the Flappy Bird game
"""

import pygame
import random
from config import *

class Bird:
    def __init__(self):
        """Initialize the bird object"""
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity = 0
        self.radius = BIRD_RADIUS

    def update(self, should_flap=False):
        """Update bird physics"""
        if should_flap:
            self.velocity = JUMP_STRENGTH

        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Keep bird within screen bounds
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.velocity = 0

    def draw(self, screen):
        """Draw the bird on screen"""
        # Draw bird body
        pygame.draw.circle(
            screen, 
            COLORS['YELLOW'], 
            (int(self.x), int(self.y)), 
            self.radius
        )

        # Draw bird outline
        pygame.draw.circle(
            screen, 
            COLORS['BLACK'], 
            (int(self.x), int(self.y)), 
            self.radius, 
            2
        )

        # Draw eye
        eye_x = int(self.x + self.radius // 3)
        eye_y = int(self.y - self.radius // 3)
        pygame.draw.circle(screen, COLORS['BLACK'], (eye_x, eye_y), 4)

        # Draw beak
        beak_points = [
            (int(self.x + self.radius), int(self.y)),
            (int(self.x + self.radius + 10), int(self.y - 5)),
            (int(self.x + self.radius + 10), int(self.y + 5))
        ]
        pygame.draw.polygon(screen, COLORS['RED'], beak_points)

    def get_rect(self):
        """Get collision rectangle for the bird"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def reset(self):
        """Reset bird to starting position"""
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity = 0

class Pipe:
    def __init__(self, x):
        """Initialize a pipe pair"""
        self.x = x
        self.width = PIPE_WIDTH
        self.gap_start = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        self.gap_end = self.gap_start + PIPE_GAP
        self.passed = False

    def update(self):
        """Update pipe position"""
        self.x -= PIPE_SPEED

    def draw(self, screen):
        """Draw the pipe pair on screen"""
        # Top pipe
        pygame.draw.rect(
            screen,
            COLORS['GREEN'],
            (self.x, 0, self.width, self.gap_start)
        )

        # Top pipe cap
        pygame.draw.rect(
            screen,
            COLORS['GREEN'],
            (self.x - 5, self.gap_start - 20, self.width + 10, 20)
        )

        # Bottom pipe
        pygame.draw.rect(
            screen,
            COLORS['GREEN'],
            (self.x, self.gap_end, self.width, SCREEN_HEIGHT - self.gap_end)
        )

        # Bottom pipe cap
        pygame.draw.rect(
            screen,
            COLORS['GREEN'],
            (self.x - 5, self.gap_end, self.width + 10, 20)
        )

        # Pipe outlines
        pygame.draw.rect(
            screen,
            COLORS['BLACK'],
            (self.x, 0, self.width, self.gap_start),
            2
        )
        pygame.draw.rect(
            screen,
            COLORS['BLACK'],
            (self.x, self.gap_end, self.width, SCREEN_HEIGHT - self.gap_end),
            2
        )

    def get_collision_rects(self):
        """Get collision rectangles for top and bottom pipes"""
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_start)
        bottom_rect = pygame.Rect(
            self.x, 
            self.gap_end, 
            self.width, 
            SCREEN_HEIGHT - self.gap_end
        )
        return top_rect, bottom_rect

    def is_off_screen(self):
        """Check if pipe is completely off screen"""
        return self.x + self.width < 0

    def is_bird_passed(self, bird_x):
        """Check if bird has passed this pipe"""
        return not self.passed and self.x + self.width < bird_x

class ScoreManager:
    def __init__(self):
        """Initialize score management"""
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)

    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass

    def update_score(self):
        """Increment score by 1"""
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def reset_score(self):
        """Reset current score"""
        self.save_high_score()
        self.score = 0

    def draw_score(self, screen):
        """Draw current score on screen"""
        score_text = self.font.render(f"Score: {self.score}", True, COLORS['WHITE'])
        screen.blit(score_text, (10, 10))

        high_score_text = self.font.render(f"High: {self.high_score}", True, COLORS['WHITE'])
        screen.blit(high_score_text, (10, 50))

    def draw_game_over(self, screen):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        screen.blit(overlay, (0, 0))

        # Game over title
        game_over_text = self.title_font.render("GAME OVER", True, COLORS['RED'])
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        screen.blit(game_over_text, game_over_rect)

        # Final score
        final_score_text = self.font.render(
            f"Score: {self.score}", True, COLORS['WHITE']
        )
        final_score_rect = final_score_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        screen.blit(final_score_text, final_score_rect)

        # High score
        high_score_text = self.font.render(
            f"Best: {self.high_score}", True, COLORS['YELLOW']
        )
        high_score_rect = high_score_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        )
        screen.blit(high_score_text, high_score_rect)

        # Instructions
        restart_text = self.font.render(
            "Press R to restart or Q to quit", True, COLORS['WHITE']
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        )
        screen.blit(restart_text, restart_rect)

class Background:
    def __init__(self):
        """Initialize scrolling background"""
        self.x1 = 0
        self.x2 = SCREEN_WIDTH
        self.speed = 1

    def update(self):
        """Update background scrolling"""
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def draw(self, screen):
        """Draw gradient background"""
        # Create gradient effect
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (200 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw some simple clouds
        cloud_color = (255, 255, 255, 100)
        for i in range(5):
            cloud_x = (self.x1 + i * 200) % (SCREEN_WIDTH + 100)
            cloud_y = 50 + i * 30
            pygame.draw.ellipse(
                screen, 
                COLORS['WHITE'], 
                (cloud_x, cloud_y, 80, 40)
            )
            pygame.draw.ellipse(
                screen, 
                COLORS['WHITE'], 
                (cloud_x + 20, cloud_y - 10, 60, 30)
            )