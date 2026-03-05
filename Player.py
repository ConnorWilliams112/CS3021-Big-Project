# Player.py
# Player module of CS3021 Big Project
#
# Contains Player class for handling player functionality
# Tie to JSON stuff for storage of player stats, etc.
#
# Winter 2026
# Last updated: 4 March 2026
#
# Author: Capt Connor Williams

#####################################################
##### IMPORTS BLOCK #################################
#####################################################

import copy as copy

#####################################################
##### Player Class ##################################
#####################################################

class Player(object):

    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.is_alive = True

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} took {damage} damage! Health is now: {self.health}")
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} has died!")

    def heal(self, amount):
        if self.is_alive:
            self.health += amount
            print(f"{self.name} healed for {amount}! Health is now: {self.health}")
        else:
            print(f"{self.name} cannot be healed because they are dead.")

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    #Develop test cases to demonstrate functionality of the Player class

    # Create an instance of Player
    player = Player("Player1", 100)
