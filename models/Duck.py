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
    Armored_Duck_Open = pg.image.load("Images/Armored_Duck_Open.png").convert_alpha()
    Armored_Duck_Closed = pg.image.load("Images/Armored_Duck_Closed.png").convert_alpha()
    Armored_Duck_Exploded = pg.image.load("Images/Armored_Duck_Exploded.png").convert_alpha()
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
        self.duck_open = pg.transform.scale(Duck_Open, (50, 50))
        self.duck_closed = pg.transform.scale(Duck_Closed, (50, 50))
        self.duck_dead = pg.transform.scale(Duck_Dead, (50, 50))

    def update(self):
        if not self.life:
            # Duck is dead and falling - move it downward
            newpos = self.rect.move(0, 8)  # Fall speed of 8 pixels per frame
            self.rect = newpos
            # Remove sprite when it reaches the bottom of the screen (HEIGHT = 540)
            if self.rect.top > 540:
                pg.sprite.Sprite.kill(self)  # Call parent class kill to remove from groups
        else:
            # Normal movement for living duck
            newpos = self.calcnewpos(self.rect, self.level)          ##### In work #####
            self.rect = newpos

    def calcnewpos(self,rect,level):
        # Simplified movement algorithm based on level
        angle = random.uniform(0, 2 * math.pi)
        z = level * 2  # Speed increases with level
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)
    
    def kill(self):
        """Kill the duck - change to dead image and make it fall to the bottom of the screen."""
        self.life = False
        self.image = self.duck_dead
        self.rect = self.image.get_rect()


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
        if self.image == self.duck_open:
            self.image = self.duck_closed
            self.rect = self.image.get_rect()
        else:
            self.image = self.duck_open
            self.rect = self.image.get_rect()
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
        self.shots = 3  # Super duck requires 2 shots to kill
        # Set default image to open state
        self.image = self.armored_duck_open
        self.rect = self.image.get_rect()
        

    def update(self):
        if self.shots == 3:
            if self.image == self.armored_duck_open:
                self.image = self.armored_duck_closed
                self.rect = self.image.get_rect()
            else:
                self.image = self.armored_duck_open
                self.rect = self.image.get_rect()

        elif self.shots == 2:
            self.image = self.armored_duck_exploded
            self.rect = self.image.get_rect()
            self.shots = 1
        
        elif self.shots == 1:
            if self.image == self.armored_duck_exploded:
                self.image = self.duck_open
                self.rect = self.image.get_rect()
            elif self.image == self.duck_open:
                self.image = self.duck_closed
                self.rect = self.image.get_rect()
            elif self.image == self.duck_closed:
                self.image = self.duck_open
                self.rect = self.image.get_rect()

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