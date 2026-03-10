# File Name: game_engine.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# Entry point. Initializes pygame, then drives the screen/state machine:
#   welcome → landscape_selector → countdown → game_loop → win/lose → (repeat or menu)
# ----------------------------------------------------------------------------------------

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER")
    clock = pygame.time.Clock()

    # Import screens here (after pygame.init so fonts/display are ready)
    from screens import welcome_screen, landscape_selector_screen, countdown_screen
    from screens import win_screen, lose_screen
    from engine import game_loop
    from engine.level import Level, MAX_LEVELS
    from persistence.save_load import load_scores, save_scores, get_top_10, submit_score

    high_score_table = load_scores()

    state     = "welcome"
    landscape = "forest"
    level_num = 1
    score     = 0

    while True:
        if state == "welcome":
            state = welcome_screen.run(screen, clock)

        elif state == "landscape_selector":
            result = landscape_selector_screen.run(screen, clock)
            if result == "back":
                state = "welcome"
            else:
                landscape = result
                state     = "countdown"

        elif state == "countdown":
            countdown_screen.run(screen, clock, level_num=level_num)
            state = "game"

        elif state == "game":
            outcome, score = game_loop.run(
                screen, clock,
                landscape=landscape,
                level=Level(level_num),
            )
            state = outcome   # "win" or "lose"

        elif state == "win":
            submit_score(f"run_{int(time.time())}", score, high_score_table)
            save_scores(high_score_table)
            result = win_screen.run(screen, clock, score=score, high_scores=get_top_10(high_score_table))
            if result == "play_again":
                if level_num >= MAX_LEVELS:
                    # Completed all 5 levels — restart from the beginning
                    level_num = 1
                    state     = "welcome"
                else:
                    level_num += 1
                    state      = "countdown"
            else:
                level_num = 1
                state     = "welcome"

        elif state == "lose":
            submit_score(f"run_{int(time.time())}", score, high_score_table)
            save_scores(high_score_table)
            result = lose_screen.run(screen, clock, score=score, high_scores=get_top_10(high_score_table))
            if result == "play_again":
                level_num = 1
                state     = "countdown"
            else:
                level_num = 1
                state     = "welcome"

        else:
            state = "welcome"


if __name__ == "__main__":
    main()
