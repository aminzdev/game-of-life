import random
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.wm_title("Conway's Game of Life")
        self._page = MainPage(self)
        self.resizable(False, False)

    def run(self):
        self.update()
        self._page.update()
        self.mainloop()


class MainPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app)

        self.pack(fill=tk.BOTH, expand=True, ipadx=0, ipady=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)

        canvas = GameCanvas(self)
        canvas.grid(column=0, row=0, columnspan=3, sticky="NSEW", padx=5, pady=3)
        self._canvas = canvas

        next_button = tk.Button(self, text="Step", command=canvas.next)
        next_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=1)

        clear_button = tk.Button(self, text="Clear", command=canvas.clear)
        clear_button.grid(column=1, row=1, sticky=tk.W, padx=5, pady=1)

        randomize_button = tk.Button(self, text="Randomize", command=canvas.randomize)
        randomize_button.grid(column=2, row=1, sticky=tk.W, padx=5, pady=1)

    def update(self):
        self._canvas.draw()


class GameCanvas(tk.Canvas):
    def __init__(self, page):
        super().__init__(page, borderwidth=0, highlightthickness=0)
        self._rows = 0
        self._cols = 0
        Cell.set_canvas(self)
        self._cells = list()

    def draw(self):
        cell_size = 30
        self._cols = self.winfo_width() // cell_size
        self._rows = self.winfo_height() // cell_size
        margin_x = (self.winfo_width() % cell_size) / 2
        margin_y = (self.winfo_height() % cell_size) / 2

        for row in range(self._rows):
            self._cells.append([])
            for col in range(self._cols):
                x = col * cell_size + margin_x
                y = row * cell_size + margin_y
                _id = self.create_rectangle(x, y, x + cell_size, y + cell_size, outline="gray", fill="black")
                self._cells[-1].append(Cell(_id))

    def next(self):
        for row, cells in enumerate(self._cells):
            for col, cell in enumerate(cells):
                live_neighbours = self._get_live_neighbours(row, col)

                next_state = (cell.get_state() and live_neighbours == 2) or live_neighbours == 3
                cell.set_next_state(next_state)

        for cells in self._cells:
            for cell in cells:
                cell.step()

    def clear(self):
        for cells in self._cells:
            for cell in cells:
                cell.set_state(False)

    def randomize(self):
        for _ in range(300):
            row = random.choice(self._cells)
            cell = random.choice(row)
            cell.set_state(True)

    def _get_live_neighbours(self, row, col):
        count = 0
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue

                x = (row + r) % self._rows
                y = (col + c) % self._cols

                cell = self._cells[x][y]
                count += cell.get_state()

        return count


class Cell:
    _canvas = None

    def __init__(self, _id):
        self._id = _id
        self._active = False
        self._canvas.tag_bind(_id, "<Button-1>", self._on_click)
        self._next_state = False

    def _on_click(self, event):
        self.set_state(not self._active)

    def set_state(self, state):
        self._active = state
        self._canvas.itemconfig(self._id, fill="green" if self._active else "black")

    def get_state(self):
        return self._active

    def set_next_state(self, state):
        self._next_state = state

    def step(self):
        self.set_state(self._next_state)

    @classmethod
    def set_canvas(cls, canvas):
        Cell._canvas = canvas


if __name__ == "__main__":
    app = App()
    app.run()
