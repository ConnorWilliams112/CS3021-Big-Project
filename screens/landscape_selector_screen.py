# File Name: landscape_selector_screen.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# The purpose of this file is to let the player choose which landscape/background
# they want to play on before the round begins.
# ----------------------------------------------------------------------------------------

import pygame
import pygame_gui
import sys

# MACROS
BG_COLOR                  = (70, 130, 180)  # steel blue
COLOR_WHITE               = (255, 255, 255)
FONT_SIZE_TITLE           = 72
LANDSCAPE_BUTTON_WIDTH    = 180
LANDSCAPE_BUTTON_HEIGHT   = 55
LANDSCAPE_BUTTON_GAP      = 28
LANDSCAPE_BUTTON_Y_OFFSET = 20              # pixels below center
BACK_BUTTON_MARGIN        = 30              # top-left corner x and y
BACK_BUTTON_WIDTH         = 120
BACK_BUTTON_HEIGHT        = 45
WIDTH, HEIGHT             = 960, 540
FPS                       = 60

# Landscape options: (button label, return key)
LANDSCAPES = [
    ("Forest", "forest"),
    ("Desert", "desert"),
    ("Arctic",   "arctic")
]


def run(screen, clock):
    """Show the landscape selection screen.

    Args:
        screen: The pygame display surface passed in from the main game.
        clock:  The pygame Clock used for framerate control.

    Returns:
        A string key for the chosen landscape (e.g. "forest"), or "back" if
        the player pressed the Back button.
    """
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

   
    title_font = pygame.font.Font(None, FONT_SIZE_TITLE)

    # Lay out landscape buttons in a centered row
    btn_w, btn_h = LANDSCAPE_BUTTON_WIDTH, LANDSCAPE_BUTTON_HEIGHT
    gap = LANDSCAPE_BUTTON_GAP
    total_w = len(LANDSCAPES) * btn_w + (len(LANDSCAPES) - 1) * gap
    start_x = (WIDTH - total_w) // 2
    btn_y = HEIGHT // 2 + LANDSCAPE_BUTTON_Y_OFFSET

    landscape_buttons = {}
    for i, (label, key) in enumerate(LANDSCAPES):
        rect = pygame.Rect(start_x + i * (btn_w + gap), btn_y, btn_w, btn_h)
        btn = pygame_gui.elements.UIButton(relative_rect=rect, text=label, manager=manager)
        landscape_buttons[btn] = key

    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((BACK_BUTTON_MARGIN, BACK_BUTTON_MARGIN), (BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)),
        text="Back",
        manager=manager,
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    manager.clear_and_reset()
                    return "back"
                for btn, key in landscape_buttons.items():
                    if event.ui_element == btn:
                        manager.clear_and_reset()
                        return key

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill(BG_COLOR)      # Remove this line once background image is set

        title_surf = title_font.render("Select Your Landscape", True, COLOR_WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

       
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER - Landscape Select")
    _clock = pygame.time.Clock()
    result = run(_screen, _clock)
    print(f"Selected landscape: {result}")
    pygame.quit()
