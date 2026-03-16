# File Name: lose_screen.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# The purpose of this file is to display the Game Over screen when the player loses,
# showing their final score and offering options to play again or return to the main menu.
# ----------------------------------------------------------------------------------------

import pygame
import pygame_gui
import sys

# MACROS

WIDTH, HEIGHT         = 960, 540
FPS                   = 60
# Colors
BG_COLOR              = (139, 0, 0)     # dark red
COLOR_WHITE           = (255, 255, 255)
COLOR_SCORE           = (255, 220, 100) # amber
COLOR_LABEL           = (220, 220, 220) # light gray
COLOR_MUTED           = (180, 180, 180) # gray
COLOR_HS_PANEL        = (100, 0, 0)     # dark red
COLOR_HS_HEADER       = (255, 220, 100) # amber
COLOR_HS_LINE         = (220, 180, 80)  # gold
COLOR_HIGHLIGHT       = (255, 255, 0)   # yellow, current score row

# Fonts
FONT_SIZE_TITLE       = 120
FONT_SIZE_SCORE       = 60
FONT_SIZE_HS_HEADER   = 34
FONT_SIZE_HS_ROW      = 26
FONT_SIZE_LABEL       = 28

# Layout
TITLE_Y_OFFSET        = 110            # pixels above center
SCORE_Y_OFFSET        = 25             # pixels above center
LABEL_Y_OFFSET        = 5              # pixels below center
NO_HS_Y_OFFSET        = 10             # pixels below center

# Name entry
ENTRY_WIDTH           = 220            # shared by name entry and buttons
ENTRY_X_OFFSET        = 110            # half entry/button width, for centering
NAME_ENTRY_Y_OFFSET   = 20             # pixels below center
NAME_ENTRY_HEIGHT     = 36
NAME_MAX_LENGTH       = 20

# Buttons
QUALIFYING_BTN_Y_OFFSET = 70           # pixels below center when qualifying
DEFAULT_BTN_Y_OFFSET    = 30           # pixels below center
BUTTON_HEIGHT           = 50
BUTTON_GAP              = 65           # gap between Play Again and Main Menu

# High scores panel
TOP_N                 = 10
HS_PANEL_X            = 635
HS_PANEL_LEFT_PAD     = 10             # extends rect left of hs_x
HS_PANEL_TOP          = 188
HS_PANEL_SIZE         = 310
HS_PANEL_RADIUS       = 6
HS_HEADER_Y           = 195
HS_LINE_Y             = 228
HS_LINE_WIDTH         = 290
HS_NAME_DISPLAY_LEN   = 11
HS_NAME_TRUNC_LEN     = 10             # truncated to this + ellipsis
HS_ROW_START_Y        = 236
HS_ROW_HEIGHT         = 26
HS_EMPTY_Y            = 136


def run(screen, clock, score=0, high_score_table=None):
    """Display the Game Over / lose screen.

    Args:
        screen:           The pygame display surface passed in from the main game.
        clock:            The pygame Clock used for framerate control.
        score:            The player's final score to display.
        high_score_table: The live HashTable from load_scores(); used for submission
                          and display.

    Returns:
        "play_again" if the player chooses to retry, or "main_menu" to return
        to the welcome screen.
    """
    from persistence.save_load import submit_score, save_scores, get_top_10, is_top_10

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    title_font  = pygame.font.Font(None, FONT_SIZE_TITLE)
    score_font  = pygame.font.Font(None, FONT_SIZE_SCORE)
    hs_hdr_font = pygame.font.Font(None, FONT_SIZE_HS_HEADER)
    hs_row_font = pygame.font.Font(None, FONT_SIZE_HS_ROW)
    label_font  = pygame.font.Font(None, FONT_SIZE_LABEL)

    high_scores = get_top_10(high_score_table) if high_score_table is not None else []
    qualifying  = is_top_10(score, high_score_table) if high_score_table is not None else False

    if qualifying:
        name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((WIDTH // 2 - ENTRY_X_OFFSET, HEIGHT // 2 + NAME_ENTRY_Y_OFFSET), (ENTRY_WIDTH, NAME_ENTRY_HEIGHT)),
            manager=manager,
        )
        name_entry.set_text_length_limit(NAME_MAX_LENGTH)
    else:
        name_entry = None

    btn_y = HEIGHT // 2 + (QUALIFYING_BTN_Y_OFFSET if qualifying else DEFAULT_BTN_Y_OFFSET)
    play_again_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - ENTRY_X_OFFSET, btn_y), (ENTRY_WIDTH, BUTTON_HEIGHT)),
        text="Play Again",
        manager=manager,
    )
    main_menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - ENTRY_X_OFFSET, btn_y + BUTTON_GAP), (ENTRY_WIDTH, BUTTON_HEIGHT)),
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

        screen.fill(BG_COLOR)      # Remove this line once background image is set

        title_surf = title_font.render("GAME OVER", True, COLOR_WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - TITLE_Y_OFFSET)))

        score_surf = score_font.render(f"Score: {score}", True, COLOR_SCORE)
        screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - SCORE_Y_OFFSET)))

        if qualifying:
            label_surf = label_font.render("Enter your name:", True, COLOR_LABEL)
            screen.blit(label_surf, label_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + LABEL_Y_OFFSET)))
        else:
            no_hs_surf = label_font.render("Score didn't make the top 10", True, COLOR_MUTED)
            screen.blit(no_hs_surf, no_hs_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + NO_HS_Y_OFFSET)))

        # ── High scores panel (right side) ───────────────────────────────────
        hs_x = HS_PANEL_X
        pygame.draw.rect(screen, COLOR_HS_PANEL, pygame.Rect(hs_x - HS_PANEL_LEFT_PAD, HS_PANEL_TOP, HS_PANEL_SIZE, HS_PANEL_SIZE), border_radius=HS_PANEL_RADIUS)
        hdr_surf = hs_hdr_font.render("HIGH SCORES", True, COLOR_HS_HEADER)
        screen.blit(hdr_surf, (hs_x, HS_HEADER_Y))
        pygame.draw.line(screen, COLOR_HS_LINE, (hs_x, HS_LINE_Y), (hs_x + HS_LINE_WIDTH, HS_LINE_Y), 1)
        if high_scores:
            for i, (entry_name, entry_score, entry_date) in enumerate(high_scores[:TOP_N]):
                row_color = COLOR_HIGHLIGHT if entry_score == score else COLOR_LABEL
                name_trunc = entry_name[:HS_NAME_DISPLAY_LEN] if len(entry_name) <= HS_NAME_DISPLAY_LEN else entry_name[:HS_NAME_TRUNC_LEN] + "…"
                row = hs_row_font.render(f"#{i + 1:<2}  {name_trunc:<11} {entry_score:>6} pts", True, row_color)
                screen.blit(row, (hs_x, HS_ROW_START_Y + i * HS_ROW_HEIGHT))
        else:
            screen.blit(hs_row_font.render("No scores yet", True, COLOR_MUTED), (hs_x, HS_EMPTY_Y))

        manager.draw_ui(screen)
        pygame.display.flip()

        if pending_return:
            manager.clear_and_reset()
            return pending_return


if __name__ == "__main__":
    pygame.init()
    _screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DUCK HUNTER - Game Over")
    _clock = pygame.time.Clock()
    result = run(_screen, _clock, score=42)
    print(f"Result: {result}")
    pygame.quit()
