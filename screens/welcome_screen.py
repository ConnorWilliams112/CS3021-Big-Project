# File Name: welcome_screen.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260303
#
# The purpose of this file is to initialize the welcome screen and provide the user with 
# options to play the game, update options within the game, or exit out of the game. 
# ----------------------------------------------------------------------------------------

import pygame
import pygame_gui
import sys
import os

WIDTH, HEIGHT = 960, 540
FPS = 60


def run(screen, clock):
    music_on = True
    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "..", "models", "sounds", "game_music.mp3"))
    pygame.mixer.music.play(-1)

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH//2-100, HEIGHT//2-40), (200, 50)),
        text="Play Game", manager=manager)

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH//2-100, HEIGHT//2+30), (200, 50)),
        text="Exit Game", manager=manager)

    music_toggle_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH-180, 30), (150, 40)),
        text="Music: On", manager=manager)

    
    background_color = (34, 85, 34)  # Fallback color — remove this line once background image is set

    title_font = pygame.font.Font(None, 100)

    while True:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    manager.clear_and_reset()
                    return "landscape_selector"
                if event.ui_element == exit_button:
                    pygame.quit()
                    sys.exit()
                if event.ui_element == music_toggle_button:
                    if music_on:
                        pygame.mixer.music.pause()
                        music_toggle_button.set_text("Music: Off")
                        music_on = False
                    else:
                        pygame.mixer.music.unpause()
                        music_toggle_button.set_text("Music: On")
                        music_on = True

            manager.process_events(event)

        manager.update(time_delta)

        # screen.blit(background, (0, 0))  # Uncomment once background image is set
        screen.fill(background_color)      # Remove this line once background image is set

        title_surf = title_font.render("DUCK HUNTER", True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120)))

        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER")
    _clock = pygame.time.Clock()
    run(_screen, _clock)

