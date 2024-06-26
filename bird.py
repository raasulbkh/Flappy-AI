import pygame

BIRD_GRAVITY = 0.6
BIRD_JUMP = -10

class Bird:
    """
    Class representing the bird in the game.
    """

    def __init__(self, x, y, bird_imgs):
        self.x = x
        self.y = y
        self.velocity = 0
        self.img_index = 0
        self.img = bird_imgs[self.img_index]
        self.tick_count = 0
        self.height = self.y
        self.bird_imgs = bird_imgs

    def jump(self):
        """Make the bird jump by setting its velocity."""
        self.velocity = BIRD_JUMP
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """Update the bird's position based on gravity and velocity."""
        self.tick_count += 1
        self.velocity += BIRD_GRAVITY
        d = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.img_index < 25:
                self.img_index = 25
        else:
            if self.img_index > -90:
                self.img_index -= 20

        self.img_index = (self.img_index + 1) % 3
        self.img = self.bird_imgs[self.img_index]

    def draw(self, screen):
        """Draw the bird on the screen."""
        screen.blit(self.img, (self.x, self.y))
