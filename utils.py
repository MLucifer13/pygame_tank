import pygame
from settings import *

def draw_health_bar(screen, x, y, current_health, max_health):
    """Draw a health bar above a character (player or enemy)."""
    bar_width = 50
    bar_height = 7
    fill = (current_health / max_health) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)

    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)  # Outline the health bar

def camera_follow(player):
    """Create a smooth camera effect that follows the player."""
    # Center the player horizontally on the screen
    camera_x = -player.rect.x + WIDTH // 2
    # Keep the camera fixed vertically (for side-scrolling)
    camera_y = 0
    return camera_x, camera_y

def game_over_screen(screen, score, font):
    """Display the game over screen with score and restart option."""
    screen.fill((0, 0, 0))  # Black background
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Red game over text
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))  # White score text
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))  # White restart text

    # Draw text in the center of the screen
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

def display_score(screen, score, font):
    """Draw the current score on the top-left corner."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
