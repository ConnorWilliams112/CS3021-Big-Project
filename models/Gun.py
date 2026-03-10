# Gun.py
# Gun module of CS3021 Big Project
#
# Contains Gun class for handling cursor functionality
# Interrupt handlers for reloading, shooting
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
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds")

# Load sounds
try:
    reload_sound = pg.mixer.Sound('Reloading.mp3')
    firing_sound = pg.mixer.Sound('Firing.mp3')
    click_sound = pg.mixer.Sound('EmptyClick.mp3')
except pg.error as e:
    print(f"Error loading sound: {e}")
    print(f"Looking for sounds in: {SOUND_DIR}")
    exit()

#####################################################
##### Constants #####################################
#####################################################

MAGAZINE = 6

#####################################################
##### Gun Class #####################################
#####################################################

class Gun(pg.sprite.Sprite):
    '''
    Class container for gun/magazine logic. Initializes a round counter at top right of screen that decrements with mouse clicks.
    Also has magazine/tube bar that decrements with click

    Start with BASE + (level - 1) * 6 rounds
    "Magazine" holds 6rds (shotgun tube)
    Spacebar reloads, decrements total,

    Spacebar and mouseclick functionality lives in game engine, calls methods that exist in the class
    '''
    def __init__(self, level):
        super.__init__()
        self.ammo_capacity = MAGAZINE + (level - 1) * MAGAZINE
        self.current_ammo = self.ammo_capacity
        self.current_mag = MAGAZINE

    def shoot(self):
        if self.current_ammo > 0:
            self.current_ammo -= 1
            pass
        else:
            pass

    def reload(self):
        if self.current_ammo

        reload_sound.play()


#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    #Develop test cases to demonstrate functionality of the Gun class
    #Functionality of shooting and reloading

    # Create an instance of Gun
    gun = Gun("Pistol", 10)