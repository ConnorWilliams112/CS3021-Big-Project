# Duck.py
# Ducks module of CS3021 Big Project 
#
# Contains Duck base class with inheritance for duck types + movement algorithms + dead/alive flags       && Curt if time
# 
#
# Winter 2026
# Last updated: 9 March 2026
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

# Load images without convert_alpha() - will be converted in Duck __init__
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
except pg.error as e:
    print(f"Error loading image: {e}")
    print(f"Looking for images in: {IMAGES_DIR}")
    exit() 

#####################################################
##### Duck Class ##################################
#####################################################
class Duck(pg.sprite.Sprite):

    # Class variable to track if images have been converted
    _images_converted = False

    def __init__(self, level):
        super().__init__()
        
        # Convert images on first instantiation (after display is initialized)
        if not Duck._images_converted:
            global Duck_Open, Duck_Closed, Duck_Dead, Duck_Open_Flipped, Duck_Closed_Flipped
            global Duck_Dead_Flipped, Armored_Duck_Open, Armored_Duck_Closed, Armored_Duck_Exploded
            global Armored_Duck_Open_Flipped, Armored_Duck_Closed_Flipped, Armored_Duck_Exploded_Flipped
            
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
            Duck._images_converted = True
        
        self.life = True        #Using to equal alive/dead status of animal
        self.level = level      #Using to determine movement algorithm of animal, later tie to difficulty levels
        self.facing_right = True  #Track horizontal direction
        
        # Smooth movement parameters
        # Speed increases linearly: level 1 = 2 pixels/frame, level 5 = 10 pixels/frame
        self.speed = 2 + (level - 1) * 2
        # Direction change interval decreases with level (higher level = more direction changes)
        # Level 1: change every 60 frames, Level 5: change every 12 frames (60 - (level-1)*12)
        self.direction_change_interval = 60 - (level - 1) * 12
        self.frames_until_direction_change = self.direction_change_interval
        
        # Initialize velocity with random direction
        angle = random.uniform(0, 2 * math.pi)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
        
        # Pause counter for movement pause effects (0.5 seconds = 15 frames at 30 FPS)
        self.pause_frames = 0
        
        # Increase size by 25% then by 50% more (50 * 1.25 * 1.5 = 93.75, round to 93)
        self.duck_open = pg.transform.scale(Duck_Open, (93, 93))
        self.duck_closed = pg.transform.scale(Duck_Closed, (93, 93))
        self.duck_dead = pg.transform.scale(Duck_Dead, (93, 93))
        self.duck_open_flipped = pg.transform.scale(Duck_Open_Flipped, (93, 93))
        self.duck_closed_flipped = pg.transform.scale(Duck_Closed_Flipped, (93, 93))
        self.duck_dead_flipped = pg.transform.scale(Duck_Dead_Flipped, (93, 93))

    def update(self):
        if not self.life:
            # Duck is dead and falling - move it downward after pause
            if self.pause_frames > 0:
                # Pause the movement
                self.pause_frames -= 1
            else:
                # After pause, move downward
                newpos = self.rect.move(0, 8)  # Fall speed of 8 pixels per frame
                self.rect = newpos
            # Remove sprite when it reaches the bottom of the screen (HEIGHT = 540)
            if self.rect.top > 540:
                pg.sprite.Sprite.kill(self)  # Call parent class kill to remove from groups
        else:
            # Store old position to determine direction
            old_x = self.rect.x
            newpos = self.calcnewpos(self.rect, self.level)
            self.rect = newpos
            
            # Determine direction based on movement
            dx = self.rect.x - old_x
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False

    def calcnewpos(self, rect, level):
        """Calculate new position using smooth movement with occasional direction changes.
        Keeps duck on screen while alive."""
        # If paused, return current position without moving
        if self.pause_frames > 0:
            self.pause_frames -= 1
            return rect
        
        # Decrement the counter
        self.frames_until_direction_change -= 1
        
        # Change direction if counter reaches 0
        if self.frames_until_direction_change <= 0:
            angle = random.uniform(0, 2 * math.pi)
            self.velocity_x = self.speed * math.cos(angle)
            self.velocity_y = self.speed * math.sin(angle)
            self.frames_until_direction_change = self.direction_change_interval
        
        # Move using current velocity
        newpos = rect.move(int(self.velocity_x), int(self.velocity_y))
        
        # Keep duck on screen (constrain to screen bounds)
        # Screen dimensions: 800x600
        screen_width = 800
        screen_height = 600
        
        # Clamp position to keep the duck fully on screen
        newpos.left = max(0, min(newpos.left, screen_width - newpos.width))
        newpos.top = max(0, min(newpos.top, screen_height - newpos.height))
        
        # If duck hits edge, reverse direction to stay on screen
        if newpos.left <= 0 or newpos.right >= screen_width:
            self.velocity_x = -self.velocity_x
        if newpos.top <= 0 or newpos.bottom >= screen_height:
            self.velocity_y = -self.velocity_y
        
        return newpos
    
    def kill(self):
        """Kill the duck - change to dead image and make it fall to the bottom of the screen."""
        self.life = False
        self.image = self.duck_dead if self.facing_right else self.duck_dead_flipped
        self.rect = self.image.get_rect(center=self.rect.center)
        # Pause movement for 0.5 seconds (15 frames at 30 FPS)
        self.pause_frames = 15


