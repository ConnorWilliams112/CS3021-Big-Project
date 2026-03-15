# CS3021-Big-Project
# Keusch - Schnabel - Williams
# Last Edited: 15 March 2026

Below is a summary of required and optional techniques included in the project:

# #######################################################
# REQUIRED TECHNIQUES
# #######################################################

# Basic Object Functionality:
  HashTable and Queue use private attributes with @property getters for read-only access and a __str__ method. 
  Duck demonstrates best-practice construction with super().__init__(),
  encapsulated state attributes, and computed velocity initialisation (trigonometry on a random angle).
  - data_structures/my_hashtable.py: 16-51  (class definition, __init__, _hash, @property getters, __str__)
  - data_structures/my_queue.py: 16-41      (Queue __init__, @property data/size, __str__)
  - models/Duck.py: 99-133                  (Duck.__init__ with super(), attribute encapsulation, velocity init)


# Exception Handling:
  Exceptions raised at validation and I/O boundaries to prevent game from crashing.
  - data_structures/my_hashtable.py: 59-60  (ValueError raised for None key in HashTable.set)
  - engine/score.py: 46-53                  (try/except FileNotFoundError and JSONDecodeError in load_scores)


# Basic Inheritance:
  NormalDuck and SuperDuck both inherit from the abstract Duck base class, overriding update()
  while calling super().__init__() and super().update() to use shared movement logic.
  Duck and Gun themselves inherit from pygame.sprite.Sprite.
  - models/Duck.py: 93   (class Duck(pygame.sprite.Sprite))
  - models/Duck.py: 248  (class NormalDuck(Duck) — calls super().__init__ line 254, super().update line 272)
  - models/Duck.py: 279  (class SuperDuck(Duck) — calls super().__init__ line 286, super().update line 345)


# GUI use including buttons and text input functionality:
  - screens/welcome_screen.py: 24-36   (UIManager creation, Play/Exit/Music UIButton)
  - screens/win_screen.py: 49-87       (UITextEntryLine for name entry, RETURN key and button-press handling)
  - engine/game_loop.py: 86-101        (KEYDOWN for reload, MOUSEBUTTONDOWN + mouse.get_pos() for shooting)


# Functional programming:
  get_top_10 defines get_score() as a named function and passes it by name as the key= argument
  to sorted(), alongside zip() to pair HashTable keys with values before sorting.
  - engine/score.py: 80-85  (get_score named function defined and passed to sorted() as key=)


# Unit tests for non-GUI functions:
  - data_structures/my_hashtable.py: 164-277  (TestHashTable — init, set/get, delete, has_key, keys/values, copy)
  - data_structures/my_queue.py: 99-207       (TestQueue — enqueue, dequeue, FIFO ordering, edge cases)
  - engine/score.py: 114-218                  (TestScore — calculate_score, submit_score, get_top_10, load/save)


# Use of Framework or Library not covered in class:
  Pygame: rendering, event, sprite, sound, and music
  - engine/game_engine.py: 20-24   (pygame.init, display setup, clock)
  - models/Duck.py: 27-53          (pygame.image.load, transform.scale, transform.flip for sprites)
  - models/Gun.py: 94-101          (pygame.mixer.Sound for shot and reload sound effects)


# Use of two data structures:
  HashTable for high-score table persistence
  Queue used for spawning ducks
  - data_structures/my_hashtable.py  (full HashTable implementation with chaining collision resolution)
  - data_structures/my_queue.py      (full FIFO Queue implementation)
  - engine/game_loop.py: 70-72        (Queue instantiated for duck spawn schedule)
  - engine/game_loop.py: 107-108      (Queue.dequeue() called to release next duck)
  - engine/score.py: 50-74            (HashTable used in load_scores / save_scores)

# ####################################################### 
# OPTIONAL TECHNIQUES
# #######################################################

# Significant functional programming use:
  Beyond the key=lambda sort, the codebase uses list comprehensions as the primary iteration
  tool, any() with a generator expression, and all() for multi-condition checks to minimize
  explicit for-loops.
  - data_structures/my_hashtable.py: 119     (has_key uses any() with generator expression)
  - data_structures/my_hashtable.py: 125-131 (keys() and values() built with list comprehensions)
  - engine/game_loop.py: 94                  (hit detection via list comprehension over sprite group)
  - models/Models_Testbed.py: 199, 224       (all() duck-life check; sum() with generator for score total)


# Grab-bag topic techniques:
  HashTable.__iter__ is a generator using yield to lazily produce each (key, value) pair
  one at a time, allowing the table to be used directly in for-loops and other iteration contexts.
  - data_structures/my_hashtable.py: 150-156  (HashTable.__iter__ generator with yield)


# Use of a Framework or Library not covered in class:
  pygame_gui is a separate library built on Pygame used for button menus and the name entry text field.
  math library used for duck movements
  - screens/welcome_screen.py: 24-36   (UIManager creation, UIButton for Play/Exit/Music)
  - screens/win_screen.py: 49-53       (UITextEntryLine for player name input)
  - models/Duck.py: 203-207            (math.cos and math.sin for duck movement)


# Data export and/or persistence:
  Score records are serialised to JSON on every submission and deserialised on startup so the
  all-time leaderboard survives between sessions.
  - engine/score.py: 38-74          (load_scores reads JSON → HashTable; save_scores writes HashTable → JSON)
  - persistence/scores.json         (live high-score data file)
  - screens/win_screen.py: 84-98    (win screen calls submit_score which triggers save_scores)


# Clever / useful techniques:
  Duck animation is driven by frame-counter parity — no animation library needed. NormalDuck and
  SuperDuck swap between two pre-loaded sprite images (including mirrored flip variants) based on
  a frame counter, giving smooth wing-flap motion at zero runtime cost.
  SuperDuck tracks hit-points and requires multiple shots, demonstrating polymorphic behaviour on
  top of the inherited Duck interface.
  - models/Duck.py: 266-270  (NormalDuck image swap on frame parity)
  - models/Duck.py: 301-343  (SuperDuck hit-point system and multi-image animation cycle)
