import os
import sys
import pygame
import neat
import pickle

from bird import Bird
from pipe import Pipe
from utils import load_images, draw_background

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)

# Game settings
BIRD_X = 50
BIRD_Y = 300
PIPE_WIDTH = 52
PIPE_GAP = 83
PIPE_VELOCITY = -4

# Load images
bg_img, ground_img, bird_imgs, pipe_top_img, pipe_bottom_img, game_over_img, start_img = load_images()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

generation = 0
high_score = 50  # Define a high score threshold to stop training

def eval_genomes(genomes, config):
    """
    Evaluate the genomes to determine the fitness of each bird.
    """
    global generation
    generation += 1

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(BIRD_X, BIRD_Y, bird_imgs))
        ge.append(genome)

    pipes = [Pipe(SCREEN_WIDTH + 200, pipe_top_img, pipe_bottom_img)]
    ground_y = SCREEN_HEIGHT - ground_img.get_height()
    score = 0
    run = True
    ticks_per_frame = 5  # Number of game ticks to simulate per frame for timelapse effect

    while run and len(birds) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for _ in range(ticks_per_frame):
            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.05  # Decreased fitness gain per frame

                output = nets[x].activate((bird.y, abs(bird.y - pipes[0].height), abs(bird.y - pipes[0].bottom)))

                if output[0] > 0.5:
                    bird.jump()

            add_pipe = False
            rem = []
            for pipe in pipes:
                pipe.move()
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        ge[x].fitness -= 1
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + PIPE_WIDTH < 0:
                    rem.append(pipe)

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(SCREEN_WIDTH, pipe_top_img, pipe_bottom_img))

            for r in rem:
                pipes.remove(r)

            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= ground_y or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            # Break if the score reaches the high score threshold
            if score >= high_score:
                break

        draw_background(screen, bg_img)
        for pipe in pipes:
            pipe.draw(screen)
        for bird in birds:
            bird.draw(screen)
        screen.blit(ground_img, (0, ground_y))

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f'Score: {score}', True, BLACK)
        gen_text = font.render(f'Generation: {generation}', True, BLACK)
        alive_text = font.render(f'Alive: {len(birds)}', True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(gen_text, (10, 50))
        screen.blit(alive_text, (10, 90))

        pygame.display.update()
        clock.tick(30)  # Control the actual rendering speed

        # Save the best genome if score reaches the high score threshold
        if score >= high_score:
            with open('best_genome.pickle', 'wb') as f:
                pickle.dump(ge[0], f)
            break

def run(config_file):
    """
    Run the NEAT algorithm to train the birds to play Flappy Bird.
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    # Save the best genome
    with open('best_genome.pickle', 'wb') as f:
        pickle.dump(winner, f)

def run_best_genome(config_file):
    """
    Load and run the best genome.
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)

    with open('best_genome.pickle', 'rb') as f:
        best_genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    bird = Bird(BIRD_X, BIRD_Y, bird_imgs)

    pipes = [Pipe(SCREEN_WIDTH + 200, pipe_top_img, pipe_bottom_img)]
    ground_y = SCREEN_HEIGHT - ground_img.get_height()
    score = 0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bird.move()
        output = net.activate((bird.y, abs(bird.y - pipes[0].height), abs(bird.y - pipes[0].bottom)))

        if output[0] > 0.5:
            bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                run = False

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + PIPE_WIDTH < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(SCREEN_WIDTH, pipe_top_img, pipe_bottom_img))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= ground_y or bird.y < 0:
            run = False

        draw_background(screen, bg_img)
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)
        screen.blit(ground_img, (0, ground_y))

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)  # Control the actual rendering speed

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    if len(sys.argv) > 1 and sys.argv[1] == "run_best":
        run_best_genome(config_path)
    else:
        run(config_path)
