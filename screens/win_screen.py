# File Name: win_screen.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# The purpose of this file is to display the win screen when the player successfully
# completes a round, showing their final score and offering options to play again
# or return to the main menu.
# ----------------------------------------------------------------------------------------

import pygame
import pygame_gui
import sys

WIDTH, HEIGHT = 960, 540
FPS = 60


def run(screen, clock, score=0, high_scores=None):
    """Display the You Win! screen.

    Args:
        screen:      The pygame display surface passed in from the main game.
        clock:       The pygame Clock used for framerate control.
        score:       The player's final score to display.
        high_scores: List of (name, score, date) tuples from get_top_10(), or None.

    Returns:
        "play_again" if the player chooses another round, or "main_menu" to
        return to the welcome screen.
    """
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    background_color = (0, 100, 0)  # Fallback color — remove this line once background image is set

    title_font  = pygame.font.Font(None, 120)
    score_font  = pygame.font.Font(None, 60)
    hs_hdr_font = pygame.font.Font(None, 34)
    hs_row_font = pygame.font.Font(None, 26)

    play_again_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 110, HEIGHT // 2 + 30), (220, 55)),
        text="Play Again",
        manager=manager,
    )
    main_menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 110, HEIGHT // 2 + 100), (220, 55)),
        text="Main Menu",
        manager=manager,
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_again_button:
                    manager.clear_and_reset()
                    return "play_again"
                if event.ui_element == main_menu_button:
                    manager.clear_and_reset()
                    return "main_menu"

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(background_color)      # Remove this line once background image is set

        title_surf = title_font.render("YOU WIN!", True, (255, 255, 100))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 110)))

        score_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))

        # ── High scores panel (right side) ───────────────────────────────────
        hs_x = 635
        pygame.draw.rect(screen, (0, 70, 0), pygame.Rect(hs_x - 10, 88, 310, 310), border_radius=6)
        hdr_surf = hs_hdr_font.render("HIGH SCORES", True, (255, 255, 100))
        screen.blit(hdr_surf, (hs_x, 95))
        pygame.draw.line(screen, (200, 200, 100), (hs_x, 128), (hs_x + 290, 128), 1)
        if high_scores:
            for i, (_, entry_score, entry_date) in enumerate(high_scores[:10]):
                row_color = (255, 255, 0) if entry_score == score else (220, 220, 220)
                row = hs_row_font.render(f"#{i + 1:<2}  {entry_score:>6} pts   {entry_date}", True, row_color)
                screen.blit(row, (hs_x, 136 + i * 26))
        else:
            screen.blit(hs_row_font.render("No scores yet", True, (180, 180, 180)), (hs_x, 136))

        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER - You Win!")
    _clock = pygame.time.Clock()
    result = run(_screen, _clock, score=150)
    print(f"Result: {result}")
    pygame.quit()
