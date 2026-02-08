import tkinter as tk
from tkinter import ttk
from src.config import *
from src.n_queen_solver import NQueenSolver

class NQueenUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queen Visualizer")
        self.root.geometry("900x700")

        self.n = tk.IntVar(value=DEFAULT_N)
        self.speed = tk.DoubleVar(value=0.5) # Seconds per step
        self.is_paused = False
        self.solver = None
        self.generator = None
        self.current_step = None
        
        self.start_col = None     # User selected start column for row 0
        self.conflict_line = None # Store coordinates for drawing line (r1, c1, r2, c2)
        
        self.setup_ui()
        self.reset_board()

    def setup_ui(self):
        # --- Control Panel (Left) ---
        control_frame = tk.Frame(self.root, padx=10, pady=10, width=200, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control_frame, text="N-Queens", font=FONT_HEADER, bg="#f0f0f0").pack(pady=10)
        
        # N Input
        tk.Label(control_frame, text="Board Size (N):", font=FONT_MAIN, bg="#f0f0f0").pack(pady=5)
        n_spinbox = tk.Spinbox(control_frame, from_=MIN_N, to=MAX_N, textvariable=self.n, font=FONT_MAIN, width=5)
        n_spinbox.pack(pady=5)

        # Speed Control
        tk.Label(control_frame, text="Speed (Fast <-> Slow):", font=FONT_MAIN, bg="#f0f0f0").pack(pady=5)
        tk.Scale(control_frame, variable=self.speed, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=150).pack(pady=5)

        button_frame = tk.Frame(control_frame, bg="#f0f0f0")
        button_frame.pack(pady=10, fill=tk.X)
        
        tk.Button(button_frame, text="Start", command=self.start_simulation, font=FONT_MAIN, bg=BUTTON_START_BG, fg=BUTTON_TEXT_COLOR, width=8).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Reset", command=self.reset_simulation, font=FONT_MAIN, bg=BUTTON_RESET_BG, fg=BUTTON_TEXT_COLOR, width=8).pack(side=tk.RIGHT, padx=2)
        self.play_pause_btn = tk.Button(control_frame, text="Pause", command=self.toggle_pause, font=FONT_MAIN, bg=BUTTON_PAUSE_BG, fg=BUTTON_TEXT_COLOR, state=tk.DISABLED)
        self.play_pause_btn.pack(pady=5, fill=tk.X)
        self.step_btn = tk.Button(control_frame, text="Step Forward", command=self.manual_step, font=FONT_MAIN, bg=BUTTON_PAUSE_BG, fg=BUTTON_TEXT_COLOR, state=tk.DISABLED)
        self.step_btn.pack(pady=5, fill=tk.X)

        # Explanation Panel (Bottom Left)
        tk.Label(control_frame, text="Status:", font=FONT_HEADER, bg="#f0f0f0").pack(pady=(20, 5))
        self.status_var = tk.StringVar(value="Ready to start.")
        self.status_label = tk.Label(control_frame, textvariable=self.status_var, font=("Helvetica", 10), wraplength=180, justify="left", bg="#fff", relief="sunken", height=10)
        self.status_label.pack(pady=5, fill=tk.X)

        # --- Canvas Area (Center) ---
        self.canvas_frame = tk.Frame(self.root, bg="#333")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#333", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.canvas.bind("<Configure>", self.draw_board) # Redraw on resize
        self.canvas.bind("<Button-1>", self.on_canvas_click) # Click to place

    def on_canvas_click(self, event):
        # Only allow setting start column if solver is not running
        if self.solver is not None:
             return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        n = self.n.get()
        size = min(w, h) - 40
        if size <= 0: return
        
        start_x = (w - size) // 2
        start_y = (h - size) // 2
        cell_size = size / n

        # Check if click is inside the board
        if start_x <= event.x <= start_x + size and start_y <= event.y <= start_y + size:
            row = int((event.y - start_y) / cell_size)
            col = int((event.x - start_x) / cell_size)
            
            # Only allow setting for the first row (row 0)
            if row == 0:
                if self.start_col == col:
                    self.start_col = None # Toggle off
                    self.status_var.set("Start lock removed.")
                else:
                    self.start_col = col
                    self.status_var.set(f"Start locked to Col {col}.")
                self.draw_board()

    def start_simulation(self):
        self.is_paused = False
        self.play_pause_btn.config(text="Pause", state=tk.NORMAL)
        self.step_btn.config(state=tk.DISABLED)
        # Don't reset start_col here, user might want to keep it
        self.reset_board(keep_start_col=True) 
        
        # Validate start_col against current N
        if self.start_col is not None and self.start_col >= self.n.get():
             self.start_col = None
             self.status_var.set("Start lock removed (out of bounds).")
             
        self.solver = NQueenSolver(self.n.get(), first_row_col=self.start_col)
        self.generator = self.solver.steps
        self.run_next_step()

    def reset_simulation(self):
        self.is_paused = False # Stop any running loop implicitly by clearing solver? No, need to stop loop
        self.solver = None
        self.generator = None
        self.reset_board(keep_start_col=False)
        self.play_pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)

    def reset_board(self, keep_start_col=False):
        self.solver = None
        self.generator = None
        self.board_state = [-1] * self.n.get()
        self.highlights = {} # (row, col) -> color
        self.conflict_line = None
        if not keep_start_col:
             self.start_col = None
        self.draw_board()
        self.status_var.set("Board reset. Click row 0 to lock start. Press Start.")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.play_pause_btn.config(text="Play")
            self.step_btn.config(state=tk.NORMAL)
        else:
            self.play_pause_btn.config(text="Pause")
            self.step_btn.config(state=tk.DISABLED)
            self.run_next_step()

    def manual_step(self):
        if self.is_paused:
             self.process_step()

    def run_next_step(self):
        if self.solver and not self.is_paused:
            if self.process_step():
                delay_ms = int(self.speed.get() * 1000)
                self.root.after(delay_ms, self.run_next_step)

    def process_step(self):
        try:
            step_type, board, message, metadata = next(self.generator)
            self.status_var.set(message)
            self.board_state = board
            
            self.highlights = {}
            if metadata:
                row, col = metadata[0], metadata[1]
            else:
                row, col = -1, -1

            self.conflict_line = None # Clear previous conflict line

            if step_type == "PLACING":
                self.highlights[(row, col)] = HIGHLIGHT_CURRENT
            elif step_type == "SAFE":
                self.highlights[(row, col)] = HIGHLIGHT_SAFE
            elif step_type == "CONFLICT":
                self.highlights[(row, col)] = HIGHLIGHT_CONFLICT
                # Metadata has conflict source
                if len(metadata) >= 4:
                    conf_r, conf_c = metadata[2], metadata[3]
                    self.highlights[(conf_r, conf_c)] = HIGHLIGHT_CONFLICT
                    self.conflict_line = (row, col, conf_r, conf_c)
            elif step_type == "BACKTRACKING":
                 self.highlights[(row, col)] = HIGHLIGHT_BACKTRACK
            elif step_type == "FOUND_SOLUTION":
                self.highlights = { (r, c): HIGHLIGHT_SAFE for r, c in enumerate(board) }
                self.status_var.set(f"Solution Found!\n{message}")
                self.play_pause_btn.config(state=tk.DISABLED)
                self.draw_board()
                return False

            self.draw_board()
            return True

        except StopIteration:
            self.status_var.set("No solution found or finished.")
            self.play_pause_btn.config(state=tk.DISABLED)
            return False

    def draw_board(self, event=None):
        self.canvas.delete("all")
        
        # Calculate cell size based on available space
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        n = self.n.get()
        size = min(w, h) - 40 # Padding
        if size <= 0: return # Too small
        
        start_x = (w - size) // 2
        start_y = (h - size) // 2
        cell_size = size / n

        for r in range(n):
            for c in range(n):
                x1 = start_x + c * cell_size
                y1 = start_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Base color
                color = BOARD_WHITE if (r + c) % 2 == 0 else BOARD_BLACK
                
                # Highlight override
                if (r, c) in self.highlights:
                    color = self.highlights[(r, c)]
                elif r == 0 and c == self.start_col:
                     color = HIGHLIGHT_LOCKED

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # Draw Queen
                if self.board_state and r < len(self.board_state) and self.board_state[r] == c:
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="♛", font=("Helvetica", int(cell_size * 0.6)), fill=QUEEN_COLOR
                    )
                # Draw locked queen indicator if no queen is actually placed there yet (pre-start)
                elif r == 0 and c == self.start_col and (not self.board_state or self.board_state[0] == -1):
                    self.canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="♛", font=("Helvetica", int(cell_size * 0.6)), fill=QUEEN_COLOR
                    )

        # Draw conflict line on top
        if self.conflict_line:
            r1, c1, r2, c2 = self.conflict_line
            x1 = start_x + c1 * cell_size + cell_size / 2
            y1 = start_y + r1 * cell_size + cell_size / 2
            x2 = start_x + c2 * cell_size + cell_size / 2
            y2 = start_y + r2 * cell_size + cell_size / 2
            self.canvas.create_line(x1, y1, x2, y2, fill=CONFLICT_LINE_COLOR, width=CONFLICT_LINE_WIDTH)
