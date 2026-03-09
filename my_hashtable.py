############################################################################################
# my_hashtable.py
#
# Last edit: Michael Schnabel
# Last updated: 08 Mar 2026
#
# Reference: A Common-Sense Guide to Data Structures and Algorithms, Wengrow, Ch 7
############################################################################################
# IMPORTS & MACROS

import copy

############################################################################################

class HashTable(object):
    '''HashTable Class

    A basic hash table with separate chaining for collision handling.
    Keys are hashed to bucket indices; each bucket holds a list of (key, value) pairs.
    Supports O(1) average-case lookup, insertion, and deletion.'''

    __hash__ = None     # HashTable is mutable

    def __init__(self, capacity=17):
        '''Constructor. Allocates an empty hash table with the given number of buckets.
        
        Default capacity is 17 to accomodate 10 scores in high score table.'''

        self.__capacity = capacity
        self.__data = [[] for _ in range(self.__capacity)]
        self.__size = 0

    # properties - getters only, setters managed by methods
    @property
    def data(self):
        return self.__data  # read-only, no setter needed

    @property
    def size(self):
        return self.__size  # read-only, set by set / delete

    @property
    def capacity(self):
        return self.__capacity  # read-only, fixed at construction


    def _hash(self, key):
        '''Returns the bucket index for a given key.'''

        return hash(key) % self.__capacity


    def set(self, key, value):
        '''Inserts a key-value pair. Overwrites the value if key already exists.
        
        Note: caller is responsible for score comparison in score.py before calling set'''

        # Note

        if key is None:
            raise ValueError("Key cannot be None")

        index = self._hash(key)
        bucket = self.__data[index]

        # update existing key if found
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # key not found, insert new pair
        bucket.append((key, value))
        self.__size += 1


    def get(self, key):
        '''Returns the value associated with the key, or None if not found.'''

        if key is None:
            raise ValueError("Key cannot be None")

        index = self._hash(key)
        bucket = self.__data[index]

        for k, v in bucket:
            if k == key:
                return v

        return None


    def delete(self, key):
        '''Removes the key-value pair for the given key. Raises KeyError if not found.'''

        if key is None:
            raise ValueError("Key cannot be None")

        index = self._hash(key)
        bucket = self.__data[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.__size -= 1
                return

        raise KeyError(f"Key '{key}' not found in hash table")


    def has_key(self, key):
        '''Returns boolean answering: does the key exist in the table?'''

        if key is None:
            return False

        index = self._hash(key)
        bucket = self.__data[index]

        return any(k == key for k, _ in bucket)


    def keys(self):
        '''Returns a list of all keys in the hash table.'''

        return [k for bucket in self.__data for k, _ in bucket]


    def values(self):
        '''Returns a list of all values in the hash table.'''

        return [v for bucket in self.__data for _, v in bucket]


    def empty(self):
        '''Returns boolean answering: is the hash table empty?'''

        return self.__size == 0


    def __str__(self):
        '''Returns string representation of the hash table as key -> value pairs.'''

        if self.empty():
            return "HashTable: {}"

        pairs = [f"{k}: {v}" for bucket in self.__data for k, v in bucket]
        return "HashTable: {" + ", ".join(pairs) + "}"


    def copy(self):
        '''Returns a shallow copy of the hash table.'''

        new_table = HashTable(self.__capacity)
        for key in self.keys():
            new_table.set(key, self.get(key))
        return new_table

    #__copy__     implemented
    #__eq__       not implemented
    #__ne__       not implemented
    #__deepcopy__ accepting default implementation


    '''UNIT TESTS: DEVELOP BELOW'''
