# Animal.py
# Animals module of CS3021 Big Project 
#
# Contains Animal base class with inheritance for duck types + movement algorithms + dead/alive flags       && Curt if time
# Photos? Hitbox?
#
# Winter 2026
# Last updated: 4 March 2026
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
##### Animal Class ##################################
#####################################################
class Animal(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.life = True        #Using to equal alive/dead status of animal
    


#####################################################
##### Normal Duck Class #############################
#####################################################

class NormalDuck(Animal):

    def __init__(self, name, age, health):
        super().__init__(name, "Normal Duck", age, health)

    def move(self):
        print(f"{self.name} the Normal duck is waddling.")

#####################################################
##### Super Duck Class ##############################
#####################################################

class SuperDuck(Animal):

    def __init__(self, name, age, health):
        super().__init__(name, "Super Duck", age, health)

    def move(self):
        print(f"{self.name} the Super duck is flying!")

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    #Develop some test cases to demonstrate functionality of the Animal and Duck classes
    #Functionality of movement algorithms, displaying ducks, later killing w/ clicks, etc.

    # Create instances of NormalDuck and SuperDuck
    normal_duck = NormalDuck("Daffy", 5, "Healthy")
    super_duck = SuperDuck("SuperDaffy", 3, "Healthy")