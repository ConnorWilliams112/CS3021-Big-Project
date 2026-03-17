# CS3021-Big-Project
# README.md
# Keusch - Schnabel - Williams
# Last Edited: 17 March 2026
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
│
├── engine/
│   |
│   ├── game_engine.py       # OUTER LOOP — state machine cycling between screens
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
│   ├── welcome_screen.py             # Logo, Play button, high score display, music toggle
│   ├── landscape_selector_screen.py  # Landscape selector, rules popup, easter egg handler
│   ├── countdown_screen.py           # "3...2...1...Go!" overlay
│   ├── overlay.py                    # In-game overlay: ammo display, score, timer
│   ├── intermediate_screen.py        # Screen between levels promppting user to continue or exit
│   ├── win_screen.py                 # Stats display, name entry prompt if top 10
│   └── lose_screen.py                # Laughing duck animation, return to menu
│
│
|
├── data_structures/
│   ├── queue.py             # Animal spawn queue
│   └── hash_table.py        # High score storage
│
|
└── persistence/
    └── save_load.py         # JSON read/write for high scores
                             # hash_table ↔ dict ↔ JSON