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

try:
    Duck_Open = pg.image.load("Images/Duck_Open.png").convert_alpha()
    Duck_Closed = pg.image.load("Images/Duck_Closed.png").convert_alpha()
    Duck_Dead = pg.image.load("Images/Duck_Dead.png").convert_alpha()
    Duck_Open_Flipped = pg.image.load("Images/Duck_Open_flipped.png").convert_alpha()
    Duck_Closed_Flipped = pg.image.load("Images/Duck_Closed_flipped.png").convert_alpha()
    Duck_Dead_Flipped = pg.image.load("Images/Duck_Dead_flipped.png").convert_alpha()
    Armored_Duck_Open = pg.image.load("Images/Armored_Duck_Open.png").convert_alpha()
    Armored_Duck_Closed = pg.image.load("Images/Armored_Duck_Closed.png").convert_alpha()
    Armored_Duck_Exploded = pg.image.load("Images/Armored_Duck_Exploded.png").convert_alpha()
    Armored_Duck_Open_Flipped = pg.image.load("Images/Armored_Duck_Open_flipped.png").convert_alpha()
    Armored_Duck_Closed_Flipped = pg.image.load("Images/Armored_Duck_Closed_flipped.png").convert_alpha()
    Armored_Duck_Exploded_Flipped = pg.image.load("Images/Armored_Duck_Exploded_flipped.png").convert_alpha()
except pg.error as e:
    print(f"Error loading image: {e}")
    exit() 

#####################################################
##### Duck Class ##################################
#####################################################
class Duck(pg.sprite.Sprite):

    def __init__(self, level):
        super().__init__()
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
        
        self.duck_open = pg.transform.scale(Duck_Open, (50, 50))
        self.duck_closed = pg.transform.scale(Duck_Closed, (50, 50))
        self.duck_dead = pg.transform.scale(Duck_Dead, (50, 50))
        self.duck_open_flipped = pg.transform.scale(Duck_Open_Flipped, (50, 50))
        self.duck_closed_flipped = pg.transform.scale(Duck_Closed_Flipped, (50, 50))
        self.duck_dead_flipped = pg.transform.scale(Duck_Dead_Flipped, (50, 50))

    def update(self):
        if not self.life:
            # Duck is dead and falling - move it downward
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
        """Calculate new position using smooth movement with occasional direction changes."""
        # Decrement the counter
        self.frames_until_direction_change -= 1
        
        # Change direction if counter reaches 0
        if self.frames_until_direction_change <= 0:
            angle = random.uniform(0, 2 * math.pi)
            self.velocity_x = self.speed * math.cos(angle)
            self.velocity_y = self.speed * math.sin(angle)
            self.frames_until_direction_change = self.direction_change_interval
        
        # Move using current velocity
        return rect.move(int(self.velocity_x), int(self.velocity_y))
    
    def kill(self):
        """Kill the duck - change to dead image and make it fall to the bottom of the screen."""
        self.life = False
        self.image = self.duck_dead if self.facing_right else self.duck_dead_flipped
        self.rect = self.image.get_rect(center=self.rect.center)


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
        # Toggle between open and closed states
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
        self.armored_duck_open = pg.transform.scale(Armored_Duck_Open, (50, 50))
        self.armored_duck_closed = pg.transform.scale(Armored_Duck_Closed, (50, 50))
        self.armored_duck_exploded = pg.transform.scale(Armored_Duck_Exploded, (50, 50))
        self.armored_duck_open_flipped = pg.transform.scale(Armored_Duck_Open_Flipped, (50, 50))
        self.armored_duck_closed_flipped = pg.transform.scale(Armored_Duck_Closed_Flipped, (50, 50))
        self.armored_duck_exploded_flipped = pg.transform.scale(Armored_Duck_Exploded_Flipped, (50, 50))
        self.shots = 3  # Super duck requires 3 shots to kill
        # Set default image to open state
        self.image = self.armored_duck_open
        self.rect = self.image.get_rect()
        

    def update(self):
        if self.shots == 3:
            if self.image in (self.armored_duck_open, self.armored_duck_open_flipped):
                self.image = self.armored_duck_closed if self.facing_right else self.armored_duck_closed_flipped
            else:
                self.image = self.armored_duck_open if self.facing_right else self.armored_duck_open_flipped
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.shots == 2:
            self.image = self.armored_duck_exploded if self.facing_right else self.armored_duck_exploded_flipped
            self.rect = self.image.get_rect(center=self.rect.center)
            self.shots = 1
        
        elif self.shots == 1:
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