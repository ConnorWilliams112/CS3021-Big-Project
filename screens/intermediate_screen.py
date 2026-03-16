import pygame

# MACROS
BG_COLOR           = (200, 220, 255) # light blue
COLOR_BLACK        = (0, 0, 0)
COLOR_WHITE        = (255, 255, 255)
COLOR_NEXT_BUTTON  = (100, 200, 100) # green
COLOR_EXIT_BUTTON  = (200, 100, 100) # red
FONT_SIZE_TITLE    = 60
FONT_SIZE_BUTTON   = 40
BUTTON_X           = 330
BUTTON_WIDTH       = 300
BUTTON_HEIGHT      = 60
NEXT_BUTTON_Y      = 300
EXIT_BUTTON_Y      = 400
TITLE_Y            = 170


class IntermediateScreen:
    def __init__(self, screen, landscape=None):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.button_font = pygame.font.Font(None, FONT_SIZE_BUTTON)
        self.next_button = pygame.Rect(BUTTON_X, NEXT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button = pygame.Rect(BUTTON_X, EXIT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.bg = None
        if landscape:
            import os
            bg_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "Images")
            try:
                raw = pygame.image.load(os.path.join(bg_dir, f"{landscape}.png")).convert()
                self.bg = pygame.transform.scale(raw, (self.screen.get_width(), self.screen.get_height()))
            except Exception:
                self.bg = None

    def run(self):
        running = True

        while running:
            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self.screen.fill(BG_COLOR)
            # Center the title
            title = self.font.render("Round Complete!", True, COLOR_BLACK)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, TITLE_Y))
            self.screen.blit(title, title_rect)

            # Draw and center text in Next Round button
            pygame.draw.rect(self.screen, COLOR_NEXT_BUTTON, self.next_button)
            next_text = self.button_font.render("Next Round", True, COLOR_WHITE)
            next_text_rect = next_text.get_rect(center=self.next_button.center)
            self.screen.blit(next_text, next_text_rect)

            # Draw and center text in Exit Game button
            pygame.draw.rect(self.screen, COLOR_EXIT_BUTTON, self.exit_button)
            exit_text = self.button_font.render("Exit Game", True, COLOR_WHITE)
            exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
            self.screen.blit(exit_text, exit_text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.next_button.collidepoint(event.pos):
                        return "next"
                    if self.exit_button.collidepoint(event.pos):
                        return "exit"
