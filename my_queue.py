############################################################################################
# my_queue.py
# 
# Last edit: Michael Schnabel
# Last updated: 03 Mar 2026
#
# Reference: A Common-Sense Guide to Data Structures and Algorithms, Wengrow, Ch 9
############################################################################################
# IMPORTS & MACROS

import copy
import unittest

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

############################################################################################
# UNIT TESTS

class TestQueue(unittest.TestCase):

    def setUp(self):
        '''Fresh Queue before each test.'''
        self.q = Queue()

    # init

    def test_init_empty(self):
        self.assertEqual(self.q.size, 0)
        self.assertTrue(self.q.empty())

    # enqueue

    def test_enqueue_increases_size(self):
        self.q.enqueue("a")
        self.assertEqual(self.q.size, 1)

    def test_enqueue_multiple(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertEqual(self.q.size, 2)

    def test_enqueue_none_raises(self):
        with self.assertRaises(ValueError):
            self.q.enqueue(None)

    # dequeue

    def test_dequeue_returns_first(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertEqual(self.q.dequeue(), "a")

    def test_dequeue_decrements_size(self):
        self.q.enqueue("a")
        self.q.dequeue()
        self.assertEqual(self.q.size, 0)

    def test_dequeue_empty_raises(self):
        with self.assertRaises(IndexError):
            self.q.dequeue()

    def test_dequeue_fifo_order(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.q.enqueue("c")
        self.assertEqual(self.q.dequeue(), "a")
        self.assertEqual(self.q.dequeue(), "b")
        self.assertEqual(self.q.dequeue(), "c")

    # empty

    def test_empty_on_new_queue(self):
        self.assertTrue(self.q.empty())

    def test_not_empty_after_enqueue(self):
        self.q.enqueue("a")
        self.assertFalse(self.q.empty())

    def test_empty_after_full_dequeue(self):
        self.q.enqueue("a")
        self.q.dequeue()
        self.assertTrue(self.q.empty())

    # read

    def test_read_returns_front(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertEqual(self.q.read(), "a")

    def test_read_does_not_remove(self):
        self.q.enqueue("a")
        self.q.read()
        self.assertEqual(self.q.size, 1)

    def test_read_empty_returns_none(self):
        self.assertIsNone(self.q.read())

    # __str__

    def test_str_empty(self):
        self.assertEqual(str(self.q), "Queue: []")

    def test_str_nonempty(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        self.assertIn("a", str(self.q))
        self.assertIn("b", str(self.q))

    # copy

    def test_copy_contains_same_data(self):
        self.q.enqueue("a")
        self.q.enqueue("b")
        q2 = self.q.copy()
        self.assertEqual(q2.dequeue(), "a")
        self.assertEqual(q2.dequeue(), "b")

    def test_copy_is_independent(self):
        self.q.enqueue("a")
        q2 = self.q.copy()
        q2.enqueue("b")
        self.assertEqual(self.q.size, 1)


if __name__ == '__main__':
    unittest.main()