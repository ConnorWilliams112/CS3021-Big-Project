############################################################################################
# score.py
#
# Last edit: Michael Schnabel
# Last updated: 08 Mar 2026
#
# Handles score calculation and JSON persistence for the high score system.
# Interfaces with HashTable from data_structures.
############################################################################################
# IMPORTS & MACROS

import json
import os
from datetime import date
from data_structures.my_hashtable import HashTable

SCORE_FILE = os.path.join(os.path.dirname(__file__), '..', 'persistence', 'scores.json')
TOP_N = 10

############################################################################################

def calculate_score(hits: int, misses: int, level: int, time_remaining: float) -> int:
    '''Calculate and return a score based on gameplay stats.

    Formula: (hits * 100) - (misses * 25) + (level * 50) + (time_remaining * 10)
    Minimum score is 0.'''

    raw = (hits * 100) - (misses * 25) + (level * 50) + int(time_remaining * 10)
    return max(0, raw)


def load_scores(filepath: str = SCORE_FILE) -> HashTable:
    '''Load scores from a JSON file and return a populated HashTable.

    If the file does not exist or is empty, returns an empty HashTable.
    Raises ValueError if the file contains malformed data.'''

    table = HashTable()

    if not os.path.exists(filepath):
        return table

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed scores file at {filepath}: {e}")

    for entry in data:
        table.set(entry['name'], {'score': entry['score'], 'date': entry['date']})

    return table


def save_scores(table: HashTable, filepath: str = SCORE_FILE) -> None:
    '''Serialize the HashTable to JSON and write to filepath.

    Creates the file and parent directories if they do not exist.'''

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    data = [
        {'name': k, 'score': v['score'], 'date': v['date']}
        for k, v in zip(table.keys(), table.values())
    ]

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_top_10(table: HashTable) -> list:
    '''Return a sorted list of the top 10 (name, score, date) tuples, highest score first.'''

    all_entries = list(zip(table.keys(), table.values()))
    sorted_entries = sorted(all_entries, key=lambda entry: entry[1]['score'], reverse=True)
    return [(name, val['score'], val['date']) for name, val in sorted_entries[:TOP_N]]


def is_top_10(score: int, table: HashTable) -> bool:
    '''Return True if the given score qualifies for the top 10.

    A score qualifies if there are fewer than 10 entries, or if it beats the lowest score.'''

    top = get_top_10(table)
    if len(top) < TOP_N:
        return True
    return score > top[-1][1]  # compare against lowest score in top 10


def submit_score(name: str, score: int, table: HashTable) -> bool:
    '''Insert or update a player's score if it beats their existing entry.

    Returns True if the score was submitted, False if the existing score was higher.
    Note: caller should check is_top_10() before calling this if top-10 gating is needed.'''
    
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Player name must be a non-empty string")
    if not isinstance(score, int) or score < 0:
        raise ValueError("Score must be a non-negative integer")

    existing = table.get(name)
    if existing is not None and existing['score'] >= score:
        return False

    table.set(name, {'score': score, 'date': str(date.today())})
    return True


'''UNIT TESTS: DEVELOP BELOW'''