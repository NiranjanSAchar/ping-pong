import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Initialize mixer for sound
        pygame.mixer.init()

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

        # Ball setup
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        """Move the ball and bounce off the top and bottom walls."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom edges
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.sound_wall.play()  # play bounce sound

    def check_collision(self, player, ai):
        """Check for collision with player and AI paddles and bounce properly."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Collision with player paddle
        if ball_rect.colliderect(player_rect):
            self.x = player_rect.right  # prevent overlap
            if self.velocity_x < 0:  # only reverse if moving toward paddle
                self.velocity_x = abs(self.velocity_x)
                self.sound_paddle.play()

            # Optional: add a little variation based on hit position
            offset = (self.y + self.height / 2) - player_rect.centery
            self.velocity_y += offset * 0.05

        # Collision with AI paddle
        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            if self.velocity_x > 0:  # only reverse if moving toward paddle
                self.velocity_x = -abs(self.velocity_x)
                self.sound_paddle.play()

            offset = (self.y + self.height / 2) - ai_rect.centery
            self.velocity_y += offset * 0.05

    def reset(self):
        """Reset ball to center and reverse direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.sound_score.play()  # play scoring sound

    def rect(self):
        """Return the ball’s current rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, color=(255, 255, 255)):
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, color, self.rect())