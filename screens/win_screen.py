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


def run(screen, clock, score=0, high_score_table=None):
    """Display the You Win! screen.

    Args:
        screen:           The pygame display surface passed in from the main game.
        clock:            The pygame Clock used for framerate control.
        score:            The player's final score to display.
        high_score_table: The live HashTable from load_scores(); used for submission
                          and display.

    Returns:
        "play_again" if the player chooses another round, or "main_menu" to
        return to the welcome screen.
    """
    from persistence.save_load import submit_score, save_scores, get_top_10, is_top_10

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    background_color = (0, 100, 0)  # Fallback color — remove this line once background image is set

    title_font  = pygame.font.Font(None, 120)
    score_font  = pygame.font.Font(None, 60)
    hs_hdr_font = pygame.font.Font(None, 34)
    hs_row_font = pygame.font.Font(None, 26)
    label_font  = pygame.font.Font(None, 28)

    high_scores = get_top_10(high_score_table) if high_score_table is not None else []
    qualifying  = is_top_10(score, high_score_table) if high_score_table is not None else False

    if qualifying:
        name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((WIDTH // 2 - 110, HEIGHT // 2 + 20), (220, 36)),
            manager=manager,
        )
        name_entry.set_text_length_limit(20)
    else:
        name_entry = None

    btn_y = HEIGHT // 2 + (70 if qualifying else 30)
    play_again_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 110, btn_y), (220, 50)),
        text="Play Again",
        manager=manager,
    )
    main_menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 110, btn_y + 65), (220, 50)),
        text="Main Menu",
        manager=manager,
    )

    submitted      = False
    pending_return = None

    while True:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # enter name
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and qualifying and name_entry and not submitted:
                    player_name = name_entry.get_text().strip() or "Player"
                    submit_score(player_name, score, high_score_table)
                    save_scores(high_score_table)
                    high_scores = get_top_10(high_score_table)
                    submitted = True

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_again_button:
                    pending_return = "play_again"
                elif event.ui_element == main_menu_button:
                    pending_return = "main_menu"

                if pending_return and qualifying and name_entry and not submitted:
                    player_name = name_entry.get_text().strip() or "Player"
                    submit_score(player_name, score, high_score_table)
                    save_scores(high_score_table)
                    high_scores = get_top_10(high_score_table)
                    submitted = True

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(background_color)      # Remove this line once background image is set

        title_surf = title_font.render("YOU WIN!", True, (255, 255, 100))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 110)))

        score_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))

        if qualifying:
            label_surf = label_font.render("Enter your name:", True, (220, 220, 220))
            screen.blit(label_surf, label_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
        else:
            no_hs_surf = label_font.render("Score didn't make the top 10", True, (180, 180, 180))
            screen.blit(no_hs_surf, no_hs_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))

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

        if pending_return:
            manager.clear_and_reset()
            return pending_return


if __name__ == "__main__":
    pygame.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER - You Win!")
    _clock = pygame.time.Clock()
    result = run(_screen, _clock, score=150)
    print(f"Result: {result}")
    pygame.quit()
