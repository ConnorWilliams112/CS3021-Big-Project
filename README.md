# CS3021-Big-Project
Duck/Buck Hunter Project

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
│   ├── animal.py            # Animal base class (position, speed, movement algo,
│   │                        # dead/alive bool, score value, sprite swap)
│   │                        # Duck(Animal), SpecialDuck(Duck) via inheritance
│   │
│   ├── gun.py               # Gun class: ammo, magazine, fire(), reload()
│   │                        # fire() takes cursor pos, compares to duck hitbox → T/F
│   │
│   └── player.py            # Player state: name, current score, level reached
│
├── gui/
│   ├── __init__.py
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── welcome_screen.py      # Logo, Play button, high score display, music toggle
│   │   ├── hunt_select_screen.py  # Landscape selector, rules popup, easter egg handler
│   │   ├── countdown_screen.py    # "3...2...1...Go!" overlay
│   │   ├── hud.py                 # In-game overlay: ammo display, score, timer
│   │   ├── win_screen.py          # Stats display, name entry prompt if top 10
│   │   └── lose_screen.py         # Laughing duck animation, return to menu
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