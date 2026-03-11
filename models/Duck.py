# Duck.py
# Ducks module of CS3021 Big Project 
#
# Contains Duck base class with inheritance for duck types + movement algorithms + dead/alive flags and logic
# 
#
# Winter 2026
# Last updated: 10 March 2026
#
# Author: Capt Connor Williams

#####################################################
##### IMPORTS BLOCK #################################
#####################################################

import copy as copy
import pygame as pg
import random as random
import math as math
import os

# Get the directory where this file is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "Images")

# Load images
try:
    Duck_Open = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Open.png"))
    Duck_Closed = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Closed.png"))
    Duck_Dead = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Dead.png"))
    Duck_Open_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Open_flipped.png"))
    Duck_Closed_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Closed_flipped.png"))
    Duck_Dead_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Duck_Dead_flipped.png"))
    Armored_Duck_Open = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Open.png"))
    Armored_Duck_Closed = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Closed.png"))
    Armored_Duck_Exploded = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Exploded.png"))
    Armored_Duck_Open_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Open_flipped.png"))
    Armored_Duck_Closed_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Closed_flipped.png"))
    Armored_Duck_Exploded_Flipped = pg.image.load(os.path.join(IMAGES_DIR, "Armored_Duck_Exploded_flipped.png"))
    
    # Convert all images for better performance
    Duck_Open = Duck_Open.convert_alpha()
    Duck_Closed = Duck_Closed.convert_alpha()
    Duck_Dead = Duck_Dead.convert_alpha()
    Duck_Open_Flipped = Duck_Open_Flipped.convert_alpha()
    Duck_Closed_Flipped = Duck_Closed_Flipped.convert_alpha()
    Duck_Dead_Flipped = Duck_Dead_Flipped.convert_alpha()
    Armored_Duck_Open = Armored_Duck_Open.convert_alpha()
    Armored_Duck_Closed = Armored_Duck_Closed.convert_alpha()
    Armored_Duck_Exploded = Armored_Duck_Exploded.convert_alpha()
    Armored_Duck_Open_Flipped = Armored_Duck_Open_Flipped.convert_alpha()
    Armored_Duck_Closed_Flipped = Armored_Duck_Closed_Flipped.convert_alpha()
    Armored_Duck_Exploded_Flipped = Armored_Duck_Exploded_Flipped.convert_alpha()
    
except pg.error as e:
    print(f"Error loading image: {e}")
    print(f"Looking for images in: {IMAGES_DIR}")
    exit() 

#####################################################
##### Constants #####################################
#####################################################
# Movement constants
BASE_SPEED = 2
SPEED_MULTIPLIER = 2
BASE_DIRECTION_CHANGE_INTERVAL = 60
DIRECTION_CHANGE_MULTIPLIER = 6

# Sprite rendering constants
DUCK_SPRITE_SIZE = 90

# Physics constants
FULL_ROTATION = 2 * math.pi
DEAD_DUCK_FALL_SPEED = 8
DEAD_DUCK_PAUSE_FRAMES = 15

# Screen constants  (must match game_loop.py resolution)
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_REMOVAL_THRESHOLD = 560  # Remove dead ducks when they fall past this

# Frames before an un-shot duck is considered escaped (~10 s at 60 fps)
ESCAPE_FRAMES = 600

# SuperDuck shot states
SUPERDUCK_INITIAL_SHOTS = 3
SUPERDUCK_DAMAGED_SHOTS = 2
SUPERDUCK_NORMAL_SHOTS = 1

