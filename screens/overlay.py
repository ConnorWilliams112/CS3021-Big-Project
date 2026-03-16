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
from models.Gun import Gun

# MACROS
WIDTH, HEIGHT      = 960, 540
BAR_COLOR          = (0, 0, 0, 150)  # semi-transparent black
COLOR_SCORE        = (255, 220, 0)   # yellow
COLOR_WHITE        = (255, 255, 255)
FONT_SIZE_SCORE    = 48
FONT_SIZE_TIMER    = 56
FONT_SIZE_HUD      = 36
BAR_HEIGHT         = 62
DEFAULT_LIVES      = 3
DEFAULT_AMMO       = 10
DEFAULT_TIME       = 60
SCORE_X            = 18
SCORE_Y            = 10
TIMER_Y            = 5
LIVES_RIGHT_MARGIN = 15
LIVES_Y            = 8


_score_font = None
_timer_font = None
_hud_font   = None


def _init_fonts():
    """Lazy-initialize fonts so this module can be imported before pygame.init()."""
    global _score_font, _timer_font, _hud_font
    if _score_font is None:
        _score_font = pygame.font.Font(None, FONT_SIZE_SCORE)
        _timer_font = pygame.font.Font(None, FONT_SIZE_TIMER)
        _hud_font   = pygame.font.Font(None, FONT_SIZE_HUD)


class OverlayHUD:
    def __init__(self):
        _init_fonts()
        self.score = 0
        self.lives = DEFAULT_LIVES
        self.ammo = DEFAULT_AMMO
        self.time_remaining = DEFAULT_TIME

    def render(self, screen):
        # Semi-transparent top bar
        bar = pygame.Surface((WIDTH, BAR_HEIGHT), pygame.SRCALPHA)
        bar.fill(BAR_COLOR)
        screen.blit(bar, (0, 0))

        # Score — top-left
        score_surf = _score_font.render(f"Score: {self.score}", True, COLOR_SCORE)
        screen.blit(score_surf, (SCORE_X, SCORE_Y))

        # Timer — top-center
        mins = int(self.time_remaining) // 60
        secs = int(self.time_remaining) % 60
        timer_surf = _timer_font.render(f"{mins}:{secs:02d}", True, COLOR_WHITE)
        screen.blit(timer_surf, timer_surf.get_rect(midtop=(WIDTH // 2, TIMER_Y)))

        # Lives — top-right
        lives_surf = _hud_font.render(f"Lives: {self.lives}", True, COLOR_WHITE)
        screen.blit(lives_surf, lives_surf.get_rect(topright=(WIDTH - LIVES_RIGHT_MARGIN, LIVES_Y)))

def draw(screen, score=0, ammo=DEFAULT_AMMO, time_remaining=DEFAULT_TIME):
    """Draw the HUD overlay on top of the current game frame.

    Args:
        screen:         The pygame surface to draw onto.
        score:          The player's current score.
        lives:          Number of lives remaining.
        ammo:           Number of shots remaining.
        time_remaining: Seconds left in the round (float or int).
    """
    _init_fonts()

    # Score — top-left
    score_surf = _score_font.render(f"Score: {score}", True, COLOR_SCORE)
    screen.blit(score_surf, (SCORE_X, SCORE_Y))

    # Timer — top-center
    mins = int(time_remaining) // 60
    secs = int(time_remaining) % 60
    timer_surf = _timer_font.render(f"{mins}:{secs:02d}", True, COLOR_WHITE)
    screen.blit(timer_surf, timer_surf.get_rect(midtop=(WIDTH // 2, TIMER_Y)))

    # Lives — top-right
    # for i in range(lives):
   


   


