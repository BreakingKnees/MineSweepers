# # board.py
# import random
# from typing import List, Tuple

# class Board:
#     def __init__(self, size: int = 9, mines: int = 10, rng: random.Random = random):
#         self.size = size
#         self.mines = mines
#         self.rng = rng
#         self.grid = [[0 for _ in range(size)] for _ in range(size)]
#         self.revealed = [[False]*size for _ in range(size)]
#         self.flagged = [[False]*size for _ in range(size)]
#         self.mine_positions: List[Tuple[int,int]] = []
#         self.generated = False

#     def generate(self, start_row: int, start_col: int):
#         """Place mines randomly but not on the first clicked cell."""
#         all_cells = [(r, c) for r in range(self.size) for c in range(self.size)
#                      if not (r == start_row and c == start_col)]
#         self.mine_positions = self.rng.sample(all_cells, self.mines)
#         for (r, c) in self.mine_positions:
#             self.grid[r][c] = -1
#         # fill numbers
#         for r in range(self.size):
#             for c in range(self.size):
#                 if self.grid[r][c] != -1:
#                     self.grid[r][c] = self.count_adjacent_mines(r, c)
#         self.generated = True

#     def count_adjacent_mines(self, r: int, c: int) -> int:
#         count = 0
#         for dr in (-1, 0, 1):
#             for dc in (-1, 0, 1):
#                 if dr == dc == 0:
#                     continue
#                 nr, nc = r + dr, c + dc
#                 if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == -1:
#                     count += 1
#         return count

#     def reveal(self, r: int, c: int) -> List[Tuple[int,int]]:
#         """Reveal cell. Return list of revealed cells."""
#         if not self.generated:
#             self.generate(r, c)

#         if self.flagged[r][c] or self.revealed[r][c]:
#             return []

#         self.revealed[r][c] = True
#         revealed_cells = [(r, c)]

#         if self.grid[r][c] == 0:
#             for dr in (-1, 0, 1):
#                 for dc in (-1, 0, 1):
#                     if dr == dc == 0:
#                         continue
#                     nr, nc = r + dr, c + dc
#                     if 0 <= nr < self.size and 0 <= nc < self.size:
#                         if not self.revealed[nr][nc] and not self.flagged[nr][nc]:
#                             revealed_cells += self.reveal(nr, nc)
#         return revealed_cells

#     def toggle_flag(self, r: int, c: int):
#         if not self.revealed[r][c]:
#             self.flagged[r][c] = not self.flagged[r][c]

#     def is_mine(self, r: int, c: int) -> bool:
#         return self.grid[r][c] == -1

#     def all_safe_revealed(self) -> bool:
#         for r in range(self.size):
#             for c in range(self.size):
#                 if self.grid[r][c] != -1 and not self.revealed[r][c]:
#                     return False
#         return True
# board.py
"""
Board logic for Minesweeper.
- size: board width/height (square board)
- mines: number of mines
- rng: random.Random instance for reproducible generation
"""
from typing import List, Tuple
import random

MINE = -1

class Board:
    def __init__(self, size: int = 9, mines: int = 10, rng: random.Random = random):
        self.size = int(size)
        self.mines = int(mines)
        self.rng = rng
        # grid: MINE (-1) for mine, otherwise 0..8 for adjacent mine counts
        self.grid: List[List[int]] = [[0]*self.size for _ in range(self.size)]
        self.revealed: List[List[bool]] = [[False]*self.size for _ in range(self.size)]
        self.flagged: List[List[bool]] = [[False]*self.size for _ in range(self.size)]
        self.mine_positions: List[Tuple[int,int]] = []
        self.generated: bool = False

    def reset_arrays(self):
        self.grid = [[0]*self.size for _ in range(self.size)]
        self.revealed = [[False]*self.size for _ in range(self.size)]
        self.flagged = [[False]*self.size for _ in range(self.size)]
        self.mine_positions = []
        self.generated = False

    def generate(self, start_r: int, start_c: int):
        """Place mines randomly, avoiding the first-click cell and its neighbors for friendlier gameplay."""
        self.reset_arrays()
        # cells forbidden to place mine: start cell and its neighbors
        forbidden = set()
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                nr, nc = start_r+dr, start_c+dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    forbidden.add((nr, nc))
        all_cells = [(r,c) for r in range(self.size) for c in range(self.size) if (r,c) not in forbidden]
        # if mines >= available cells, fallback to full random excluding just start cell
        if self.mines > len(all_cells):
            all_cells = [(r,c) for r in range(self.size) for c in range(self.size) if not (r==start_r and c==start_c)]
        self.mine_positions = list(self.rng.sample(all_cells, self.mines))
        for (r, c) in self.mine_positions:
            self.grid[r][c] = MINE
        # compute adjacent counts
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == MINE:
                    continue
                self.grid[r][c] = self.count_adjacent_mines(r, c)
        self.generated = True

    def count_adjacent_mines(self, r:int, c:int) -> int:
        cnt = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == MINE:
                    cnt += 1
        return cnt

    def in_bounds(self, r:int, c:int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def reveal(self, r:int, c:int) -> List[Tuple[int,int]]:
        """
        Reveal a cell and recursively reveal neighbors if it is zero.
        Returns a list of coordinates that became revealed during this action.
        If the board wasn't generated yet, generation happens with safe-first-click logic.
        """
        if not self.in_bounds(r,c):
            return []
        if not self.generated:
            self.generate(r, c)
        if self.flagged[r][c] or self.revealed[r][c]:
            return []   # nothing changed
        revealed = []
        # BFS/stack for flood-fill revealing zeros
        stack = [(r,c)]
        while stack:
            cr, cc = stack.pop()
            if not self.in_bounds(cr, cc):
                continue
            if self.revealed[cr][cc] or self.flagged[cr][cc]:
                continue
            self.revealed[cr][cc] = True
            revealed.append((cr,cc))
            if self.grid[cr][cc] == 0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = cr+dr, cc+dc
                        if self.in_bounds(nr,nc) and not self.revealed[nr][nc] and not self.flagged[nr][nc]:
                            stack.append((nr,nc))
        return revealed

    def toggle_flag(self, r:int, c:int):
        if not self.in_bounds(r,c):
            return
        if self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]

    def is_mine(self, r:int, c:int) -> bool:
        return self.in_bounds(r,c) and self.grid[r][c] == MINE

    def all_safe_revealed(self) -> bool:
        """Victory: every non-mine cell is revealed."""
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != MINE and not self.revealed[r][c]:
                    return False
        return True

    def reveal_all_mines(self) -> List[Tuple[int,int]]:
        """Mark all mines as revealed and return list of positions"""
        revealed = []
        for (r,c) in self.mine_positions:
            if not self.revealed[r][c]:
                self.revealed[r][c] = True
                revealed.append((r,c))
        return revealed

    def remaining_flags(self) -> int:
        """Number of flags remaining (for UI)."""
        placed = sum(1 for r in range(self.size) for c in range(self.size) if self.flagged[r][c])
        return max(0, self.mines - placed)
