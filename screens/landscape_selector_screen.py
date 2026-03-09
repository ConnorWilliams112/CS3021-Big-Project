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

WIDTH, HEIGHT = 960, 540
FPS = 60

# Landscape options: (button label, return key)
LANDSCAPES = [
    ("Forest", "forest"),
    ("Desert", "desert"),
    ("Lake",   "lake"),
    ("Snow",   "snow"),
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

    # TODO: Replace the path below with the actual selector background image file path
    # background = pygame.image.load("PATH_TO_IMAGE/selector_background.png").convert()
    # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_color = (70, 130, 180)  # Fallback color — remove this line once background image is set

    # TODO: Replace the paths below with the actual landscape thumbnail image file paths
    # thumbnails = {
    #     "forest": pygame.transform.scale(pygame.image.load("PATH_TO_IMAGE/thumb_forest.png").convert(), (180, 120)),
    #     "desert": pygame.transform.scale(pygame.image.load("PATH_TO_IMAGE/thumb_desert.png").convert(), (180, 120)),
    #     "lake":   pygame.transform.scale(pygame.image.load("PATH_TO_IMAGE/thumb_lake.png").convert(),   (180, 120)),
    #     "snow":   pygame.transform.scale(pygame.image.load("PATH_TO_IMAGE/thumb_snow.png").convert(),   (180, 120)),
    # }

    title_font = pygame.font.Font(None, 72)

    # Lay out landscape buttons in a centered row
    btn_w, btn_h = 180, 55
    gap = 28
    total_w = len(LANDSCAPES) * btn_w + (len(LANDSCAPES) - 1) * gap
    start_x = (WIDTH - total_w) // 2
    btn_y = HEIGHT // 2 + 20

    landscape_buttons = {}
    for i, (label, key) in enumerate(LANDSCAPES):
        rect = pygame.Rect(start_x + i * (btn_w + gap), btn_y, btn_w, btn_h)
        btn = pygame_gui.elements.UIButton(relative_rect=rect, text=label, manager=manager)
        landscape_buttons[btn] = key

    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((30, 30), (120, 45)),
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

        # screen.blit(background, (0, 0))  # Uncomment once background image is set
        screen.fill(background_color)      # Remove this line once background image is set

        title_surf = title_font.render("Select Your Landscape", True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

        # Uncomment the block below once thumbnail images are set to show landscape previews:
        # for i, (label, key) in enumerate(LANDSCAPES):
        #     screen.blit(thumbnails[key], (start_x + i * (btn_w + gap), btn_y - 130))

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