#####################################################
##### Duck Class ####################################
#####################################################
class Duck(pg.sprite.Sprite):
    '''
    Base class for all duck types. Inherits from pygame.sprite.Sprite for easy integration with Pygame's sprite groups and rendering system.
    Contains common attributes and methods for movement, state management, and rendering.
    Also contains logic for handling being shot (killed) and transitioning to a falling state befor erasure from the game.
    '''
    def __init__(self, level):
        super().__init__()
        self.life = True        #Using to show alive/dead status of animal
        self.level = level      #Using to determine movement algorithm of animal, later tie to difficulty levels
        self.facing_right = True  #Track horizontal direction
        
        # Smooth movement parameters

        # Speed increases linearly with level
        self.speed = BASE_SPEED + (level - 1) * SPEED_MULTIPLIER

        # Direction change interval decreases with level (higher level = more direction changes)
        self.direction_change_interval = BASE_DIRECTION_CHANGE_INTERVAL - (level - 1) * DIRECTION_CHANGE_MULTIPLIER
        self.frames_until_direction_change = self.direction_change_interval
        
        # Initialize velocity with random direction
        angle = random.uniform(0, FULL_ROTATION)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
        
        # Pause counter for movement pause effects (0.5 seconds = 15 frames at 30 FPS)
        self.pause_frames = 0

        # Integration attributes used by game_loop.py
        self.escaped        = False
        self._should_remove = False
        self._frame_count   = 0   # frames spent alive (for escape timer)
        
        # Initialize common sprite images
        self.duck_open = pg.transform.scale(Duck_Open, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.duck_closed = pg.transform.scale(Duck_Closed, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.duck_dead = pg.transform.scale(Duck_Dead, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.duck_open_flipped = pg.transform.scale(Duck_Open_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.duck_closed_flipped = pg.transform.scale(Duck_Closed_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.duck_dead_flipped = pg.transform.scale(Duck_Dead_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))

    #####################################################
    ##### Standard dunder override methods Block ########
    #####################################################

    # Accepting default hash, eq, neq behaviors due to not needing
    # to compare ducks based on identity or value, and not using them in hash-based collections.

    # Accepting default copy and deepcopy behaviors since we don't need to create copies of ducks in our game logic, 
    # and the default behavior of copying the sprite's attributes is sufficient for our purposes.

    # Accepting default str behavior since we won't be printing duck instances directly, 
    # and the default representation is sufficient for debugging purposes.

    #####################################################
    ##### Custom Behaviors Block ########################
    #####################################################

    def update(self):
        '''
        Update method for duck movement and state management. Called every frame by the game loop.
        Handles movement based on velocity, direction changes, and state transitions when killed.
        '''
        if not self.life:       # Duck is dead and falling - move it downward after pause
            if self.pause_frames > 0:
                # Pause the movement, decrement the pause counter
                self.pause_frames -= 1
            else:               # After pause, move downward
                newpos = self.rect.move(0, DEAD_DUCK_FALL_SPEED)  # Fall speed
                self.rect = newpos
            # Signal removal when the duck has fallen off the bottom of the screen
            if self.rect.top > SCREEN_REMOVAL_THRESHOLD:
                self._should_remove = True
        else:
            # Escape timer — duck vanishes if never shot within time limit
            self._frame_count += 1
            if self._frame_count > ESCAPE_FRAMES:
                self.escaped        = True
                self._should_remove = True
                return

            # Store old position to determine direction
            old_x = self.rect.x

            #calculate new position using movement algorithm and update rect
            newpos = self.calcnewpos(self.rect, self.level)
            self.rect = newpos
            
            # Determine direction based on movement
            dx = self.rect.x - old_x
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False

    def calcnewpos(self, rect):
        '''
        Calculate new position using smooth movement with occasional direction changes.
        Keeps duck on screen while alive.
        '''
        # If paused, return current position without moving
        if self.pause_frames > 0:
            self.pause_frames -= 1
            return rect
        
        # Decrement the counter
        self.frames_until_direction_change -= 1
        
        # Change direction if counter reaches 0
        if self.frames_until_direction_change <= 0:
            angle = random.uniform(0, FULL_ROTATION)
            self.velocity_x = self.speed * math.cos(angle)
            self.velocity_y = self.speed * math.sin(angle)
            self.frames_until_direction_change = self.direction_change_interval
        
        # Move using current velocity
        newpos = rect.move(int(self.velocity_x), int(self.velocity_y))
        
        # Keep duck on screen (constrain to screen bounds)
        # Clamp position to keep the duck fully on screen
        newpos.left = max(0, min(newpos.left, SCREEN_WIDTH - newpos.width))
        newpos.top = max(0, min(newpos.top, SCREEN_HEIGHT - newpos.height))
        
        # If duck hits edge, reverse direction to stay on screen
        if newpos.left <= 0 or newpos.right >= SCREEN_WIDTH:
            self.velocity_x = -self.velocity_x
        if newpos.top <= 0 or newpos.bottom >= SCREEN_HEIGHT:
            self.velocity_y = -self.velocity_y
        
        return newpos
    
    def kill(self):
        '''
        Kills the duck. Changes to dead image and make it fall to the bottom of the screen before being removed from the game.
        '''
        self.life = False
        self.image = self.duck_dead if self.facing_right else self.duck_dead_flipped
        self.rect = self.image.get_rect(center=self.rect.center)
        # Pause movement for 0.5 seconds (15 frames at 30 FPS)
        self.pause_frames = DEAD_DUCK_PAUSE_FRAMES

    def shoot(self):
        '''
        Registers a shot on the duck instance. For generality, this base class version kills the duck.
        Implemented to reduce hit logic and type checks in game engine.
        SuperDuck override will provide additional logic.
        '''
        self.kill()
        return True
    
#####################################################
##### Normal Duck Class #############################
#####################################################

class NormalDuck(Duck):
    '''
    Normal, unarmored duck type. Uses the base movement and state management from Duck class, with specific sprite images for normal duck.
    '''

    def __init__(self, level):
        super().__init__(level)
        # Set default image to open state
        self.image = self.duck_open
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, SCREEN_WIDTH  - self.rect.width))
        self.rect.y = random.randint(0, max(0, SCREEN_HEIGHT - self.rect.height))

    def update(self):
        '''
        Toggle between open and closed images based on movement state while alive (flapping)
        Call base update for movement and state management.
        '''
        if self.life:
            if self.image == self.duck_open or self.image == self.duck_open_flipped:
                self.image = self.duck_closed if self.facing_right else self.duck_closed_flipped
            else:
                self.image = self.duck_open if self.facing_right else self.duck_open_flipped
            self.rect = self.image.get_rect(center=self.rect.center)
        return super().update()
    

#####################################################
##### Super Duck Class ##############################
#####################################################

class SuperDuck(Duck):
    '''
    Armored duck type that requires multiple hits to kill. Has additional states for armored, damaged, and normal appearances.
    Inherits movement and state management from Duck class, with specific logic for handling multiple hits and sprite changes based on shot state.
    '''

    def __init__(self, level):
        super().__init__(level)
        # Create sprite instances from armored duck images
        self.armored_duck_open = pg.transform.scale(Armored_Duck_Open, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.armored_duck_closed = pg.transform.scale(Armored_Duck_Closed, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.armored_duck_exploded = pg.transform.scale(Armored_Duck_Exploded, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.armored_duck_open_flipped = pg.transform.scale(Armored_Duck_Open_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.armored_duck_closed_flipped = pg.transform.scale(Armored_Duck_Closed_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.armored_duck_exploded_flipped = pg.transform.scale(Armored_Duck_Exploded_Flipped, (DUCK_SPRITE_SIZE, DUCK_SPRITE_SIZE))
        self.shots = SUPERDUCK_INITIAL_SHOTS  # Super duck requires 2 shots to kill (uses 3 for state management: 3 = armored, 2 = exploded, 1 = normal)
        # Set default image to open state
        self.image = self.armored_duck_open
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, SCREEN_WIDTH  - self.rect.width))
        self.rect.y = random.randint(0, max(0, SCREEN_HEIGHT - self.rect.height))

    def shoot(self):
        '''
        Additional logic to support external shoot method on all Duck subclasses.
        Does checking/setting of self.shots
        '''
        if self.shots > SUPERDUCK_NORMAL_SHOTS:
            self.shots       -= 1
            self.pause_frames = DEAD_DUCK_PAUSE_FRAMES  # brief stagger animation
            return False
        else:
            super().shoot()

    def update(self):
        '''
        Toggles between open and closed images based on movement state while alive (flapping)
        Changes sprite based on shot state (armored, damaged, normal).
        '''
        if self.shots == SUPERDUCK_INITIAL_SHOTS:
            # Armored state
            if self.image in (self.armored_duck_open, self.armored_duck_open_flipped):
                self.image = self.armored_duck_closed if self.facing_right else self.armored_duck_closed_flipped
            else:
                self.image = self.armored_duck_open if self.facing_right else self.armored_duck_open_flipped
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.shots == SUPERDUCK_DAMAGED_SHOTS:
            # Exploded/damaged state that shows exploded image while paused
            self.image = self.armored_duck_exploded if self.facing_right else self.armored_duck_exploded_flipped
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # Transition after pause completes
            if self.pause_frames == 0:
                self.shots = SUPERDUCK_NORMAL_SHOTS
        
        elif self.shots == SUPERDUCK_NORMAL_SHOTS:
            # Normal duck state
            if self.image in (self.armored_duck_exploded, self.armored_duck_exploded_flipped):
                self.image = self.duck_open if self.facing_right else self.duck_open_flipped
            elif self.image in (self.duck_open, self.duck_open_flipped):
                self.image = self.duck_closed if self.facing_right else self.duck_closed_flipped
            else:
                self.image = self.duck_open if self.facing_right else self.duck_open_flipped
            self.rect = self.image.get_rect(center=self.rect.center)

        return super().update()
    

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    print("This module is not meant to be run directly. Please run DuckDuckGo.py to play the game.")