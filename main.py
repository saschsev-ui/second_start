import random
import tkinter as tk

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
TICK_MS = 350

SHAPES = {
    "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "O": [(1, 0), (2, 0), (1, 1), (2, 1)],
    "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
    "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
    "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
    "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
}

COLORS = {
    "I": "#00BCD4",
    "O": "#FFEB3B",
    "T": "#9C27B0",
    "L": "#FF9800",
    "J": "#3F51B5",
    "S": "#4CAF50",
    "Z": "#F44336",
}


class Tetris:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Einfaches Tetris")

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#121212",
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.info = tk.Label(
            root,
            text="Punkte: 0\nLevel: 1",
            justify="left",
            font=("Arial", 14),
        )
        self.info.pack(side=tk.RIGHT, padx=10)

        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.current_piece = self.new_piece()

        self.root.bind("<Left>", lambda _event: self.move(-1, 0))
        self.root.bind("<Right>", lambda _event: self.move(1, 0))
        self.root.bind("<Down>", lambda _event: self.move(0, 1))
        self.root.bind("<Up>", lambda _event: self.rotate())
        self.root.bind("<space>", lambda _event: self.drop())

        self.tick()

    def new_piece(self):
        kind = random.choice(list(SHAPES.keys()))
        return {
            "kind": kind,
            "cells": SHAPES[kind][:],
            "x": 3,
            "y": 0,
            "color": COLORS[kind],
        }

    def piece_positions(self, piece=None):
        if piece is None:
            piece = self.current_piece
        return [(piece["x"] + x, piece["y"] + y) for x, y in piece["cells"]]

    def is_valid(self, piece):
        for x, y in self.piece_positions(piece):
            if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                return False
            if self.board[y][x] is not None:
                return False
        return True

    def move(self, dx, dy):
        if self.game_over:
            return

        moved = self.current_piece.copy()
        moved["cells"] = self.current_piece["cells"][:]
        moved["x"] += dx
        moved["y"] += dy

        if self.is_valid(moved):
            self.current_piece = moved
            self.draw()
            return True
        return False

    def rotate(self):
        if self.game_over:
            return

        rotated = self.current_piece.copy()
        rotated["cells"] = [(-y + 1, x) for x, y in self.current_piece["cells"]]

        min_x = min(x for x, _ in rotated["cells"])
        min_y = min(y for _, y in rotated["cells"])
        rotated["cells"] = [(x - min_x, y - min_y) for x, y in rotated["cells"]]

        if self.is_valid(rotated):
            self.current_piece = rotated
            self.draw()

    def lock_piece(self):
        for x, y in self.piece_positions():
            self.board[y][x] = self.current_piece["color"]
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.is_valid(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = GRID_HEIGHT - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [None for _ in range(GRID_WIDTH)])
        self.board = new_board

        if cleared:
            self.lines_cleared += cleared
            self.score += (cleared ** 2) * 100
            self.level = 1 + self.lines_cleared // 10

    def drop(self):
        if self.game_over:
            return
        while self.move(0, 1):
            pass
        self.lock_piece()
        self.draw()

    def tick(self):
        if not self.game_over:
            if not self.move(0, 1):
                self.lock_piece()
            self.draw()
            speed = max(80, TICK_MS - (self.level - 1) * 20)
            self.root.after(speed, self.tick)
        else:
            self.draw(game_over=True)

    def draw(self, game_over=False):
        self.canvas.delete("all")

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.board[y][x]
                if color:
                    self.draw_cell(x, y, color)
                else:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        (x + 1) * CELL_SIZE,
                        (y + 1) * CELL_SIZE,
                        outline="#1F1F1F",
                    )

        if not self.game_over:
            for x, y in self.piece_positions():
                self.draw_cell(x, y, self.current_piece["color"])

        self.info.config(text=f"Punkte: {self.score}\nLevel: {self.level}")

        if game_over:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="GAME OVER",
                fill="white",
                font=("Arial", 24, "bold"),
            )

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill=color,
            outline="#333333",
        )


def main():
    root = tk.Tk()
    Tetris(root)
    root.mainloop()


if __name__ == "__main__":
    main()
