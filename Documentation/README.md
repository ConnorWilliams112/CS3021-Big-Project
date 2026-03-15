# CS3021-Big-Project
# README.md
# Keusch - Schnabel - Williams
# Last Edited: 15 March 2026
Duck/Buck Hunter Project

# BASIC INSTRUCTIONS



# GAME INSTRUCTIONS




# FILE ORGANIZATION
duck_hunter/
│
├── main.py                  # Entry point. Creates GameManager, calls .run()
│
├── engine/
│   ├── __init__.py
│   ├── game_manager.py      # OUTER LOOP — state machine cycling between screens
│   │                        # States: WELCOME, HUNT_SELECT, PLAYING, WIN, LOSE
│   │                        # Owns the top-level pygame.init() and clock
│   │
│   ├── game_loop.py         # INNER LOOP — per-frame Pygame loop during active play
│   │                        # Called by game_manager when state == PLAYING
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
│   ├── __init__.py
│   ├── Duck.py              # Duck base class (position, speed, movement algo,
│   │                        # dead/alive flags, sprite animation)
│   │                        # NormalDuck & SuperDuck subclasses via inheritance
│   │
│   ├── DuckDuckGo.py        # Main game file (pygame launch point)
│   │
│   ├── Gun.py               # Gun class: ammo, magazine, fire(), reload()
│   │                        # fire() takes cursor pos, compares to duck hitbox → T/F
│   │
│   ├── Player.py            # Player state: name, current score, level reached
│   │
│   ├── Images/              # Duck sprite assets (PNG with transparent backgrounds)
│   │                        # Processing note: white backgrounds removed via PIL
│   │                        # (see Image Processing Pipeline below)
│   │
│   └── remove_white_background.py  # [ARCHIVE] One-time image processing script
│                            # Removes white backgrounds from PNGs → transparency
│                            # Kept for reference/future image reprocessing
│
├── gui/
│   ├── __init__.py
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── welcome_screen.py             # Logo, Play button, high score display, music toggle
│   │   ├── landscape_selector_screen.py  # Landscape selector, rules popup, easter egg handler
│   │   ├── countdown_screen.py           # "3...2...1...Go!" overlay
│   │   ├── overlay.py                    # In-game overlay: ammo display, score, timer
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
└── tests/
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