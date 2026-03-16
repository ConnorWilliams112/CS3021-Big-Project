# CS3021-Big-Project
# README.md
# Keusch - Schnabel - Williams
# Last Edited: 15 March 2026
Duck/Buck Hunter Project

# BASIC INSTRUCTIONS
## Requirements:
- Python 3.13.x (pygame 2.6.1 is not compatible with Python 3.14+)
- pygame 2.6.1 installed
- pygame_gui 0.6.14 installed
- python-i18n 0.3.9 installed

## To run the game:
- run from project root directory:

python engine/game_engine.py


# GAME INSTRUCTIONS
Aim:    mouse / mousepad
Shoot:  left-click
Reload: 'R' or 'Space'



# FILE ORGANIZATION
duck_hunter/
│
├── main.py                  # Entry point. Creates GameManager, calls .run()             #####Don't have this, entry point is the game_engine
│
├── engine/
│   |
│   ├── game_engine.py      # OUTER LOOP — state machine cycling between screens
│   │                        # States: WELCOME, HUNT_SELECT, PLAYING, WIN, LOSE
│   │                        # Owns the top-level pygame.init() and clock
│   │
│   ├── game_loop.py         # INNER LOOP — per-frame Pygame loop during active play
│   │                        # Called by game_engine when state == PLAYING
│   │                        # Handles: event polling, update(), draw() each frame
│   │                        # Owns: pygame.event.get(), frame timing
│   │
│   ├── level.py             # Level configuration and state
│   │                        # Duck count, speed params, point threshold per level
│   │                        # Instantiated by game_loop, passed to animal spawner
│   │
│   └── score.py             # Score logic: calc points, track hits/misses
│                            # Interface between gameplay and persistence layer
│
├── models/        
|   |
│   ├── Duck.py              # Duck base class (position, speed, movement algo,
│   │                        # dead/alive flags, sprite animation, etc.)
│   │                        # NormalDuck & SuperDuck subclasses via inheritance
│   │
|   |
│   ├── Models_Testbed.py    # Used instead of unit tests to check functionality of 
|   |                        # Duck and Gun classes/sprites
│   │
|   |
│   ├── Gun.py               # Gun class: ammo, magazine, fire(), reload()
│   │                        # fire() takes cursor pos, compares to duck hitbox → T/F
│   │
│   │
│   ├── Images/              # Duck sprite assets (PNG with transparent backgrounds)
│   │                        # Gun sprites for various ammo levels
|   |                        # Images of landscape (Desert, Forest, Arctic) 
│   │ 
|   |
│   └── Sounds/              #Empty Click for gun
│                            #Firing Sound for gun
|                            #Reloading sound for gun
│                            #Game Music
│    
│
├── screens/
│   │   ├── __init__.py
│   │   ├── welcome_screen.py             # Logo, Play button, high score display, music toggle
│   │   ├── landscape_selector_screen.py  # Landscape selector, rules popup, easter egg handler
│   │   ├── countdown_screen.py           # "3...2...1...Go!" overlay
│   │   ├── overlay.py                    # In-game overlay: ammo display, score, timer
│   │   ├── intermediate_screen.py        # Screen between levels promppting user to continue or exit
│   │   ├── win_screen.py                 # Stats display, name entry prompt if top 10
│   │   └── lose_screen.py                # Laughing duck animation, return to menu
│   │
│   └── button.py            # Button class — click handling, callback via
│                            # function-as-argument (satisfies functional prog req)
│
├── data_structures/
│   ├── __init__.py
│   ├── queue.py             # Animal spawn queue
│   └── hash_table.py        # High score storage
│
├── persistence/
│   ├── __init__.py
│   └── save_load.py         # JSON read/write for high scores
│                            # hash_table ↔ dict ↔ JSON
│
└── tests/                                                                                        #######Don't see as apart of final submission. Is apart of required techniques "Unittests"
    ├── __init__.py
    ├── test_queue.py
    ├── test_hash_table.py
    ├── test_score.py
    ├── test_gun.py
    ├── test_animal.py
    └── test_button.py

## Image Processing Pipeline

### Duck Sprite Assets

All duck sprites in `models/Images/` have been processed to have transparent backgrounds instead of white:

- **Original Format**: PNG images with solid white backgrounds
- **Processing Method**: `remove_white_background.py` script (PIL-based)
  - Converts images to RGBA mode
  - Detects near-white pixels (RGB > 240 on all channels)
  - Replaces white pixels with transparent (alpha = 0)
  - Preserves original image dimensions and anti-aliasing

### Processed Images

- `Duck_Open.png` / `Duck_Open_flipped.png` — Normal duck open wings
- `Duck_Closed.png` / `Duck_Closed_flipped.png` — Normal duck closed wings
- `Duck_Dead.png` / `Duck_Dead_flipped.png` — Dead duck state
- `Armored_Duck_Open.png` / `Armored_Duck_Open_flipped.png` — SuperDuck armored state (open)
- `Armored_Duck_Closed.png` / `Armored_Duck_Closed_flipped.png` — SuperDuck armored state (closed)
- `Armored_Duck_Exploded.png` / `Armored_Duck_Exploded_flipped.png` — SuperDuck damaged state

### Archive Note

The `remove_white_background.py` script is preserved in the repository for reference and future image reprocessing if needed. It is **not** part of the game runtime.