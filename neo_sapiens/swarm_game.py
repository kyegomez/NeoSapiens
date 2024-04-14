import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
ENEMY_SPAWN_RATE = 25  # Lower is faster

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Swarm Attack")

# Player
player_img = pygame.Surface((50, 30))
player_img.fill(WHITE)
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 60

# Bullets
bullets = []

# Enemies
enemies = []

# Clock
clock = pygame.time.Clock()


def move_player(dx):
    global player_x
    player_x += dx * PLAYER_SPEED
    player_x = max(0, min(SCREEN_WIDTH - 50, player_x))


def fire_bullet():
    bullets.append([player_x + 25, player_y - 20])


def move_bullets():
    for bullet in bullets:
        bullet[1] -= BULLET_SPEED
    # Remove bullets that go off the screen
    while bullets and bullets[0][1] < 0:
        bullets.pop(0)


def spawn_enemy():
    if random.randint(1, ENEMY_SPAWN_RATE) == 1:
        enemy_x = random.randint(0, SCREEN_WIDTH - 50)
        enemies.append([enemy_x, -30])


def move_enemies():
    for enemy in enemies:
        enemy[1] += ENEMY_SPEED
    # Remove enemies that go off the screen
    while enemies and enemies[0][1] > SCREEN_HEIGHT:
        enemies.pop(0)


def check_collisions():
    global enemies
    for bullet in bullets:
        for enemy in enemies:
            if (enemy[0] < bullet[0] < enemy[0] + 50) and (
                enemy[1] < bullet[1] < enemy[1] + 30
            ):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break


def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_player(-1)
                elif event.key == pygame.K_RIGHT:
                    move_player(1)
                elif event.key == pygame.K_SPACE:
                    fire_bullet()

        move_bullets()
        spawn_enemy()
        move_enemies()
        check_collisions()

        screen.fill(BLACK)
        screen.blit(player_img, (player_x, player_y))
        for bullet in bullets:
            pygame.draw.rect(
                screen, WHITE, (bullet[0], bullet[1], 2, 10)
            )
        for enemy in enemies:
            pygame.draw.rect(
                screen, RED, (enemy[0], enemy[1], 50, 30)
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


game_loop()
