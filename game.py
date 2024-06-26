import pygame
from bird import Bird
from pipe import Pipe
import sys

class FlappyBirdGame:
    """
    Class representing the Flappy Bird game.
    """
    def __init__(self, screen, assets):
        self.screen = screen
        self.bg_img, self.ground_img, self.bird_imgs, self.pipe_top_img, self.pipe_bottom_img, self.game_over_img, self.start_img = assets
        self.ground_y = 600 - self.ground_img.get_height()
        self.bird = Bird(50, 300, self.bird_imgs)
        self.pipes = [Pipe(400 + 200, self.pipe_top_img, self.pipe_bottom_img)]
        self.score = 0

    def draw_background(self):
        """Draw the background on the screen."""
        self.screen.blit(self.bg_img, (0, 0))

    def update_pipes(self):
        """Update the pipes' positions and check for collisions."""
        add_pipe = False
        rem = []
        for pipe in self.pipes:
            pipe.move()
            if pipe.collide(self.bird):
                return False
            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                add_pipe = True
            if pipe.x + 52 < 0:
                rem.append(pipe)
        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(400, self.pipe_top_img, self.pipe_bottom_img))
        for r in rem:
            self.pipes.remove(r)
        return True

    def run(self):
        """Run the game loop."""
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.jump()

            self.bird.move()
            run = self.update_pipes()
            if self.bird.y + self.bird.img.get_height() >= self.ground_y or self.bird.y < 0:
                run = False

            self.draw_background()
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.bird.draw(self.screen)
            self.screen.blit(self.ground_img, (0, self.ground_y))

            font = pygame.font.SysFont(None, 35)
            score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.update()
            clock.tick(30)
