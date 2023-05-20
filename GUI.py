import tkinter as tk

class GUI:

    @property
    def restart_action(self):
        return self._restart_action

    @restart_action.setter
    def restart_action(self, action):
        self._restart_action = action

    @property
    def move_action(self):
        return self._move_action

    @move_action.setter
    def move_action(self, action):
        self._move_action = action

    @property
    def selection_action(self):
        return self._selection_action

    @selection_action.setter
    def selection_action(self, action):
        self._selection_action = action

    @property
    def cost(self):
        return self._cost['text']

    @cost.setter
    def cost(self, cost):
        self._cost['text'] = "Cost: {}".format(cost)

    @property
    def step(self):
        return self._step['text']

    @step.setter
    def step(self, step):
        self._step['text'] = "Steps: {}".format(step)

    def __init__(self, boardsize=400):
        self._restart_action = None
        self._move_action = None
        self._boardsize = boardsize
        self._cellsize = boardsize / 8

        self._window = tk.Tk()
        self._window.title("8-queens problem")
        self._window.resizable(False, False)

        self._canvas = tk.Canvas(self._window, bg="black", height=400, width=400)
        self._canvas.pack(side=tk.LEFT, padx=10)

        buttons = tk.Frame(self._window)
        buttons.pack(side=tk.LEFT, padx=10)

        restart = tk.Button(buttons, text="Restart", command=self.on_restart, bg="red")
        restart.pack(side=tk.TOP, padx=10, pady=10)

        move = tk.Button(buttons, text="Move", command=self.on_move)
        move.pack(side=tk.TOP, padx=10, pady=10)

        choices = (
            "Hill-Climbing",
            "Stochastic Hill-Climbing",
            "Greedy Best First Search",
            "Beam Search (beam width=4)",
        )
        self._choice_var = tk.StringVar(self._window, choices[0])
        self._choice_var.trace("w", self.on_select)

        select = tk.OptionMenu(buttons, self._choice_var, *choices)
        select.pack(side=tk.TOP, padx=10, pady=10)

        labels = tk.Frame(self._window)
        labels.pack(side=tk.LEFT, padx=10)

        self._cost = tk.Label(labels)
        self._cost.pack(side=tk.TOP, padx=10, pady=10)

        self._step = tk.Label(labels)
        self._step.pack(side=tk.TOP, padx=10, pady=10)

    def draw_board(self, positions=[]):
        self._canvas.delete("all")

        for r in range(0, 8):
            for c in range(0, 4):
                start_x = (c * self._cellsize * 2) + (self._cellsize if r % 2 == 1 else 0)
                start_y = r * self._cellsize
                self._canvas.create_rectangle(start_x, start_y, start_x + self._cellsize, start_y + self._cellsize, fill="white", width=0)

        
    def draw_position(self, column=0, row=0):
      start_x = (column * self._cellsize) + int(self._cellsize * 0.15)
      start_y = (row * self._cellsize) + int(self._cellsize * 0.15)
      end_x = start_x + int(self._cellsize * 0.7)
      end_y = start_y + int(self._cellsize * 0.7)

      self._canvas.create_text((start_x+end_x)/2, (start_y+end_y)/2, text="♕", font=("Arial", int(self._cellsize*0.5)), fill="red")
    

    def draw_value(self, column=0, row=0, value="99"):
        start_x = (column * self._cellsize) + int(self._cellsize * 0.8)
        start_y = (row * self._cellsize) + int(self._cellsize * 0.2)

        self._canvas.create_text(start_x, start_y, text=str(value), fill="red")

    def on_restart(self):
        if self._restart_action:
            self._restart_action()

    def on_move(self):
        if self._move_action:
            self._move_action()

    def on_select(self, *args):
        if self._selection_action:
            self._selection_action(self._choice_var.get())

    def show(self):
        self._window.mainloop()
