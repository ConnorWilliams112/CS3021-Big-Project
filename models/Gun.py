# Gun.py
# Gun module of CS3021 Big Project
#
# Contains Gun class for handling cursor functionality
# Includes sound effects, ammo displayed via a gun image, and reloading logic 
#
#
# Winter 2026
# Last updated: 11 March 2026
#
# Author: Capt Connor Williams

#####################################################
##### IMPORTS BLOCK #################################
#####################################################

import copy as copy
import pygame as pg
import pygame_gui as gui            #Needed?
import random as random
import math as math
import os

# Get the directory where this file is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds")
IMAGES_DIR = os.path.join(SCRIPT_DIR, "Images")

# load images
try:
    _6rds = pg.image.load(os.path.join(IMAGES_DIR, "6rds.png"))
    _6rds = _6rds.convert_alpha()
    _5rds = pg.image.load(os.path.join(IMAGES_DIR, "5rds.png"))
    _5rds = _5rds.convert_alpha()
    _4rds = pg.image.load(os.path.join(IMAGES_DIR, "4rds.png"))
    _4rds = _4rds.convert_alpha()
    _3rds = pg.image.load(os.path.join(IMAGES_DIR, "3rds.png"))
    _3rds = _3rds.convert_alpha()
    _2rds = pg.image.load(os.path.join(IMAGES_DIR, "2rds.png"))
    _2rds = _2rds.convert_alpha()
    _1rds = pg.image.load(os.path.join(IMAGES_DIR, "1rds.png"))
    _1rds = _1rds.convert_alpha()
    _0rds = pg.image.load(os.path.join(IMAGES_DIR, "0rds.png"))
    _0rds = _0rds.convert_alpha()
except pg.error as er:
    print(f"Error loading image: {er}")
    print(f"Looking for images in: {IMAGES_DIR}")
    exit()

#####################################################
##### Constants #####################################
#####################################################

# Gun display constants
GUN_WIDTH = 140
GUN_HEIGHT = 80
MAGAZINE = 6
SMALL_FONT = 20
BIG_FONT = 32
HOR_BUFFER = 5
VERT_BUFFER = 50

# Scale all gun images to gun dimensions
_6rds = pg.transform.scale(_6rds, (GUN_WIDTH, GUN_HEIGHT))
_5rds = pg.transform.scale(_5rds, (GUN_WIDTH, GUN_HEIGHT))
_4rds = pg.transform.scale(_4rds, (GUN_WIDTH, GUN_HEIGHT))
_3rds = pg.transform.scale(_3rds, (GUN_WIDTH, GUN_HEIGHT))
_2rds = pg.transform.scale(_2rds, (GUN_WIDTH, GUN_HEIGHT))
_1rds = pg.transform.scale(_1rds, (GUN_WIDTH, GUN_HEIGHT))
_0rds = pg.transform.scale(_0rds, (GUN_WIDTH, GUN_HEIGHT))

#####################################################
##### Gun Class #####################################
#####################################################

class Gun(pg.sprite.Sprite):
    '''
    Class container for gun/magazine logic. Initializes a round counter at top right of screen that decrements with reloads.
    Also has revolver cylinder that decrements with mouseclick 

    Start with BASE + (level - 1) * 6 rounds
    "Magazine" holds 6rds
    Spacebar reloads, decrements total

    Spacebar and mouseclick functionality lives in game engine, calls methods that exist in the class
    '''
    def __init__(self, level):
        super().__init__()
        self.ammo_capacity = MAGAZINE + (level - 1) * MAGAZINE      
        self.current_ammo = self.ammo_capacity
        self.current_mag = MAGAZINE
        self.image = _6rds
        self.rect = self.image.get_rect()
        try:
            self.reload_sound = pg.mixer.Sound(os.path.join(SOUND_DIR, 'Reloading.mp3'))
            self.firing_sound = pg.mixer.Sound(os.path.join(SOUND_DIR, 'Firing.mp3'))
            self.click_sound  = pg.mixer.Sound(os.path.join(SOUND_DIR, 'EmptyClick.mp3'))
        except pg.error as e:
            print(f"Error loading sound: {e}")
            print(f"Looking for sounds in: {SOUND_DIR}")
            exit()

    #####################################################
    ##### Standard dunder override methods Block ########
    #####################################################

    # Accepting default hash, eq, neq behaviors due to not needing
    # to compare guns (as there is only ever 1 gun instance at a time)

    # Accepting default copy and deepcopy behaviors since we don't need to create copies of guns in our game logic, 
    # and the default behavior of copying the sprite's attributes is sufficient for our purposes.

    # Accepting default str behavior since we won't be printing gun instances directly, 
    # and the default representation is sufficient for debugging purposes.

    #####################################################
    ##### Custom Behaviors Block ########################
    #####################################################

    def shoot(self):
        '''
        If rounds left in magazine, plays "firing" sound and decrements magazine
        If no rounds, plays clicking sound
        '''
        if self.current_mag > 0:
            self.current_mag -= 1
            self.update()
            self.rect = self.image.get_rect(topright=self.rect.topright)
            return self.firing_sound.play()
        else:
            self.image = _0rds
            self.rect = self.image.get_rect(topright=self.rect.topright)
            return self.click_sound.play()

    def reload(self):
        '''
        Accessed from game via spacebar

        Reloads and plays sound only if ammo remains and magazine not already full
        If reloads, decrements capacity by # rounds reloaded
        '''
        remaining = self.current_ammo
        magazine = self.current_mag

        if magazine == MAGAZINE or remaining == 0:
            return
        else:
            delta = MAGAZINE - magazine
            if remaining >= delta:
                self.current_ammo -= delta
                self.current_mag = MAGAZINE
                return self.reload_sound.play()
            else:
                self.current_mag += remaining
                self.current_ammo = 0
                return self.reload_sound.play()

    def update(self):
        '''
        Update method syncs the gun image to match current magazine state every frame.
        '''
        if self.current_mag == 6:
            self.image = _6rds
        elif self.current_mag == 5:
            self.image = _5rds
        elif self.current_mag == 4:
            self.image = _4rds
        elif self.current_mag == 3:
            self.image = _3rds
        elif self.current_mag == 2:
            self.image = _2rds
        elif self.current_mag == 1:
            self.image = _1rds
        else:
            self.image = _0rds

    def render_ammo_display(self, surface, position):
        '''
        Render the ammo display (title and count) at the given position.
        '''
        # Small font for title, medium font for count
        small_font = pg.font.Font(None, SMALL_FONT)
        medium_font = pg.font.Font(None, BIG_FONT)
        
        # Render title
        title_text = small_font.render(" Total \n Rounds \n Remaining", True, (0, 0, 0))
        surface.blit(title_text, position)
        
        # Render count below title
        count_text = medium_font.render(str(self.current_ammo), True, (0, 0, 0))
        surface.blit(count_text, (position[0] + HOR_BUFFER, position[1] + VERT_BUFFER))

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    print("This module is not meant to be run directly. Please run Models_Testbed.py to test Gun() functionality.")