import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.game_over = False

        # --- Colours ---
        self.bg_color = "#1e1e2e"
        self.btn_color = "#313244"
        self.btn_hover = "#45475a"
        self.x_color = "#f38ba8"   # rose
        self.o_color = "#89b4fa"   # blue
        self.win_color = "#a6e3a1" # green highlight
        self.text_color = "#cdd6f4"
        self.accent = "#cba6f7"    # mauve

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        # Title
        title = tk.Label(
            self.root, text="Tic-Tac-Toe", font=("Segoe UI", 22, "bold"),
            bg=self.bg_color, fg=self.accent
        )
        title.pack(pady=(18, 4))

        # Turn indicator
        self.turn_label = tk.Label(
            self.root, text="Player X's Turn", font=("Segoe UI", 14),
            bg=self.bg_color, fg=self.x_color
        )
        self.turn_label.pack(pady=(0, 10))

        # 3×3 grid
        grid_frame = tk.Frame(self.root, bg=self.bg_color)
        grid_frame.pack(padx=20)

        for i in range(9):
            btn = tk.Button(
                grid_frame, text="", width=5, height=2,
                font=("Segoe UI", 24, "bold"),
                bg=self.btn_color, fg=self.text_color,
                activebackground=self.btn_hover,
                activeforeground=self.text_color,
                relief="flat", bd=0,
                cursor="hand2",
                command=lambda idx=i: self._on_click(idx),
            )
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=4, pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.btn_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(
                bg=self.btn_color if b["fg"] != self.win_color else b["bg"]
            ))
            self.buttons.append(btn)

        # Reset button
        reset_btn = tk.Button(
            self.root, text="⟳  Reset", font=("Segoe UI", 13, "bold"),
            bg=self.accent, fg="#1e1e2e",
            activebackground="#b4befe", activeforeground="#1e1e2e",
            relief="flat", bd=0, cursor="hand2",
            padx=18, pady=6,
            command=self._reset,
        )
        reset_btn.pack(pady=(16, 20))

    # --------------------------------------------------------------- Logic
    def _on_click(self, idx):
        if self.board[idx] != "" or self.game_over:
            return

        self.board[idx] = self.current_player
        color = self.x_color if self.current_player == "X" else self.o_color
        self.buttons[idx].configure(text=self.current_player, fg=color)

        winner, combo = self._check_winner()
        if winner:
            self._highlight_winner(combo)
            self.game_over = True
            messagebox.showinfo("Game Over", f"🎉  Player {winner} wins!")
            return

        if "" not in self.board:
            self.game_over = True
            self.turn_label.configure(text="It's a Tie!", fg=self.accent)
            messagebox.showinfo("Game Over", "It's a tie! 🤝")
            return

        # Switch turns
        self.current_player = "O" if self.current_player == "X" else "X"
        color = self.x_color if self.current_player == "X" else self.o_color
        self.turn_label.configure(
            text=f"Player {self.current_player}'s Turn", fg=color
        )

    def _check_winner(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6),              # diagonals
        ]
        for a, b, c in combos:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a], (a, b, c)
        return None, None

    def _highlight_winner(self, combo):
        for idx in combo:
            self.buttons[idx].configure(fg=self.win_color, bg="#45475a")
        self.turn_label.configure(
            text=f"Player {self.current_player} Wins! 🎉", fg=self.win_color
        )

    def _reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        for btn in self.buttons:
            btn.configure(text="", fg=self.text_color, bg=self.btn_color)
        self.turn_label.configure(text="Player X's Turn", fg=self.x_color)


# -------------------------------------------------------------- Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
