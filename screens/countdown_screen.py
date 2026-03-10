# File Name: countdown_screen.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# The purpose of this file is to display a 3-2-1-GO! countdown sequence before each
# round begins, then signal the main game to start.
# ----------------------------------------------------------------------------------------

import pygame
import sys

WIDTH, HEIGHT = 960, 540
FPS = 60


def run(screen, clock, level_num=1):
    """Display the countdown sequence (3, 2, 1, GO!) then return "done".

    Args:
        screen:    The pygame display surface passed in from the main game.
        clock:     The pygame Clock used for framerate control.
        level_num: The level number about to start, displayed above the countdown.

    Returns:
        "done" once the full countdown finishes.
    """
    
    # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_color = (30, 30, 30)  # Fallback color — remove this line once background image is set

    font_number = pygame.font.Font(None, 220)
    font_go     = pygame.font.Font(None, 160)
    font_level  = pygame.font.Font(None, 72)

    # Each entry: (label_text, display_duration_ms)
    countdown_steps = [("3", 1000), ("2", 1000), ("1", 1000), ("GO!", 800)]
    step_index = 0
    step_start = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()
        if now - step_start >= countdown_steps[step_index][1]:
            step_index += 1
            step_start = now
            if step_index >= len(countdown_steps):
                return "done"

        label = countdown_steps[step_index][0]
        font  = font_go if label == "GO!" else font_number
        color = (255, 220, 0) if label == "GO!" else (255, 255, 255)

        screen.fill(background_color)      # Remove this line once background image is set

        level_surf = font_level.render(f"LEVEL {level_num}", True, (255, 180, 0))
        screen.blit(level_surf, level_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140)))

        text_surf = font.render(label, True, color)
        screen.blit(text_surf, text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER - Countdown")
    _clock = pygame.time.Clock()
    run(_screen, _clock, level_num=1)
    pygame.quit()
