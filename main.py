import pygame
import random
import time

# Initialize pygame
pygame.init()
font = pygame.font.Font(None, 36)  # Font for displaying score
start_time = time.time()  # Track when the game starts


# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLANE_SPEED = 3
BULLET_SPEED = 10
ENEMY_SPEED = 5
ENEMY_BULLET_SPEED = 10
HEALTH_DECREASE = 10
HEALTH_REGEN_AMOUNT = 50
HEALTH_REGEN_INTERVAL = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter Game")

# Load assets
plane_img = pygame.image.load("plane image png.png")
plane_img = pygame.transform.scale(plane_img, (70, 100))
enemy_plane_img = pygame.image.load("enemy_plane.png")
enemy_plane_img = pygame.transform.scale(enemy_plane_img, (50, 70))
enemy_plane_img = pygame.transform.rotate(enemy_plane_img, 180)

# Plane properties
plane_x, plane_y = WIDTH // 4, HEIGHT - 150
plane_health = 100
last_regen_time = time.time()
score = 0

def reset_game():
    global plane_x, plane_y, bullets, enemy_planes, enemy_bullets, plane_health
    global last_regen_time, score, game_over, start_time, difficulty  

    plane_x, plane_y = WIDTH // 4, HEIGHT - 150
    plane_health = 100
    bullets = []
    enemy_planes = []
    enemy_bullets = []
    last_regen_time = time.time()
    score = 0
    game_over = False
    start_time = time.time()  # Reset start time on restart
    difficulty = 1  # Reset difficulty


def check_collision():
    global plane_health, game_over
    for bullet in enemy_bullets[:]:
        if plane_x < bullet[0] + 10 and plane_x + 100 > bullet[0] and plane_y < bullet[1] + 10 and plane_y + 120 > bullet[1]:
            plane_health -= HEALTH_DECREASE
            enemy_bullets.remove(bullet)
    if plane_health <= 0:
        game_over = True
    return game_over



def check_bullet_hits():
    global bullets, enemy_planes, score
    for bullet in bullets[:]:
        for enemy in enemy_planes[:]:
            if bullet[0] < enemy[0] + 80 and bullet[0] + 10 > enemy[0] and bullet[1] < enemy[1] + 100 and bullet[1] + 5 > enemy[1]:
                bullets.remove(bullet)
                enemy_planes.remove(enemy)
                score += 1
                break

def regenerate_health():
    global plane_health, last_regen_time
    if time.time() - last_regen_time >= HEALTH_REGEN_INTERVAL:
        plane_health = min(100, plane_health + HEALTH_REGEN_AMOUNT)
        last_regen_time = time.time()

def draw_restart_button():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    restart_text = font.render("Restart", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(text, text_rect)
    screen.blit(restart_text, (WIDTH // 2 - 35, HEIGHT // 2 + 10))
    return button_rect

# Game loop
running = True
game_over = False
restart_button = None
bullets = []
enemy_planes = []
enemy_bullets = []


while running:
    pygame.time.delay(30)  # Frame delay
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullets.append([plane_x + 45, plane_y, 0, -BULLET_SPEED])
            elif event.key == pygame.K_z:
                bullets.append([plane_x + 45, plane_y, -BULLET_SPEED * 0.7, -BULLET_SPEED * 0.7])
            elif event.key == pygame.K_x:
                bullets.append([plane_x + 45, plane_y, BULLET_SPEED * 0.7, -BULLET_SPEED * 0.7])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_over and restart_button and restart_button.collidepoint(mouse_pos):
                reset_game()
    
    if not game_over:
        # Get key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and plane_x > 0:
            plane_x -= PLANE_SPEED
        if keys[pygame.K_RIGHT] and plane_x < WIDTH - 100:
            plane_x += PLANE_SPEED
        
        # Spawn enemy planes randomly (controlled frequency)
        if random.randint(1, 100) < 1:
           
            enemy_planes.append([enemy_x, enemy_y])

       
        spawn_chance = 3  # Adjust this value to control enemy spawn rate

        if random.randint(1, 100) < spawn_chance:  # Adjusted spawn chance check
            enemy_x = random.randint(50, WIDTH - 130)  # Define enemy_x here
            enemy_y = 0  # Enemy starts at the top
            enemy_planes.append([enemy_x, enemy_y])  # Add enemy to the list

        
        # Spawn enemy bullets
        for enemy in enemy_planes:
            if random.randint(1, 100) < 3:
                dx = plane_x - enemy[0]
                dy = plane_y - enemy[1]
                magnitude = max((dx ** 2 + dy ** 2) ** 0.5, 1)
                enemy_bullets.append([enemy[0] + 40, enemy[1] + 100, dx / magnitude * ENEMY_BULLET_SPEED, dy / magnitude * ENEMY_BULLET_SPEED])
        
        # Move bullets
        for bullet in bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
        bullets = [bullet for bullet in bullets if 0 < bullet[0] < WIDTH and bullet[1] > 0]
        
        # Move enemy planes
        for enemy in enemy_planes:
            enemy[1] += ENEMY_SPEED
        enemy_planes = [enemy for enemy in enemy_planes if enemy[1] < HEIGHT]
        
        # Move enemy bullets
        for bullet in enemy_bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
        enemy_bullets = [bullet for bullet in enemy_bullets if 0 < bullet[0] < WIDTH and 0 < bullet[1] < HEIGHT]
        
        # Check for bullet collisions
        check_bullet_hits()
        
        # Check for collision
        check_collision()
        
        # Regenerate health
        regenerate_health()
        
    else:
        restart_button = draw_restart_button()
    
    # Draw everything
    screen.blit(plane_img, (plane_x, plane_y))
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], 5, 7))
    for enemy in enemy_planes:
        screen.blit(enemy_plane_img, (enemy[0], enemy[1]))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 7))
    pygame.draw.rect(screen, RED, (20, 20, plane_health * 1, 10))
    score_text = font.render(f"Score: {score}", True, WHITE)  # Create score text
    screen.blit(score_text, (WIDTH - 150, 20))  # Draw text at the top-right

    pygame.display.update()



pygame.quit()