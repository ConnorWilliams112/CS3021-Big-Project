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

# MACROS
BG_COLOR                  = (34, 85, 34)    # dark green
COLOR_WHITE               = (255, 255, 255)
TEXTBOX_BG_COLOR          = (0, 0, 0, 150)  # semi-transparent black
FONT_SIZE_TITLE           = 100
FONT_SIZE_INSTRUCTIONS    = 32
BUTTON_WIDTH              = 200
BUTTON_HEIGHT             = 50
BUTTON_X_OFFSET           = 100             # half button width, for centering
PLAY_BUTTON_Y_OFFSET      = 40              # pixels above center
EXIT_BUTTON_Y_OFFSET      = 30              # pixels below center
MUSIC_BUTTON_RIGHT_MARGIN = 180             # pixels from right edge
MUSIC_BUTTON_TOP          = 30
MUSIC_BUTTON_WIDTH        = 150
MUSIC_BUTTON_HEIGHT       = 40
TITLE_Y_OFFSET            = 120             # pixels above center
INSTRUCTIONS_BOTTOM_MARGIN = 30             # pixels from bottom edge
TEXTBOX_PAD_X             = 10
TEXTBOX_PAD_Y             = 5
WIDTH, HEIGHT             = 960, 540
FPS                       = 60

def run(screen, clock):
    music_on = True
    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "..", "models", "sounds", "game_music.mp3"))
    pygame.mixer.music.play(-1)

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH//2-BUTTON_X_OFFSET, HEIGHT//2-PLAY_BUTTON_Y_OFFSET), (BUTTON_WIDTH, BUTTON_HEIGHT)),
        text="Play Game", manager=manager)

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH//2-BUTTON_X_OFFSET, HEIGHT//2+EXIT_BUTTON_Y_OFFSET), (BUTTON_WIDTH, BUTTON_HEIGHT)),
        text="Exit Game", manager=manager)

    music_toggle_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH-MUSIC_BUTTON_RIGHT_MARGIN, MUSIC_BUTTON_TOP), (MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT)),
        text="Music: On", manager=manager)

    title_font = pygame.font.Font(None, FONT_SIZE_TITLE)

    # Font for instructions
    instructions_font = pygame.font.Font(None, FONT_SIZE_INSTRUCTIONS)
    instructions_text = "HOW TO PLAY: Aim with mouse, left click to shoot, press spacebar to reload."
    instructions_color = COLOR_WHITE

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
        screen.fill(BG_COLOR)      # Remove this line once background image is set

        title_surf = title_font.render("DUCK HUNTER", True, COLOR_WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - TITLE_Y_OFFSET)))

        # Draw UI elements
        manager.draw_ui(screen)

        # Draw instructions textbox at the bottom
        instructions_surf = instructions_font.render(instructions_text, True, instructions_color)
        instructions_rect = instructions_surf.get_rect(center=(WIDTH // 2, HEIGHT - INSTRUCTIONS_BOTTOM_MARGIN))
        # Draw a semi-transparent background for the textbox
        textbox_rect = pygame.Rect(instructions_rect.left - TEXTBOX_PAD_X, instructions_rect.top - TEXTBOX_PAD_Y, instructions_rect.width + TEXTBOX_PAD_X * 2, instructions_rect.height + TEXTBOX_PAD_Y * 2)
        s = pygame.Surface((textbox_rect.width, textbox_rect.height), pygame.SRCALPHA)
        s.fill(TEXTBOX_BG_COLOR)
        screen.blit(s, (textbox_rect.left, textbox_rect.top))
        screen.blit(instructions_surf, instructions_rect)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER")
    _clock = pygame.time.Clock()
    run(_screen, _clock)

