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
import unittest

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

############################################################################################
# UNIT TESTS

class TestHashTable(unittest.TestCase):

    def setUp(self):
        '''Fresh HashTable before each test.'''
        self.ht = HashTable()

    # init

    def test_init_default_capacity(self):
        self.assertEqual(self.ht.size, 0)
        self.assertEqual(self.ht.capacity, 17)
        self.assertTrue(self.ht.empty())

    def test_init_custom_capacity(self):
        ht = HashTable(capacity=5)
        self.assertEqual(ht.capacity, 5)

    # set / get

    def test_set_and_get(self):
        self.ht.set("alice", 100)
        self.assertEqual(self.ht.get("alice"), 100)
        self.assertEqual(self.ht.size, 1)

    def test_set_overwrites_existing_key(self):
        self.ht.set("alice", 100)
        self.ht.set("alice", 200)
        self.assertEqual(self.ht.get("alice"), 200)
        self.assertEqual(self.ht.size, 1)   # size must not grow on overwrite

    def test_get_missing_key_returns_none(self):
        self.assertIsNone(self.ht.get("ghost"))

    def test_set_none_key_raises(self):
        with self.assertRaises(ValueError):
            self.ht.set(None, 42)

    def test_get_none_key_raises(self):
        with self.assertRaises(ValueError):
            self.ht.get(None)

    # delete

    def test_delete_removes_key(self):
        self.ht.set("alice", 100)
        self.ht.delete("alice")
        self.assertEqual(self.ht.size, 0)
        self.assertIsNone(self.ht.get("alice"))
        self.assertFalse(self.ht.has_key("alice"))

    def test_delete_missing_key_raises(self):
        with self.assertRaises(KeyError):
            self.ht.delete("ghost")

    def test_delete_none_key_raises(self):
        with self.assertRaises(ValueError):
            self.ht.delete(None)

    # has_key

    def test_has_key_present(self):
        self.ht.set("alice", 100)
        self.assertTrue(self.ht.has_key("alice"))

    def test_has_key_absent(self):
        self.assertFalse(self.ht.has_key("bob"))

    def test_has_key_none(self):
        self.assertFalse(self.ht.has_key(None))

    # keys / values

    def test_keys_and_values(self):
        self.ht.set("alice", 100)
        self.ht.set("bob", 200)
        self.assertEqual(sorted(self.ht.keys()), ["alice", "bob"])
        self.assertEqual(sorted(self.ht.values()), [100, 200])

    # empty

    def test_empty_on_new_table(self):
        self.assertTrue(self.ht.empty())

    def test_not_empty_after_insert(self):
        self.ht.set("alice", 100)
        self.assertFalse(self.ht.empty())

    # __str__

    def test_str_empty(self):
        self.assertEqual(str(self.ht), "HashTable: {}")

    def test_str_nonempty(self):
        self.ht.set("alice", 100)
        result = str(self.ht)
        self.assertIn("alice", result)
        self.assertIn("100", result)

    # copy

    def test_copy_contains_same_data(self):
        self.ht.set("alice", 100)
        ht2 = self.ht.copy()
        self.assertEqual(ht2.get("alice"), 100)
        self.assertEqual(ht2.size, 1)

    def test_copy_is_independent(self):
        self.ht.set("alice", 100)
        ht2 = self.ht.copy()
        ht2.set("bob", 200)
        self.assertFalse(self.ht.has_key("bob"))


if __name__ == '__main__':
    unittest.main()
