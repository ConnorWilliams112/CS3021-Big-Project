import pygame

class IntermediateScreen:
    def __init__(self, screen, landscape=None):
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        self.button_font = pygame.font.Font(None, 40)
        self.next_button = pygame.Rect(330, 300, 300, 60)
        self.exit_button = pygame.Rect(330, 400, 300, 60)
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
                self.screen.fill((200, 220, 255))
            # Center the title
            title = self.font.render("Round Complete!", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 170))
            self.screen.blit(title, title_rect)

            # Draw and center text in Next Round button
            pygame.draw.rect(self.screen, (100, 200, 100), self.next_button)
            next_text = self.button_font.render("Next Round", True, (255, 255, 255))
            next_text_rect = next_text.get_rect(center=self.next_button.center)
            self.screen.blit(next_text, next_text_rect)

            # Draw and center text in Exit Game button
            pygame.draw.rect(self.screen, (200, 100, 100), self.exit_button)
            exit_text = self.button_font.render("Exit Game", True, (255, 255, 255))
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
