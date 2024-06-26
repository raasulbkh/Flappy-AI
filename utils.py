import pygame

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Pipe settings
PIPE_WIDTH = 52

def load_images():
    bg_img = pygame.image.load('assets/background.png')
    ground_img = pygame.image.load('assets/ground.png')
    bird_imgs = [
        pygame.image.load('assets/bird_up.png'),
        pygame.image.load('assets/bird_mid.png'),
        pygame.image.load('assets/bird_down.png')
    ]
    pipe_top_img = pygame.image.load('assets/pipe_top.png')
    pipe_bottom_img = pygame.image.load('assets/pipe_bottom.png')
    game_over_img = pygame.image.load('assets/game_over.png')
    start_img = pygame.image.load('assets/start.png')

    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, 100))
    bird_imgs = [pygame.transform.scale(img, (34, 24)) for img in bird_imgs]
    pipe_top_img = pygame.transform.scale(pipe_top_img, (PIPE_WIDTH, pipe_top_img.get_height()))
    pipe_bottom_img = pygame.transform.scale(pipe_bottom_img, (PIPE_WIDTH, pipe_bottom_img.get_height()))
    game_over_img = pygame.transform.scale(game_over_img, (200, 100))
    start_img = pygame.transform.scale(start_img, (200, 100))

    return bg_img, ground_img, bird_imgs, pipe_top_img, pipe_bottom_img, game_over_img, start_img

def draw_background(screen, bg_img):
    """Draw the background on the screen."""
    screen.blit(bg_img, (0, 0))

def draw_text(screen, text, x, y, color):
    """Draw text on the screen."""
    font = pygame.font.SysFont(None, 35)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
