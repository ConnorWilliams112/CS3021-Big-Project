# Gun.py
# Gun module of CS3021 Big Project
#
# Contains Gun class for handling cursor functionality
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
import pygame_gui as gui            #Needed?
import random as random
import math as math
import os

# Get the directory where this file is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds")
IMAGES_DIR = os.path.join(SCRIPT_DIR, "Images")
# Load sounds
try:
    reload_sound = pg.mixer.Sound('Reloading.mp3')              #FAHHHH sound for miss
    firing_sound = pg.mixer.Sound('Firing.mp3')
    click_sound = pg.mixer.Sound('EmptyClick.mp3')
except pg.error as e:
    print(f"Error loading sound: {e}")
    print(f"Looking for sounds in: {SOUND_DIR}")
    exit()

# load images
try:
    _6rds = pg.image.load(os.path.join(IMAGES_DIR, "6rds.png"))             #Need to clear out whitespace
    _6rds = _6rds.convert_alpha()
    _5rds = pg.image.load(os.path.join(IMAGES_DIR, "5rds.png"))             #Are images best way to do it? or just do a status bar or something?
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

MAGAZINE = 6

#####################################################
##### Gun Class #####################################
#####################################################

class Gun(pg.sprite.Sprite):
    '''
    Class container for gun/magazine logic. Initializes a round counter at top right of screen that decrements with reloads.
    Also has magazine/tube bar that decrements with mouseclick 

    Start with BASE + (level - 1) * 6 rounds
    "Magazine" holds 6rds (shotgun tube)
    Spacebar reloads, decrements total,

    Spacebar and mouseclick functionality lives in game engine, calls methods that exist in the class
    '''
    def __init__(self, level):
        super().__init__()
        self.ammo_capacity = MAGAZINE + (level - 1) * MAGAZINE          ### Would like to display this in top right of screen ###
        self.current_ammo = self.ammo_capacity                          ### Getter/setter ??? Protect current_ammo and mag ???
        self.current_mag = MAGAZINE
        self.image = _6rds
        self.rect = self.image.get_rect()                               ### Display functionality called via testbed (like DuckDuckGo)
        try:
            self.reload_sound = pg.mixer.Sound(os.path.join(SOUND_DIR, 'Reloading.mp3'))
            self.firing_sound = pg.mixer.Sound(os.path.join(SOUND_DIR, 'Firing.mp3'))
            self.click_sound  = pg.mixer.Sound(os.path.join(SOUND_DIR, 'EmptyClick.mp3'))
        except pg.error as e:
            print(f"Error loading sound: {e}")
            print(f"Looking for sounds in: {SOUND_DIR}")
            exit()

    def shoot(self):
        '''
        If rounds left in magazine, plays "firing" sound and decrements magazine
        If no rounds, plays clicking sound
        '''
        if self.current_mag > 0:
            self.current_mag -= 1
            if self.current_mag == 5:
                self.image = _5rds
                self.rect = self.image.get_rect()
            elif self.current_mag == 4:
                self.image = _4rds
                self.rect = self.image.get_rect()
            elif self.current_mag == 3:
                self.image - _3rds
                self.rect = self.image.get_rect()
            elif self.current_mag == 2:
                self.image = _2rds
                self.rect = self.image.get_rect()
            elif self.current_mag == 1:
                self.image = _1rds
                self.rect = self.image.get_rect()
            else:
                self.image = _0rds
                self.rect = self.image.get_rect()
            return self.firing_sound.play()
        else:
            self.image = _0rds
            self.rect = self.image.get_rect()
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
                return reload_sound.play()
            else:
                self.current_mag += remaining
                self.current_ammo = 0
                return reload_sound.play()

    #def update(self):
        # TO DO

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    pass