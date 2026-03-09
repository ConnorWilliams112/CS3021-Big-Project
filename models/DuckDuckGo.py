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

# Initialize pygame
pg.init()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constants must be defined before imports that create the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue

# Create a temporary display so Duck imports can load images
_temp_display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Duck Hunt - Sprite Test Engine")

# Now import Duck classes after display is created
from Duck import NormalDuck, SuperDuck, Duck


#####################################################
##### TEST GAME ENGINE CLASS ########################
#####################################################

class TestGameEngine:
    
    def __init__(self):
        """Initialize the test game engine."""
        # Set up display first so Duck image loading can work
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Duck Hunt - Sprite Test Engine")
        
        # Create clock for FPS
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = FPS
        
        # Sprite groups for management
        self.all_sprites = pg.sprite.Group()
        self.ducks = pg.sprite.Group()
        
        # 10-second timer for auto-flying ducks off screen
        self.timer_duration = 10 * FPS  # 10 seconds in frames (600 frames at 60 FPS)
        self.timer = self.timer_duration
        self.timer_expired = False
        
        # Level progression
        self.level = 1
        self.max_level = 2
        
        # Initialize sprites
        self.init_sprites()
    
    def init_sprites(self):
        """Initialize all test sprites (ducks) based on current level."""
        if self.level == 1:
            # Level 1: 3 NormalDucks
            for i in range(3):
                duck = NormalDuck(level=1)
                duck.rect.x = 100 + (i * 200)
                duck.rect.y = 100 + (i * 100)
                self.all_sprites.add(duck)
                self.ducks.add(duck)
        
        elif self.level == 2:
            # Level 2: 2 NormalDucks and 2 SuperDucks
            for i in range(2):
                duck = NormalDuck(level=2)
                duck.rect.x = 100 + (i * 250)
                duck.rect.y = 100
                self.all_sprites.add(duck)
                self.ducks.add(duck)
            
            for i in range(2):
                super_duck = SuperDuck(level=2)
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
        """Handle clicking on sprites."""
        clicked_sprites = [sprite for sprite in self.ducks if sprite.rect.collidepoint(mouse_pos)]
        
        for sprite in clicked_sprites:
            if sprite.life:  # Only affect if alive
                # Check if it's a SuperDuck
                if isinstance(sprite, SuperDuck):
                    # Decrement shots counter
                    sprite.shots -= 1
                    if sprite.shots <= 0:
                        # Kill the duck when shots reach 0
                        sprite.kill()
                        print(f"SuperDuck killed at position {mouse_pos}")
                    elif sprite.shots == 2:
                        # Initialize pause for exploded state (0.5 seconds = 15 frames at 30 FPS)
                        sprite.pause_frames = 15
                        print(f"SuperDuck hit! {sprite.shots} shots remaining")
                    else:
                        print(f"SuperDuck hit! {sprite.shots} shots remaining")
                else:
                    # Normal duck - kill immediately
                    sprite.kill()
                    print(f"Duck killed at position {mouse_pos}")
    
    def reset_sprites(self):
        """Reset all sprites to alive state and reset timer."""
        self.all_sprites.empty()
        self.ducks.empty()
        self.timer = self.timer_duration
        self.timer_expired = False
        self.init_sprites()
        print(f"Sprites reset! Level: {self.level}")
    
    def update(self):
        """Update all sprite states."""
        # Decrement timer
        if self.timer > 0:
            self.timer -= 1
        
        # When timer expires, fly all remaining alive ducks off screen
        if self.timer <= 0 and not self.timer_expired:
            self.timer_expired = True
            for duck in self.ducks:
                if duck.life:  # Only affect alive ducks
                    # Set velocity to fly off top of screen
                    duck.velocity_x = 0
                    duck.velocity_y = -duck.speed * 2  # Fast upward movement
        
        self.all_sprites.update()
        
        # Remove sprites that have fallen off screen or flown off top
        for sprite in list(self.ducks):  # Use list() to avoid modifying while iterating
            if hasattr(sprite, 'rect'):
                if sprite.rect.top > SCREEN_HEIGHT or sprite.rect.bottom < 0:
                    if sprite in self.all_sprites:
                        self.all_sprites.remove(sprite)
                    if sprite in self.ducks:
                        self.ducks.remove(sprite)
        
        # Check if all ducks are dead and advance level
        if len(self.ducks) == 0 or all(not duck.life for duck in self.ducks):
            if self.level < self.max_level:
                self.level += 1
                print(f"\n*** LEVEL {self.level} COMPLETE! Advancing... ***\n")
                self.init_sprites()
                # Reset timer for next level
                self.timer = self.timer_duration
                self.timer_expired = False
    
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
        
        # Draw level
        level_text = font.render(f"Level: {self.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 10))
        
        # Draw timer
        timer_seconds = max(0, self.timer / FPS)
        timer_text = font.render(f"Timer: {timer_seconds:.1f}s", True, (255, 0, 0) if timer_seconds < 2 else (0, 0, 0))
        self.screen.blit(timer_text, (10, 50))
        
        # Draw instructions
        small_font = pg.font.Font(None, 24)
        instructions = small_font.render("Click to shoot | SPACE to reset | ESC to quit", True, (0, 0, 0))
        self.screen.blit(instructions, (10, 90))
        
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
