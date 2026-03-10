############################################################################################
# level.py
#
# Last edit: Michael Schnabel
# Last updated: 09 Mar 2026
#
# Manages level state: countdown, timer, hit/miss tracking, and win/lose conditions.
# Logic only — no Pygame. Rendering handled by gui/level_screen.py.
############################################################################################
# IMPORTS & MACROS

import unittest
import time
from data_structures.my_queue import Queue

LEVEL_DURATION     = 30.0   # seconds per level
COUNTDOWN_DURATION = 3      # seconds for 3...2...1...Go!
WIN_THRESHOLD      = 0.6    # fraction of animals that must be hit to win

############################################################################################

class Level(object):
    '''Level Class

    Manages the state of a single gameplay level.
    Tracks countdown, timer, animal queue, hits, misses, and win/lose conditions.
    Stateless with respect to rendering — all display handled externally.'''

    __hash__ = None     # Level is mutable

    def __init__(self, level_number: int, animal_queue: Queue):
        '''Constructor. Initializes level state.

        Args:
            level_number: 1-indexed level number (affects win threshold scaling)
            animal_queue: pre-populated Queue of Animal objects for this level
        '''

        if not isinstance(level_number, int) or level_number < 1:
            raise ValueError("Level number must be a positive integer")
        if not isinstance(animal_queue, Queue):
            raise TypeError("animal_queue must be a Queue instance")
        if animal_queue.empty():
            raise ValueError("animal_queue cannot be empty")

        self.__level_number  = level_number
        self.__animal_queue  = animal_queue
        self.__total_animals = animal_queue.size

        self.__hits           = 0
        self.__misses         = 0
        self.__time_remaining = LEVEL_DURATION
        self.__countdown      = COUNTDOWN_DURATION
        self.__started        = False
        self.__countdown_done = False
        self.__over           = False

    # properties - getters only, setters managed by methods

    @property
    def level_number(self):
        return self.__level_number

    @property
    def hits(self):
        return self.__hits

    @property
    def misses(self):
        return self.__misses

    @property
    def time_remaining(self):
        return self.__time_remaining

    @property
    def countdown(self):
        '''Current countdown value (3, 2, 1, 0 = Go!). Returns 0 once countdown is done.'''
        return max(0, int(self.__countdown))

    @property
    def countdown_done(self):
        return self.__countdown_done

    @property
    def animal_queue(self):
        return self.__animal_queue

    @property
    def over(self):
        return self.__over

    # methods

    def start(self):
        '''Begin the level countdown. Must be called before update().'''

        if self.__started:
            raise RuntimeError("Level has already been started")
        self.__started = True

    def update(self, dt: float):
        '''Advance level state by dt seconds. Call once per game loop tick.

        Args:
            dt: delta time in seconds since last update
        '''

        if not self.__started or self.__over:
            return

        if not self.__countdown_done:
            self.__countdown -= dt
            if self.__countdown <= 0:
                self.__countdown_done = True
            return

        self.__time_remaining -= dt
        if self.__time_remaining <= 0:
            self.__time_remaining = 0
            self.__over = True

    def register_hit(self):
        '''Record a successful hit. Raises RuntimeError if level is not active.'''
        
        if not self.__countdown_done or self.__over:
            raise RuntimeError("Cannot register hit — level is not active")
        self.__hits += 1
        if self.__hits + self.__misses >= self.__total_animals:
            self.__over = True

    def register_miss(self):
        '''Record a missed shot. Raises RuntimeError if level is not active.'''
        
        if not self.__countdown_done or self.__over:
            raise RuntimeError("Cannot register miss — level is not active")
        self.__misses += 1
        if self.__hits + self.__misses >= self.__total_animals:
            self.__over = True

    def is_won(self):
        '''Returns True if the player hit enough animals to pass the level.'''
        
        if self.__total_animals == 0:
            return False
        return self.__hits / self.__total_animals >= WIN_THRESHOLD

    def is_lost(self):
        '''Returns True if the level is over and the player did not win.'''
        
        return self.__over and not self.is_won()

    def get_stats(self):
        '''Return level stats as a dict for consumption by score.py.

        Returns:
            dict with keys: hits, misses, level, time_remaining
        '''
        
        return {
            'hits': self.__hits,
            'misses': self.__misses,
            'level': self.__level_number,
            'time_remaining': self.__time_remaining
        }

    def __str__(self):
        
        status = "countdown" if not self.__countdown_done else ("over" if self.__over else "active")
        
        return (f"Level {self.__level_number} [{status}] | "
                f"Hits: {self.__hits} | Misses: {self.__misses} | "
                f"Time: {self.__time_remaining:.1f}s")

    #__copy__     not implemented
    #__eq__       not implemented
    #__ne__       not implemented
    #__deepcopy__ accepting default implementation

