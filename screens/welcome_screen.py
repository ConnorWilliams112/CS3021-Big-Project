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


#Screen Configuration
WIDTH, HEIGHT = 960, 540
FPS = 60 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DUCK HUNTER")
clock = pygame.time.Clock()

#Pygame has a built in User Interface object to control all GUIs, layouts, interactions
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

#Create the GUIsfor the welcome/menu screen
play_button = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((WIDTH//2-100, HEIGHT//2-40), (200, 50)),
    text = "Play Game", manager = manager ) #Manager = informs pygame_gui who manages element

exit_button = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((WIDTH//2-100, HEIGHT//2+30), (200, 50)),
    text = "Exit Game", manager = manager )

music_toggle_button = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((WIDTH-180, 30), (150, 40)),
    text = "Music: On", manager = manager )

#Initialize background
# TODO: Replace the path below with the actual welcome screen background image file path
# background = pygame.image.load("PATH_TO_IMAGE/welcome_background.png").convert()
# background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_color = (34, 85, 34)  # Fallback color — remove this line once background image is set

# TODO: Replace the path below with the actual background music file path
# pygame.mixer.music.load("PATH_TO_AUDIO/background_music.mp3")
# pygame.mixer.music.play(-1)  # -1 loops the music indefinitely
music_on = True


def run():
    global music_on
    while True:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
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
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    run()