#####################################################
##### Normal Duck Class #############################
#####################################################

class NormalDuck(Duck):

    def __init__(self, level):
        super().__init__(level)
        # Set default image to open state
        self.image = self.duck_open
        self.rect = self.image.get_rect()
    
    def update(self):
        # Only toggle between open and closed states if duck is alive
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

    def __init__(self, level):
        super().__init__(level)
        # Create sprite instances from armored duck images
        # Increase size by 25% (50 * 1.25 = 62.5, round to 62)
        self.armored_duck_open = pg.transform.scale(Armored_Duck_Open, (93, 93))
        self.armored_duck_closed = pg.transform.scale(Armored_Duck_Closed, (93, 93))
        self.armored_duck_exploded = pg.transform.scale(Armored_Duck_Exploded, (93, 93))
        self.armored_duck_open_flipped = pg.transform.scale(Armored_Duck_Open_Flipped, (93, 93))
        self.armored_duck_closed_flipped = pg.transform.scale(Armored_Duck_Closed_Flipped, (93, 93))
        self.armored_duck_exploded_flipped = pg.transform.scale(Armored_Duck_Exploded_Flipped, (93, 93))
        self.shots = 3  # Super duck requires 3 shots to kill (3 states)
        # Set default image to open state
        self.image = self.armored_duck_open
        self.rect = self.image.get_rect()
        

    def update(self):
        if self.shots == 3:
            # Armored state - toggle between open/closed
            if self.image in (self.armored_duck_open, self.armored_duck_open_flipped):
                self.image = self.armored_duck_closed if self.facing_right else self.armored_duck_closed_flipped
            else:
                self.image = self.armored_duck_open if self.facing_right else self.armored_duck_open_flipped
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.shots == 2:
            # Exploded/damaged state - show exploded image while paused
            self.image = self.armored_duck_exploded if self.facing_right else self.armored_duck_exploded_flipped
            self.rect = self.image.get_rect(center=self.rect.center)
            
            # Transition after pause completes
            if self.pause_frames == 0:
                self.shots = 1
        
        elif self.shots == 1:
            # Normal duck state - toggle between open/closed
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
    
    #Develop some test cases to demonstrate functionality of the Animal and Duck classes
    #Functionality of movement algorithms, displaying ducks, later killing w/ clicks, etc.

    # Create instances of NormalDuck and SuperDuck
    normal_duck = NormalDuck("Daffy", 5, "Healthy")
    super_duck = SuperDuck("SuperDaffy", 3, "Healthy")