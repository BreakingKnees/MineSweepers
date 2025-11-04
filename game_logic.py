# # game_logic.py
# from board import Board
# import random

# class Game:
#     def __init__(self, size: int = 9, mines: int = 10, seed: int = None, rng_state=None):
#         self.random = random.Random()
#         if seed is not None:
#             self.random.seed(seed)
#         if rng_state:
#             self.random.setstate(rng_state)
#         self.board = Board(size=size, mines=mines, rng=self.random)
#         self.game_over = False
#         self.win = False

#     def reveal_cell(self, r, c):
#         if self.board.flagged[r][c] or self.game_over:
#             return []

#         revealed = self.board.reveal(r, c)
#         if self.board.is_mine(r, c):
#             self.game_over = True
#             self.win = False
#         elif self.board.all_safe_revealed():
#             self.game_over = True
#             self.win = True
#         return revealed

#     def flag_cell(self, r, c):
#         if not self.game_over:
#             self.board.toggle_flag(r, c)

#     def get_state(self):
#         return {
#             "grid": self.board.grid,
#             "revealed": self.board.revealed,
#             "flagged": self.board.flagged,
#             "mine_positions": self.board.mine_positions,
#             "generated": self.board.generated,
#             "game_over": self.game_over,
#             "win": self.win,
#             "rng_state": self.random.getstate()
#         }

#     def load_state(self, state):
#         self.board.grid = state["grid"]
#         self.board.revealed = state["revealed"]
#         self.board.flagged = state["flagged"]
#         self.board.mine_positions = state["mine_positions"]
#         self.board.generated = state["generated"]
#         self.game_over = state["game_over"]
#         self.win = state["win"]
#         self.random.setstate(state["rng_state"])

# game_logic.py
from board import Board
import random
from typing import Dict, Any, Tuple, List

class Game:
    """
    Orchestrates Board + RNG state + high level actions.
    """
    def __init__(self, size:int=9, mines:int=10, seed: int = None, rng_state=None):
        self.random = random.Random()
        if seed is not None:
            self.random.seed(seed)
        if rng_state is not None:
            # assume valid random.getstate() object
            self.random.setstate(rng_state)
        self.board = Board(size=size, mines=mines, rng=self.random)
        self.game_over: bool = False
        self.win: bool = False
        self.start_time = None   # can be set by UI to track elapsed seconds

    def left_click(self, r:int, c:int) -> Dict[str, Any]:
        """
        Returns a dict with:
          - 'revealed': list[(r,c)] newly revealed
          - 'hit_mine': bool if user clicked a mine
          - 'win': bool if this move caused win
          - 'game_over': bool overall game over
        """
        result = {'revealed':[], 'hit_mine':False, 'win':False, 'game_over':False}
        if self.game_over:
            return result
        # reveal - board.generate is triggered inside reveal for first-click safety
        newly = self.board.reveal(r,c)
        result['revealed'] = newly
        if self.board.is_mine(r,c):
            # hit mine: reveal all mines; game over
            result['hit_mine'] = True
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
            result['game_over'] = True
        elif self.board.all_safe_revealed():
            self.game_over = True
            self.win = True
            result['win'] = True
            result['game_over'] = True
        return result

    def right_click(self, r:int, c:int) -> Dict[str, Any]:
        """
        Toggle flag; returns summary: {'flagged': bool, 'remaining_flags': int}
        """
        if self.game_over:
            return {'flagged': False, 'remaining_flags': self.board.remaining_flags()}
        self.board.toggle_flag(r,c)
        return {'flagged': self.board.flagged[r][c], 'remaining_flags': self.board.remaining_flags()}

    def new_game(self, size:int, mines:int, seed: int = None):
        self.__init__(size=size, mines=mines, seed=seed)

    def get_state(self) -> Dict[str, Any]:
        """Serialize state for saving. RNG state pickled by file_manager."""
        return {
            'size': self.board.size,
            'mines': self.board.mines,
            'grid': self.board.grid,
            'revealed': self.board.revealed,
            'flagged': self.board.flagged,
            'mine_positions': self.board.mine_positions,
            'generated': self.board.generated,
            'game_over': self.game_over,
            'win': self.win,
            'rng_state': self.random.getstate()
        }

    def load_state(self, state: Dict[str,Any]):
        self.board.size = int(state.get('size', self.board.size))
        self.board.mines = int(state.get('mines', self.board.mines))
        self.board.grid = state['grid']
        self.board.revealed = state['revealed']
        self.board.flagged = state['flagged']
        self.board.mine_positions = state.get('mine_positions', [])
        self.board.generated = state.get('generated', True)
        self.game_over = state.get('game_over', False)
        self.win = state.get('win', False)
        rng_state = state.get('rng_state', None)
        if rng_state is not None:
            self.random.setstate(rng_state)
        # ensure board.rng points to this game's RNG
        self.board.rng = self.random
