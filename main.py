# minesweeper_gui.py

import tkinter as tk
from tkinter import messagebox
from minesweeper import Minesweeper  # your existing class

class MinesweeperGUI:
    def __init__(self, master, rows=9, cols=9, mines=10):
        self.master = master
        self.master.title("Minesweeper")
        self.game = Minesweeper(rows, cols, mines)
        self.rows = rows
        self.cols = cols
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.create_buttons()

    def create_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.master,
                    width=3,
                    height=1,
                    font=("Arial", 12),
                    command=lambda r=r, c=c: self.on_left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def on_left_click(self, r, c):
        if self.game.revealed[r][c] and self.game.board[r][c] > 0:
            # Chord: reveal neighbors if flags match number
            flagged_neighbors = sum(
                self.game.flagged[nr][nc] for nr, nc in self.game._neighbors(r, c)
            )
            if flagged_neighbors == self.game.board[r][c]:
                for nr, nc in self.game._neighbors(r, c):
                    if not self.game.revealed[nr][nc] and not self.game.flagged[nr][nc]:
                        self.game.reveal(nr, nc)
        else:
            self.game.reveal(r, c)

        self.update_buttons()
        if self.game.game_over:
            self.show_end_game()

    def on_right_click(self, r, c):
        self.game.toggle_flag(r, c)
        self.update_buttons()
        if self.game.game_over:
            self.show_end_game()

    def update_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                if self.game.revealed[r][c]:
                    val = self.game.board[r][c]
                    btn.config(relief=tk.SUNKEN, bg="lightgrey")
                    if val == -1:
                        btn.config(text="*", bg="red", fg="black")
                    elif val == 0:
                        btn.config(text="")
                    else:
                        colors = ["blue","green","red","darkblue","brown","cyan","black","grey"]
                        color = colors[val-1] if val-1 < len(colors) else "black"
                        btn.config(text=str(val), fg=color)
                elif self.game.flagged[r][c]:
                    btn.config(text="F", bg="yellow", fg="black")
                else:
                    btn.config(text="", bg="SystemButtonFace", relief=tk.RAISED)

    def show_end_game(self):
        # reveal all mines
        for r in range(self.rows):
            for c in range(self.cols):
                if self.game.board[r][c] == -1:
                    self.buttons[r][c].config(text="*", bg="red")
        if self.game.win:
            messagebox.showinfo("Minesweeper", "Congratulations! You cleared the board!")
        else:
            messagebox.showinfo("Minesweeper", "BOOM! You hit a mine.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root, rows=9, cols=9, mines=10)
    root.mainloop()