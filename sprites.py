import pygame
from settings import *

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))  # Represent player tank as a rectangle
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP
        self.health = PLAYER_HEALTH
        self.lives = PLAYER_LIVES
        self.velocity_y = 0
        self.on_ground = False
        self.projectiles = pygame.sprite.Group()  # Group to store player's projectiles

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:  # Jump
            self.velocity_y = -self.jump_power
            self.on_ground = False

        # Apply gravity
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Simple ground collision
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.velocity_y = 0

        # Update projectiles
        self.projectiles.update()

    def shoot(self):
        """Shoot a projectile from the player tank."""
        projectile = Projectile(self.rect.right, self.rect.centery)
        self.projectiles.add(projectile)

    def draw(self, screen, camera_x, camera_y):
        """Draw player and its projectiles with the camera offset."""
        screen.blit(self.image, (self.rect.x + camera_x, self.rect.y + camera_y))
        self.projectiles.draw(screen)

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # Small rectangle for projectile
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10  # Speed of the projectile

    def update(self):
        """Move the projectile to the right."""
        self.rect.x += self.speed

        # Remove projectile if it goes off screen
        if self.rect.left > WIDTH:
            self.kill()


# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x -= self.speed  # Move left continuously


# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if self.type == "health":
            self.image.fill(GREEN)
        elif self.type == "life":
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
