# minesweeper.py
# Simple console Minesweeper for Python 3
# Controls: enter commands like "r 3 5" to reveal row 3 col 5, or "f 3 5" to toggle flag.
# Rows and columns are 0-indexed in prompts (easy to change if you prefer 1-indexed).

import random
import sys
from collections import deque

class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        assert 0 < mines < rows * cols, "mines must be between 1 and rows*cols-1"
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self._init_board()

    def _init_board(self):
        # internal board: -1 = mine, 0..8 = adjacent mine count
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.win = False

        # place mines
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mines_positions = random.sample(all_cells, self.mines)
        for (r, c) in mines_positions:
            self.board[r][c] = -1

        # calculate adjacent counts
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == -1:
                                count += 1
                self.board[r][c] = count

    def display(self, reveal_all=False):
        # header
        header = "   " + " ".join(f"{c:2d}" for c in range(self.cols))
        print(header)
        print("   " + "--" * self.cols + "-")
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                if reveal_all:
                    cell = self._cell_to_char_revealed(r, c)
                else:
                    if self.revealed[r][c]:
                        cell = self._cell_to_char_revealed(r, c)
                    elif self.flagged[r][c]:
                        cell = " F"
                    else:
                        cell = " ■"
                row_cells.append(cell)
            print(f"{r:2d}| " + " ".join(row_cells))
        print()

    def _cell_to_char_revealed(self, r, c):
        val = self.board[r][c]
        if val == -1:
            return " *"
        if val == 0:
            return "  "  # empty
        return f" {val}"

    def reveal(self, r, c):
        if self.game_over:
            return
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print("Coordinates out of range.")
            return
        if self.flagged[r][c]:
            print("Cell is flagged. Unflag it first if you want to reveal.")
            return
        if self.revealed[r][c]:
            # allow chord: reveal neighbors if flagged count equals number on cell
            if self.board[r][c] > 0:
                flagged_neighbors = sum(self.flagged[nr][nc] for nr, nc in self._neighbors(r, c))
                if flagged_neighbors == self.board[r][c]:
                    for nr, nc in self._neighbors(r, c):
                        if not self.flagged[nr][nc] and not self.revealed[nr][nc]:
                            self._reveal_cell(nr, nc)
            return

        self._reveal_cell(r, c)
        self._check_win()

    def _reveal_cell(self, r, c):
        if self.revealed[r][c] or self.flagged[r][c]:
            return
        if self.board[r][c] == -1:
            # hit a mine
            self.revealed[r][c] = True
            self.game_over = True
            self.win = False
            print("BOOM! You hit a mine.")
            return
        # flood fill for zeros
        if self.board[r][c] == 0:
            self._flood_fill(r, c)
        else:
            self.revealed[r][c] = True

    def _flood_fill(self, r, c):
        q = deque()
        q.append((r, c))
        while q:
            cr, cc = q.popleft()
            if self.revealed[cr][cc] or self.flagged[cr][cc]:
                continue
            self.revealed[cr][cc] = True
            if self.board[cr][cc] == 0:
                for nr, nc in self._neighbors(cr, cc):
                    if not self.revealed[nr][nc] and not self.flagged[nr][nc]:
                        q.append((nr, nc))

    def toggle_flag(self, r, c):
        if self.game_over:
            return
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print("Coordinates out of range.")
            return
        if self.revealed[r][c]:
            print("Can't flag a revealed cell.")
            return
        self.flagged[r][c] = not self.flagged[r][c]
        print(f"{'Flagged' if self.flagged[r][c] else 'Unflagged'} cell ({r}, {c}).")
        self._check_win()

    def _neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def _check_win(self):
        # win if all non-mine cells revealed OR all mines flagged and others revealed
        all_non_mines_revealed = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    all_non_mines_revealed = False
                    break
            if not all_non_mines_revealed:
                break
        if all_non_mines_revealed:
            self.game_over = True
            self.win = True

    def reveal_all_and_show(self):
        self.display(reveal_all=True)
        if self.win:
            print("Congratulations — you cleared the board!")
        else:
            print("Game over. Better luck next time.")

def play_console(rows=9, cols=9, mines=10):
    game = Minesweeper(rows, cols, mines)
    print("Welcome to Minesweeper (console).")
    print("Commands:")
    print("  r ROW COL   -> reveal cell at ROW COL")
    print("  f ROW COL   -> toggle flag at ROW COL")
    print("  q           -> quit")
    print()
    while not game.game_over:
        game.display()
        cmd = input("Enter command: ").strip().split()
        if not cmd:
            continue
        op = cmd[0].lower()
        if op == "q":
            print("Quitting. Final board:")
            game.reveal_all_and_show()
            return
        if len(cmd) < 3:
            print("Invalid command. Example: r 3 5 or f 2 1")
            continue
        try:
            r = int(cmd[1])
            c = int(cmd[2])
        except ValueError:
            print("Row and column must be integers.")
            continue
        if op == "r":
            game.reveal(r, c)
        elif op == "f":
            game.toggle_flag(r, c)
        else:
            print("Unknown command. Use 'r' to reveal or 'f' to flag.")
    # finished
    game.reveal_all_and_show()

if __name__ == "__main__":
    # default settings; you can change difficulty by command-line args
    # example: python minesweeper.py 16 30 99 (rows cols mines)
    if len(sys.argv) == 4:
        try:
            r = int(sys.argv[1])
            c = int(sys.argv[2])
            m = int(sys.argv[3])
            play_console(r, c, m)
        except Exception as e:
            print("Invalid arguments. Usage: python minesweeper.py [rows cols mines]")
            raise
    else:
        play_console()