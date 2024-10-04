import pygame
import sys
from settings import *
from sprites import Player
from levels import Level
from utils import draw_health_bar, camera_follow, game_over_screen, display_score

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Side-Scrolling Game")

# Load Font
font = pygame.font.Font(None, 36)


def main():
    # Initialize the game state
    clock = pygame.time.Clock()
    player = Player()
    level = Level(1)  # Start at Level 1
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    level.update(player, enemies, collectibles)

    score = 0
    camera_x, camera_y = 0, 0

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle shooting and restarting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not game_over:  # Shoot only when not in Game Over state
                    player.shoot()
                if game_over and event.key == pygame.K_r:  # Restart game if 'R' is pressed during Game Over
                    main()

        if not game_over:
            # Update player, enemies, and collectibles
            level.update(player, enemies, collectibles)
            player.update()
            enemies.update()
            collectibles.update()

            # Check for collisions between projectiles and enemies
            hits = pygame.sprite.groupcollide(enemies, player.projectiles, True, True)
            score += len(hits) * 10  # Increase score by 10 for each enemy hit

            # Check if player's health reaches zero and decrease life
            if player.health <= 0:
                player.lives -= 1
                player.health = PLAYER_HEALTH  # Reset health if a life is lost

            # Check for game over condition
            if player.lives <= 0:
                game_over = True

            # Update the camera position
            camera_x, camera_y = camera_follow(player)

            # Draw everything with the camera offset
            screen.fill((135, 206, 250))  # Sky blue background
            # Offset all elements based on the camera position
            level.draw(screen, camera_x, camera_y)

            player.draw(screen, camera_x, camera_y)

            # Draw player projectiles with the camera offset
            for projectile in player.projectiles:
                screen.blit(projectile.image, (projectile.rect.x + camera_x, projectile.rect.y + camera_y))

            # Draw health bars and score
            draw_health_bar(screen, player.rect.x + camera_x, player.rect.y + camera_y - 20, player.health, PLAYER_HEALTH)
            display_score(screen, score, font)

        else:
            # Draw the Game Over screen
            game_over_screen(screen, score, font)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
