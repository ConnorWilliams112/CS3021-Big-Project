# File Name: overlay.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# The purpose of this file is to draw a HUD overlay on top of the active game frame,
# displaying the player's score, remaining lives, ammo count, and round timer.
# Call overlay.draw() once per frame after drawing the game world.
# ----------------------------------------------------------------------------------------

import pygame

WIDTH, HEIGHT = 960, 540

# TODO: Replace the paths below with the actual HUD icon image file paths
# HEART_ICON = pygame.transform.scale(
#     pygame.image.load("PATH_TO_IMAGE/heart_icon.png").convert_alpha(), (28, 28))
# AMMO_ICON = pygame.transform.scale(
#     pygame.image.load("PATH_TO_IMAGE/ammo_icon.png").convert_alpha(), (22, 28))

_score_font = None
_timer_font = None
_hud_font   = None


def _init_fonts():
    """Lazy-initialize fonts so this module can be imported before pygame.init()."""
    global _score_font, _timer_font, _hud_font
    if _score_font is None:
        _score_font = pygame.font.Font(None, 48)
        _timer_font = pygame.font.Font(None, 56)
        _hud_font   = pygame.font.Font(None, 36)


def draw(screen, score=0, lives=3, ammo=10, time_remaining=60):
    """Draw the HUD overlay on top of the current game frame.

    Args:
        screen:         The pygame surface to draw onto.
        score:          The player's current score.
        lives:          Number of lives remaining.
        ammo:           Number of shots remaining.
        time_remaining: Seconds left in the round (float or int).
    """
    _init_fonts()

    # Semi-transparent top bar
    bar = pygame.Surface((WIDTH, 62), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 150))
    screen.blit(bar, (0, 0))

    # Score — top-left
    score_surf = _score_font.render(f"Score: {score}", True, (255, 220, 0))
    screen.blit(score_surf, (18, 10))

    # Timer — top-center
    mins = int(time_remaining) // 60
    secs = int(time_remaining) % 60
    timer_surf = _timer_font.render(f"{mins}:{secs:02d}", True, (255, 255, 255))
    screen.blit(timer_surf, timer_surf.get_rect(midtop=(WIDTH // 2, 5)))

    # Lives — top-right
    # Uncomment the block below once HEART_ICON image is set:
    # for i in range(lives):
    #     screen.blit(HEART_ICON, (WIDTH - 36 - i * 34, 14))
    lives_surf = _hud_font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_surf, lives_surf.get_rect(topright=(WIDTH - 15, 8)))

    # Ammo — below lives on the right
    # Uncomment the block below once AMMO_ICON image is set:
    # for i in range(ammo):
    #     screen.blit(AMMO_ICON, (WIDTH - 30 - i * 28, 36))
    ammo_surf = _hud_font.render(f"Ammo: {ammo}", True, (255, 255, 255))
    screen.blit(ammo_surf, ammo_surf.get_rect(topright=(WIDTH - 15, 34)))
