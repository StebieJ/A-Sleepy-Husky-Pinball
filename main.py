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
ball_ready = False
score = 0
# Bumper settings
bumper_x = 400
bumper_y = 200
bumper_radius = 30

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
                

    screen.fill((0, 0, 0))

    # Move the ball
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

    # Check if ball hits the bumper
    distance = math.sqrt((ball_x - bumper_x) ** 2 + (ball_y - bumper_y) ** 2)

    if distance <= ball_radius + bumper_radius:
        ball_speed_y *= -1
        score += 25

    # Reset ball if it falls below the screen
    if ball_y > HEIGHT + ball_radius:
        ball_x = 400
        ball_y = 500
        ball_speed_x = 0
        ball_speed_y = 0
        ball_ready = True
    # Draw bumper
    pygame.draw.circle(screen, (255, 0, 255), (bumper_x, bumper_y), bumper_radius)
    # Draw the ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Win condition
    if score >= 250:
        running = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()