############################################################################################
# UNIT TESTS

class TestLevel(unittest.TestCase):

    def setUp(self):
        '''Fresh Level before each test.'''
        self.queue = Queue()
        self.queue.enqueue("duck")
        self.queue.enqueue("duck")
        self.queue.enqueue("duck")
        self.level = Level(1, self.queue)

    # init

    def test_init_valid(self):
        self.assertEqual(self.level.level_number, 1)
        self.assertEqual(self.level.hits, 0)
        self.assertEqual(self.level.misses, 0)
        self.assertFalse(self.level.over)

    def test_init_invalid_level_number_raises(self):
        q = Queue()
        q.enqueue("duck")
        with self.assertRaises(ValueError):
            Level(0, q)

    def test_init_non_int_level_raises(self):
        q = Queue()
        q.enqueue("duck")
        with self.assertRaises(ValueError):
            Level("one", q)

    def test_init_invalid_queue_type_raises(self):
        with self.assertRaises(TypeError):
            Level(1, [])

    def test_init_empty_queue_raises(self):
        with self.assertRaises(ValueError):
            Level(1, Queue())

    # start

    def test_start_leaves_countdown_active(self):
        self.level.start()
        self.assertFalse(self.level.countdown_done)

    def test_start_twice_raises(self):
        self.level.start()
        with self.assertRaises(RuntimeError):
            self.level.start()

    # update

    def test_update_before_start_does_nothing(self):
        self.level.update(1.0)
        self.assertEqual(self.level.time_remaining, LEVEL_DURATION)

    def test_update_ticks_countdown(self):
        self.level.start()
        self.level.update(1.0)
        self.assertEqual(self.level.countdown, COUNTDOWN_DURATION - 1)

    def test_update_finishes_countdown(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.assertTrue(self.level.countdown_done)

    def test_update_decrements_time(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.update(5.0)
        self.assertAlmostEqual(self.level.time_remaining, LEVEL_DURATION - 5.0, places=1)

    def test_update_time_expires_ends_level(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.update(LEVEL_DURATION + 1.0)
        self.assertTrue(self.level.over)
        self.assertEqual(self.level.time_remaining, 0)

    # register_hit / register_miss

    def test_register_hit_increments(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.register_hit()
        self.assertEqual(self.level.hits, 1)

    def test_register_miss_increments(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.register_miss()
        self.assertEqual(self.level.misses, 1)

    def test_register_hit_before_countdown_raises(self):
        self.level.start()
        with self.assertRaises(RuntimeError):
            self.level.register_hit()

    def test_register_miss_before_countdown_raises(self):
        self.level.start()
        with self.assertRaises(RuntimeError):
            self.level.register_miss()

    def test_all_animals_tallied_ends_level(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.register_hit()
        self.level.register_hit()
        self.level.register_hit()
        self.assertTrue(self.level.over)

    # is_won / is_lost

    def test_is_won_sufficient_hits(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.register_hit()
        self.level.register_hit()
        self.level.register_hit()
        self.assertTrue(self.level.is_won())

    def test_is_lost_insufficient_hits(self):
        self.level.start()
        self.level.update(COUNTDOWN_DURATION + 0.1)
        self.level.register_miss()
        self.level.register_miss()
        self.level.register_miss()
        self.assertTrue(self.level.is_lost())

    # get_stats

    def test_get_stats_keys(self):
        stats = self.level.get_stats()
        self.assertIn('hits', stats)
        self.assertIn('misses', stats)
        self.assertIn('level', stats)
        self.assertIn('time_remaining', stats)

    def test_get_stats_initial_values(self):
        stats = self.level.get_stats()
        self.assertEqual(stats['hits'], 0)
        self.assertEqual(stats['misses'], 0)
        self.assertEqual(stats['level'], 1)
        self.assertEqual(stats['time_remaining'], LEVEL_DURATION)

    # __str__

    def test_str_contains_level_number(self):
        self.assertIn("1", str(self.level))

    def test_str_shows_status(self):
        self.assertIn("countdown", str(self.level))


if __name__ == '__main__':
    unittest.main()
