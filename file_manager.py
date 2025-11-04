# # file_manager.py
# import json, pickle, base64
# from typing import Any, Dict

# SAVE_FILE = "minesweeper save.txt"

# def save_game(state: Dict[str, Any], filename: str = SAVE_FILE):
#     state_copy = dict(state)
#     state_copy["rng_state"] = base64.b64encode(pickle.dumps(state["rng_state"])).decode()
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(state_copy, f, indent=2)

# def load_game(filename: str = SAVE_FILE):
#     with open(filename, "r", encoding="utf-8") as f:
#         state = json.load(f)
#     state["rng_state"] = pickle.loads(base64.b64decode(state["rng_state"]))
#     return state
# file_manager.py
"""
Save/load helper. Saves a JSON file that includes a base64-pickled RNG state so reloads
are reproducible.
"""
import json, pickle, base64
from typing import Dict, Any

SAVE_FILENAME = "minesweeper save.txt"

def save_game(state: Dict[str, Any], filename: str = SAVE_FILENAME):
    data = dict(state)
    # pickle RNG state (it is a tuple) and base64 encode so JSON-friendly
    if 'rng_state' in data:
        data['rng_state'] = base64.b64encode(pickle.dumps(data['rng_state'])).decode('ascii')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_game(filename: str = SAVE_FILENAME) -> Dict[str, Any]:
    with open(filename, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    if 'rng_state' in raw:
        raw['rng_state'] = pickle.loads(base64.b64decode(raw['rng_state'].encode('ascii')))
    return raw
