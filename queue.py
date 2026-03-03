############################################################################################
# queue.py
# 
# Last edit: Michael Schnabel
# Last updated: 03 Mar 2026
#
# Reference: A Common-Sense Guide to Data Structures and Algorithms, Wengrow, Ch 9
############################################################################################
# IMPORTS & MACROS

import copy

############################################################################################

class Queue(object):
    '''Queue Class
    
    A basic queue implemented with First In, First Out (FIFO) properties
    Data inserted at the end of the queue
    Data deleted from the front of the queue
    Only the element at the front of the queue can be read'''

    __hash__ = None
    # Queue is mutable

    def __init__(self):
        ''' Constructor. Allocates an empty queue. '''

        self.__data = []
        self.__size = 0
    
    # properties - getters only, setters managed by methods
    @property
    def data(self):
        return self.__data  # read-only, no setter needed


    @property
    def size(self):
        return self.__size  # read-only, set by enqueue / dequeue


    def enqueue(self, item):
        '''Adds a new item to the end of the queue.'''

        if item is None:
            raise ValueError("Item cannot be None")
        
        # add to end of queue, increase size by 1
        self.__data.append(item)
        self.__size += 1

    def dequeue(self):
        '''Removes and returns the first element of the queue.'''
        
        # protect from removing from an empty queue
        if self.empty():
            raise IndexError("Cannot dequeue from an empty queue")
        
        # decrease size, return and pop first item in queue
        self.__size -= 1
        return self.__data.pop(0)
        

    def empty(self):
        '''Returns boolean answering: is the queue empty?'''

        return self.size == 0       # True if empty
        

    def read(self):
        '''Returns the next item in the queue (to be dequeued). Returns None if empty'''
        
        if not self.empty():
            return self.data[0]
        
        return None
    
    def __str__(self):
        '''Returns string representation of queue from newest addition on left to oldest on right.'''
        
        if self.empty():
            return "Queue: []"
        
        return "Queue: " + " -> ".join(str(item) for item in reversed(self.data))

    def copy(self):
        new_queue = Queue()
        for item in self.data:
            new_queue.enqueue(item)
        return new_queue
        
    #__copy__     implemented
    #__eq__       not applying this to a FIFO
    #__ne__       not applying this to a FIFO
    #__deepcopy__ accepting default implementation


    '''UNIT TESTS: DEVELOP BELOW'''