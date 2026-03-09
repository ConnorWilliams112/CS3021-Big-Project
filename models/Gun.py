# Gun.py
# Gun module of CS3021 Big Project
#
# Contains Gun class for handling cursor functionality
# Interrupt handlers for reloading, shooting
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
##### Gun Class #####################################
#####################################################

class Gun(object):

    def __init__(self, name, ammo_capacity):
        self.name = name
        self.ammo_capacity = ammo_capacity
        self.current_ammo = ammo_capacity

    def shoot(self):
        if self.current_ammo > 0:
            self.current_ammo -= 1
            print(f"{self.name} fired! Ammo left: {self.current_ammo}")
        else:
            print(f"{self.name} is out of ammo!")

    def reload(self):
        self.current_ammo = self.ammo_capacity
        print(f"{self.name} reloaded! Ammo is now full: {self.current_ammo}")

#####################################################
##### MAIN BLOCK ####################################
#####################################################

if __name__ == "__main__":
    
    #Develop test cases to demonstrate functionality of the Gun class
    #Functionality of shooting and reloading

    # Create an instance of Gun
    gun = Gun("Pistol", 10)