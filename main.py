import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Adventure")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)       # Enemies
BLUE = (0, 0, 255)      # Boss and life collectibles
GREEN = (0, 255, 0)     # Player and health collectibles
YELLOW = (255, 255, 0)  # Projectiles
SKY_BLUE = (135, 206, 235)  # Sky background
LIGHT_SKY_BLUE = (135, 206, 250)
DEEP_SKY_BLUE = (0, 191, 255)
BLACK = (0, 0, 0)

# Background colors for levels
background_colors = [SKY_BLUE, LIGHT_SKY_BLUE, DEEP_SKY_BLUE]
max_levels = 3

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(GREEN)  # Animal hero is green
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 4
        self.rect.bottom = HEIGHT - 50
        self.speed = 7  # Increased speed
        self.jump_power = 20  # Increased jump power
        self.vel_y = 0
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.lives = 3
        self.score = 0
        self.damage = 25  # Damage the player can inflict

    def update(self):
        self.apply_gravity()
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += 0.6  # Reduced gravity effect
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 12  # Increased projectile speed
        self.damage = 25

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=50, speed=3):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)  # Human enemies are red
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speed = speed
        self.health = health
        self.max_health = health

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Boss Enemy class (inherits from Enemy)
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=200, speed=3)
        self.image = pygame.Surface((100, 160))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type='health'):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        if type == 'health':
            self.image.fill(GREEN)
        elif type == 'life':
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass  # Collectibles do not move

# Draw health bar
def draw_health_bar(surface, x, y, health, max_health):
    BAR_WIDTH = 50
    BAR_HEIGHT = 5
    fill = (health / max_health) * BAR_WIDTH
    border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, RED, fill_rect)
    pygame.draw.rect(surface, WHITE, border_rect, 1)

# Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Level management
level = 1
level_completed = False

levels = [
    {'enemy_health': 50, 'enemy_speed_range': (3, 5), 'enemy_spawn_rate': 100},
    {'enemy_health': 75, 'enemy_speed_range': (4, 6), 'enemy_spawn_rate': 80},
    {'enemy_health': 100, 'enemy_speed_range': (5, 7), 'enemy_spawn_rate': 60},
]

def spawn_enemy():
    enemy_health = current_level['enemy_health']
    enemy_speed = random.randint(*current_level['enemy_speed_range'])
    enemy = Enemy(WIDTH + random.randint(0, 300), HEIGHT - 50, health=enemy_health, speed=enemy_speed)
    all_sprites.add(enemy)
    enemies.add(enemy)

def spawn_collectible():
    collectible_type = random.choice(['health', 'life'])
    collectible = Collectible(WIDTH + random.randint(0, 300), random.randint(100, HEIGHT - 100), collectible_type)
    all_sprites.add(collectible)
    collectibles.add(collectible)

def spawn_boss():
    boss = BossEnemy(WIDTH + 100, HEIGHT - 50)
    all_sprites.add(boss)
    enemies.add(boss)

# Game over function
def game_over_screen():
    font = pygame.font.SysFont(None, 60)
    text = font.render('Game Over! Press R to Restart', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Main game loop
enemy_timer = 0
collectible_timer = 0
camera_offset_x = 0

running = True
game_over = False

while running:
    clock.tick(60)  # 60 FPS

    if not game_over:
        current_level = levels[level - 1]

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_z:
                    player.shoot()

        # Spawn enemies and collectibles periodically
        enemy_timer += 1
        if enemy_timer > current_level['enemy_spawn_rate']:
            if level < max_levels:
                spawn_enemy()
            elif level == max_levels and not level_completed:
                spawn_boss()
                level_completed = True
            enemy_timer = 0

        collectible_timer += 1
        if collectible_timer > 200:
            spawn_collectible()
            collectible_timer = 0

        # Update
        all_sprites.update()

        # Collision detection
        # Projectiles hitting enemies
        hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)
        for enemy in hits:
            enemy.health -= player.damage
            if enemy.health <= 0:
                enemy.kill()
                player.score += 10

        # Enemies hitting player
        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in enemy_hits:
            player.health -= 1
            if player.health <= 0:
                player.lives -= 1
                player.health = player.max_health
                if player.lives <= 0:
                    game_over = True

        # Player collecting collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for item in collected:
            if item.type == 'health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif item.type == 'life':
                player.lives += 1
            player.score += 5

        # Level progression
        if player.score >= level * 100 and level < max_levels:
            level += 1

        # Dynamic camera (follows player smoothly)
        desired_camera_x = -player.rect.x + WIDTH // 4
        camera_offset_x += (desired_camera_x - camera_offset_x) * 0.1

        # Drawing
        SCREEN.fill(background_colors[level - 1])

        for sprite in all_sprites:
            SCREEN.blit(sprite.image, (sprite.rect.x + camera_offset_x, sprite.rect.y))
            if isinstance(sprite, Enemy):
                draw_health_bar(SCREEN, sprite.rect.x + camera_offset_x, sprite.rect.y - 10, sprite.health, sprite.max_health)

        # HUD
        font = pygame.font.SysFont(None, 30)
        lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
        score_text = font.render(f'Score: {player.score}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        health_text = font.render(f'Health:', True, WHITE)
        SCREEN.blit(lives_text, (10, 10))
        SCREEN.blit(score_text, (10, 40))
        SCREEN.blit(level_text, (10, 70))
        SCREEN.blit(health_text, (10, 100))
        draw_health_bar(SCREEN, 80, 105, player.health, player.max_health)

        pygame.display.flip()

    else:
        game_over_screen()
        # Reset game state
        game_over = False
        level = 1
        player.health = player.max_health
        player.lives = 3
        player.score = 0
        level_completed = False
        all_sprites.empty()
        enemies.empty()
        projectiles.empty()
        collectibles.empty()
        player = Player()
        all_sprites.add(player)

pygame.quit()
