# DuckDuckGo.py
# Test Game Engine for CS3021 Big Project
#
# Simple game engine to test sprite functionality including:
# - Initializing sprites (ducks)
# - Killing sprites on mouse click
# - Rendering and updating sprites in game loop
#
# Winter 2026
# Last updated: 9 March 2026
#
# Author: Capt Connor Williams

#####################################################
##### IMPORTS BLOCK #################################
#####################################################

import pygame as pg
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Duck import NormalDuck, SuperDuck

#####################################################
##### CONSTANTS BLOCK ###############################
#####################################################

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue


#####################################################
##### TEST GAME ENGINE CLASS ########################
#####################################################

class TestGameEngine:
    
    def __init__(self):
        """Initialize the test game engine."""
        # Initialize Pygame
        pg.init()
        
        # Set up display
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Duck Hunt - Sprite Test Engine")
        
        # Create clock for FPS
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = FPS
        
        # Sprite groups for management
        self.all_sprites = pg.sprite.Group()
        self.ducks = pg.sprite.Group()
        
        # Initialize sprites
        self.init_sprites()
    
    def init_sprites(self):
        """Initialize all test sprites (ducks)."""
        # Create NormalDuck at random starting positions
        for i in range(3):
            duck = NormalDuck(level=2)
            duck.rect.x = 100 + (i * 200)
            duck.rect.y = 100 + (i * 100)
            self.all_sprites.add(duck)
            self.ducks.add(duck)
        
        # Create SuperDuck at different positions
        for i in range(2):
            super_duck = SuperDuck(level=3)
            super_duck.rect.x = 150 + (i * 300)
            super_duck.rect.y = 350
            self.all_sprites.add(super_duck)
            self.ducks.add(super_duck)
    
    def handle_events(self):
        """Handle all user input and events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    self.handle_mouse_click(event.pos)
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_SPACE:
                    # Reset ducks on spacebar press
                    self.reset_sprites()
    
    def handle_mouse_click(self, mouse_pos):
        """Kill any sprite clicked on."""
        clicked_sprites = [sprite for sprite in self.ducks if sprite.rect.collidepoint(mouse_pos)]
        
        for sprite in clicked_sprites:
            if sprite.life:  # Only kill if alive
                sprite.kill()
                print(f"Duck killed at position {mouse_pos}")
    
    def reset_sprites(self):
        """Reset all sprites to alive state."""
        self.all_sprites.empty()
        self.ducks.empty()
        self.init_sprites()
        print("Sprites reset!")
    
    def update(self):
        """Update all sprite states."""
        self.all_sprites.update()
        
        # Remove sprites that have fallen off screen
        for sprite in self.ducks:
            if hasattr(sprite, 'rect') and sprite.rect.top > SCREEN_HEIGHT:
                if sprite in self.all_sprites:
                    self.all_sprites.remove(sprite)
                if sprite in self.ducks:
                    self.ducks.remove(sprite)
    
    def render(self):
        """Render all graphics to screen."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw HUD text
        font = pg.font.Font(None, 36)
        ducks_alive = sum(1 for duck in self.ducks if duck.life)
        text = font.render(f"Ducks Alive: {ducks_alive}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        
        # Draw instructions
        small_font = pg.font.Font(None, 24)
        instructions = small_font.render("Click to shoot | SPACE to reset | ESC to quit", True, (0, 0, 0))
        self.screen.blit(instructions, (10, 50))
        
        # Update display
        pg.display.flip()
    
    def run(self):
        """Main game loop for test engine."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        self.quit()
    
    def quit(self):
        """Clean up and exit."""
        pg.quit()
        sys.exit()


#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    # Create and run the test game engine
    # This engine tests:
    # - Sprite initialization (creating ducks at various positions)
    # - Sprite movement and animation (Duck update logic)
    # - Mouse click detection and sprite killing
    # - Sprite rendering and game loop
    
    engine = TestGameEngine()
    engine.run()
