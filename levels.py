import pygame
from sprites import Enemy, Collectible
from settings import *

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()  # New: Group for platform tiles

        # Define the level length in pixels (longer than the screen width)
        self.length = 5000  # Increase this value to extend the level

        # Create the selected level
        if self.level_num == 1:
            self.create_level_1()
        elif self.level_num == 2:
            self.create_level_2()
        elif self.level_num == 3:
            self.create_level_3()

    def create_level_1(self):
        """Level 1: Create a basic level layout with enemies, tiles, and collectibles."""
        # Adding platforms (tiles)
        for x in range(0, self.length, 200):  # Generate tiles every 200 pixels
            tile = Tile(x, HEIGHT - 50)  # Adjust tile position as needed
            self.tiles.add(tile)

        # Add enemies at varying positions along the level
        for i in range(10):  # Add 10 enemies at different positions
            self.enemies.add(Enemy(600 + i * 400, HEIGHT - 100))

        # Add collectibles at specific points in the level
        self.collectibles.add(Collectible(1200, HEIGHT - 120, "health"))
        self.collectibles.add(Collectible(1600, HEIGHT - 120, "life"))
        self.collectibles.add(Collectible(2500, HEIGHT - 120, "health"))

    def update(self, player, enemies_group, collectibles_group):
        """Update enemies and collectible positions, handle collisions."""
        self.enemies.update()
        self.collectibles.update()

        # Check player collisions with enemies
        enemy_collisions = pygame.sprite.spritecollide(player, self.enemies, False)
        for enemy in enemy_collisions:
            player.health -= 10  # Deal damage on collision
            if player.health <= 0:
                player.health = 0

        # Check player collisions with collectibles
        collectible_collisions = pygame.sprite.spritecollide(player, self.collectibles, True)
        for item in collectible_collisions:
            if item.type == "health":
                player.health = min(PLAYER_HEALTH, player.health + 20)  # Boost health
            elif item.type == "life":
                player.lives += 1  # Extra life

        # Update global groups
        enemies_group.empty()
        collectibles_group.empty()
        enemies_group.add(self.enemies)
        collectibles_group.add(self.collectibles)

    def draw(self, screen, camera_x, camera_y):
        """Draw tiles, enemies, and collectibles with camera offset."""
        # Draw all tiles
        for tile in self.tiles:
            screen.blit(tile.image, (tile.rect.x + camera_x, tile.rect.y + camera_y))

        # Draw enemies
        self.enemies.draw(screen)
        # Draw collectibles
        self.collectibles.draw(screen)

# New: Tile class for platform generation
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((200, 50))  # Tile size
        self.image.fill((139, 69, 19))  # Brown color for the platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
