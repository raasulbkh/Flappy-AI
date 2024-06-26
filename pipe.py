import pygame
import random

PIPE_WIDTH = 52
PIPE_GAP = 83
PIPE_VELOCITY = -4

class Pipe:
    """
    Class representing the pipes in the game.
    """

    def __init__(self, x, pipe_top_img, pipe_bottom_img):
        self.x = x
        self.height = random.randint(50, 600 - PIPE_GAP - 150)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP
        self.passed = False
        self.pipe_top_img = pipe_top_img
        self.pipe_bottom_img = pipe_bottom_img

    def move(self):
        """Move the pipe leftward based on the pipe velocity."""
        self.x += PIPE_VELOCITY

    def draw(self, screen):
        """Draw the pipe on the screen."""
        screen.blit(self.pipe_top_img, (self.x, self.top - self.pipe_top_img.get_height()))
        screen.blit(self.pipe_bottom_img, (self.x, self.bottom))

    def collide(self, bird):
        """Check if the pipe collides with the bird."""
        bird_mask = pygame.mask.from_surface(bird.img)
        top_mask = pygame.mask.from_surface(self.pipe_top_img)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom_img)

        top_offset = (self.x - bird.x, self.top - round(bird.y) - self.pipe_top_img.get_height())
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False
