import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Restartable Edition")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Constants
bird_x = 50
bird_radius = 20
gravity = 0.5
flap_strength = -10
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3

def draw_bird(y):
    pygame.draw.circle(screen, YELLOW, (bird_x, int(y)), bird_radius)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pipe["x"], 0, pipe_width, pipe["height"]))
        bottom_y = pipe["height"] + pipe_gap
        pygame.draw.rect(screen, GREEN, pygame.Rect(pipe["x"], bottom_y, pipe_width, HEIGHT - bottom_y))

def check_collision(bird_y, pipes):
    for pipe in pipes:
        pipe_rect_top = pygame.Rect(pipe["x"], 0, pipe_width, pipe["height"])
        pipe_rect_bottom = pygame.Rect(pipe["x"], pipe["height"] + pipe_gap, pipe_width, HEIGHT - (pipe["height"] + pipe_gap))
        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
        if pipe_rect_top.colliderect(bird_rect) or pipe_rect_bottom.colliderect(bird_rect):
            return True
    if bird_y > HEIGHT or bird_y < 0:
        return True
    return False

def show_score(score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def show_game_over():
    text = font.render("Game Over! Tap to Restart", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - 160, HEIGHT//2))

def reset_game():
    return {
        "bird_y": HEIGHT // 2,
        "bird_velocity": 0,
        "pipes": [{"x": WIDTH, "height": random.randint(100, HEIGHT - pipe_gap - 100)}],
        "score": 0,
        "game_over": False
    }

# --- GAME LOOP ---
game_data = reset_game()

running = True
while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_data["game_over"]:
                game_data = reset_game()
            else:
                game_data["bird_velocity"] = flap_strength

    if not game_data["game_over"]:
        # Bird physics
        game_data["bird_velocity"] += gravity
        game_data["bird_y"] += game_data["bird_velocity"]

        # Move pipes
        for pipe in game_data["pipes"]:
            pipe["x"] -= pipe_velocity

        # Add new pipes
        if game_data["pipes"][-1]["x"] < WIDTH - 200:
            game_data["pipes"].append({
                "x": WIDTH,
                "height": random.randint(100, HEIGHT - pipe_gap - 100)
            })

        # Remove pipes and update score
        if game_data["pipes"][0]["x"] < -pipe_width:
            game_data["pipes"].pop(0)
            game_data["score"] += 1

        # Collision check
        if check_collision(game_data["bird_y"], game_data["pipes"]):
            game_data["game_over"] = True

    # Drawing everything
    draw_bird(game_data["bird_y"])
    draw_pipes(game_data["pipes"])
    show_score(game_data["score"])
    
    if game_data["game_over"]:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
