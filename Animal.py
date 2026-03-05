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

#####################################################
##### Animal Class ##################################
#####################################################
class Animal(object):

    def __init__(self, name, species, age, health):
        self.name = name
        self.species = species
        self.age = age
        self.health = health
        self.is_alive = True

    def move(self):
        print(f"{self.name} the {self.species} is moving.")

    def eat(self):
        print(f"{self.name} the {self.species} is eating.")

    def sleep(self):
        print(f"{self.name} the {self.species} is sleeping.")

#^^^ Inline colleague slop base

#####################################################
##### Duck Class ####################################
#####################################################
class Duck(Animal):

    def __init__(self, name, age, health, duck_type):
        super().__init__(name, "Duck", age, health)
        self.duck_type = duck_type

    def quack(self):
        print(f"{self.name} the {self.duck_type} duck says: Quack!")

    def move(self):
        print(f"{self.name} the {self.duck_type} duck is waddling.")

#^^^ Inline colleague slop duck

#####################################################
##### Normal Duck Class #############################
#####################################################

class NormalDuck(Duck):

    def __init__(self, name, age, health):
        super().__init__(name, age, health, "Normal")

    def move(self):
        print(f"{self.name} the Normal duck is waddling.")

#####################################################
##### Super Duck Class ##############################
#####################################################

class SuperDuck(Duck):

    def __init__(self, name, age, health):
        super().__init__(name, age, health, "Super")

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