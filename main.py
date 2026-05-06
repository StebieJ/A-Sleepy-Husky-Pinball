import pygame
import sys
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Sleepy Husky Pinball")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Ball settings
ball_x = 400
ball_y = 300
ball_radius = 12
ball_speed_x = 3
ball_speed_y = 3
gravity = 0.03
ball_ready = True
score = 0

# Launcher position
launcher_x = 700
launcher_y = 535

# Flipper settings
left_flipper_down = [(230, 540), (350, 500), (360, 525), (240, 565)]
left_flipper_up = [(230, 540), (350, 470), (360, 495), (240, 565)]

right_flipper_down = [(570, 540), (450, 500), (440, 525), (560, 565)]
right_flipper_up = [(570, 540), (450, 470), (440, 495), (560, 565)]

# Bumper settings
bumpers = [
    {"x": 400, "y": 200, "radius": 30, "color": (255, 0, 255), "points": 25},
    {"x": 250, "y": 300, "radius": 30, "color": (0, 255, 255), "points": 50},
    {"x": 550, "y": 300, "radius": 30, "color": (150, 0, 255), "points": 75},
]

running = True
while running:
    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_ready:
                ball_speed_x = 5
                ball_speed_y = -6
                ball_ready = False
                

    # Check which keys are being held down
    keys = pygame.key.get_pressed()
   
    screen.fill((0, 0, 0))

    # Move the ball only after it has been launched
    if not ball_ready:
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        ball_speed_y += gravity

    # Bounce off left and right walls
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_speed_x *= -1
        score += 10

    # Bounce off the top wall only
    if ball_y <= ball_radius:
        ball_speed_y *= -1
        score += 10  

    # Check if ball hits any bumper
    for bumper in bumpers:
        distance_x = ball_x - bumper["x"]
        distance_y = ball_y - bumper["y"]
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance <= ball_radius + bumper["radius"]:
            ball_speed_x *= -1
            ball_speed_y *= -1
            score += bumper["points"]

            # Push the ball away so it does not score over and over
            ball_x += ball_speed_x * 3
            ball_y += ball_speed_y * 3

    # Reset ball if it falls below the screen
    if ball_y > HEIGHT + ball_radius:
        ball_x = launcher_x
        ball_y = launcher_y
        ball_speed_x = 0
        ball_speed_y = 0
        ball_ready = True
    
    # Draw all bumpers
    for bumper in bumpers:
        pygame.draw.circle(
           screen,
           bumper["color"],
           (bumper["x"], bumper["y"]),
           bumper["radius"]
    )
    
    # Draw sleepy launcher bed
    pygame.draw.rect(screen, (100, 50, 150), (650, 520, 100, 50), border_radius=15)

    # Draw launcher walls
    pygame.draw.rect(screen, (80, 80, 80), (640, 350, 10, 220))
    pygame.draw.rect(screen, (80, 80, 80), (750, 350, 10, 220))
    
    # Draw flippers
    if keys[pygame.K_a]:
        pygame.draw.polygon(screen, (0, 200, 255), left_flipper_up)
    else:
        pygame.draw.polygon(screen, (0, 200, 255), left_flipper_down)

    if keys[pygame.K_d]:
        pygame.draw.polygon(screen, (255, 0, 180), right_flipper_up)
    else:
        pygame.draw.polygon(screen, (255, 0, 180), right_flipper_down)
    
    # Draw the ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Win condition
    if score >= 1000:
        running = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()