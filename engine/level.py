# File Name: level.py
# CS3021 Big Project - Duck Hunter
# Owen Keusch, Michael Schnabel, Connor Williams
# Last Updated: 20260309
#
# Level configuration: duck count, speed multiplier, time limit, and score threshold.
# Instantiated by game_loop before each round.
# ----------------------------------------------------------------------------------------


# MACROS
MAX_LEVELS                   = 5
DUCK_COUNT_BASE              = 5     # starting duck count at level 1
TIME_LIMIT_SEC               = 60
POINT_THRESHOLD_PER_LEVEL    = 300
SPECIAL_DUCK_CHANCE_PER_LEVEL = 0.15
SPECIAL_DUCK_CHANCE_MAX      = 0.5


class Level:
    """Configuration for a single game level.

    Attributes:
        number              (int):   Level number (1–5).
        duck_count          (int):   Total ducks spawned this level.
        duck_speed          (float): Base speed for ducks this level (pixels per frame).
        time_limit          (int):   Seconds the player has to complete the level.
        point_threshold     (int):   Minimum score required to win the level.
        special_duck_chance (float): Probability [0.0–1.0] a spawned duck is a special duck.
    """

    # Per-level duck base speeds: levels 1-5
    _DUCK_SPEEDS = {1: 2, 2: 3, 3: 4, 4: 6, 5: 8}

    def __init__(self, number: int = 1):
        self.number              = max(1, min(number, MAX_LEVELS))
        self.duck_count          = DUCK_COUNT_BASE + (self.number - 1) * 2               # 5, 7, 9, 11, 13
        self.duck_speed          = self._DUCK_SPEEDS[self.number]                        # 2, 3, 4, 6, 8
        self.time_limit          = TIME_LIMIT_SEC
        self.point_threshold     = self.number * POINT_THRESHOLD_PER_LEVEL              # 300, 600, 900, …
        self.special_duck_chance = min(SPECIAL_DUCK_CHANCE_PER_LEVEL * self.number, SPECIAL_DUCK_CHANCE_MAX)
