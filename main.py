
"""
Minesweeper GUI Deluxe — polished version
Features:
- Main menu with animated preview & difficulty cards
- Practice (seed) working properly
- Safer timer (no label crash)
- Smooth explosion + mine glow animation
- Hint, Save/Load, Back to Menu
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from game_logic import Game
from file_manager import save_game, load_game, SAVE_FILENAME
import random
import time

# ----- Styling constants -----
BG = "#101217"
PANEL = "#14181D"
TILE_BG = "#d6d6d6"
TILE_REVEALED = "#e9e7e3"
FLAG_COLOR = "#e74c3c"
MINE_COLOR = "#ff4d4d"
TEXT_COLOR = "#222"
TITLE_FONT = ("Inter", 20, "bold")
SMALL_FONT = ("Inter", 10)
DIGIT_FONTS = ("Helvetica", 14, "bold")
EMOJI_FLAG = "🚩"
EMOJI_MINE = "💣"

NUMBER_COLORS = {
    1: "#2b6cb0", 2: "#2f855a", 3: "#c53030", 4: "#2c5282",
    5: "#b83280", 6: "#2c7a7b", 7: "#1a202c", 8: "#4a5568"
}


def choose_cell_size(board_px: int, size: int, max_cell: int = 48, min_cell: int = 18):
    return max(min_cell, min(max_cell, board_px // size))


class MinesweeperApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("⚡️ Minesweeper Deluxe")
        self.root.geometry("820x620")
        self.root.configure(bg=BG)
        self.current_game: Game = None
        self.elapsed_sec = 0
        self.timer_job = None

        self._build_main_menu()

    # -----------------------
    # Main Menu
    # -----------------------
    def _build_main_menu(self):
        for w in self.root.winfo_children():
            w.destroy()

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=18)

        tk.Label(header, text="Minesweeper — Deluxe", fg="white", bg=BG,
                 font=("Inter", 28, "bold")).pack()
        tk.Label(header, text="Stylish UI • Animations • Save System",
                 fg="#b9c0c8", bg=BG, font=SMALL_FONT).pack(pady=(6, 12))

        preview = tk.Canvas(self.root, width=700, height=140, bg="#0b0d0f", highlightthickness=0)
        preview.pack()
        self._draw_preview_animation(preview)

        menu_frame = tk.Frame(self.root, bg=BG)
        menu_frame.pack(pady=14)

        difficulties = [
            ("Easy", 9, 9, 10),
            ("Medium", 16, 16, 40),
            ("Hard", 22, 22, 99)
        ]

        for name, side_r, side_c, mines in difficulties:
            card = tk.Frame(menu_frame, bg=PANEL, padx=18, pady=12)
            card.pack(side="left", padx=12)

            tk.Label(card, text=name, bg=PANEL, fg="white",
                     font=("Inter", 14, "bold")).pack(anchor="w")
            tk.Label(card, text=f"{side_r}×{side_c} • {mines} mines",
                     bg=PANEL, fg="#cbd5e1", font=SMALL_FONT).pack(anchor="w", pady=(4, 10))

            btn_frame = tk.Frame(card, bg=PANEL)
            btn_frame.pack()
            tk.Button(btn_frame, text="Play", width=10,
                      command=lambda s=side_r, m=mines: self.start_new_game(s, m)).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Practice (seed)", width=12,
                      command=lambda s=side_r, m=mines: self._seed_and_start(s, m)).pack(side="left")

        ctl = tk.Frame(self.root, bg=BG)
        ctl.pack(pady=14)
        tk.Button(ctl, text="Load Saved Game", width=18, command=self.load_game_ui).pack(side="left", padx=8)
        tk.Button(ctl, text="How to play", width=12, command=self.show_help).pack(side="left", padx=8)
        tk.Button(ctl, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=8)

    def _draw_preview_animation(self, canvas: tk.Canvas):
        canvas.delete("all")
        cols, rows, pad = 7, 5, 8
        cellw, cellh = (int(canvas["width"]) - pad * 2) // cols, (int(canvas["height"]) - pad * 2) // rows
        for r in range(rows):
            for c in range(cols):
                x0, y0 = pad + c * cellw, pad + r * cellh
                x1, y1 = x0 + cellw - 6, y0 + cellh - 6
                canvas.create_rectangle(x0, y0, x1, y1, fill="#cfd8dc", outline="#b0bec5", width=1)
        sparks = [(1, 1), (1, 3), (2, 5), (3, 2), (3, 4)]

        def step(i=0):
            canvas.delete("spark")
            r, c = sparks[i % len(sparks)]
            x0 = pad + c * cellw + 6
            y0 = pad + r * cellh + 6
            x1 = x0 + cellw - 18
            y1 = y0 + cellh - 18
            canvas.create_oval(x0, y0, x1, y1, fill="#ff2c2c", outline="", tags="spark")
            canvas.after(420, lambda: step(i + 1))

        step(0)

    # -----------------------
    # Game logic + UI
    # -----------------------
    def _seed_and_start(self, size, mines):
        val = simpledialog.askstring("Seed", "Enter numeric seed (leave empty for random):", parent=self.root)
        try:
            seed = int(val) if val else None
        except Exception:
            seed = None
        self.start_new_game(size, mines, seed=seed)

    def start_new_game(self, size: int, mines: int, seed=None):
        self.current_game = Game(size=size, mines=mines, seed=seed)
        self.elapsed_sec = 0
        self._build_game_ui(size, mines)
        self._start_timer()

    def _build_game_ui(self, size, mines):
        for w in self.root.winfo_children():
            w.destroy()

        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", pady=8)

        left = tk.Frame(top, bg=BG)
        left.pack(side="left", padx=12)
        self.flags_label = tk.Label(left, text=f"💠 Mines: {mines}", fg="#e6eef6", bg=BG, font=("Inter", 12))
        self.flags_label.pack()

        self.face_btn = tk.Button(top, text="🙂", font=("Arial", 18), width=3, command=self._restart_current)
        self.face_btn.pack(side="top", pady=2)

        right = tk.Frame(top, bg=BG)
        right.pack(side="right", padx=12)
        self.timer_label = tk.Label(right, text="Time: 0s", fg="#e6eef6", bg=BG, font=("Inter", 12))
        self.timer_label.pack()
        tk.Button(right, text="Save", command=self.save_game_ui).pack(pady=(6, 0))

        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.pack(pady=6, expand=True)

        cell_px = choose_cell_size(560, size, max_cell=44, min_cell=18)
        self.cell_px = cell_px
        canvas_w, canvas_h = cell_px * size, cell_px * size
        self.board_canvas = tk.Canvas(board_frame, width=min(canvas_w, 700), height=min(canvas_h, 500),
                                      bg="#101217", highlightthickness=0)
        self.board_canvas.pack(side="left", padx=12, pady=6)
        self.board_canvas.config(scrollregion=(0, 0, canvas_w, canvas_h))

        self.canvas_cells = [[None] * size for _ in range(size)]
        self.canvas_texts = [[None] * size for _ in range(size)]

        for r in range(size):
            for c in range(size):
                x0, y0 = c * cell_px, r * cell_px
                x1, y1 = x0 + cell_px - 2, y0 + cell_px - 2
                rect = self.board_canvas.create_rectangle(x0 + 4, y0 + 4, x1 + 4, y1 + 4,
                                                          fill=TILE_BG, outline="#9aa6b2", width=2)
                txt = self.board_canvas.create_text(x0 + cell_px / 2 + 4, y0 + cell_px / 2 + 4,
                                                    text="", font=DIGIT_FONTS, fill=TEXT_COLOR)
                self.canvas_cells[r][c] = rect
                self.canvas_texts[r][c] = txt
                self.board_canvas.tag_bind(rect, "<Button-1>", lambda e, rr=r, cc=c: self.on_left_click(rr, cc))
                self.board_canvas.tag_bind(txt, "<Button-1>", lambda e, rr=r, cc=c: self.on_left_click(rr, cc))
                self.board_canvas.tag_bind(rect, "<Button-3>", lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                self.board_canvas.tag_bind(txt, "<Button-3>", lambda e, rr=r, cc=c: self.on_right_click(rr, cc))

        bot = tk.Frame(self.root, bg=BG)
        bot.pack(fill="x", pady=8)
        tk.Button(bot, text="Back to Menu", command=self._back_to_menu).pack(side="left", padx=12)
        tk.Button(bot, text="Hint (safe reveal)", command=self._safe_hint).pack(side="left", padx=10)

        self._redraw_board()

    # -----------------------
    # Clicks
    # -----------------------
    def on_left_click(self, r, c):
        if not self.current_game:
            return
        res = self.current_game.left_click(r, c)
        for (rr, cc) in res["revealed"]:
            self._reveal_tile(rr, cc)
        if res["hit_mine"]:
            self.face_btn.config(text="💥")
            self._play_explosion_animation()
            self._stop_timer()
            messagebox.showerror("Boom!", "You hit a mine! Game over.")
            self._reveal_all_mines_visual()
        elif res["win"]:
            self.face_btn.config(text="😎")
            self._stop_timer()
            messagebox.showinfo("You win!", f"You cleared the board in {self.elapsed_sec} seconds!")
        self._update_info()

    def on_right_click(self, r, c):
        res = self.current_game.right_click(r, c)
        self._redraw_tile(r, c)
        self._update_info()

    # -----------------------
    # Visuals
    # -----------------------
    def _reveal_tile(self, r, c):
        board = self.current_game.board
        rect = self.canvas_cells[r][c]
        txt = self.canvas_texts[r][c]
        self.board_canvas.itemconfig(rect, fill=TILE_REVEALED, outline="#bfc6cc")
        val = board.grid[r][c]
        if val == -1:
            self.board_canvas.itemconfig(txt, text=EMOJI_MINE, fill=MINE_COLOR)
        elif val == 0:
            self.board_canvas.itemconfig(txt, text="")
        else:
            self.board_canvas.itemconfig(txt, text=str(val), fill=NUMBER_COLORS.get(val, "#333"))

    def _redraw_tile(self, r, c):
        b = self.current_game.board
        rect, txt = self.canvas_cells[r][c], self.canvas_texts[r][c]
        if b.revealed[r][c]:
            self._reveal_tile(r, c)
        else:
            self.board_canvas.itemconfig(rect, fill=TILE_BG)
            if b.flagged[r][c]:
                self.board_canvas.itemconfig(txt, text=EMOJI_FLAG, fill=FLAG_COLOR)
            else:
                self.board_canvas.itemconfig(txt, text="")

    def _redraw_board(self):
        for r in range(self.current_game.board.size):
            for c in range(self.current_game.board.size):
                self._redraw_tile(r, c)
        self._update_info()

    def _reveal_all_mines_visual(self):
        for (r, c) in self.current_game.board.mine_positions:
            self._reveal_tile(r, c)

    def _update_info(self):
        if self.current_game:
            rem = self.current_game.board.remaining_flags()
            self.flags_label.config(
                text=f"💠 Mines: {self.current_game.board.mines}  •  Flags left: {rem}"
            )

    def _play_explosion_animation(self):
        b = self.current_game.board
        centers = []
        for (r, c) in b.mine_positions:
            x = c * self.cell_px + self.cell_px / 2 + 4
            y = r * self.cell_px + self.cell_px / 2 + 4
            centers.append((x, y))
        steps = 15

        def tick(step=0):
            self.board_canvas.delete("anim")
            t = step / steps
            for (x, y) in centers:
                radius = 4 + 40 * t
                color = MINE_COLOR if step % 2 == 0 else "#ff9999"
                self.board_canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                              fill="", outline=color, width=3, tags="anim")
            if step < steps:
                self.board_canvas.after(40, lambda: tick(step + 1))
            else:
                self.board_canvas.delete("anim")

        tick(0)

    # -----------------------
    # Misc controls
    # -----------------------
    def _start_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.elapsed_sec = 0
        self.timer_label.config(text="Time: 0s")

        def tick():
            if not self.timer_label.winfo_exists():
                return
            self.elapsed_sec += 1
            self.timer_label.config(text=f"Time: {self.elapsed_sec}s")
            self.timer_job = self.root.after(1000, tick)

        self.timer_job = self.root.after(1000, tick)

    def _stop_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def _safe_hint(self):
        b = self.current_game.board
        candidates = [(r, c) for r in range(b.size) for c in range(b.size)
                      if not b.revealed[r][c] and not b.flagged[r][c] and b.grid[r][c] != -1]
        if not candidates:
            messagebox.showinfo("Hint", "No safe hints available.")
            return
        zeros = [p for p in candidates if b.grid[p[0]][p[1]] == 0]
        pick = random.choice(zeros if zeros else candidates)
        res = self.current_game.left_click(*pick)
        for (rr, cc) in res["revealed"]:
            self._reveal_tile(rr, cc)
        if res["win"]:
            messagebox.showinfo("You win!", "Nice! You cleared the board.")
        self._update_info()

    def _restart_current(self):
        if self.current_game:
            s = self.current_game.board.size
            m = self.current_game.board.mines
            self.start_new_game(s, m)

    def _back_to_menu(self):
        self._stop_timer()
        self._build_main_menu()

    def save_game_ui(self):
        if not self.current_game:
            messagebox.showwarning("Save", "No game running.")
            return
        save_game(self.current_game.get_state())
        messagebox.showinfo("Save", f"Game saved to {SAVE_FILENAME}")

    def load_game_ui(self):
        try:
            state = load_game()
        except FileNotFoundError:
            messagebox.showwarning("Load", "No saved game file found.")
            return
        g = Game()
        g.load_state(state)
        self.current_game = g
        self.elapsed_sec = 0
        self._build_game_ui(g.board.size, g.board.mines)
        self._redraw_board()
        self._start_timer()
        messagebox.showinfo("Load", "Saved game loaded successfully.")

    def show_help(self):
        msg = ("Left click → reveal a tile\n"
               "Right click → flag/unflag\n"
               "Use the main menu for difficulty / practice / save & load\n"
               "First click is always safe.")
        messagebox.showinfo("How to play", msg)


# ----- Run -----
if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
